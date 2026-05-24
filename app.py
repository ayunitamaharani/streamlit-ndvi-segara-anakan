import streamlit as st
import rasterio
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
from PIL import Image
import io

# CONFIG
st.set_page_config(
    page_title="Dashboard NDVI · Segara Anakan",
    layout="wide",
    page_icon="🌿",
    initial_sidebar_state="expanded"
)

# CSS — Minimalist UI · Pale Sage Green Theme
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Newsreader:ital,wght@0,400;0,500;1,400;1,500&family=DM+Sans:wght@300;400;500;600&family=Geist+Mono:wght@400;500&display=swap');

/* ── BASE ── */
html, body, [class*="css"], * {
    font-family: 'DM Sans', 'Helvetica Neue', sans-serif !important;
}

/* ── PAGE BACKGROUND: Pale Sage Green ── */
.stApp {
    background-color: #EEF2EC !important;
}
[data-testid="stAppViewContainer"] {
    background-color: #EEF2EC !important;
}
[data-testid="stMain"] {
    background-color: #EEF2EC !important;
}
.main .block-container {
    background-color: transparent !important;
    padding-top: 1.5rem !important;
    padding-bottom: 2rem !important;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background-color: #E4EBE1 !important;
    border-right: 1px solid #C8D9C3 !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] li,
[data-testid="stSidebar"] label {
    color: #2F3D2B !important;
    font-size: 13px !important;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #1A2E18 !important;
}

/* ── METRIC CARDS ── */
[data-testid="stMetric"] {
    background-color: #F4F7F2 !important;
    border: 1px solid #C8D9C3 !important;
    border-radius: 10px !important;
    padding: 1.1rem 1.4rem !important;
    box-shadow: none !important;
}
[data-testid="stMetricLabel"] p {
    font-size: 11px !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: #5A7057 !important;
}
[data-testid="stMetricValue"] {
    font-family: 'Newsreader', Georgia, serif !important;
    font-size: 28px !important;
    font-weight: 400 !important;
    letter-spacing: -0.02em !important;
    color: #1A2E18 !important;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background-color: #DDE7DA;
    border-radius: 10px;
    padding: 5px;
    gap: 4px;
    border: none;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 7px;
    font-size: 13px;
    font-weight: 500;
    color: #5A7057;
    padding: 8px 18px;
    background: transparent;
    border: none;
}
.stTabs [aria-selected="true"] {
    background-color: #2F5C2A !important;
    color: #ffffff !important;
    font-weight: 600 !important;
    border-bottom: none !important;
}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] {
    display: none !important;
}

/* ── HEADINGS ── */
h1, h2, h3, h4 {
    font-family: 'Newsreader', Georgia, serif !important;
    color: #1A2E18 !important;
    font-weight: 400 !important;
    letter-spacing: -0.02em !important;
}

/* ── DOWNLOAD BUTTON ── */
.stDownloadButton > button {
    background-color: #F4F7F2 !important;
    color: #2F5C2A !important;
    border: 1px solid #A8C5A2 !important;
    border-radius: 6px !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    padding: 6px 16px !important;
    letter-spacing: 0.02em;
    box-shadow: none !important;
}
.stDownloadButton > button:hover {
    background-color: #2F5C2A !important;
    color: #ffffff !important;
    border-color: #2F5C2A !important;
}

/* ── DIVIDER ── */
hr {
    border-color: #C8D9C3 !important;
}

/* ── CAPTION ── */
.stCaption, [data-testid="stCaptionContainer"] p {
    color: #111111 !important;
    font-size: 12px !important;
    opacity: 1 !important;
}

/* ── HEADER BLOCK ── */
.ndvi-header {
    background: #F4F7F2;
    border: 1px solid #C8D9C3;
    border-radius: 12px;
    padding: 2.2rem 2.8rem;
    margin-bottom: 1.6rem;
    position: relative;
    overflow: hidden;
}
.ndvi-header::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 220px; height: 220px;
    background: radial-gradient(circle, rgba(47,92,42,0.05) 0%, transparent 70%);
    pointer-events: none;
}
.ndvi-badge {
    display: inline-block;
    background: #DDE7DA;
    border: 1px solid #C8D9C3;
    border-radius: 9999px;
    padding: 3px 13px;
    font-size: 10px;
    font-weight: 600;
    color: #2F5C2A;
    letter-spacing: 0.07em;
    margin-bottom: 10px;
    text-transform: uppercase;
}
.ndvi-header-title {
    font-family: 'Newsreader', Georgia, serif !important;
    font-size: 34px;
    font-weight: 400;
    letter-spacing: -0.03em;
    color: #1A2E18;
    line-height: 1.1;
    margin-bottom: 6px;
}
.ndvi-header-title span {
    font-style: italic;
    color: #2F5C2A;
}
.ndvi-header-sub {
    font-size: 13px;
    color: #5A7057;
    font-weight: 400;
}

/* ── MORAN CHIPS ── */
.moran-chips {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    margin: 12px 0 20px;
}
.moran-chip {
    background: #F4F7F2;
    border: 1px solid #C8D9C3;
    border-radius: 10px;
    padding: 14px 20px;
    min-width: 150px;
}
.moran-chip-label {
    font-size: 10px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: .07em;
    color: #7A9475;
    margin-bottom: 4px;
}
.moran-chip-value {
    font-family: 'Newsreader', Georgia, serif;
    font-size: 26px;
    font-weight: 400;
    letter-spacing: -0.02em;
    color: #1A2E18;
}
.moran-chip-desc {
    font-size: 11px;
    color: #7A9475;
    margin-top: 2px;
}

/* ── NDVI SCALE BAR ── */
.ndvi-scale-bar {
    height: 10px;
    border-radius: 5px;
    background: linear-gradient(90deg, #ef4444, #f97316, #eab308, #84cc16, #22c55e, #15803d);
    margin: 8px 0 4px;
}
.ndvi-scale-labels {
    display: flex;
    justify-content: space-between;
    font-size: 10px;
    font-family: 'Geist Mono', monospace;
    color: #7A9475;
}

/* ── TABLES ── */
table {
    border-collapse: collapse !important;
}
thead tr {
    background-color: #DDE7DA !important;
}
tbody tr {
    background-color: #F4F7F2 !important;
}
tbody tr:hover {
    background-color: #EEF2EC !important;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #EEF2EC; }
::-webkit-scrollbar-thumb { background: #A8C5A2; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# UTILS
def fig_to_bytes(fig, fmt="png", dpi=150):
    buf = io.BytesIO()
    fig.savefig(buf, format=fmt, dpi=dpi, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    buf.seek(0)
    return buf.read()


# LOAD DATA
@st.cache_data
def load_data():
    return pd.read_csv("data/ndvi_segara_anakan25.csv")

df = load_data()


# SIDEBAR
with st.sidebar:
    st.markdown("""
<div style="background:#2F5C2A; border-radius:10px; padding:16px 18px; margin-bottom:4px;">
    <div style="font-size:10px; font-weight:600; letter-spacing:0.08em; text-transform:uppercase; color:rgba(255,255,255,0.6); margin-bottom:6px;">Analisis Vegetasi</div>
    <div style="font-family:'Georgia',serif; font-size:20px; font-weight:400; color:#ffffff; letter-spacing:-0.02em; line-height:1.2;">Dashboard NDVI</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div style="background:#F4F7F2; border:1px solid #C8D9C3; border-radius:10px; padding:14px 16px; margin-bottom:4px;">
    <div style="font-size:10px; font-weight:600; letter-spacing:0.07em; text-transform:uppercase; color:#7A9475; margin-bottom:10px;">Informasi</div>
    <div style="font-size:12px; color:#2F3D2B; line-height:1.8;">
        <div style="margin-bottom:4px;"><span style="color:#7A9475;">Wilayah</span><br><strong>Segara Anakan, Cilacap</strong></div>
        <div style="border-top:1px solid #C8D9C3; padding-top:8px; margin-top:4px;"><span style="color:#7A9475;">Sumber Data</span><br><a href="https://developers.google.com/earth-engine/datasets/catalog/sentinel-2" target="_blank" style="color:#2F5C2A; font-weight:600; text-decoration:none;">Sentinel-2 MSI (2025) ↗</a></div>
        <div style="border-top:1px solid #C8D9C3; padding-top:8px; margin-top:4px;"><span style="color:#7A9475;">Metode</span><br><strong>Moran's I · LISA Cluster</strong></div>
    </div>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div style="background:#F4F7F2; border:1px solid #C8D9C3; border-radius:10px; padding:14px 16px; margin-bottom:4px;">
    <div style="font-size:10px; font-weight:600; letter-spacing:0.07em; text-transform:uppercase; color:#5A7057; margin-bottom:10px;">Skala Warna NDVI</div>
    <div style="height:10px; border-radius:5px; background:linear-gradient(90deg,#ef4444,#f97316,#eab308,#84cc16,#22c55e,#15803d); margin-bottom:6px;"></div>
    <div style="display:flex; justify-content:space-between; font-size:10px; font-family:monospace; color:#7A9475;">
        <span>0.0</span><span>0.2</span><span>0.4</span><span>0.6</span><span>0.8</span><span>1.0</span>
    </div>
    <div style="margin-top:12px; display:flex; flex-direction:column; gap:6px;">
        <div style="display:flex; align-items:center; gap:8px; font-size:11px; color:#2F3D2B;">
            <div style="width:10px;height:10px;border-radius:50%;background:#15803d;flex-shrink:0;"></div>
            <span>≥ 0.6 — Vegetasi Lebat</span>
        </div>
        <div style="display:flex; align-items:center; gap:8px; font-size:11px; color:#2F3D2B;">
            <div style="width:10px;height:10px;border-radius:50%;background:#84cc16;flex-shrink:0;"></div>
            <span>0.4–0.6 — Vegetasi Sedang</span>
        </div>
        <div style="display:flex; align-items:center; gap:8px; font-size:11px; color:#2F3D2B;">
            <div style="width:10px;height:10px;border-radius:50%;background:#f97316;flex-shrink:0;"></div>
            <span>0.1–0.4 — Vegetasi Jarang</span>
        </div>
        <div style="display:flex; align-items:center; gap:8px; font-size:11px; color:#2F3D2B;">
            <div style="width:10px;height:10px;border-radius:50%;background:#ef4444;flex-shrink:0;"></div>
            <span>&lt; 0.1 — Non-vegetasi</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div style="text-align:center; font-size:10px; color:#7A9475; padding-top:8px;">
    Dibuat dengan Streamlit · Sentinel-2 2025
</div>
""", unsafe_allow_html=True)


# HEADER
st.markdown("""
<div class="ndvi-header">
    <div class="ndvi-badge">Sentinel-2 · 2025</div>
    <div class="ndvi-header-title">Dashboard NDVI<br><span>Segara Anakan</span></div>
    <div class="ndvi-header-sub">Analisis Autokorelasi Spasial · Moran's I · Peta Klaster LISA</div>
</div>
""", unsafe_allow_html=True)


# METRIC CARDS
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Titik Sampel", f"{len(df):,}")
c2.metric("NDVI Rata-rata", f"{df['NDVI'].mean():.3f}")
c3.metric("NDVI Maksimum", f"{df['NDVI'].max():.3f}")
c4.metric("NDVI Minimum", f"{df['NDVI'].min():.3f}")

st.markdown("---")


# TABS
tab1, tab2, tab3 = st.tabs([
    "Citra Satelit",
    "Sebaran NDVI",
    "Autokorelasi Spasial"
])

# TAB 1 — Citra Satelit
with tab1:
    st.markdown("### Peta Raster NDVI Sentinel-2 (2025)")
    st.caption("Resolusi spasial 10m. Warna hijau menunjukkan vegetasi lebat, warna merah menunjukkan vegetasi rendah atau non-vegetasi.")

    with rasterio.open("data/NDVI_Sentinel2_2025_Float.tif") as src:
        ndvi_raster = src.read(1).astype(float)
        nodata = src.nodata
    if nodata is not None:
        ndvi_raster[ndvi_raster == nodata] = np.nan

    fig, ax = plt.subplots(figsize=(12, 7))
    fig.patch.set_facecolor('#F4F7F2')
    ax.set_facecolor('#F4F7F2')

    im = ax.imshow(ndvi_raster, cmap="RdYlGn", vmin=0, vmax=1, interpolation='bilinear')
    cbar = plt.colorbar(im, ax=ax, shrink=0.55, pad=0.02)
    cbar.set_label("Nilai NDVI", fontsize=11, color='#2F3D2B')
    cbar.ax.yaxis.set_tick_params(color='#2F3D2B')
    plt.setp(cbar.ax.yaxis.get_ticklabels(), color='#2F3D2B', fontsize=9)
    ax.set_title("Peta NDVI Wilayah Segara Anakan 2025",
                 fontsize=14, fontweight='bold', color='#1A2E18', pad=14,
                 fontfamily='DejaVu Sans')
    ax.axis("off")

    st.pyplot(fig)

    img_bytes = fig_to_bytes(fig, fmt="png", dpi=200)
    st.download_button(
        label="Download Peta PNG (Hi-Res)",
        data=img_bytes,
        file_name="peta_ndvi_segara_anakan_2025.png",
        mime="image/png"
    )


# TAB 2 — Sebaran NDVI
with tab2:
    col_h, col_dl = st.columns([3, 1])
    with col_h:
        st.markdown("### Peta Interaktif Sebaran Titik NDVI")
        st.caption("Klik setiap titik untuk melihat nilai NDVI, koordinat latitude, dan longitude.")
    with col_dl:
        st.markdown(" ")
        csv_bytes = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download CSV",
            data=csv_bytes,
            file_name="ndvi_segara_anakan25.csv",
            mime="text/csv"
        )

    center_lat = df["latitude"].mean()
    center_lon = df["longitude"].mean()

    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=11,
        tiles=None
    )

    folium.TileLayer(
        tiles="CartoDB positron",
        name="Peta Jalan",
        control=True
    ).add_to(m)

    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="Citra Satelit",
        control=True
    ).add_to(m)

    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="Label",
        overlay=True,
        control=True
    ).add_to(m)

    def ndvi_color(val):
        if val >= 0.6:
            return "#15803d"
        elif val >= 0.4:
            return "#84cc16"
        elif val >= 0.1:
            return "#f97316"
        else:
            return "#ef4444"

    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row["latitude"], row["longitude"]],
            radius=4,
            color=ndvi_color(row["NDVI"]),
            fill=True,
            fill_color=ndvi_color(row["NDVI"]),
            fill_opacity=0.8,
            weight=0.5,
            popup=folium.Popup(
                f"<b>NDVI: {row['NDVI']:.3f}</b><br>Lat: {row['latitude']:.5f}<br>Lon: {row['longitude']:.5f}",
                max_width=160
            )
        ).add_to(m)

    folium.LayerControl(position="topright", collapsed=False).add_to(m)
    st_folium(m, width="100%", height=480)

    # Histogram
    st.markdown("### Distribusi Nilai NDVI")

    fig2, ax2 = plt.subplots(figsize=(10, 3.5))
    fig2.patch.set_facecolor('#F4F7F2')
    ax2.set_facecolor('#F4F7F2')

    n, bins, patches = ax2.hist(df['NDVI'], bins=60, edgecolor='none')
    for patch, left in zip(patches, bins[:-1]):
        if left >= 0.6:   patch.set_facecolor('#15803d')
        elif left >= 0.4: patch.set_facecolor('#84cc16')
        elif left >= 0.1: patch.set_facecolor('#f97316')
        else:             patch.set_facecolor('#ef4444')

    mean_ndvi = df['NDVI'].mean()
    ax2.axvline(mean_ndvi, color='#2F5C2A', linewidth=1.8, linestyle='--', alpha=0.85)
    ax2.text(mean_ndvi + 0.01, ax2.get_ylim()[1] * 0.88,
             f"Rata-rata: {mean_ndvi:.3f}", color='#2F5C2A', fontsize=10)

    ax2.set_xlabel("Nilai NDVI", fontsize=11, color='#2F3D2B')
    ax2.set_ylabel("Frekuensi", fontsize=11, color='#2F3D2B')
    ax2.set_title("Histogram Distribusi NDVI — Segara Anakan 2025",
                  fontsize=12, fontweight='bold', color='#1A2E18')
    ax2.tick_params(colors='#7A9475')
    ax2.spines[['top', 'right']].set_visible(False)
    ax2.spines[['left', 'bottom']].set_color('#C8D9C3')

    st.pyplot(fig2)

    hist_bytes = fig_to_bytes(fig2)
    st.download_button(
        "Download Histogram PNG",
        data=hist_bytes,
        file_name="histogram_ndvi_2025.png",
        mime="image/png"
    )


# TAB 3 — Autokorelasi Spasial
with tab3:
    st.markdown("### Analisis Autokorelasi Spasial")
    st.caption("Hasil Moran's I global dan peta klaster LISA.")

    moran_i = 0.0225
    e_i     = -0.000386
    var_i   =  0.00116
    z_i     = 22.4738

    st.markdown(f"""
<div class="moran-chips">
    <div class="moran-chip">
        <div class="moran-chip-label">Moran's I</div>
        <div class="moran-chip-value">{moran_i:.4f}</div>
        <div class="moran-chip-desc">Indeks autokorelasi spasial</div>
    </div>
    <div class="moran-chip">
        <div class="moran-chip-label">E(I)</div>
        <div class="moran-chip-value" style="color:#1F6C9F">{e_i:.6f}</div>
        <div class="moran-chip-desc">Nilai ekspektasi</div>
    </div>
    <div class="moran-chip">
        <div class="moran-chip-label">Var(I)</div>
        <div class="moran-chip-value" style="color:#5A3EA6">{var_i:.5f}</div>
        <div class="moran-chip-desc">Varians</div>
    </div>
    <div class="moran-chip">
        <div class="moran-chip-label">Z(I)</div>
        <div class="moran-chip-value" style="color:#956400">{z_i:.4f}</div>
        <div class="moran-chip-desc">Z(I) &gt; Z&#x2080;.&#x2080;&#x2082;&#x2085; = 1,96</div>
    </div>
</div>
""", unsafe_allow_html=True)

    col_m, col_l = st.columns(2)

    with col_m:
        st.markdown("#### Moran Scatterplot")
        moran_img = Image.open("data/plot_moran_scatterplot.png")
        st.image(moran_img, use_container_width=True)
        buf = io.BytesIO()
        moran_img.save(buf, format="PNG")
        st.download_button(
            "Download Moran Scatterplot",
            data=buf.getvalue(),
            file_name="moran_scatterplot.png",
            mime="image/png"
        )

    with col_l:
        st.markdown("#### Peta Klaster LISA")
        lisa_img = Image.open("data/plot_peta_klaster_LISA.png")
        st.image(lisa_img, use_container_width=True)
        buf2 = io.BytesIO()
        lisa_img.save(buf2, format="PNG")
        st.download_button(
            "Download Peta LISA",
            data=buf2.getvalue(),
            file_name="peta_klaster_LISA.png",
            mime="image/png"
        )

    st.markdown("---")
    st.markdown("#### Tabulasi Klaster LISA")

    lisa_rows = [
        ("High-High (HH)", 1042, "40,19%", "#d73027"),
        ("High-Low (HL)",  632,  "24,37%", "#fc8d59"),
        ("Low-Low (LL)",   358,  "13,81%", "#4575b4"),
        ("Low-High (LH)",  561,  "21,63%", "#91bfdb"),
    ]
    rows_html = ""
    for klaster, jumlah, persen, color in lisa_rows:
        dot = f'<span style="display:inline-block;width:9px;height:9px;border-radius:50%;background:{color};margin-right:8px;vertical-align:middle;"></span>'
        rows_html += f"""
        <tr style="border-bottom:1px solid #C8D9C3;">
            <td style="padding:10px 16px;">{dot}{klaster}</td>
            <td style="padding:10px 16px; text-align:right;">{jumlah:,}</td>
            <td style="padding:10px 16px; text-align:right;">{persen}</td>
        </tr>"""
    rows_html += """
        <tr style="border-top:2px solid #A8C5A2; font-weight:600; color:#1A2E18;">
            <td style="padding:10px 16px;">Total</td>
            <td style="padding:10px 16px; text-align:right;">2.593</td>
            <td style="padding:10px 16px; text-align:right;">100%</td>
        </tr>"""

    st.markdown(f"""
<div style="background:#F4F7F2; border:1px solid #C8D9C3; border-radius:10px; overflow:hidden; margin-bottom:1.4rem;">
    <table style="width:100%; border-collapse:collapse; font-family:'DM Sans','Helvetica Neue',sans-serif; font-size:13px;">
        <thead>
            <tr style="background:#DDE7DA;">
                <th style="padding:11px 16px; text-align:left; font-weight:600; font-size:10px; text-transform:uppercase; letter-spacing:.07em; color:#5A7057;">Klaster</th>
                <th style="padding:11px 16px; text-align:right; font-weight:600; font-size:10px; text-transform:uppercase; letter-spacing:.07em; color:#5A7057;">Jumlah Titik</th>
                <th style="padding:11px 16px; text-align:right; font-weight:600; font-size:10px; text-transform:uppercase; letter-spacing:.07em; color:#5A7057;">Persentase</th>
            </tr>
        </thead>
        <tbody style="color:#2F3D2B;">{rows_html}</tbody>
    </table>
</div>
""", unsafe_allow_html=True)

    st.markdown("#### Interpretasi Hasil")
    st.markdown(f"""
Hasil perhitungan statistik uji Moran's I menghasilkan nilai **E(I) = {e_i:.6f}**, **Var(I) = {var_i:.5f}**,
dan **Z(I) = {z_i:.4f}**. Karena nilai Z(I) = {z_i:.4f} lebih besar dari Z&#x2080;.&#x2080;&#x2082;&#x2085; = 1,96,
maka H&#x2080; ditolak. Dengan demikian dapat disimpulkan bahwa terdapat autokorelasi spasial
positif namun korelasinya tergolong lemah karena mendekati nol. Hal ini mengindikasikan
bahwa kerapatan vegetasi antar titik yang berdekatan memiliki kemiripan nilai,
namun pola pengelompokannya tidak terlalu kuat.

Hasil analisis LISA menunjukkan karakteristik sebaran kerapatan vegetasi di wilayah Segara Anakan
pada tahun 2025. Klaster High-High sebesar 40,19% menunjukkan area vegetasi lebat yang cenderung
mengelompok secara spasial dengan sangat kuat, dan klaster Low-Low sebesar 13,81% menunjukkan
area vegetasi rendah yang juga mengelompok, yang mungkin merupakan area yang mengalami degradasi
vegetasi akibat aktivitas manusia dan proses sedimentasi yang signifikan. Selain itu, terdapat
outlier spasial berupa klaster High-Low sebesar 24,37% dan klaster Low-High sebesar 21,63%,
masing-masing yang menunjukkan area transisi antara area bervegetasi lebat dan rendah, yang
mungkin merupakan zona tepi laguna atau zona pasang surut yang lebih dinamis.
""")
