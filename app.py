import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import fastf1
from fastf1 import plotting

plotting.setup_mpl()
fastf1.Cache.enable_cache('cache')

st.set_page_config(page_title="Verstappen Bahrain vs Suzuka 2025", layout="wide")
st.title("🏁 Verstappen Analysis: Bahrain vs Suzuka 2025")

# Load sessions
@st.cache_data(show_spinner=True)
def load_sessions():
    bahrain = fastf1.get_session(2025, 'Bahrain', 'R')
    bahrain.load()
    suzuka = fastf1.get_session(2025, 'Japan', 'R')
    suzuka.load()
    return bahrain, suzuka

bahrain, suzuka = load_sessions()

# Sector Comparison
def compare_sectors():
    bh_lap = bahrain.laps.pick_drivers("VER").pick_fastest()
    sz_lap = suzuka.laps.pick_drivers("VER").pick_fastest()

    bh_sectors = [bh_lap[f'Sector{i}Time'].total_seconds() for i in range(1, 4)]
    sz_sectors = [sz_lap[f'Sector{i}Time'].total_seconds() for i in range(1, 4)]

    df = pd.DataFrame({
        "Sector": ["Sector 1", "Sector 2", "Sector 3"],
        "Bahrain": bh_sectors,
        "Suzuka": sz_sectors
    })

    fig, ax = plt.subplots()
    df.plot(kind='bar', x='Sector', ax=ax)
    plt.title("Sector Comparison (Fastest Lap)")
    plt.ylabel("Time (s)")
    plt.grid(True)
    st.pyplot(fig)

# Tyre Degradation
def tyre_degradation(session, title):
    laps = session.laps.pick_drivers("VER")
    fig, ax = plt.subplots()
    sns.lineplot(data=laps, x='LapNumber', y='LapTime', hue='Compound', ax=ax)
    ax.set_title(title)
    ax.set_ylabel("Lap Time")
    ax.grid(True)
    st.pyplot(fig)

# Throttle Trace

def throttle_trace():
    bh_data = bahrain.laps.pick_drivers("VER").pick_fastest().get_car_data().add_distance()
    sz_data = suzuka.laps.pick_drivers("VER").pick_fastest().get_car_data().add_distance()

    fig, ax = plt.subplots()
    ax.plot(bh_data['Distance'], bh_data['Throttle'], label="Bahrain")
    ax.plot(sz_data['Distance'], sz_data['Throttle'], label="Suzuka")
    ax.set_title("Throttle Trace Comparison")
    ax.set_xlabel("Distance (m)")
    ax.set_ylabel("Throttle (%)")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

# Weather Overview
def weather_summary():
    bh_weather = bahrain.weather_data.iloc[0]
    sz_weather = suzuka.weather_data.iloc[0]

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🏜️ Bahrain Weather")
        st.json(bh_weather.to_dict())
    with col2:
        st.subheader("🌸 Suzuka Weather")
        st.json(sz_weather.to_dict())

# Tabs for Navigation
tab1, tab2, tab3, tab4 = st.tabs(["Sector Comparison", "Tyre Degradation", "Throttle Trace", "Weather"])

with tab1:
    compare_sectors()

with tab2:
    st.subheader("Bahrain")
    tyre_degradation(bahrain, "Tyre Degradation - Bahrain")
    st.subheader("Suzuka")
    tyre_degradation(suzuka, "Tyre Degradation - Suzuka")

with tab3:
    throttle_trace()

with tab4:
    weather_summary()
