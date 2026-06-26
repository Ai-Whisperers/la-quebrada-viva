"""Build all 2km AOI close-up composites for Blender."""
import os, sys, numpy as np
import rasterio
from rasterio.windows import from_bounds
from PIL import Image
sys.path.insert(0, '.')
from AOI_2km import BBOX, CE_UTM, CN_UTM
from pyproj import Transformer

W, S, E, N = BBOX
t = Transformer.from_crs('EPSG:4326', 'EPSG:32721', always_xy=True)
W_e, S_n = t.transform(W, S); E_e, N_n = t.transform(E, N)
print(f'2km AOI: WGS84 {BBOX}  UTM21J E[{W_e:.1f},{E_e:.1f}] N[{S_n:.1f},{N_n:.1f}]')

# === 1. DEM clip ===
with rasterio.open('dem/terrarium_monday_2_5m_utm21j.tif') as ds:
    win = from_bounds(W_e, S_n, E_e, N_n, ds.transform).intersection(rasterio.windows.Window(0,0,ds.width,ds.height))
    dem2 = ds.read(1, window=win)
    dem_t = ds.window_transform(win)
print(f'DEM clip: {dem2.shape}  range {dem2.min():.1f}..{dem2.max():.1f}m')
prof = {'driver':'GTiff','height':dem2.shape[0],'width':dem2.shape[1],'count':1,
        'dtype':'float32','crs':'EPSG:32721','transform':dem_t,'compress':'lzw','tiled':True}
with rasterio.open('dem/terrarium_monday_2km_2_5m.tif', 'w', **prof) as dst:
    dst.write(dem2, 1)
print(f'  -> dem/terrarium_monday_2km_2_5m.tif  {os.path.getsize("dem/terrarium_monday_2km_2_5m.tif")//1024} KB')

# Hillshade + slope
xres = abs(dem_t.a); yres = abs(dem_t.e)
e = dem2.astype(np.float32)
e_p = np.pad(e, 1, mode='edge')
dz_dx = ((e_p[0:-2,2:]+2*e_p[1:-1,2:]+e_p[2:,2:]) - (e_p[0:-2,0:-2]+2*e_p[1:-1,0:-2]+e_p[2:,0:-2])) / (8*xres)
dz_dy = ((e_p[2:,0:-2]+2*e_p[2:,1:-1]+e_p[2:,2:]) - (e_p[0:-2,0:-2]+2*e_p[0:-2,1:-1]+e_p[0:-2,2:])) / (8*yres)
slope = np.degrees(np.arctan(np.hypot(dz_dx, dz_dy)))
sl = np.arctan(np.hypot(dz_dx, dz_dy)); asp = np.arctan2(dz_dy, -dz_dx)
for label, az in [('az315_NW', 315), ('az045_NE', 45), ('az180_S', 180), ('az090_E_low', 90)]:
    azr = np.radians(90-az); altr = np.radians(35)
    hs = np.clip(np.sin(altr)*np.cos(sl) + np.cos(altr)*np.sin(sl)*np.cos(azr-asp), 0, 1)
    Image.fromarray((hs*255).astype(np.uint8)).save(f'analysis/hillshade_2km_{label}.png', optimize=True)
    print(f'  hillshade_2km_{label}: {os.path.getsize(f"analysis/hillshade_2km_{label}.png")//1024} KB')
slope_p = np.clip(slope / 60 * 255, 0, 255).astype(np.uint8)
Image.fromarray(slope_p).save('analysis/slope_2km.png', optimize=True)
en = ((dem2 - np.nanmin(dem2)) / (np.nanmax(dem2) - np.nanmin(dem2) + 1e-6) * 255).clip(0,255).astype(np.uint8)
Image.fromarray(en).save('analysis/heightmap_2km.png', optimize=True)

# === 2. S2 RGB clip ===
with rasterio.open('analysis/rgb_truecolor_utm21j.tif') as ds:
    win = from_bounds(W_e, S_n, E_e, N_n, ds.transform).intersection(rasterio.windows.Window(0,0,ds.width,ds.height))
    rgb = ds.read(window=win)
    rgb_t = ds.window_transform(win)
prof_rgb = {'driver':'GTiff','height':rgb.shape[1],'width':rgb.shape[2],'count':3,
            'dtype':'uint8','crs':'EPSG:32721','transform':rgb_t,'compress':'lzw','tiled':True}
with rasterio.open('analysis/rgb_2km_utm21j.tif', 'w', **prof_rgb) as dst:
    dst.write(rgb)
Image.fromarray(np.transpose(rgb,(1,2,0))).save('analysis/rgb_2km_10m.png', optimize=True)
print(f'  rgb_2km: {os.path.getsize("analysis/rgb_2km_utm21j.tif")//1024} KB, png {os.path.getsize("analysis/rgb_2km_10m.png")//1024} KB')

# === 3. NDVI clip ===
with rasterio.open('analysis/ndvi_utm21j.tif') as ds:
    win = from_bounds(W_e, S_n, E_e, N_n, ds.transform).intersection(rasterio.windows.Window(0,0,ds.width,ds.height))
    ndvi = ds.read(1, window=win)
ndvi_p = np.clip((ndvi+1)*127.5, 0, 255).astype(np.uint8)
Image.fromarray(ndvi_p).save('analysis/ndvi_2km.png', optimize=True)
print(f'  ndvi_2km: {os.path.getsize("analysis/ndvi_2km.png")//1024} KB')

# === 4. ESA WorldCover clip ===
with rasterio.open('landcover/esa_worldcover_utm21j.tif') as ds:
    win = from_bounds(W_e, S_n, E_e, N_n, ds.transform).intersection(rasterio.windows.Window(0,0,ds.width,ds.height))
    lc = ds.read(1, window=win)
colormap = {10:(40,100,50),20:(80,140,60),30:(180,220,100),40:(220,200,80),50:(180,80,80),60:(180,150,100),70:(230,230,230),80:(50,70,180),90:(80,80,200),95:(0,150,80),100:(180,200,180)}
lc_rgb = np.zeros((*lc.shape, 3), dtype=np.uint8)
for k, v in colormap.items():
    lc_rgb[lc == k] = v
Image.fromarray(lc_rgb).save('landcover/esa_worldcover_2km.png', optimize=True)
unique, counts = np.unique(lc, return_counts=True)
print(f'  landcover_2km: {os.path.getsize("landcover/esa_worldcover_2km.png")//1024} KB')
for u, c in zip(unique, counts):
    if u == 0: continue
    pct = c / lc.size * 100
    if pct > 0.05: print(f'    class {u}: {pct:.1f}%')

# === 5. Composite: Esri z=18 + hillshade + RGB ===
print('\nBuilding 2km composite (Esri z18 + hillshade + RGB)...')
esri18 = np.array(Image.open('hd_imagery/esri_z18_2km_stitched.png').convert('RGB'))
hs18 = np.array(Image.open('analysis/hillshade_2km_az315_NW.png').convert('L'))
# need to align: esri is at the 2km bounding box, hillshade is 817x784 px
# use a bilinear resize to match
from PIL import Image as I
hs18_r = I.fromarray(hs18).resize((esri18.shape[1], esri18.shape[0]), I.BILINEAR)
hs18_arr = np.array(hs18_r).astype(np.float32) / 255.0
# Blend: brightness reduction on shadowed areas (multiply 0.5..1.0)
shadow = 0.5 + 0.5 * hs18_arr  # 0.5 dark, 1.0 bright
composite = np.clip(esri18.astype(np.float32) * shadow[:,:,None], 0, 255).astype(np.uint8)
I.fromarray(composite).save('analysis/composite_esri18_hillshade_2km.png', optimize=True)
print(f'  composite: {os.path.getsize("analysis/composite_esri18_hillshade_2km.png")//1024} KB')

# === 6. final summary ===
print(f'\n2km AOI outputs:')
import subprocess
for p in [
    'dem/terrarium_monday_2km_2_5m.tif',
    'analysis/hillshade_2km_az315_NW.png',
    'analysis/hillshade_2km_az045_NE.png',
    'analysis/hillshade_2km_az180_S.png',
    'analysis/slope_2km.png',
    'analysis/heightmap_2km.png',
    'analysis/rgb_2km_utm21j.tif',
    'analysis/rgb_2km_10m.png',
    'analysis/ndvi_2km.png',
    'landcover/esa_worldcover_2km.png',
    'analysis/composite_esri18_hillshade_2km.png',
    'hd_imagery/esri_z18_2km_stitched.png',
    'hd_imagery/esri_z17_2km_stitched.png',
]:
    sz = os.path.getsize(p) // 1024
    print(f'  {sz:>6} KB  {p}')
