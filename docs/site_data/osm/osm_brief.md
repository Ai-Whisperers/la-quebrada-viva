# OSM brief — La Quebrada Viva (5 km radius around KML centroid)

Source: OpenStreetMap via Overpass API, ODbL 1.0  
Pulled: 2026-06-29T18:18:08Z  
Centroid: lon=-57.0355, lat=-25.6073  
Radius: 5000 m for site features, 15000 m for places

## Feature counts by category

| Category | Count | Closest to centroid |
| --- | --- | --- |
| buildings | 645 | 213.6 m · building=house |
| water | 30 | 998.9 m · name=Aqua Basin |
| waterways | 23 | 3019.6 m · waterway=ditch |
| trees | 174 | 251.6 m · landuse=farmland |
| roads | 205 | 481.8 m · name=Camino a Escobar |
| pois | 20 | 1174.1 m · building=yes |
| landuse | 89 | 251.6 m · landuse=farmland |
| places | 49 | 2073.1 m · name=Machado |

## Tag breakdown by category

### buildings (645 features)

- **amenity**: `place_of_worship`×2, `police`×2
- **building**: `house`×620, `yes`×14, `warehouse`×4, `barn`×3, `greenhouse`×2, `church`×1, `cabin`×1

### water (30 features)

- **natural**: `wetland`×20, `water`×10

### waterways (23 features)

- **waterway**: `ditch`×14, `stream`×9

### trees (174 features)

- **natural**: `wood`×96, `tree`×23, `tree_row`×2
- **landuse**: `forest`×41, `orchard`×10, `farmland`×2

### roads (205 features)

- **highway**: `track`×113, `residential`×46, `service`×19, `unclassified`×10, `trunk`×5, `path`×5, `footway`×4, `tertiary`×3

### pois (20 features)

- **amenity**: `police`×4, `place_of_worship`×3, `school`×1
- **tourism**: `guest_house`×2, `camp_site`×2, `hotel`×1, `wilderness_hut`×1
- **shop**: `supermarket`×1
- **building**: `yes`×4
- **leisure**: `pitch`×3, `swimming_pool`×2

### landuse (89 features)

- **landuse**: `forest`×41, `grass`×20, `orchard`×10, `plant_nursery`×5, `allotments`×5, `farmland`×2, `cemetery`×2, `brownfield`×1, `quarry`×1, `religious`×1

### places (49 features)

- **place**: `quarter`×25, `village`×11, `town`×4, `hamlet`×4, `neighbourhood`×4, `city`×1
- **landuse**: `residential`×11

## Interpretation

- **Buildings: 645 within 5 km** — primary cluster identified; see `buildings.geojson` for footprints to overlay on the 62-ha digital twin.
- **Surface water: 30 polygons / 23 waterway segments** within 5 km. Cross-reference with JRC GSW + Sentinel-2 NDWI for full surface-water inventory.
- **Vegetation: 174 forest/tree features** — see `trees.geojson` for tagged orchards/forest patches near the parcel.
- **Roads: 205 segments** — access network for site servicing.
- **Named places within 15 km: 49** — see `places.geojson` for hamlets/villages relevant to logistics, labour, and amenity catchment.
