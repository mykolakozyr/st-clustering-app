# st-clustering-app

## Overview
Streamlit demo that showcases spatio-temporal clustering of polygons using the [ST-PolygonCluster](https://github.com/mykolakozyr/ST-PolygonCluster) library. Upload a GeoJSON file, choose a time column and clustering window, adjust spatial and temporal thresholds, then explore the resulting clusters on an interactive Folium map.

## Key Features
- Interactive parameter tuning for time window, minimum cluster size, and polygon overlap threshold.
- Immediate data preview and tabular cluster results for quick validation.
- Color-coded Folium map that visualizes clusters and exposes attributes in tooltips.
- Session-based color persistence for improved visual comparison between runs.

## Running the App
- **Streamlit Cloud:** Visit https://st-clustering.streamlit.app/ to launch the hosted demo instantly. No setup is required beyond uploading your dataset.
- **Run locally (optional):**
  1. `python -m venv .venv && source .venv/bin/activate`
  2. `pip install --upgrade --force-reinstall --no-cache-dir -r requirements.txt` (ensures the latest ST-PolygonCluster build with `overlap_threshold` support)
  3. `streamlit run app.py`

## Data Preparation Tips
- Upload GeoJSON or JSON files containing polygon geometries; ensure geometries are valid and projected consistently.
- Provide a datetime column (ISO 8601 recommended) to enable temporal clustering; otherwise the app falls back to purely spatial grouping.
- Large datasets can slow down Folium rendering—start with small samples when tuning parameters.

## Development Notes
- `app.py` contains the complete UI workflow; expect Python 3.10+ and follow PEP 8 style.
- To refresh clustering results after dependency updates, restart Streamlit and clear cache with `streamlit cache clear` if behavior seems stale.
- Contributions should document manual testing steps and include visuals for UI changes; see `AGENTS.md` for full guidelines.

## License
The project is released under the MIT License; see `LICENSE` for details.
