import plotly.express as px
import pandas as pd
import json
from pathlib import Path

# Veri yolları
DATA_DIR = Path("data")
regions_path = DATA_DIR / "regions.json"
geojson_path = DATA_DIR / "uk_regions.geojson"

# Verileri yükle
with open(regions_path, encoding="utf-8") as f:
    regions = pd.read_json(f)
 

with open(geojson_path, "r", encoding="utf-8") as f:
    geojson = json.load(f)

# Choropleth haritası
fig = px.choropleth(
    regions,
    geojson=geojson,
    locations="id",  # regions.json’daki bölge ID'si
    featureidkey="properties.rgn19cd",  # geojson’daki karşılık gelen key
    color="poverty_rate",
    hover_name="name",
    color_continuous_scale="Reds",
    range_color=(regions["poverty_rate"].min(), regions["poverty_rate"].max()),  # Dinamik renk aralığı
    projection="mercator",
    title="UK Regions by Poverty Rate"
)

fig.update_geos(
    fitbounds="locations",
    visible=True,
    resolution=110,
    showcountries=True,
    showlakes=True,
    landcolor="lightgray"
)
fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
fig.show()

region_ids = set(regions["id"])
geojson_ids = set([feature["properties"]["rgn19cd"] for feature in geojson["features"]])
missing = region_ids - geojson_ids

if missing:
    print("Eşleşmeyen ID'ler:", missing)
else:
    print("Tüm ID'ler eşleşiyor.")

print("Haritada gösterilen ID'ler:", regions["id"].tolist())
print(regions[regions["poverty_rate"].isna()])