"""
Career and Competition in the Industrial Era
Implementasi sederhana: analisis keterampilan kerja dan rekomendasi keterampilan
yang perlu ditingkatkan berdasarkan lowongan kerja contoh.

Program:
- Membaca data lowongan kerja contoh.
- Menganalisis keterampilan yang paling sering diminta.
- Membandingkan keterampilan kandidat dengan kebutuhan pasar.
- Memberikan rekomendasi keterampilan prioritas.

Jalankan:
    pip install -r requirements.txt
    python career_competition_industrial_era.py
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def sample_job_data():
    """Dataset ilustrasi lowongan kerja; bukan data lowongan aktual."""
    rows = [
        ("Data Analyst", ["Python", "SQL", "Excel", "Data Visualization", "Communication"]),
        ("Junior Data Scientist", ["Python", "Machine Learning", "SQL", "Statistics", "Communication"]),
        ("AI Engineer", ["Python", "Machine Learning", "Deep Learning", "Cloud", "Problem Solving"]),
        ("Web Developer", ["HTML/CSS", "JavaScript", "Git", "Problem Solving", "Communication"]),
        ("Business Intelligence Analyst", ["SQL", "Excel", "Data Visualization", "Communication", "Problem Solving"]),
        ("IT Support", ["Networking", "Cybersecurity", "Communication", "Problem Solving", "Cloud"]),
        ("Cybersecurity Analyst", ["Cybersecurity", "Networking", "Python", "Problem Solving", "Cloud"]),
        ("Machine Learning Engineer", ["Python", "Machine Learning", "Deep Learning", "SQL", "Cloud"]),
        ("Digital Marketing Analyst", ["Excel", "Data Visualization", "Communication", "Problem Solving", "SQL"]),
        ("Software Developer", ["Python", "JavaScript", "Git", "Problem Solving", "Communication"]),
    ]

    records = []
    for role, skills in rows:
        for skill in skills:
            records.append({"posisi": role, "keterampilan": skill})
    return pd.DataFrame(records)


def analyze_market(df, output_dir):
    skill_counts = (
        df.groupby("keterampilan")
        .size()
        .sort_values(ascending=False)
        .rename("jumlah_lowongan_contoh")
        .reset_index()
    )

    print("\n=== CAREER AND COMPETITION IN THE INDUSTRIAL ERA ===")
    print("\n1. Keterampilan yang sering muncul pada lowongan contoh:")
    print(skill_counts.to_string(index=False))

    plt.figure(figsize=(10, 6))
    sorted_counts = skill_counts.sort_values("jumlah_lowongan_contoh")
    plt.barh(sorted_counts["keterampilan"], sorted_counts["jumlah_lowongan_contoh"])
    plt.title("Keterampilan yang Dibutuhkan pada Dataset Lowongan Contoh")
    plt.xlabel("Jumlah kemunculan pada lowongan contoh")
    plt.ylabel("Keterampilan")
    plt.tight_layout()
    plt.savefig(output_dir / "keterampilan_pasar_kerja.png", dpi=150)
    plt.close()

    return skill_counts


def recommend_skills(skill_counts):
    print("\n2. Masukkan keterampilan yang sudah kamu kuasai.")
    print("Contoh: Python, SQL, Excel")
    raw = input("Keterampilan yang dikuasai: ").strip()

    candidate_skills = {
        item.strip().lower()
        for item in raw.split(",")
        if item.strip()
    }

    normalized_market = {
        row["keterampilan"].lower(): int(row["jumlah_lowongan_contoh"])
        for _, row in skill_counts.iterrows()
    }

    matched = [
        skill for skill in normalized_market
        if skill in candidate_skills
    ]
    missing = [
        (skill, count) for skill, count in normalized_market.items()
        if skill not in candidate_skills
    ]
    missing.sort(key=lambda item: item[1], reverse=True)

    print("\n3. Hasil kecocokan keterampilan:")
    if matched:
        print("Keterampilan yang cocok dengan dataset:", ", ".join(matched))
    else:
        print("Belum ada keterampilan yang cocok berdasarkan nama yang dimasukkan.")

    print("\n4. Rekomendasi keterampilan untuk dipelajari:")
    for skill, count in missing[:5]:
        print(f"- {skill.title()} (muncul {count} kali pada lowongan contoh)")

    print("\nCatatan:")
    print("- Dataset ini hanya ilustrasi untuk demonstrasi analisis data.")
    print("- Rekomendasi bukan jaminan pekerjaan; kebutuhan tiap perusahaan berbeda.")
    print("- Untuk analisis nyata, ganti dataset dengan data lowongan kerja aktual.")


def main():
    output_dir = Path(__file__).resolve().parent / "output"
    output_dir.mkdir(exist_ok=True)

    df = sample_job_data()
    df.to_csv(output_dir / "dataset_lowongan_contoh.csv", index=False)

    skill_counts = analyze_market(df, output_dir)
    recommend_skills(skill_counts)

    print("\nSelesai. Hasil disimpan di folder:", output_dir)
    print("- dataset_lowongan_contoh.csv")
    print("- keterampilan_pasar_kerja.png")


if __name__ == "__main__":
    main()
