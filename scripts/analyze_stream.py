#!/usr/bin/env python3
"""Stream long-profile and micro-hydro intake analysis from ALOS DEM."""
import argparse, json, math, os, sys
import numpy as np
import rasterio as rio

BASE = os.path.dirname(os.path.abspath(__file__))
DEM  = os.path.join(BASE, "docs/site_data/alos_aw3d30_dem.tif")
OUT  = os.path.join(BASE, "docs/site_data/analysis")

HAS_PYSHEDS = False
try:
    import pysheds
    from pysheds.sview import FlowModel
    HAS_PYSHEDS = True
except ImportError:
    pass

def fill_pits(dem):
    h, w = dem.shape
    filled = dem.copy()
    changed = True
    while changed:
        changed = False
        for y in range(1, h-1):
            for x in range(1, w-1):
                if np.isnan(filled[y,x]): continue
                nbrs = [
                    filled[y-1,x], filled[y+1,x],
                    filled[y,x-1], filled[y,x+1],
                    filled[y-1,x-1], filled[y-1,x+1],
                    filled[y+1,x-1], filled[y+1,x+1]
                ]
                nbrs = [v for v in nbrs if not np.isnan(v)]
                if nbrs and min(nbrs) > filled[y,x]:
                    filled[y,x] = min(nbrs)
                    changed = True
    return filled

def d8_flow_dir(fdem):
    h, w = fdem.shape
    fdir = np.zeros_like(fdem, dtype=np.int8)
    dirs = [[-1,0,1,-1,-1,1,1,-1],[0,-1,-1,-1,1,0,1,1]]
    D8 = [32,64,128,16,1,4,2,8]
    for y in range(1, h-1):
        for x in range(1, w-1):
            if np.isnan(fdem[y,x]): continue
            dmax = fdem[y,x]; idx = -1
            for i in range(8):
                ny, nx = y+dirs[0][i], x+dirs[1][i]
                if 0<=ny<h and 0<=nx<w and not np.isnan(fdem[ny,nx]):
                    if fdem[ny,nx] < dmax:
                        dmax = fdem[ny,nx]; idx = i
            if idx >= 0: fdir[y,x] = D8[idx]
    return fdir

def flow_accum(fdem, fdir):
    h, w = fdem.shape
    acc = np.ones_like(fdem, dtype=np.int32)
    acc[np.isnan(fdem)] = 0
    for y in range(1, h-1):
        for x in range(1, w-1):
            if fdir[y,x] == 0: continue
            dmap = {32:(1,0),64:(0,1),128:(-1,0),16:(0,-1),1:(-1,-1),4:(-1,1),2:(1,1),8:(1,-1)}
            d = fdir[y,x]
            if d in dmap:
                ny, nx = y+dmap[d][0], x+dmap[d][1]
                acc[ny,nx] += acc[y,x]
    return acc

def extract_longprofile(fdem, fdir, accum, threshold=50):
    acc_thr = accum > threshold
    pts = np.where(acc_thr & (fdem == fdem))  # valid stream pixels
    if pts[0].size == 0:
        print("No stream pixels found at threshold", threshold)
        return [], []
    # walk from outlet to headwater
    rows, cols = pts[0], pts[1]
    sorter = np.argsort(fdem[rows, cols])[::-1]
    ordered = [(rows[i], cols[i]) for i in sorter]
    dist, elev = [0.0], [fdem[ordered[0][0], ordered[0][1]]]
    with rio.open(DEM) as src:
        res = (abs(src.transform.a), abs(src.transform.e))
    cum_dist = 0.0
    for i in range(1, min(len(ordered), 500)):
        dy = (ordered[i][0] - ordered[i-1][0]) * res[1]
        dx = (ordered[i][1] - ordered[i-1][1]) * res[0]
        cum_dist += math.sqrt(dx*dx + dy*dy)
        dist.append(cum_dist)
        elev.append(fdem[ordered[i][0], ordered[i][1]])
    return dist, elev

def write_csv(path, dist, elev):
    with open(path, "w") as f:
        f.write("distance_m,elevation_m\n")
        for d, e in zip(dist, elev):
            f.write(f"{d:.2f},{e:.2f}\n")
    print(f"  Wrote {path}")

def write_plot(path, dist, elev):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(10,5))
    ax.plot(dist, elev, color="steelblue", linewidth=1.5)
    ax.set_xlabel("Distance along stream (m)"); ax.set_ylabel("Elevation (m)")
    ax.set_title("Stream Long Profile")
    ax.grid(True, alpha=0.3)
    fig.savefig(path, bbox_inches="tight")
    print(f"  Wrote {path}")

def microhydro_analysis(dist, elev, summary_path):
    with rio.open(DEM) as src:
        res = (abs(src.transform.a), abs(src.transform.e))
    # approximate real-world scale: res in degrees, convert to meters
    # 1 deg lat ~ 111000 m
    m_per_cell = res[1] * 111000.0
    stream_m = dist[-1] * m_per_cell if dist else 0
    elev_min, elev_max = elev[-1] if elev else 116, elev[0] if elev else 380
    intake_elevs = [250, 200, 150]
    head_turbine = 120
    lines = ["Micro-hydro Intake Analysis", f"Stream length (approx): {stream_m:.0f} m"]
    lines.append(f"Inlet elevation: {elev_max:.1f} m  Outlet: {head_turbine:.1f} m")
    lines.append("")
    for ie in intake_elevs:
        head = ie - head_turbine
        power_kw = 9.81 * head * 0.05 * 0.8 / 1000  # Q~50L/s=0.05, eff 0.8
        lines.append(f"  Intake at {ie:.0f}m: gross head={head:.0f}m  P~{power_kw:.2f} kW")
    txt = "\n".join(lines) + "\n"
    print(txt)
    with open(summary_path,"a") as f: f.write(txt)
    intxt = os.path.join(OUT, "microhydro_intake_sites.txt")
    with open(intxt,"w") as f: f.write(txt)
    print(f"  Wrote {intxt}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force",action="store_true")
    args = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    out_csv = os.path.join(OUT, "stream_longprofile.csv")
    out_png = os.path.join(OUT, "stream_longprofile.png")
    summary  = os.path.join(OUT, "analysis_summary.txt")
    if os.path.exists(out_csv) and os.path.exists(out_png) and not args.force:
        print("Stream outputs exist. Use --force to overwrite.")
        return
    print(f"Reading {DEM}...")
    with rio.open(DEM) as src:
        dem = src.read(1).astype(np.float32)
        nodata = src.nodata
    dem[dem == nodata] = np.nan
    print("Filling pits...")
    fdem = fill_pits(dem)
    print("Computing D8 flow direction...")
    fdir = d8_flow_dir(fdem)
    print("Computing flow accumulation...")
    accum = flow_accum(fdem, fdir)
    print("Extracting stream network (threshold=50)...")
    dist, elev = extract_longprofile(fdem, fdir, accum, threshold=50)
    if dist:
        write_csv(out_csv, dist, elev)
        write_plot(out_png, dist, elev)
        microhydro_analysis(dist, elev, summary)
    else:
        print("No stream network extracted.")

if __name__=="__main__": main()
