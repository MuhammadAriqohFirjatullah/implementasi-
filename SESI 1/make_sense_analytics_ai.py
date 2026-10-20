"""
Make Sense of Data with Analytics and AI
Contoh implementasi sederhana: analisis data penjualan dan prediksi penjualan.

Cara menjalankan:
1. Install Python 3.10+.
2. Buka terminal di folder file ini.
3. Jalankan: pip install -r requirements.txt
4. Jalankan: python make_sense_analytics_ai.py

Script memakai dataset contoh buatan sendiri, jadi tidak perlu mengunduh dataset.
Output:
- Ringkasan statistik di terminal
- Grafik tren penjualan dan perbandingan kategori
- Prediksi penjualan untuk bulan berikutnya
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score


def create_sample_data():
    """Membuat data penjualan bulanan contoh."""
    data = {
        "bulan": pd.date_range(start="2025-01-01", periods=18, freq="MS"),
        "produk": [
            "Laptop", "Ponsel", "Aksesori", "Laptop", "Ponsel", "Aksesori",
            "Laptop", "Ponsel", "Aksesori", "Laptop", "Ponsel", "Aksesori",
            "Laptop", "Ponsel", "Aksesori", "Laptop", "Ponsel", "Aksesori",
        ],
        "jumlah_terjual": [
            18, 35, 60, 20, 38, 65, 22, 42, 70,
            25, 45, 73, 27, 48, 78, 30, 52, 82
        ],
        "harga_satuan": [
            8500000, 4500000, 150000, 8500000, 4500000, 150000,
            8500000, 4500000, 150000, 8500000, 4500000, 150000,
            8500000, 4500000, 150000, 8500000, 4500000, 150000
        ],
    }
    df = pd.DataFrame(data)
    df["pendapatan"] = df["jumlah_terjual"] * df["harga_satuan"]
    return df


def run_analytics(df, output_dir):
    print("\n=== MAKE SENSE OF DATA WITH ANALYTICS AND AI ===")
    print("\n1. Lima baris data pertama:")
    print(df.head().to_string(index=False))

    print("\n2. Ringkasan data:")
    print(f"Total unit terjual : {df['jumlah_terjual'].sum():,}")
    print(f"Total pendapatan   : Rp{df['pendapatan'].sum():,.0f}")
    print(f"Rata-rata pendapatan per catatan: Rp{df['pendapatan'].mean():,.0f}")

    category_summary = (
        df.groupby("produk", as_index=False)
        .agg(total_unit=("jumlah_terjual", "sum"),
             total_pendapatan=("pendapatan", "sum"))
        .sort_values("total_pendapatan", ascending=False)
    )
    print("\n3. Analisis per produk:")
    print(category_summary.to_string(index=False))

    monthly = df.groupby("bulan", as_index=False).agg(
        total_pendapatan=("pendapatan", "sum"),
        total_unit=("jumlah_terjual", "sum")
    )

    # Grafik 1: tren pendapatan bulanan
    plt.figure(figsize=(10, 5))
    plt.plot(monthly["bulan"], monthly["total_pendapatan"], marker="o")
    plt.title("Tren Pendapatan Bulanan")
    plt.xlabel("Bulan")
    plt.ylabel("Pendapatan (Rp)")
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_dir / "tren_pendapatan.png", dpi=150)
    plt.close()

    # Grafik 2: pendapatan berdasarkan produk
    plt.figure(figsize=(8, 5))
    plt.bar(category_summary["produk"], category_summary["total_pendapatan"])
    plt.title("Total Pendapatan per Produk")
    plt.xlabel("Produk")
    plt.ylabel("Pendapatan (Rp)")
    plt.tight_layout()
    plt.savefig(output_dir / "pendapatan_per_produk.png", dpi=150)
    plt.close()

    return monthly


def run_ai_prediction(monthly, output_dir):
    """Melatih regresi linear sederhana untuk memperkirakan pendapatan berikutnya."""
    model_data = monthly.copy()
    model_data["urutan_bulan"] = range(1, len(model_data) + 1)

    X = model_data[["urutan_bulan"]]
    y = model_data["total_pendapatan"]

    # Demonstrasi sederhana: evaluasi pada 3 bulan terakhir.
    X_train, X_test = X.iloc[:-3], X.iloc[-3:]
    y_train, y_test = y.iloc[:-3], y.iloc[-3:]

    evaluation_model = LinearRegression()
    evaluation_model.fit(X_train, y_train)
    predictions = evaluation_model.predict(X_test)

    print("\n4. Evaluasi model prediksi (3 bulan terakhir):")
    print(f"MAE : Rp{mean_absolute_error(y_test, predictions):,.0f}")
    print(f"R²  : {r2_score(y_test, predictions):.3f}")

    # Latih ulang memakai seluruh data, lalu prediksi bulan berikutnya.
    final_model = LinearRegression()
    final_model.fit(X, y)
    next_month_number = len(model_data) + 1
    next_prediction = final_model.predict(pd.DataFrame({"urutan_bulan": [next_month_number]}))[0]
    next_month = model_data["bulan"].max() + pd.offsets.MonthBegin(1)

    print("\n5. Hasil prediksi AI:")
    print(f"Perkiraan pendapatan {next_month.strftime('%B %Y')}: Rp{next_prediction:,.0f}")
    print("Catatan: ini hanya demonstrasi regresi linear pada data contoh, bukan jaminan hasil nyata.")

    # Grafik aktual vs garis model dan prediksi berikutnya.
    future_dates = list(model_data["bulan"]) + [next_month]
    future_x = pd.DataFrame({"urutan_bulan": range(1, len(model_data) + 2)})
    future_y = final_model.predict(future_x)

    plt.figure(figsize=(10, 5))
    plt.plot(model_data["bulan"], y, marker="o", label="Pendapatan aktual")
    plt.plot(future_dates, future_y, linestyle="--", marker="x", label="Garis prediksi")
    plt.scatter([next_month], [next_prediction], marker="*", s=180, label="Prediksi bulan berikutnya")
    plt.title("Prediksi Pendapatan Menggunakan Regresi Linear")
    plt.xlabel("Bulan")
    plt.ylabel("Pendapatan (Rp)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_dir / "prediksi_pendapatan.png", dpi=150)
    plt.close()


def main():
    output_dir = Path(__file__).resolve().parent / "output"
    output_dir.mkdir(exist_ok=True)

    df = create_sample_data()
    monthly = run_analytics(df, output_dir)
    run_ai_prediction(monthly, output_dir)

    csv_path = output_dir / "data_penjualan_contoh.csv"
    df.to_csv(csv_path, index=False)

    print("\nSelesai! File hasil disimpan di folder:")
    print(output_dir)
    print("- data_penjualan_contoh.csv")
    print("- tren_pendapatan.png")
    print("- pendapatan_per_produk.png")
    print("- prediksi_pendapatan.png")


if __name__ == "__main__":
    main()
