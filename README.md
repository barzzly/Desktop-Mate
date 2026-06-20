# Desktop Mate: Kucing Pixel Bongo

Aplikasi desktop mascot interaktif berbentuk Kucing Bongo lucu menggunakan PyQt6 dan Python. Maskot ini akan menemanimu di layar dengan berbagai reaksi animasi lucu, fitur alarm pengingat, dan status manja/sedih.

## Fitur Utama

- 🐾 **Maskot Melayang Transparan**: Maskot melayang di atas semua jendela (always on top) tanpa mengganggu pekerjaanmu.
- ⏰ **Alarm Pengingat Heboh**: Kucing akan melompat secara aktif dan memutar suara `nontifalarm.mp3` secara terus-menerus ketika waktu alarm tiba.
- 🛑 **Matikan Alarm Mudah**: Cukup klik pada tubuh kucing melompat atau tekan tombol "Berhenti Lompat" di Dashboard untuk menghentikan alarm.
- ⌨️ **Deteksi Ketikan Global**: Kucing akan bereaksi ikut sibuk mengetik (`typing`) saat mendeteksi ketikan keyboard global. Jika mengetik terlalu cepat/bising, kucing akan marah (`angry`).
- 🧻 **Deteksi Scroll Mouse**: Kucing akan beraksi menarik tisu toilet (`scroll`) saat mendeteksi scroll mouse.
- 🥺 **Status Sedih (Sad Mode)**: Kucing akan sesekali masuk ke status sedih gabut, memutar suara `mintadihelus.mp3`, dan memunculkan balon ucapan minta di-patpat. Cukup arahkan mouse ke kucing untuk membuatnya bahagia kembali!
- 💖 **Interaktif (Petting & Feeding)**: Berikan makan atau panggil kucing langsung dari Dashboard, serta elus tubuh kucing untuk memunculkan efek hati.

## Cara Instalasi

1. **Pastikan Python 3.10+ sudah terinstal di Windows.**
2. **Buka Terminal (PowerShell/CMD) di folder proyek.**
3. **Buat Virtual Environment (Opsional tetapi disarankan):**
   ```powershell
   python -m venv venv
   ```
4. **Aktifkan Virtual Environment:**
   - **PowerShell:**
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - **CMD:**
     ```cmd
     .\venv\Scripts\activate.bat
     ```
5. **Instal Dependensi:**
   ```powershell
   pip install -r requirements.txt
   ```
6. **Jalankan Aplikasi:**
   ```powershell
   python main.py
   ```
