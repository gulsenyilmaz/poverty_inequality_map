import streamlit as st
import pandas as pd
import plotly.express as px
import json

st.set_page_config(layout="wide")

# Başlık
st.title("UK Poverty & Health Dashboard")
st.markdown("Explore regional differences in poverty rates and key health indicators across the United Kingdom.")

tab1, tab2 = st.tabs(["📊 Region Comparison", "🗺️ Map View"])


# Veriyi yükle
df = pd.read_json("data/regions.json")

# Sidebar - filtreleme
st.sidebar.header("Filters")
threshold = st.sidebar.slider("Poverty rate ≥", min_value=15.0, max_value=30.0, value=20.0)


filtered_df = df[df["poverty_rate"] >= threshold]

with tab1:

    col1, col2 = st.columns([1, 2])  # sol dar, sağ geniş

    with col1:
        
        
        st.subheader("Region Overview")
        st.metric("Regions Displayed", len(filtered_df))

        avg_poverty = round(filtered_df["poverty_rate"].mean(), 2)
        st.metric("Average Poverty Rate", f"{avg_poverty}%")

        avg_life = round(filtered_df["life_expectancy_female"].mean(), 1)
        st.metric("Avg. Female Life Expectancy", f"{avg_life} years")

        st.subheader("Select a Region")

        selected_region = st.selectbox(
            "Choose a region",
            options=df["name"].tolist()
        )

        region_data = df[df["name"] == selected_region].iloc[0]

        st.write("**Selected Region Details:**")
        st.write(f"**Population:** {region_data['population']:,}")
        st.write(f"**Poverty Rate:** {region_data['poverty_rate']}%")
        st.write(f"**Female Life Expectancy:** {region_data['life_expectancy_female']} years")
        st.write(f"**Male Life Expectancy:** {region_data['life_expectancy_male']} years")
        st.write(f"**Child Obesity Rate:** {region_data['child_obesity_rate']}%")
        st.write(f"**Mental Health Index:** {region_data['mental_health_index']}")


    # Bar chart
    with col2:
        fig = px.bar(
            filtered_df.sort_values(by="poverty_rate", ascending=False),
            x="name",
            y="poverty_rate",
            color="poverty_rate",
            color_continuous_scale="Reds",
            title="Poverty Rate by Region"
        )

        st.plotly_chart(fig, use_container_width=True)

        # Ekstra: Sağlıkla ilgili scatter plot
        fig2 = px.scatter(
            df,
            x="poverty_rate",
            y="life_expectancy_female",
            size="population",
            color="name",
            title="Poverty vs Female Life Expectancy",
            hover_name="name"
        )
        st.plotly_chart(fig2, use_container_width=True)

with tab2:
    with open("data/uk_regions.geojson", "r", encoding="utf-8") as f:
        geojson = json.load(f)

    fig_map = px.choropleth(
        df,
        geojson=geojson,
        locations="id",
        featureidkey="properties.rgn19cd",
        color="poverty_rate",
        hover_name="name",
        color_continuous_scale="Reds",
        title="UK Regions by Poverty Rate (Choropleth)"
    )

    fig_map.update_geos(
        fitbounds="locations",
        visible=False
    )

    st.plotly_chart(fig_map, use_container_width=True)