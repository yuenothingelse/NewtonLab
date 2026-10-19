<div align="center">

# 🧮 NewtonLab

### Kalkulator Penyelesaian Persamaan Nonlinier dengan Metode **Newton-Raphson**

*Project UTS Praktikum Komputasi Numerik C*

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-8B7CFF?style=for-the-badge)
![SymPy](https://img.shields.io/badge/SymPy-Symbolic-3B5526?style=for-the-badge)
![NumPy](https://img.shields.io/badge/NumPy-Numerical-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Plot-11557C?style=for-the-badge)

<img src="assets/screenshot.png" alt="Tampilan NewtonLab" width="850">

</div>

---

## 📑 Daftar Isi

- [✨ Fitur](#-fitur)
- [🎯 Tentang Metode Newton-Raphson](#-tentang-metode-newton-raphson)
- [🚀 Cara Menjalankan](#-cara-menjalankan)
- [🕹️ Cara Menggunakan](#️-cara-menggunakan)
- [🧪 Contoh Kasus](#-contoh-kasus)
- [🧠 Penjelasan Kode](#-penjelasan-kode)
- [📁 Struktur Repository](#-struktur-repository)
- [👥 Anggota Kelompok](#-anggota-kelompok)

---

## ✨ Fitur

| Fitur | Keterangan |
|---|---|
| ✍️ **Input fungsi bebas** | Ketik f(x) sendiri, misalnya `x^3 - x - 2` atau `cos(x) - x` |
| ⚙️ **Parameter fleksibel** | Tebakan awal (x₀), toleransi error, dan maksimum iterasi |
| 📊 **Kartu ringkasan** | Perkiraan akar, error akhir, dan jumlah iterasi tampil di bagian atas |
| 📋 **Riwayat iterasi** | Tabel n, xₙ, f(xₙ), f′(xₙ), xₙ₊₁, dan error di setiap langkah |
| 📈 **Grafik fungsi** | Kurva f(x), garis sumbu x, serta penanda titik akar yang ditemukan |
| 🧮 **Turunan otomatis** | f′(x) dihitung secara simbolik oleh SymPy, tidak perlu input manual |
| 🛑 **Kriteria berhenti** | Berhenti saat error ≤ toleransi **atau** iterasi mencapai batas maksimum |
| ✅ **Status konvergensi** | Pesan status di bawah tabel, misalnya "BERHASIL · Konvergen: error ≤ toleransi" |
| 💡 **Panduan input** | Contoh fungsi dan daftar fungsi yang didukung langsung di panel input |
| 🛡️ **Validasi input** | Pesan kesalahan jelas untuk fungsi kosong, format salah, toleransi ≤ 0, dan turunan mendekati nol |
| 🌙 **Tampilan dark mode** | Antarmuka modern dengan aksen ungu |

---
