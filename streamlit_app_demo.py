# Demo version without Earth Engine - for quick deployment
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium

# ---------------- Streamlit page config ----------------
st.set_page_config(layout="wide", page_title="Flood + Hurricane Viewer - Demo")

st.title("🌊 Flood + Hurricane Viewer - Demo Mode")
st.info("🚧 This is a demo version. Full functionality requires Earth Engine authentication.")

# ---------------- Constants ----------------
MONTH_LABELS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

# ---------------- UI state ----------------
if "selected_month" not in st.session_state: st.session_state["selected_month"] = "01"
if "center_lat"   not in st.session_state: st.session_state["center_lat"] = 30.0
if "center_lon"   not in st.session_state: st.session_state["center_lon"] = -90.0
if "zoom"         not in st.session_state: st.session_state["zoom"] = 5
if "clicked_lat"  not in st.session_state: st.session_state["clicked_lat"] = st.session_state["center_lat"]
if "clicked_lon"  not in st.session_state: st.session_state["clicked_lon"] = st.session_state["center_lon"]

with st.sidebar:
    st.markdown('<h2 style="margin-top:0rem;margin-bottom:0.5rem">🌊 Sea Level Rise</h2>', unsafe_allow_html=True)
    years = [str(y) for y in range(1993, 2023)]
    year = st.selectbox("SLA Year", years, index=years.index("2020"))

    st.markdown("### Select Month")
    month_map = {label: f"{i+1:02d}" for i, label in enumerate(MONTH_LABELS)}
    for row in [MONTH_LABELS[i:i+4] for i in range(0, 12, 4)]:
        cols = st.columns(4, gap="small")
        for i, label in enumerate(row):
            if cols[i].button(label, key=f"month_{label}"):
                st.session_state["selected_month"] = month_map[label]
                st.rerun()

    st.markdown("### Flood Controls")
    adj_val = st.slider("Extra Sea Level Rise (m)", 0.0, 5.0, 0.0, 0.05, key="sld_adj")
    
    st.markdown("### 🌀 Hurricanes (Demo Mode)")
    st.info("Hurricane data requires Earth Engine authentication")
    
    st.markdown("### Location Search")
    c1, c2 = st.columns(2)
    with c1: st.text_input("Lat", value=str(st.session_state["center_lat"]), key="lat_in")
    with c2: st.text_input("Lon", value=str(st.session_state["center_lon"]), key="lon_in")

selected_month = st.session_state["selected_month"]
center_lat = float(st.session_state["center_lat"])
center_lon = float(st.session_state["center_lon"])
zoom = int(st.session_state["zoom"])

# ---------------- Map build ----------------
m = folium.Map(location=[center_lat, center_lon], zoom_start=zoom, tiles='OpenStreetMap')

# Add some demo markers
folium.Marker([30.0, -90.0], popup="Demo Location 1").add_to(m)
folium.Marker([29.5, -89.5], popup="Demo Location 2").add_to(m)

# Clicked point marker
clicked_lat = float(st.session_state["clicked_lat"])
clicked_lon = float(st.session_state["clicked_lon"])
folium.CircleMarker([clicked_lat, clicked_lon], radius=5, color="red",
                    fill=True, fill_opacity=1.0, popup="Selected Point").add_to(m)

# --------- Layout: Map (left) & Right panel ----------
map_col, right_col = st.columns([3, 2], gap="large")

with map_col:
    st_data = st_folium(m, width=None, height=720, key="demo_map")

# Handle map clicks
click_info = st_data.get("last_clicked") if st_data else None
if click_info:
    new_lat = float(click_info["lat"])
    new_lon = float(click_info["lng"])
    if (abs(new_lat - float(st.session_state["clicked_lat"])) > 1e-6 or
        abs(new_lon - float(st.session_state["clicked_lon"])) > 1e-6):
        st.session_state["clicked_lat"] = new_lat
        st.session_state["clicked_lon"] = new_lon
        st.session_state["center_lat"] = new_lat
        st.session_state["center_lon"] = new_lon
        st.rerun()

with right_col:
    st.markdown("## 📊 Demo Analytics")
    
    # Demo time series plot
    years_list = list(range(1993, 2023))
    values_list = [0.1 + 0.05 * (y - 1993) + 0.01 * (y % 5) for y in years_list]
    
    label = MONTH_LABELS[int(selected_month)-1]
    st.markdown(f"**SLA Time Series at ({st.session_state['clicked_lat']:.4f}, "
                f"{st.session_state['clicked_lon']:.4f}) — {label} 1993–2022**")
    
    fig, ax = plt.subplots()
    ax.plot(years_list, values_list, marker='o', color='blue')
    ax.set_xlabel("Year")
    ax.set_ylabel("Sea Level Anomaly (m)")
    ax.set_title(f"Demo SLA Data — {label}")
    ax.grid(True, alpha=0.3)
    st.pyplot(fig, clear_figure=True)
    
    # Demo metrics
    st.metric("Elevation at Clicked Point", "2.5 m (Demo)")
    st.metric("Sea level at Clicked Point", "0.3 m (Demo)")
    st.metric("Flood Risk", "Low (Demo)")

st.markdown("---")
st.markdown("### 🚀 To Enable Full Functionality:")
st.markdown("1. Set up Google Earth Engine authentication")
st.markdown("2. Deploy with proper service account credentials")
st.markdown("3. Or convert to a React/JavaScript app for better performance")
