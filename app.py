import streamlit as st
import pandas as pd
import numpy as np

# 1. CONFIGURE THE PAGE
st.set_page_config(
    page_title="CrystalScout AI",
    page_icon="⚛️",
    layout="wide"
)

# 2. THE HEADER
st.title("⚛️ CrystalScout: AI-Powered Materials Discovery")
st.markdown("""
**Objective:** Autonomous screening of inorganic semiconductors for photovoltaic applications.
*Built by [Your Name] using Python & Streamlit.*
""")
st.divider()

# 3. SIDEBAR (The "Lab Controls")
st.sidebar.header("🔬 Filter Parameters")
st.sidebar.info("Adjust the sliders to filter the AI-predicted candidates.")

target_bg = st.sidebar.slider("Band Gap Range (eV)", 0.0, 5.0, (1.0, 2.0))
max_cost = st.sidebar.slider("Max Synthesis Cost ($/kg)", 0, 1000, 200)
min_stability = st.sidebar.select_slider(
    "Stability Level",
    options=["Unstable", "Meta-Stable", "Stable"],
    value="Meta-Stable"
)

# 4. SIMULATE AI DATA (The "Backend")
# This creates 500 fake materials that look like your VAE results
np.random.seed(42)
data_size = 500
df = pd.DataFrame({
    'Material_ID': [f'mp-{np.random.randint(1000,9999)}' for _ in range(data_size)],
    'Formula': np.random.choice(['LiCoO2', 'FePO4', 'SiC', 'GaN', 'TiO2', 'MAPbI3', 'CsSnI3'], data_size),
    'Band_Gap_eV': np.random.normal(1.8, 0.8, data_size).round(2),
    'Predicted_Stability': np.random.choice(['Stable', 'Meta-Stable', 'Unstable'], data_size, p=[0.2, 0.5, 0.3]),
    'Synthesis_Cost': np.random.randint(50, 800, data_size)
})

# 5. FILTER LOGIC
# Filter by Band Gap
filtered_df = df[
    (df['Band_Gap_eV'] >= target_bg[0]) & 
    (df['Band_Gap_eV'] <= target_bg[1]) &
    (df['Synthesis_Cost'] <= max_cost)
]

# Filter by Stability (Text logic)
if min_stability == "Stable":
    filtered_df = filtered_df[filtered_df['Predicted_Stability'] == "Stable"]
elif min_stability == "Meta-Stable":
    filtered_df = filtered_df[filtered_df['Predicted_Stability'].isin(["Stable", "Meta-Stable"])]

# 6. DASHBOARD LAYOUT
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader(f"✅ Candidates Found: {len(filtered_df)}")
    st.dataframe(filtered_df, height=400, use_container_width=True)

with col2:
    st.subheader("📊 Property Distribution")
    # Built-in Streamlit Chart (No extra libraries needed)
    st.scatter_chart(
        filtered_df,
        x='Band_Gap_eV',
        y='Synthesis_Cost',
        color='Predicted_Stability',
        size=50,
        height=400
    )

# 7. EXPORT SECTION
st.caption("Data Source: Simulated inference from Random Forest & VAE models.")