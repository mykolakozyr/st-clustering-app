# Repository Guidelines

## Project Structure & Module Organization
- `app.py` hosts the entire Streamlit application, including upload flow, clustering invocation, and Folium map rendering.
- External clustering logic lives in the `st_polygoncluster` dependency declared in `requirements.txt`; keep this repo UI-focused.
- Temporary uploads remain in memory; no extra assets or persistent storage directories are created.

## Build, Test, and Development Commands
- `python -m venv .venv && source .venv/bin/activate` – create and activate a local virtual environment.
- `pip install --upgrade --force-reinstall --no-cache-dir -r requirements.txt` – ensures the latest ST-PolygonCluster build with `overlap_threshold` support lands locally.
- `streamlit run app.py` – start the demo locally; Streamlit auto-reloads on save.
- `streamlit cache clear` – reset cached session state when debugging unusual clustering behaviour.

## Hosting & Operations
- Production runs on Streamlit Cloud at https://st-clustering.streamlit.app/; verify issues there before reproducing locally.
- Streamlit caching and pip wheels can mask dependency updates—restart the app after clearing cache and forcing reinstall of `st_polygoncluster`.
- Changes that alter clustering parameters (e.g., overlap slider defaults) should ship with brief release notes for hosted users.

## Coding Style & Naming Conventions
- Target Python 3.10+ with 4-space indentation and PEP 8 naming (`snake_case` for functions, `CapWords` for classes).
- Keep UI widgets and session keys prefixed (`cluster_*`, `time_*`) to avoid collisions inside `st.session_state`.
- Prefer docstrings on helpers (e.g., `get_color`) and inline comments only for non-obvious Folium or GeoPandas transforms.

## Testing Guidelines
- No automated tests exist yet; add lightweight unit tests under a future `tests/` package using `pytest`.
- Mock GeoDataFrames or use small static GeoJSON fixtures to validate clustering parameters before hitting Streamlit.
- Run `pytest` (after adding it to your dev dependencies) and include baseline coverage output in PR discussions.

## Commit & Pull Request Guidelines
- Follow the short, imperative message style already in history (e.g., `reduce dependencies`, `remove artefacts`).
- Reference issues when available and mention datasets or sample files used in manual verification.
- For UI-affecting changes, attach a screenshot or GIF from Streamlit and call out any new requirements or secrets.
