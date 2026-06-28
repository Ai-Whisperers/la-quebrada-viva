# Sentinel-1 SLC scenes — La Quebrada Viva parcel

Source: ASF DAAC (https://search.asf.alaska.edu), Sentinel: CC0  
Window: 2024-01-01 → 2026-06-18  
Pulled: 2026-06-18T18:13:00Z

Total scenes returned: **73**

## Coherent stacks (relative orbit × pass direction)

| Rel. orbit | Direction | Scenes | Date range |
| --- | --- | ---:| --- |
| 68 | DESCENDING | 73 | 2024-01-03 → 2026-06-04 |

## Next step (manual / scripted)

- Pick the largest bucket above → that's your coherent stack.
- Submit InSAR pairs to HyP3 (cloud processing):

  ```bash
  export EARTHDATA_USER=...
  export EARTHDATA_PASS=...
  python3 -m tools.site_data.sentinel1 --submit-insar
  ```

  Submission picks the two most-recent scenes from the largest
  coherent stack. Edit the script if you need a specific pair.

- Result downloads from `https://hyp3-api.asf.alaska.edu/jobs/<id>` once
  the job finishes (usually under an hour).