# Dashboard NDVI Segara Anakan 🌿

Dashboard interaktif untuk menganalisis kerapatan vegetasi dan autokorelasi spasial di kawasan pesisir Segara Anakan, Kabupaten Cilacap, menggunakan citra satelit Sentinel-2 (2025).

## Live Demo
[app-ndvi-segara-anakan.streamlit.app](https://app-ndvi-segara-anakan.streamlit.app)

---

## Overview

Segara Anakan merupakan ekosistem lahan basah pesisir yang dinamis, dicirikan oleh hutan mangrove, tambak budidaya, lahan pertanian, dan kawasan terbangun. Sedimentasi yang cepat, pengaruh pasang surut, serta aktivitas manusia mendorong perubahan tutupan vegetasi secara terus-menerus — sehingga pemantauan yang berkala dan akurat menjadi hal yang esensial dalam pengelolaan pesisir berkelanjutan.

Dashboard ini memproses data Sentinel-2 (resolusi spasial 10m, revisit 5 hari) yang diperoleh melalui Google Earth Engine (GEE) untuk menghitung nilai NDVI di seluruh wilayah kajian, kemudian menerapkan metode statistik spasial untuk mendeteksi pola pengelompokan vegetasi.

---

## Fitur

- **Peta Citra Satelit** — Visualisasi raster NDVI dari Sentinel-2 dengan colormap RdYlGn
- **Peta Titik Interaktif** — Peta Folium dengan titik NDVI berkode warna dan popup; dapat beralih antara peta jalan dan citra satelit
- **Distribusi NDVI** — Histogram dengan pewarnaan kelas vegetasi dan indikator rata-rata
- **Autokorelasi Spasial** — Statistik Moran's I global, Moran Scatterplot, dan peta klaster LISA
- **Tabel Klaster LISA** — Rincian High-High, High-Low, Low-Low, Low-High beserta persentasenya

---

## Metode

| Metode | Deskripsi |
|--------|-----------|
| **NDVI** | Normalized Difference Vegetation Index yang diturunkan dari Band 8 (NIR) dan Band 4 (Red) Sentinel-2 |
| **Moran's I Global** | Mengukur autokorelasi spasial keseluruhan kerapatan vegetasi antar titik pengamatan |
| **LISA** | Local Indicator of Spatial Association — mengidentifikasi klaster spasial lokal dan pencilan spasial |

Taraf signifikansi: α = 5%

---

## Hasil

| Metrik | Nilai |
|--------|-------|
| Total titik pengamatan | 2.593 |
| Rata-rata NDVI | 0,761 |
| Moran's I | 0,0225 |
| Statistik Z(I) | 22,47 |
| Autokorelasi spasial | Positif, signifikan secara statistik |

**Klaster LISA:**
- High-High: **40,19%**
- High-Low: **24,37%**
- Low-High: **21,63%**
- Low-Low: **13,81%**

---

## Tech Stack yang digunakan

- [Streamlit](https://streamlit.io) — dashboard framework
- [Rasterio](https://rasterio.readthedocs.io) — pemrosesan data raster
- [Folium](https://python-visualization.github.io/folium) — peta interaktif
- [Matplotlib](https://matplotlib.org) — grafik dan visualisasi data
- [Google Earth Engine](https://earthengine.google.com) — penggunaan data satelit

---

## Setup Lokal

```bash
git clone https://github.com/ayunitamaharani/streamlit-ndvi-segara-anakan.git
cd streamlit-ndvi-segara-anakan
pip install -r requirements.txt
python -m streamlit run app.py
```

Pastikan folder `data/` berisi file berikut:

```
data/
├── ndvi_segara_anakan25.csv
├── NDVI_Sentinel2_2025_Float.tif
├── plot_moran_scatterplot.png
└── plot_peta_klaster_LISA.png
```

---

## Sumber Data

Citra satelit dari [Sentinel-2 MSI](https://developers.google.com/earth-engine/datasets/catalog/sentinel-2) melalui Google Earth Engine, diperoleh untuk wilayah Segara Anakan, Cilacap (2025).

---
