# Implementasi sederhana Machine Learning untuk prediksi potensi banjir
# Catatan: dataset yang digunakan dibuat secara simulasi untuk demonstrasi.

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

def buat_data_simulasi(jumlah=500, seed=42):
    """Membuat data contoh; bukan data banjir nyata."""
    data = pd.DataFrame({
        "curah_hujan_mm": [],
        "tinggi_sungai_cm": [],
        "kelembapan_persen": [],
        "banjir": []
    })
    rng = __import__("numpy").random.default_rng(seed)
    hujan = rng.uniform(0, 180, jumlah)
    sungai = rng.uniform(20, 250, jumlah)
    lembap = rng.uniform(40, 100, jumlah)

    # Label simulasi berdasarkan kombinasi hujan dan tinggi sungai.
    skor = (hujan > 100).astype(int) + (sungai > 170).astype(int) + (lembap > 85).astype(int)
    banjir = (skor >= 2).astype(int)

    data = pd.DataFrame({
        "curah_hujan_mm": hujan.round(1),
        "tinggi_sungai_cm": sungai.round(1),
        "kelembapan_persen": lembap.round(1),
        "banjir": banjir
    })
    return data

def main():
    data = buat_data_simulasi()
    X = data[["curah_hujan_mm", "tinggi_sungai_cm", "kelembapan_persen"]]
    y = data["banjir"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    prediksi = model.predict(X_test)
    print("=== Evaluasi model pada data simulasi ===")
    print(f"Akurasi: {accuracy_score(y_test, prediksi):.2%}")
    print(classification_report(y_test, prediksi, target_names=["Tidak Banjir", "Potensi Banjir"], zero_division=0))

    # Contoh prediksi untuk kondisi baru (ubah angka sesuai skenario).
    kondisi_baru = pd.DataFrame([{
        "curah_hujan_mm": 125,
        "tinggi_sungai_cm": 190,
        "kelembapan_persen": 90
    }])
    hasil = model.predict(kondisi_baru)[0]
    probabilitas = model.predict_proba(kondisi_baru)[0][1]

    print("=== Contoh prediksi ===")
    print("Input: hujan 125 mm, tinggi sungai 190 cm, kelembapan 90%")
    print("Hasil:", "Potensi Banjir" if hasil == 1 else "Tidak terindikasi banjir")
    print(f"Skor probabilitas model untuk kelas banjir: {probabilitas:.1%}")
    print("\nPENTING: Ini demonstrasi dengan data buatan, bukan sistem peringatan dini.")

if __name__ == "__main__":
    main()
