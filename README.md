<p align="center">
  <img src="https://raw.githubusercontent.com/itsreallyryuu/Siesta-Osint/main/assets/banner.png" width="100%">
</p>

<h1 align="center">🕵️‍♂️ Siesta OSINT v1</h1>

<p align="center">
  <b>Simple • Fast • Structured OSINT Toolkit</b><br>
  Built for reconnaissance, information gathering, and learning OSINT from terminal.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?style=flat-square">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-green?style=flat-square">
  <img src="https://img.shields.io/badge/OSINT-Toolkit-red?style=flat-square">
</p>

---

## 🔍 About Siesta OSINT

**Siesta OSINT v1** adalah **tool CLI (Command Line Interface) berbasis Python** yang dirancang untuk melakukan **Open Source Intelligence (OSINT)** secara cepat, praktis, dan terstruktur langsung dari terminal.

Tool ini membantu proses:
- Information Gathering  
- Reconnaissance  
- Analisis awal target  

dengan memanfaatkan **data terbuka (open-source)** dari internet dan layanan publik.

Siesta OSINT cocok digunakan oleh:
- OSINT Researcher  
- Security Enthusiast  
- Bug Hunter  
- Pentester pemula hingga menengah  
- Investigator Digital  
- Pelajar yang ingin belajar OSINT secara praktis  

---

## ✨ Features

### 🔐 Whois Domain
- Mengambil data WHOIS dari registry resmi (IANA & WHOIS server terkait)
- Mendukung berbagai TLD secara otomatis
- Menampilkan informasi domain selengkap yang tersedia (non-GDPR protected)

**Data yang bisa diperoleh:**
- Domain Name
- Registrar
- Creation Date
- Expiration Date
- Updated Date
- Name Server
- Domain Status
- Informasi tambahan lainnya (jika tersedia)

---

### 🌐 IP Information
- Informasi dasar alamat IP
- ISP & Organization
- ASN
- Country / Region
- Network information

Digunakan untuk analisis awal target berbasis IP.

---

### 📡 DNS Lookup
Melakukan pengecekan DNS record pada domain.

**Record yang didukung:**
- A
- MX
- NS
- TXT

Berguna untuk memahami konfigurasi DNS dan potensi misconfiguration.

---

### 👤 Username Checker
- Mengecek ketersediaan atau keberadaan username di berbagai platform populer
- Cocok untuk OSINT profiling dan investigasi identitas digital

---

### 📄 HTTP Header Analyzer
- Analisis HTTP response header
- Deteksi server
- Security headers
- Informasi konfigurasi HTTP

---

### 🧠 Web Technology Detection
- Deteksi teknologi website
- Web server
- Framework
- CMS (jika terdeteksi)
- Teknologi frontend/backend umum

Digunakan untuk fingerprinting awal website.

---

### 📍 IP Geolocation
- Pelacakan lokasi IP berbasis database publik
- Negara, region, kota
- ISP / Organization
- Latitude & Longitude
- Link Google Maps (copyable)

⚠️ Tidak melakukan pelacakan real-time.

---

### 🎯 Attack Surface Mapper
Melakukan pemetaan permukaan serangan (*attack surface*) pada sebuah domain.

**Fungsi utama:**
- Resolve IP address
- Enumerasi subdomain sederhana
- Pengambilan DNS record penting
- Deteksi hosting dan CDN dasar

Digunakan untuk reconnaissance awal dan asset discovery.

---

### 🌍 Online Presence Scanner
- Mencari jejak kehadiran online username / keyword
- Menampilkan platform yang terdeteksi
- URL profile
- Confidence level (LOW / MEDIUM / HIGH)

---

### 🔄 Website Change Monitor
- Mengambil snapshot website
- Membandingkan perubahan konten
- Mendeteksi perubahan mencurigakan atau defacement

---

## 🖥️ Platform Support

Siesta OSINT dapat dijalankan di:

- ✅ Windows (CMD / PowerShell)
- ✅ Linux (Terminal)
- ✅ macOS (Terminal)
- ✅ WSL (Windows Subsystem for Linux)
- ✅ Server / VPS Linux

❌ Tidak direkomendasikan untuk Termux (Android)

---

## 📦 Installation

### Requirements
- Python 3.8 atau lebih baru
- Koneksi internet aktif

---

### Install & Run

```bash
git clone https://github.com/itsreallyryuu/Siesta-Osint.git
cd Siesta-Osint
pip install -r requirements.txt

# jika terjadi error pada dnspython
python -m pip install dnspython

# jalankan tools
python main.py
