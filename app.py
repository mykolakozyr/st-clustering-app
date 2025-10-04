import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
from st_polygoncluster.clustering import cluster_polygons
import random

st.set_page_config(page_title="ST-PolygonCluster Demo")
st.title("🌀 Spatio-Temporal Polygon Clustering Demo")

# --- Helpers ---
def get_color(cid):
    """Get or assign a persistent random color for a cluster."""
    if "colors" not in st.session_state:
        st.session_state["colors"] = {}
    if cid not in st.session_state["colors"]:
        st.session_state["colors"][cid] = "#{:06x}".format(random.randint(0, 0xFFFFFF))
    return st.session_state["colors"][cid]

st.markdown(
    """
Welcome to the **Spatio-Temporal Polygon Clustering Demo** 🎯  

This tool lets you:
- Upload a **GeoJSON** file with polygons
- Select a **time column** and define the clustering period (seconds, minutes, hours, days)
- Set a **minimum cluster size** (small groups are filtered as noise)
- Set a **minimum overlap percentage** for polygons to be considered neighbors
- Run the analysis and explore the results

Clusters are identified by their spatial overlaps and temporal proximity, and shown in different random colors on an interactive map.  
"""
)

# --- Step 1: Upload file ---
uploaded_file = st.file_uploader("Upload a GeoJSON file", type=["geojson", "json"])

if uploaded_file:
    gdf = gpd.read_file(uploaded_file)

    # Step 2: Preview
    st.subheader("Preview of uploaded data")
    st.dataframe(gdf.head(5))

    # Step 3: Parameters
    datetime_cols = [c for c in gdf.columns if gdf[c].dtype.kind in ("M", "O")]
    time_key = st.selectbox(
        "Select datetime column", 
        options=datetime_cols, 
        index=0 if datetime_cols else None
    )

    st.markdown("**Cluster period length**")
    col1, col2 = st.columns(2)
    with col1:
        cluster_value = st.number_input("Value", min_value=1, value=1, step=1, key="cluster_value")
    with col2:
        cluster_unit = st.selectbox("Unit", ["seconds", "minutes", "hours", "days"], index=2, key="cluster_unit")

    unit_multipliers = {"seconds": 1, "minutes": 60, "hours": 3600, "days": 86400}
    cluster_period = cluster_value * unit_multipliers[cluster_unit]

    col_cluster_size, col_overlap = st.columns(2)
    with col_cluster_size:
        min_cluster_size = st.number_input(
            "Minimum cluster size",
            min_value=1,
            value=2,
            step=1,
            key="min_cluster_size"
        )
    with col_overlap:
        overlap_threshold = st.slider(
            "Minimum overlap (%)",
            min_value=0,
            max_value=100,
            value=0,
            step=5,
            help="Intersection-over-union percentage needed for polygons to be considered neighbors."
        )

    # Step 4: Action buttons
    col1, col2 = st.columns(2)
    with col1:
        run_clicked = st.button("Run analysis")
    with col2:
        reset_clicked = st.button("Reset")

    if reset_clicked:
        st.session_state.pop("clustered", None)
        st.session_state.pop("colors", None)

    if run_clicked:
        st.session_state["clustered"] = cluster_polygons(
            gdf,
            time_key=time_key if time_key else None,
            time_threshold=cluster_period,
            min_cluster_size=min_cluster_size,
            overlap_threshold=overlap_threshold
        )

    # Step 5: Show results if available
    if "clustered" in st.session_state:
        clustered = st.session_state["clustered"]

        st.subheader("Clustered result (first 10 rows)")
        st.dataframe(clustered.head(10))

        # --- Map ---
        st.subheader("Clustered Polygons Map")

        clustered_map = clustered.copy()
        for col in clustered_map.columns:
            if clustered_map[col].dtype.kind in ("M", "m"):
                clustered_map[col] = clustered_map[col].astype(str)

        # Drop noise (-1)
        clustered_map = clustered_map[clustered_map["cluster_id"] >= 0]

        # Center map
        if not clustered_map.empty:
            center = [
                clustered_map.geometry.centroid.y.mean(),
                clustered_map.geometry.centroid.x.mean()
            ]
            m = folium.Map(location=center, zoom_start=6)

            def style_fn(feature):
                cid = feature["properties"].get("cluster_id", -1)
                return {
                    "fillColor": get_color(cid),
                    "color": "black",
                    "weight": 1,
                    "fillOpacity": 0.7,
                }

            tooltip_fields = ["cluster_id"]
            if time_key and time_key in clustered_map.columns:
                tooltip_fields.append(time_key)

            folium.GeoJson(
                clustered_map,
                style_function=style_fn,
                tooltip=folium.GeoJsonTooltip(fields=tooltip_fields)
            ).add_to(m)

            st_folium(m, width="100%", height=600)
        else:
            st.info("No valid clusters to display on map.")

st.markdown("---")
st.markdown(
    """
📦 This demo is powered by [**ST-PolygonCluster**](https://github.com/mykolakozyr/ST-PolygonCluster), a lightweight library for spatio-temporal clustering of polygons.  

🔗 Connect with me:  
- [LinkedIn](https://www.linkedin.com/in/mykolakozyr/)  
- [Twitter/X](https://x.com/mykolakozyr)  
    """
)
