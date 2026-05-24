# Dashboard NDVI Segara Anakan 🌿

Interactive dashboard for analyzing vegetation density and spatial autocorrelation in the Segara Anakan coastal area, Cilacap Regency, using Sentinel-2 satellite imagery (2025).

**Live Demo → [segara-anakan-ndvi.streamlit.app](https://segara-anakan-ndvi.streamlit.app)**

---

## Overview

Segara Anakan is a dynamic coastal wetland ecosystem characterized by mangrove forests, aquaculture ponds, agricultural land, and built-up areas. Rapid sedimentation, tidal influence, and human activity drive continuous changes in vegetation cover — making periodic, accurate monitoring essential for sustainable coastal management.

This dashboard processes Sentinel-2 data (10m spatial resolution, 5-day revisit) acquired via Google Earth Engine (GEE) to compute NDVI values across the study area, then applies spatial statistical methods to detect clustering patterns.

---

## Features

- **Satellite Map** — NDVI raster visualization from Sentinel-2 with RdYlGn colormap
- **Interactive Point Map** — Folium map with color-coded NDVI points and popups; toggle between street map and satellite imagery
- **NDVI Distribution** — Histogram with vegetation class coloring and mean indicator
- **Spatial Autocorrelation** — Global Moran's I statistics, Moran Scatterplot, and LISA cluster map
- **LISA Cluster Table** — High-High, High-Low, Low-Low, Low-High breakdown with percentages

---

## Methods

| Method | Description |
|--------|-------------|
| **NDVI** | Normalized Difference Vegetation Index derived from Sentinel-2 Band 8 (NIR) and Band 4 (Red) |
| **Global Moran's I** | Measures overall spatial autocorrelation of vegetation density across observation points |
| **LISA** | Local Indicator of Spatial Association — identifies local spatial clusters and outliers |

Significance level: α = 5% (Z-threshold = 1.96)

---

## Results Summary

| Metric | Value |
|--------|-------|
| Total observation points | 2,593 |
| Mean NDVI | 0.761 |
| Moran's I | 0.0225 |
| Z(I) statistic | 22.47 |
| Spatial autocorrelation | Positive, statistically significant |

**LISA Clusters:**
- High-High (dense vegetation clusters): **40.19%**
- High-Low (spatial outliers): **24.37%**
- Low-High (spatial outliers): **21.63%**
- Low-Low (degraded vegetation clusters): **13.81%**

---

## Tech Stack

- [Streamlit](https://streamlit.io) — dashboard framework
- [Rasterio](https://rasterio.readthedocs.io) — raster data processing
- [Folium](https://python-visualization.github.io/folium) — interactive maps
- [Matplotlib](https://matplotlib.org) — charts and visualizations
- [Google Earth Engine](https://earthengine.google.com) — satellite data acquisition

---

## Local Setup

```bash
git clone https://github.com/your-username/ndvi-segara-anakan.git
cd ndvi-segara-anakan
pip install -r requirements.txt
python -m streamlit run app.py
```

Make sure the `data/` folder contains:
```
data/
├── ndvi_segara_anakan25.csv
├── NDVI_Sentinel2_2025_Float.tif
├── plot_moran_scatterplot.png
└── plot_peta_klaster_LISA.png
```

---

## Data Source

Satellite imagery from [Sentinel-2 MSI](https://developers.google.com/earth-engine/datasets/catalog/sentinel-2) via Google Earth Engine, acquired for Segara Anakan, Cilacap — 2025.

---
