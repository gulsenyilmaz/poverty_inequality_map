# main.py
from fastapi import FastAPI, HTTPException
import json
from pathlib import Path

app = FastAPI()

# Veriyi dosyadan yükle
DATA_PATH = Path("data/regions.json")
with open(DATA_PATH, "r", encoding="utf-8") as f:
    regions = json.load(f)

@app.get("/regions")
def get_regions():
    return regions


@app.get("/regions/with-high-poverty")
def get_high_poverty_regions(threshold: float = 25.0):
    return [r for r in regions if r["poverty_rate"] >= threshold]


@app.get("/regions/compare")
def compare_regions(region1: str, region2: str):
    r1 = next((r for r in regions if r["id"] == region1), None)
    r2 = next((r for r in regions if r["id"] == region2), None)
    if not r1 or not r2:
        raise HTTPException(status_code=404, detail="One or both regions not found")
    return {"region1": r1, "region2": r2}

@app.get("/regions/{region_id}")
def get_region_by_id(region_id: str):
    for region in regions:
        if region["id"] == region_id:
            return region
    raise HTTPException(status_code=404, detail="Region not found")