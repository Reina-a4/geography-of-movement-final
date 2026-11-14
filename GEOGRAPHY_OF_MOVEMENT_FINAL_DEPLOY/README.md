# The Geography of Movement — deployment package

Streamlit interactive three-chapter data story.

## Deploy on Streamlit Community Cloud
1. Extract this ZIP. Open the extracted `GEOGRAPHY_OF_MOVEMENT_DEPLOY_READY` folder.
2. Upload the **contents** of that folder to the **root** of a GitHub repository (do not upload the ZIP as a file, and do not nest everything under another project folder).
3. Confirm that GitHub's top level lists `app.py`, `requirements.txt`, `Displacement(1).csv`, `pages/`, and `data/`.
4. In Streamlit Community Cloud select your repo, branch `main`, and main file **app.py**.
5. Check all three links and Home navigation on desktop and mobile.

## Files
- `app.py` — homepage and navigation
- `pages/01_Lebanon_Through_Time.py` — AUB observations map
- `pages/02_Trace_the_Journey.py` — IOM documented connections
- `pages/03_The_Bigger_Picture.py` — The Illusion of Precision
- `data/iom_round7_selected_routes.csv` — selected IOM record subset
- `Displacement(1).csv` — original AUB records
- `requirements.txt` — Cloud dependencies

## Limitations
Chapter 1 shows locations associated with reports, not physical travel paths. Chapter 2 uses approximate town centers and a selection of IOM reporting entries (not a comprehensive total), and the drawn connections are schematic, not actual routes traveled. Chapter 3 illustrates possible double counting, not proven duplication. Chapter 1 Plotly tiles and Chapter 2 Leaflet tiles/CDN need an internet connection.

This package was validated for Python syntax, required source columns, paths, and JavaScript syntax; no live browser/Streamlit Cloud execution was available in this environment. Test mobile layout and interactivity on the deployed site.
