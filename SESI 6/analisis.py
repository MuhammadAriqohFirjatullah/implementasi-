"""
Analisis Hotspot terhadap Tutupan Lahan di Bengkulu
--------------------------------------------------
Input:
  - hotspot.csv: CSV hotspot NASA FIRMS, minimal memiliki kolom latitude dan longitude.
  - tutupan_lahan.shp beserta file pendamping (.shx, .dbf, .prj, dll).
Output:
  - hasil_analisis.csv
  - grafik_hotspot.png
  - peta_hotspot.png

PENTING:
1. Letakkan semua file input di folder yang sama dengan analisis.py.
2. Sesuaikan NAMA_KOLOM_KELAS di bawah dengan nama kolom kelas tutupan lahan.
3. Data tutupan lahan sebaiknya sudah dibatasi untuk Provinsi Bengkulu.
"""

from pathlib import Path
import sys

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

FOLDER = Path(__file__).resolve().parent
FILE_HOTSPOT = FOLDER / "hotspot.csv"
FILE_TUTUPAN_LAHAN = FOLDER / "tutupan_lahan.shp"

# Ganti sesuai nama kolom kelas pada shapefile, misalnya "NAMOBJ", "kelas", atau "landcover".
NAMA_KOLOM_KELAS = "NAMA_KELAS"


def main():
    # Periksa file input
    if not FILE_HOTSPOT.exists():
        sys.exit(
            f"File tidak ditemukan: {FILE_HOTSPOT.name}\\n"
            "Letakkan CSV hotspot di folder proyek dan beri nama hotspot.csv."
        )
    if not FILE_TUTUPAN_LAHAN.exists():
        sys.exit(
            f"File tidak ditemukan: {FILE_TUTUPAN_LAHAN.name}\\n"
            "Letakkan shapefile tutupan lahan beserta file pendampingnya di folder proyek."
        )

    print("Membaca data...")
    hotspot = pd.read_csv(FILE_HOTSPOT)
    lahan = gpd.read_file(FILE_TUTUPAN_LAHAN)

    # Nama kolom sering berbeda antar-sumber data; samakan huruf kecil/besar.
    kolom_lookup = {str(c).strip().lower(): c for c in hotspot.columns}
    lat_col = kolom_lookup.get("latitude") or kolom_lookup.get("lat")
    lon_col = (
        kolom_lookup.get("longitude")
        or kolom_lookup.get("lon")
        or kolom_lookup.get("long")
    )
    if lat_col is None or lon_col is None:
        sys.exit(
            "Kolom koordinat tidak ditemukan. CSV harus memiliki kolom latitude/longitude "
            "(atau lat/lon). Kolom tersedia: " + ", ".join(map(str, hotspot.columns))
        )

    # Konversi koordinat menjadi numerik dan buang baris yang tidak valid.
    hotspot[lat_col] = pd.to_numeric(hotspot[lat_col], errors="coerce")
    hotspot[lon_col] = pd.to_numeric(hotspot[lon_col], errors="coerce")
    hotspot = hotspot.dropna(subset=[lat_col, lon_col]).copy()

    if hotspot.empty:
        sys.exit("Tidak ada koordinat hotspot valid di dalam CSV.")

    if lahan.crs is None:
        sys.exit(
            "CRS shapefile tidak diketahui. Pastikan file .prj tersedia "
            "atau tetapkan CRS yang benar di GIS terlebih dahulu."
        )

    # Temukan kolom kelas jika nama yang ditentukan belum cocok.
    kelas_col = NAMA_KOLOM_KELAS
    if kelas_col not in lahan.columns:
        kandidat = [
            c for c in lahan.columns
            if any(k in str(c).lower() for k in ["kelas", "class", "landcover", "land_cover", "nama"])
        ]
        print("\\nKolom pada shapefile:", list(lahan.columns))
        if kandidat:
            print("Kolom yang mungkin berisi kelas:", kandidat)
        sys.exit(
            f"Kolom kelas '{kelas_col}' tidak ditemukan. "
            "Ubah NAMA_KOLOM_KELAS di bagian atas analisis.py sesuai kolom yang benar."
        )

    titik = gpd.GeoDataFrame(
        hotspot,
        geometry=gpd.points_from_xy(hotspot[lon_col], hotspot[lat_col]),
        crs="EPSG:4326",
    ).to_crs(lahan.crs)

    print("Menggabungkan titik hotspot dengan tutupan lahan...")
    hasil = gpd.sjoin(
        titik,
        lahan[[kelas_col, "geometry"]],
        how="inner",
        predicate="within",
    )

    if hasil.empty:
        sys.exit(
            "Tidak ada hotspot yang jatuh di dalam poligon tutupan lahan. "
            "Periksa cakupan wilayah dan sistem koordinat (CRS) kedua data."
        )

    ringkasan = (
        hasil.groupby(kelas_col)
        .size()
        .sort_values(ascending=False)
        .rename("jumlah_hotspot")
        .reset_index()
    )
    ringkasan.to_csv(FOLDER / "hasil_analisis.csv", index=False)

    # Grafik
    ax = ringkasan.set_index(kelas_col)["jumlah_hotspot"].plot(
        kind="bar", figsize=(11, 6)
    )
    ax.set_title("Jumlah Hotspot Berdasarkan Tutupan Lahan")
    ax.set_xlabel("Kelas Tutupan Lahan")
    ax.set_ylabel("Jumlah hotspot")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(FOLDER / "grafik_hotspot.png", dpi=300, bbox_inches="tight")
    plt.close()

    # Peta
    fig, ax = plt.subplots(figsize=(10, 9))
    lahan.plot(ax=ax, color="lightgrey", edgecolor="white", linewidth=0.25)
    hasil.plot(ax=ax, color="red", markersize=5, alpha=0.75)
    ax.set_title("Persebaran Hotspot pada Tutupan Lahan")
    ax.set_axis_off()
    plt.tight_layout()
    plt.savefig(FOLDER / "peta_hotspot.png", dpi=300, bbox_inches="tight")
    plt.close()

    print("\\nAnalisis selesai.")
    print(ringkasan.to_string(index=False))
    print("\\nFile hasil tersimpan:")
    print("- hasil_analisis.csv")
    print("- grafik_hotspot.png")
    print("- peta_hotspot.png")
    print("\\nCatatan: hasil ini menunjukkan tumpang tindih spasial, bukan bukti penyebab kebakaran.")


if __name__ == "__main__":
    main()
