import os
import sys
import random
import ctypes
from ctypes import wintypes
from PyQt6.QtCore import Qt, QTimer, QPoint, QSize, QTime
from PyQt6.QtGui import QPixmap, QIcon, QAction, QCursor, QGuiApplication, QPainter, QColor
from PyQt6.QtWidgets import (QApplication, QMenu, QSystemTrayIcon, QWidget, 
                             QDialog, QVBoxLayout, QHBoxLayout, QLabel, QSlider, 
                             QComboBox, QPushButton, QProgressBar, QCheckBox, QLineEdit, QTimeEdit)

# Deteksi ketikan keyboard global menggunakan GetAsyncKeyState ya Putri cantik

# Ini fungsi buat nyari path asset-nya ya Putri cantik, biar kalau di-build jadi .exe gak error
def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Ini UI/UX lucu (Dashboard Control Panel) yang muncul di navbar/taskbar ya Putri cantik
class CatDashboard(QWidget):
    def __init__(self, mascot):
        super().__init__()
        self.mascot = mascot
        self.mascot.dashboard = self # Sambungkan ke mascotnya ya Putri cantik
        
        # Atur judul dan ikon di taskbar biar kelihatan profesional tapi imut
        self.setWindowTitle("Dashboard Kucing Pixel")
        self.setWindowIcon(QIcon(get_resource_path("assets/idle_left.png")))
        
        # Desain gaya tampilan Dashboard dengan pastel pink & ungu yang super lucu ya Putri cantik
        self.setStyleSheet("""
            QWidget {
                background-color: #FFF0F5; /* LavenderBlush yang soft */
                font-family: 'Comic Sans MS', 'Segoe UI', sans-serif;
            }
            QLabel {
                color: #C71585; /* MediumVioletRed biar kontras & imut */
                font-weight: bold;
                font-size: 13px;
            }
            #TitleLabel {
                font-size: 18px;
                color: #FF1493; /* DeepPink untuk judul utama */
                margin-bottom: 10px;
            }
            QProgressBar {
                border: 2px solid #FF69B4; /* HotPink border */
                border-radius: 8px;
                text-align: center;
                color: #C71585;
                font-weight: bold;
                background-color: #FFFFFF;
            }
            QProgressBar::chunk {
                background-color: #FF69B4;
                border-radius: 6px;
            }
            QPushButton {
                background-color: #FF69B4;
                color: white;
                border: 2px solid #FF1493;
                border-radius: 12px;
                padding: 6px 12px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #FF1493;
            }
            QPushButton:pressed {
                background-color: #C71585;
            }
            QCheckBox {
                color: #C71585;
                font-weight: bold;
                font-size: 13px;
            }
            QComboBox {
                border: 2px solid #FF69B4;
                border-radius: 6px;
                padding: 4px;
                background-color: white;
                color: #C71585;
                font-weight: bold;
            }
            QLineEdit, QTimeEdit {
                border: 2px solid #FF69B4;
                border-radius: 6px;
                padding: 4px;
                background-color: white;
                color: #C71585;
                font-weight: bold;
            }
            QSlider::groove:horizontal {
                border: 1px solid #FF69B4;
                height: 8px;
                background: white;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background: #FF1493;
                border: 1px solid #C71585;
                width: 16px;
                height: 16px;
                margin: -4px 0;
                border-radius: 8px;
            }
        """)
        
        self.setFixedSize(360, 520)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Judul Utama Dashboard
        title = QLabel("🐾 DASHBOARD KUCING PUTERI IMUP 🐾")
        title.setObjectName("TitleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Status Kucing (Tidur/Mengejar/Wandering)
        status_layout = QHBoxLayout()
        status_layout.addWidget(QLabel("Status Kucing:"))
        self.status_val = QLabel("🧍 Diam Santai")
        status_layout.addWidget(self.status_val)
        layout.addLayout(status_layout)
        
        # Input Nama Kucing
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Nama Mascot:"))
        self.name_input = QLineEdit()
        self.name_input.setText(self.mascot.pet_name)
        self.name_input.textChanged.connect(self.update_pet_name)
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)
        
        # Indikator Energi Kucing (Progress Bar Hati)
        layout.addWidget(QLabel("Tingkat Energi Kucing (Bisa Capek):"))
        self.energy_bar = QProgressBar()
        self.energy_bar.setRange(0, 100)
        self.energy_bar.setValue(int(self.mascot.energy))
        layout.addWidget(self.energy_bar)
        
        layout.addSpacing(10)
        
        # Pengaturan Fitur Mengejar Kursor (Checkbox default Mati/Unchecked)
        self.follow_chk = QCheckBox("Ikuti Kursor Mouse (Chase Mode)")
        self.follow_chk.setChecked(self.mascot.follow_cursor)
        self.follow_chk.stateChanged.connect(self.toggle_follow)
        layout.addWidget(self.follow_chk)
        
        layout.addSpacing(10)
        
        # 1. Pilihan Ukuran Kucing
        layout.addWidget(QLabel("Ukuran Kucing:"))
        self.size_combo = QComboBox()
        self.size_combo.addItems(["128 x 128", "256 x 256"])
        self.size_combo.setCurrentText(f"{self.mascot.mascot_size.width()} x {self.mascot.mascot_size.height()}")
        self.size_combo.currentTextChanged.connect(self.change_size)
        layout.addWidget(self.size_combo)
        
        # 2. Pengatur Kecepatan Mengejar Kursor
        layout.addWidget(QLabel("Kecepatan Mengejar Kursor:"))
        self.glide_slider = QSlider(Qt.Orientation.Horizontal)
        self.glide_slider.setRange(2, 15)
        self.glide_slider.setValue(self.mascot.glide_speed)
        self.glide_slider.valueChanged.connect(self.change_glide_speed)
        layout.addWidget(self.glide_slider)
        
        layout.addSpacing(10)
        
        # --- Bagian Pengingat / Alarm ---
        layout.addWidget(QLabel("⏰ ALARM PENGINGAT ⏰"))
        
        time_layout = QHBoxLayout()
        time_layout.addWidget(QLabel("Waktu:"))
        self.alarm_time_edit = QTimeEdit()
        self.alarm_time_edit.setDisplayFormat("HH:mm")
        self.alarm_time_edit.setTime(QTime.currentTime().addSecs(60))
        time_layout.addWidget(self.alarm_time_edit)
        layout.addLayout(time_layout)
        
        msg_layout = QHBoxLayout()
        msg_layout.addWidget(QLabel("Pesan:"))
        self.alarm_msg_edit = QLineEdit()
        self.alarm_msg_edit.setText("Waktunya Istirahat! 🐾")
        msg_layout.addWidget(self.alarm_msg_edit)
        layout.addLayout(msg_layout)
        
        self.alarm_chk = QCheckBox("Aktifkan Alarm")
        self.alarm_chk.setChecked(False)
        self.alarm_chk.stateChanged.connect(self.toggle_alarm)
        layout.addWidget(self.alarm_chk)
        
        self.stop_alarm_btn = QPushButton("🛑 Berhenti Lompat")
        self.stop_alarm_btn.setEnabled(False)
        self.stop_alarm_btn.clicked.connect(self.stop_alarm_firing)
        layout.addWidget(self.stop_alarm_btn)
        
        layout.addSpacing(10)

        # Tombol-tombol Aksi Interaktif yang Lucu
        btn_layout = QHBoxLayout()
        
        feed_btn = QPushButton("🍖 Beri Makan")
        feed_btn.clicked.connect(self.feed_cat)
        btn_layout.addWidget(feed_btn)
        
        call_btn = QPushButton("📢 Panggil Kucing")
        call_btn.clicked.connect(self.call_cat)
        btn_layout.addWidget(call_btn)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def toggle_follow(self, state):
        # Update centang checkbox dan sinkronisasi ke mascot Putri cantik
        is_checked = (state == 2)
        self.mascot.follow_cursor = is_checked
        self.mascot.follow_action.setChecked(is_checked)
        if not is_checked:
            self.mascot.make_decision()

    def change_size(self, size_str):
        # Update ukuran mascot secara real-time Putri cantik
        w, h = map(int, size_str.split(" x "))
        self.mascot.mascot_size = QSize(w, h)
        self.mascot.load_sprites()
        # Resize window biar ada ruang melayang hati di atasnya ya Putri cantik
        self.mascot.resize(w, h + h // 2)
        self.mascot.update()

    def change_glide_speed(self, value):
        self.mascot.glide_speed = value

    def update_pet_name(self, text):
        self.mascot.pet_name = text
        self.mascot.update()

    def toggle_alarm(self, state):
        is_active = (state == 2)
        self.mascot.alarm_active = is_active
        if not is_active:
            self.mascot.stop_alarm()
            self.stop_alarm_btn.setEnabled(False)

    def stop_alarm_firing(self):
        self.mascot.stop_alarm()
        self.stop_alarm_btn.setEnabled(False)

    def feed_cat(self):
        # Kasih makan kucing Putri cantik biar energinya nambah banyak & ada animasinya
        self.mascot.start_eating()
        self.status_val.setText("😋 Nyam Nyam Enak!")

    def call_cat(self):
        # Panggil kucingnya balik ke tengah layar Putri cantik biar gak ilang
        screen_geometry = QGuiApplication.primaryScreen().availableGeometry()
        start_x = screen_geometry.width() // 2 - self.mascot.mascot_size.width() // 2
        start_y = screen_geometry.height() // 2 - self.mascot.mascot_size.height() // 2
        self.mascot.move(start_x, start_y)
        self.mascot.change_state("idle")

    def update_dashboard_data(self):
        """Update data energi dan status kucing di layar Dashboard Putri cantik"""
        self.energy_bar.setValue(int(self.mascot.energy))
        
        # Format status text agar lucu dan emoji pas
        state_labels = {
            "idle": "🧍 Diam Santai",
            "walk_left": "🏃 Mondar-mandir Kiri",
            "walk_right": "🏃 Mondar-mandir Kanan",
            "pet": "❤️ Manja Dielus",
            "sleep": "💤 Tidur Nyenyak (Kecapean)",
            "sleep_roll": "🔄 Guling-guling Lucu",
            "typing": "⌨️ Mengetik Sibuk",
            "angry": "💢 Marah (Bising!)",
            "eat": "😋 Nyam Nyam Enak!",
            "play_heart": "💖 Main Emoji Hati",
            "exhausted": "🥵 Kecapean (Istirahat)",
            "exhausted_transition": "🥺 Mulai Segar Kembali",
            "scroll": "🧻 Menarik Tisu Toilet",
            "reminder": "⏰ Pengingat: Lompat-Lompat!"
        }
        self.status_val.setText(state_labels.get(self.mascot.state, "🧍 Santai"))


class DesktopMate(QWidget):
    def __init__(self):
        super().__init__()
        
        # Ini ukuran kucing pixel kita ya Putri cantik, diatur biar pas di layar (128x128 px default)
        self.mascot_size = QSize(128, 128)
        self.pet_name = "Putri"
        
        # Ini buat ngatur kecepatan meluncur kucingnya mengejar kursor ya Putri cantik
        self.glide_speed = 6 # Jarak piksel per langkah gerakan mengejar
        self.walk_speed = 2 # Kecepatan jalan mondar-mandir sendiri
        self.tick_interval = 30 # Jeda waktu gerak (milidetik), diturunkan ke 30ms biar meluncur lebih mulus!
        
        # Fitur Alarm / Pengingat
        self.alarm_active = False
        self.alarm_firing = False
        self.alarm_message = "Waktunya Istirahat! 🐾"
        self.alarm_time = QTime(12, 0)
        
        # Ini jeda waktu buat ganti gambar animasinya ya Putri cantik
        self.anim_tick_interval = 200 # Lebih cepat sedikit biar gerakan kaki pas lari kelihatan pas
        
        # Sistem Energi / Kelelahan ya Putri cantik
        self.energy = 100.0 # Nilai awal energi (maksimal 100.0)
        
        # Ini daftar status kucingnya ya Putri cantik, diawali dengan diam
        self.state = "idle"
        self.direction = "left" # Arah hadap (kiri atau kanan)
        self.anim_frame = 1 # Frame animasi yang aktif (1 or 2)
        
        # Defaultnya tidak ikuti kursor (Wandering otomatis) sesuai perintah Putri cantik
        self.follow_cursor = False
        
        # Ini buat nandain kalau kucingnya lagi diseret atau dideketin mouse ya Putri cantik
        self.is_dragging = False
        self.drag_position = QPoint()
        self.press_pos = QPoint() # Koordinat saat klik pertama untuk bedain klik vs seret
        self.is_hovered = False
        
        # Sambungan ke Dashboard
        self.dashboard = None
        
        # Ini daftar buat nampung partikel hati merah yang melayang pas dielus ya Putri cantik
        self.hearts = []
        
        # Kita load semua gambar kucing pixelnya di sini ya Putri cantik
        self.load_sprites()
        
        # Ini buat ngatur tampilan jendelanya biar transparan ya Putri cantik
        self.init_ui()
        
        # Di sini kita pasang timer biar kucingnya bisa mengejar kursor dan ganti gaya ya Putri cantik
        # 1. Timer buat Gerakan Mengejar Kursor (Tanpa Gravitasi!)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_behavior)
        self.timer.start(self.tick_interval)
        
        # 2. Timer buat Frame Animasi
        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self.update_animation)
        self.anim_timer.start(self.anim_tick_interval)
        
        # 3. Timer buat nentuin pilihan gaya berikutnya saat tidak ikuti kursor ya Putri cantik
        self.decision_timer = QTimer(self)
        self.decision_timer.timeout.connect(self.make_decision)
        self.decision_timer.start(5000) # Ganti keputusan tiap 5 detik
        
        # Letakkan posisi awal kucing di tengah layar ya Putri cantik
        screen_geometry = QGuiApplication.primaryScreen().availableGeometry()
        start_x = screen_geometry.width() // 2 - self.mascot_size.width() // 2
        # Tengahkan koordinat Y dengan menghitung tinggi ekstra ruang hati ya Putri cantik
        start_y = screen_geometry.height() // 2 - (self.mascot_size.height() + self.mascot_size.height() // 2) // 2
        self.move(start_x, start_y)
        
        # Inisialisasi deteksi ngetik global ya Putri cantik
        self.typing_streak = 0
        self.typing_timer = QTimer(self)
        self.typing_timer.setSingleShot(True)
        self.typing_timer.timeout.connect(self.stop_typing)
        
        # Timer makan kucing Putri cantik
        self.eat_timer = QTimer(self)
        self.eat_timer.setSingleShot(True)
        self.eat_timer.timeout.connect(self.stop_eating)
        
        # Timer kecapean setelah marah Putri cantik
        self.exhausted_timer = QTimer(self)
        self.exhausted_timer.setSingleShot(True)
        self.exhausted_timer.timeout.connect(self.start_transition_idle)
        
        # Timer transisi kecapean ke idle Putri cantik
        self.transition_timer = QTimer(self)
        self.transition_timer.setSingleShot(True)
        self.transition_timer.timeout.connect(self.stop_exhausted)
        
        # Counter/timer untuk roll tidur Putri cantik
        self.sleep_duration_ticks = 0
        self.roll_frame_idx = 0
        self.roll_timer = QTimer(self)
        self.roll_timer.timeout.connect(self.advance_sleep_roll)
        
        # Timer deteksi scroll mouse global ya Putri cantik
        self.scroll_timer = QTimer(self)
        self.scroll_timer.setSingleShot(True)
        self.scroll_timer.timeout.connect(self.stop_scroll)
        self.scroll_streak = 0
        self.scroll_accumulator = 0
        self.scroll_direction = 1
        
        self.setup_keyboard_hook()
        self.setup_mouse_hook()

    def load_sprites(self):
        """Fungsi ini buat ngambil gambar terus diperbesar biar tetep keliatan pixelated yang lucu ya Putri cantik"""
        self.sprites = {}
        sprite_files = {
            "idle_left": "assets/idle_left.png",
            "idle_right": "assets/idle_right.png",
            "idle_left_1": "assets/idle_left_1.png",
            "idle_left_2": "assets/idle_left_2.png",
            "idle_left_3": "assets/idle_left_3.png",
            "idle_left_4": "assets/idle_left_4.png",
            "idle_right_1": "assets/idle_right_1.png",
            "idle_right_2": "assets/idle_right_2.png",
            "idle_right_3": "assets/idle_right_3.png",
            "idle_right_4": "assets/idle_right_4.png",
            "walk_left_1": "assets/walk_left_1.png",
            "walk_left_2": "assets/walk_left_2.png",
            "walk_right_1": "assets/walk_right_1.png",
            "walk_right_2": "assets/walk_right_2.png",
            "happy_left": "assets/happy_left.png",
            "happy_right": "assets/happy_right.png",
            "sleep_left_1": "assets/sleep_left_1.png",
            "sleep_left_2": "assets/sleep_left_2.png",
            "sleep_right_1": "assets/sleep_right_1.png",
            "sleep_right_2": "assets/sleep_right_2.png",
            "typing_left_1": "assets/typing_left_1.png",
            "typing_left_2": "assets/typing_left_2.png",
            "typing_right_1": "assets/typing_right_1.png",
            "typing_right_2": "assets/typing_right_2.png",
            "angry_left": "assets/angry_left.png",
            "angry_right": "assets/angry_right.png",
            "angry_left_1": "assets/angry_left_1.png",
            "angry_left_2": "assets/angry_left_2.png",
            "angry_right_1": "assets/angry_right_1.png",
            "angry_right_2": "assets/angry_right_2.png",
            "eat_left_1": "assets/eat_left_1.png",
            "eat_left_2": "assets/eat_left_2.png",
            "eat_right_1": "assets/eat_right_1.png",
            "eat_right_2": "assets/eat_right_2.png",
            "play_heart_left_1": "assets/play_heart_left_1.png",
            "play_heart_left_2": "assets/play_heart_left_2.png",
            "play_heart_left_3": "assets/play_heart_left_3.png",
            "play_heart_left_4": "assets/play_heart_left_4.png",
            "play_heart_right_1": "assets/play_heart_right_1.png",
            "play_heart_right_2": "assets/play_heart_right_2.png",
            "play_heart_right_3": "assets/play_heart_right_3.png",
            "play_heart_right_4": "assets/play_heart_right_4.png",
            "sleep_roll_left_1": "assets/sleep_roll_left_1.png",
            "sleep_roll_left_2": "assets/sleep_roll_left_2.png",
            "sleep_roll_left_3": "assets/sleep_roll_left_3.png",
            "sleep_roll_left_4": "assets/sleep_roll_left_4.png",
            "sleep_roll_right_1": "assets/sleep_roll_right_1.png",
            "sleep_roll_right_2": "assets/sleep_roll_right_2.png",
            "sleep_roll_right_3": "assets/sleep_roll_right_3.png",
            "sleep_roll_right_4": "assets/sleep_roll_right_4.png",
            "sleep_back_left": "assets/sleep_back_left.png",
            "sleep_back_right": "assets/sleep_back_right.png",
            "scroll_left_1": "assets/scroll_left_1.png",
            "scroll_left_2": "assets/scroll_left_2.png",
            "scroll_right_1": "assets/scroll_right_1.png",
            "scroll_right_2": "assets/scroll_right_2.png",
            "exhausted_left_1": "assets/exhausted_left_1.png",
            "exhausted_left_2": "assets/exhausted_left_2.png",
            "exhausted_right_1": "assets/exhausted_right_1.png",
            "exhausted_right_2": "assets/exhausted_right_2.png",
            "exhausted_transition_left_1": "assets/exhausted_transition_left_1.png",
            "exhausted_transition_left_2": "assets/exhausted_transition_left_2.png",
            "exhausted_transition_right_1": "assets/exhausted_transition_right_1.png",
            "exhausted_transition_right_2": "assets/exhausted_transition_right_2.png",
            "reminder_left_1": "assets/reminder_left_1.png",
            "reminder_left_2": "assets/reminder_left_2.png",
            "reminder_right_1": "assets/reminder_right_1.png",
            "reminder_right_2": "assets/reminder_right_2.png",
            "sad_left": "assets/sad_left.png",
            "sad_right": "assets/sad_right.png",
        }
        
        for name, filename in sprite_files.items():
            path = get_resource_path(filename)
            if not os.path.exists(path):
                if "reminder" in name:
                    # Fallback ke animasi jalan jika aset lompat belum ditambahkan
                    dir_part = "left" if "left" in name else "right"
                    frame_num = "1" if "1" in name else "2"
                    fallback_path = get_resource_path(f"assets/walk_{dir_part}_{frame_num}.png")
                    if os.path.exists(fallback_path):
                        pixmap = QPixmap(fallback_path)
                    else:
                        pixmap = QPixmap(get_resource_path(f"assets/idle_{dir_part}_1.png"))
                    scaled_pixmap = pixmap.scaled(
                        self.mascot_size, 
                        Qt.AspectRatioMode.KeepAspectRatio, 
                        Qt.TransformationMode.FastTransformation
                    )
                    self.sprites[name] = scaled_pixmap
                else:
                    print(f"Warning: Sprite file not found: {path}", file=sys.stderr)
                    pixmap = QPixmap(self.mascot_size)
                    pixmap.fill(Qt.GlobalColor.red)
                    self.sprites[name] = pixmap
            else:
                pixmap = QPixmap(path)
                scaled_pixmap = pixmap.scaled(
                    self.mascot_size, 
                    Qt.AspectRatioMode.KeepAspectRatio, 
                    Qt.TransformationMode.FastTransformation
                )
                self.sprites[name] = scaled_pixmap

    def setup_keyboard_hook(self):
        """Timer polling GetAsyncKeyState untuk mendeteksi ketikan keyboard secara global ya Putri cantik"""
        self.keyboard_poll_timer = QTimer(self)
        self.keyboard_poll_timer.timeout.connect(self.poll_keyboard)
        self.keyboard_poll_timer.start(50) # Cek tiap 50 milidetik ya Putri cantik

    def setup_mouse_hook(self):
        """Setup Windows low-level mouse hook to capture mouse scroll events globally with fixed ctypes signatures"""
        self.mouse_hook = None
        
        # We must keep a reference to the callback to prevent garbage collection
        LRESULT = ctypes.c_int64
        HOOKPROC = ctypes.WINFUNCTYPE(LRESULT, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM)
        
        user32 = ctypes.windll.user32
        kernel32 = ctypes.windll.kernel32
        
        # Setup explicit argtypes and restypes to prevent 64-bit truncation (Error 126)
        kernel32.GetModuleHandleW.argtypes = [wintypes.LPCWSTR]
        kernel32.GetModuleHandleW.restype = wintypes.HMODULE
        
        user32.SetWindowsHookExW.argtypes = [ctypes.c_int, HOOKPROC, wintypes.HINSTANCE, wintypes.DWORD]
        user32.SetWindowsHookExW.restype = wintypes.HANDLE
        
        user32.CallNextHookEx.argtypes = [wintypes.HANDLE, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM]
        user32.CallNextHookEx.restype = LRESULT
        
        user32.UnhookWindowsHookEx.argtypes = [wintypes.HANDLE]
        user32.UnhookWindowsHookEx.restype = wintypes.BOOL
        
        class MSLLHOOKSTRUCT(ctypes.Structure):
            _fields_ = [
                ("pt", wintypes.POINT),
                ("mouseData", wintypes.DWORD),
                ("flags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", ctypes.c_void_p)
            ]
            
        def hook_proc(nCode, wParam, lParam):
            if nCode >= 0:
                if wParam == 0x020A: # WM_MOUSEWHEEL
                    # Safely invoke the scroll handler
                    try:
                        ms = ctypes.cast(lParam, ctypes.POINTER(MSLLHOOKSTRUCT)).contents
                        raw_delta = ms.mouseData >> 16
                        delta = ctypes.c_short(raw_delta).value
                        self.on_mouse_scroll(delta)
                    except Exception as e:
                        print(f"Error handling scroll: {e}")
            return user32.CallNextHookEx(self.mouse_hook, nCode, wParam, lParam)
            
        self.mouse_hook_callback = HOOKPROC(hook_proc)
        h_module = kernel32.GetModuleHandleW(None)
        if not h_module:
            h_module = kernel32.GetModuleHandleW("kernel32.dll")
            
        self.mouse_hook = user32.SetWindowsHookExW(
            14, # WH_MOUSE_LL
            self.mouse_hook_callback,
            h_module,
            0
        )
        if not self.mouse_hook:
            print(f"Warning: Low-level mouse hook failed with code {ctypes.GetLastError()}")

    def on_mouse_scroll(self, delta):
        # Don't trigger if cat is sleeping, dragging, or alarm is firing
        if self.state in ("sleep", "sleep_roll") or self.is_dragging or self.alarm_firing:
            return
            
        # Tambah streak scroll
        self.scroll_streak += 1
        
        # Start/reset scroll timer. Set it to 300ms so it stops instantly and resets to idle/exhausted!
        self.scroll_timer.start(300)
        
        if self.state != "scroll":
            # Mulai animasi scroll
            self.anim_frame = 1
            self.change_state("scroll")
        else:
            # Bergantian/alternate frame 1 dan 2 saja setiap kali mendeteksi gerakan scroll!
            self.anim_frame = 2 if self.anim_frame == 1 else 1
            self.update()

    def stop_scroll(self):
        if self.state == "scroll":
            # Jika user scroll cukup banyak (streak >= 15), transisi ke kecapean dulu selama 3 detik
            if self.scroll_streak >= 15:
                self.scroll_streak = 0
                self.change_state("exhausted")
                self.exhausted_timer.start(3000)
            else:
                self.scroll_streak = 0
                if self.follow_cursor:
                    self.change_state("idle")
                else:
                    self.make_decision()

    def poll_keyboard(self):
        # Jangan ganggu kalau kucing lagi tidur atau alarm berbunyi ya Putri cantik
        if self.state == "sleep" or self.alarm_firing:
            return
            
        # Cek tombol ketik standar secara global untuk menghindari tombol virtual driver yang nyangkut
        GetAsyncKeyState = ctypes.windll.user32.GetAsyncKeyState
        any_key = False
        
        # Cek Backspace (8), Tab (9), Enter (13), Space (32)
        for vk in (8, 9, 13, 32):
            if GetAsyncKeyState(vk) & 0x8000:
                any_key = True
                break
        
        # Cek Angka 0-9 (48-57)
        if not any_key:
            for vk in range(48, 58):
                if GetAsyncKeyState(vk) & 0x8000:
                    any_key = True
                    break
                    
        # Cek Huruf A-Z (65-90)
        if not any_key:
            for vk in range(65, 91):
                if GetAsyncKeyState(vk) & 0x8000:
                    any_key = True
                    break
                    
        # Cek Numpad (96-105)
        if not any_key:
            for vk in range(96, 106):
                if GetAsyncKeyState(vk) & 0x8000:
                    any_key = True
                    break
                    
        # Cek Tombol Baca/Tanda Hubung (186-192, 219-222)
        if not any_key:
            for vk in (186, 187, 188, 189, 190, 191, 192, 219, 220, 221, 222):
                if GetAsyncKeyState(vk) & 0x8000:
                    any_key = True
                    break
                
        if any_key:
            self.on_key_press()

    def on_key_press(self):
        # Jangan ganggu kalau kucing lagi tidur ya Putri cantik
        if self.state == "sleep":
            return
            
        # Cat sedang mengetik! Reset timer 800ms biar kembali diam lebih cepat pas berhenti ngetik
        self.typing_timer.start(800)
        
        # Tambahkan streak mengetik
        self.typing_streak += 1
        
        # Ketukan keyboard memakan energi kucing ya Putri cantik
        drain = 0.45 if self.typing_streak >= 50 else 0.18
        self.energy = max(0.0, self.energy - drain)
        
        # Tentukan status berdasarkan streak ngetik
        if self.energy <= 0.0:
            self.energy = 0.0
            self.change_state("sleep")
            self.typing_streak = 0
            return
            
        if self.typing_streak >= 50:
            if self.state != "angry":
                self.anim_frame = 1
                self.change_state("angry")
            else:
                self.anim_frame = 2 if self.anim_frame == 1 else 1
                self.update()
        else:
            if self.state not in ("typing", "angry"):
                self.anim_frame = 1
                self.change_state("typing")
            else:
                self.anim_frame = 2 if self.anim_frame == 1 else 1
                self.update()

    def stop_typing(self):
        # Saat user berhenti mengetik
        was_angry = (self.state == "angry")
        self.typing_streak = 0
        if self.state in ("typing", "angry"):
            if was_angry:
                # Transisi ke kecapean dulu selama 3 detik Putri cantik
                self.change_state("exhausted")
                self.exhausted_timer.start(3000)
            else:
                if self.follow_cursor:
                    self.change_state("idle")
                else:
                    self.make_decision()

    def start_transition_idle(self):
        if self.state == "exhausted":
            # Mulai transisi dari kecapean ke idle selama 500ms Putri cantik
            self.change_state("exhausted_transition")
            self.transition_timer.start(500)

    def stop_exhausted(self):
        if self.state == "exhausted_transition":
            if self.follow_cursor:
                self.change_state("idle")
            else:
                self.make_decision()

    def start_sleep_roll(self):
        # Mulai berguling saat tidur Putri cantik
        self.change_state("sleep_roll")
        self.roll_frame_idx = 0
        self.roll_timer.start(300)

    def advance_sleep_roll(self):
        if self.state != "sleep_roll":
            self.roll_timer.stop()
            return
            
        self.roll_frame_idx += 1
        if self.roll_frame_idx <= 5:
            self.update()
        else:
            # Selesai berguling, balik tidur lagi Putri cantik
            self.roll_timer.stop()
            self.change_state("sleep")
            self.sleep_duration_ticks = 0

    def start_eating(self):
        # Tambah energi kucing Putri cantik biar langsung kenyang dan segar!
        self.energy = min(100.0, self.energy + 35.0)
        self.change_state("eat")
        # Jalankan animasi makan selama 3 detik (3000ms) ya Putri cantik
        self.eat_timer.start(3000)

    def stop_eating(self):
        if self.state == "eat":
            if self.follow_cursor:
                self.change_state("idle")
            else:
                self.make_decision()

    def start_alarm(self):
        self.alarm_firing = True
        self.change_state("reminder")
        try:
            import ctypes
            sound_path = os.path.abspath(get_resource_path("assets/sounds/nontifalarm.mp3"))
            ctypes.windll.winmm.mciSendStringW("close nontifalarm", None, 0, 0)
            ctypes.windll.winmm.mciSendStringW(f'open "{sound_path}" type mpegvideo alias nontifalarm', None, 0, 0)
            ctypes.windll.winmm.mciSendStringW("play nontifalarm repeat", None, 0, 0)
        except Exception as e:
            print(f"Gagal memutar alarm: {e}")
        if self.dashboard:
            self.dashboard.alarm_chk.blockSignals(True)
            self.dashboard.alarm_chk.setChecked(False)
            self.dashboard.alarm_chk.blockSignals(False)
            self.dashboard.stop_alarm_btn.setEnabled(True)

    def stop_alarm(self):
        self.alarm_firing = False
        try:
            import ctypes
            ctypes.windll.winmm.mciSendStringW("stop nontifalarm", None, 0, 0)
            ctypes.windll.winmm.mciSendStringW("close nontifalarm", None, 0, 0)
        except Exception as e:
            print(f"Gagal menghentikan alarm: {e}")
        if self.state == "reminder":
            if self.follow_cursor:
                self.change_state("idle")
            else:
                self.make_decision()

    def closeEvent(self, event):
        # Tutup aplikasi secara aman ya Putri cantik
        if hasattr(self, 'mouse_hook') and self.mouse_hook:
            ctypes.windll.user32.UnhookWindowsHookEx(self.mouse_hook)
            self.mouse_hook = None
        event.accept()

    def init_ui(self):
        # Jendela kucing dibikin frameless, selalu paling depan, dan TIDAK muncul di taskbar bawah
        # (Karena kita hanya memunculkan jendela Dashboard di taskbar bawah biar rapi ya Putri cantik)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |          # Biar gak ada border jendela
            Qt.WindowType.WindowStaysOnTopHint |         # Biar selalu melayang di paling depan
            Qt.WindowType.SubWindow                      # Sembunyikan jendela kucing dari taskbar bawah
        )
        
        # Bikin background jendelanya transparan ya Putri cantik
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        # Tambahkan tinggi jendela sebesar 50% biar hati gak terpotong pas melayang ke atas ya Putri cantik
        self.resize(self.mascot_size.width(), self.mascot_size.height() + self.mascot_size.height() // 2)
        
        # Kita aktifkan sensor deteksi kursor mouse biar bisa dielus ya Putri cantik
        self.setMouseTracking(True)
        
        # Bikin menu klik kanan/kiri ya Putri cantik
        self.context_menu = QMenu(self)
        
        status_action = QAction("Desktop Mate: Kucing Putih", self)
        status_action.setEnabled(False)
        self.context_menu.addAction(status_action)
        self.context_menu.addSeparator()
        
        # Opsi untuk menyalakan/mematikan fitur mengikuti kursor ya Putri cantik
        self.follow_action = QAction("Ikuti Kursor Mouse", self, checkable=True)
        self.follow_action.setChecked(self.follow_cursor)
        self.follow_action.triggered.connect(self.toggle_follow_cursor)
        self.context_menu.addAction(self.follow_action)
        
        # Opsi Tampilkan Dashboard UI yang lucu Putri cantik
        show_db_action = QAction("Tampilkan Dashboard", self)
        show_db_action.triggered.connect(self.show_dashboard_panel)
        self.context_menu.addAction(show_db_action)
        self.context_menu.addSeparator()
        
        # Menu rahasia buat maksa ganti status kucingnya ya Putri cantik
        state_menu = self.context_menu.addMenu("Paksa Status")
        
        action_idle = QAction("Diam/Berdiri", self)
        action_idle.triggered.connect(lambda: self.change_state("idle"))
        state_menu.addAction(action_idle)
        
        action_walk_l = QAction("Jalan Kiri", self)
        action_walk_l.triggered.connect(lambda: self.change_state("walk_left"))
        state_menu.addAction(action_walk_l)
        
        action_walk_r = QAction("Jalan Kanan", self)
        action_walk_r.triggered.connect(lambda: self.change_state("walk_right"))
        state_menu.addAction(action_walk_r)
        
        action_pet = QAction("Senang/Dielus", self)
        action_pet.triggered.connect(lambda: self.change_state("pet"))
        state_menu.addAction(action_pet)
        
        action_sleep_f = QAction("Tidur", self)
        action_sleep_f.triggered.connect(lambda: self.force_sleep)
        state_menu.addAction(action_sleep_f)
        
        self.context_menu.addSeparator()
        
        exit_action = QAction("Keluar Aplikasi", self)
        exit_action.triggered.connect(QApplication.instance().quit)
        self.context_menu.addAction(exit_action)
        
        # Bikin ikon kecil di pojok kanan bawah dekat jam biar gampang keluar ya Putri cantik
        self.tray_icon = QSystemTrayIcon(self)
        tray_pixmap = self.sprites.get("idle_left")
        if tray_pixmap:
            self.tray_icon.setIcon(QIcon(tray_pixmap))
        self.tray_icon.setContextMenu(self.context_menu)
        self.tray_icon.show()

    def show_dashboard_panel(self):
        if self.dashboard:
            self.dashboard.show()
            self.dashboard.activateWindow()

    def force_sleep(self):
        # Paksa kucing tidur dengan mengosongkan energinya ya Putri cantik
        self.energy = 0.0
        self.change_state("sleep")

    def toggle_follow_cursor(self):
        """Mengubah status ikuti kursor Putri cantik secara dinamis"""
        self.follow_cursor = self.follow_action.isChecked()
        if self.dashboard:
            self.dashboard.follow_chk.setChecked(self.follow_cursor)
        if not self.follow_cursor:
            self.make_decision()

    def change_state(self, new_state):
        if self.alarm_firing and new_state != "reminder":
            return
            
        if self.state == "sad" and new_state != "sad":
            self.stop_sad_sound()
            
        self.state = new_state
        if new_state == "walk_left":
            self.direction = "left"
        elif new_state == "walk_right":
            self.direction = "right"
            
        if new_state == "sad":
            try:
                import ctypes
                sound_path = os.path.abspath(get_resource_path("assets/sounds/mintadihelus.mp3"))
                ctypes.windll.winmm.mciSendStringW("close mintadihelus", None, 0, 0)
                ctypes.windll.winmm.mciSendStringW(f'open "{sound_path}" type mpegvideo alias mintadihelus', None, 0, 0)
                ctypes.windll.winmm.mciSendStringW("play mintadihelus", None, 0, 0)
            except Exception as e:
                print(f"Gagal memutar suara sedih: {e}")
        self.update()

    def stop_sad_sound(self):
        try:
            import ctypes
            ctypes.windll.winmm.mciSendStringW("stop mintadihelus", None, 0, 0)
            ctypes.windll.winmm.mciSendStringW("close mintadihelus", None, 0, 0)
        except:
            pass

    def get_current_sprite_name(self):
        """Fungsi ini buat milih gambar mana yang harus ditampilin sesuai gaya kucingnya ya Putri cantik"""
        f2 = (self.anim_frame - 1) % 2 + 1
        
        if self.state == "idle":
            return f"idle_{self.direction}_{self.anim_frame}"
        elif self.state == "walk_left":
            return f"walk_left_{f2}"
        elif self.state == "walk_right":
            return f"walk_right_{f2}"
        elif self.state == "pet":
            return f"happy_{self.direction}"
        elif self.state == "sleep":
            return f"sleep_{self.direction}_{f2}" # Alternasi frame tidur biar nafas ya Putri cantik
        elif self.state == "sleep_roll":
            if self.roll_frame_idx == 1:
                return f"sleep_roll_{self.direction}_1"
            elif self.roll_frame_idx == 2:
                return f"sleep_roll_{self.direction}_2"
            elif self.roll_frame_idx == 3:
                return f"sleep_back_{self.direction}"
            elif self.roll_frame_idx == 4:
                return f"sleep_roll_{self.direction}_3"
            elif self.roll_frame_idx == 5:
                return f"sleep_roll_{self.direction}_4"
            return f"sleep_{self.direction}_1"
        elif self.state == "play_heart":
            return f"play_heart_{self.direction}_{self.anim_frame}"
        elif self.state == "scroll":
            return f"scroll_{self.direction}_{self.anim_frame}"
        elif self.state == "reminder":
            return f"reminder_{self.direction}_{f2}"
        elif self.state == "exhausted":
            return f"exhausted_{self.direction}_{f2}"
        elif self.state == "exhausted_transition":
            return f"exhausted_transition_{self.direction}_{f2}"
        elif self.state == "typing":
            return f"typing_{self.direction}_{f2}"
        elif self.state == "angry":
            return f"angry_{self.direction}_{f2}"
        elif self.state == "eat":
            return f"eat_{self.direction}_{f2}"
        elif self.state == "sad":
            return f"sad_{self.direction}"
        return f"idle_{self.direction}_1"

    def update_animation(self):
        """Ini buat gantian frame 1 sampai 4 biar kucingnya keliatan jalan/hidup ya Putri cantik"""
        if self.is_dragging:
            return
            
        if self.state == "idle":
            if not hasattr(self, 'idle_ticks_since_blink'):
                self.idle_ticks_since_blink = 0
                self.is_blinking = False
            
            if self.is_blinking:
                self.anim_frame = 2 # Mata merem
                self.is_blinking = False
            else:
                self.anim_frame = 1 # Mata melek
                self.idle_ticks_since_blink += 1
                # Setiap > 3 detik (15 ticks), ada kesempatan 25% untuk berkedip
                if self.idle_ticks_since_blink > 15 and random.random() < 0.25:
                    self.is_blinking = True
                    self.idle_ticks_since_blink = 0
        elif self.state in ("scroll", "typing", "angry"):
            # Jangan update frame otomatis lewat timer,
            # biar gerak frame-nya murni saat mendeteksi input saja (berhenti instan!)
            pass
        else:
            self.anim_frame = self.anim_frame + 1
            max_frames = 4
            if self.anim_frame > max_frames:
                self.anim_frame = 1
                
        self.update()

    def update_behavior(self):
        """Logika meluncur mengejar kursor, jalan mandiri, capek tidur, tanpa batas layar ya Putri cantik"""
        if self.is_dragging:
            return
            
        curr_pos = self.pos()
        x, y = curr_pos.x(), curr_pos.y()
        
        # Batasan area layar biar kucing gak meluncur keluar layar ya Putri cantik
        screen_geometry = QGuiApplication.primaryScreen().availableGeometry()
        min_x = screen_geometry.left()
        max_x = screen_geometry.right() - self.mascot_size.width()
        min_y = screen_geometry.top()
        max_y = screen_geometry.bottom() - (self.mascot_size.height() + self.mascot_size.height() // 2)

        # --- SISTEM ALARM / PENGINGAT LOMPAT ---
        if self.alarm_active and not self.alarm_firing:
            if self.dashboard:
                self.alarm_time = self.dashboard.alarm_time_edit.time()
                self.alarm_message = self.dashboard.alarm_msg_edit.text()
            curr_time = QTime.currentTime()
            if curr_time.hour() == self.alarm_time.hour() and curr_time.minute() == self.alarm_time.minute():
                self.start_alarm()

        if self.state == "reminder":
            # Pergerakan melompat/bouncing heboh
            if not hasattr(self, 'reminder_bounce_tick'):
                self.reminder_bounce_tick = 0
            self.reminder_bounce_tick += 1
            
            import math
            # Melompat menggunakan fungsi abs(sin)
            bounce = abs(math.sin(self.reminder_bounce_tick * 0.15)) * 60 # lompat setinggi 60px
            target_y = max_y - int(bounce)
            
            # Berjalan perlahan kiri/kanan saat melompat
            if not hasattr(self, 'reminder_dir'):
                self.reminder_dir = 1
            x += self.reminder_dir * 3
            if x <= min_x:
                x = min_x
                self.reminder_dir = 1
                self.direction = "right"
            elif x >= max_x:
                x = max_x
                self.reminder_dir = -1
                self.direction = "left"
                
            self.move(x, target_y)
            self.update_hearts()
            self.update()
            if self.dashboard:
                self.dashboard.update_dashboard_data()
            return
        
        # Batasan area layar biar kucing gak meluncur keluar layar ya Putri cantik
        screen_geometry = QGuiApplication.primaryScreen().availableGeometry()
        min_x = screen_geometry.left()
        max_x = screen_geometry.right() - self.mascot_size.width()
        min_y = screen_geometry.top()
        # Hitung tinggi maksimal dengan menyertakan area kosong hati agar kaki kucing tetap menempel di bawah ya Putri cantik
        max_y = screen_geometry.bottom() - (self.mascot_size.height() + self.mascot_size.height() // 2)
        
        # --- SISTEM ENERGI / CAPEK TIDUR ---
        if self.state == "sleep":
            # Kucing memulihkan energi pas tidur ya Putri cantik (diperlambat biar harus dikasih makan)
            self.energy = min(100.0, self.energy + 0.02)
            
            # Klamp posisi biar gak keluar layar pas tidur
            x = max(min_x, min(x, max_x))
            y = max(min_y, min(y, max_y))
            self.move(x, y)
            
            # Setiap 10 detik (333 ticks * 30ms), kucing berguling-guling lucu Putri cantik
            self.sleep_duration_ticks += 1
            if self.sleep_duration_ticks >= 333:
                self.sleep_duration_ticks = 0
                self.start_sleep_roll()
            
            if self.energy >= 100.0:
                self.change_state("idle")
            self.update_hearts()
            self.update()
            if self.dashboard:
                self.dashboard.update_dashboard_data()
            return
            
        # Jika kucing sedang mengetik, marah, makan, juggling hati, berguling, kecapean, atau scroll, diam di tempat ya Putri cantik
        if self.state in ("typing", "angry", "eat", "play_heart", "exhausted", "exhausted_transition", "sleep_roll", "scroll"):
            # Jika sedang berguling tidur, energinya tetap pulih sedikit ya Putri cantik
            if self.state == "sleep_roll":
                self.energy = min(100.0, self.energy + 0.02)
            self.update_hearts()
            self.update()
            if self.dashboard:
                self.dashboard.update_dashboard_data()
            return
            
        # Kurangi energi berdasarkan aktivitas kucing ya Putri cantik
        if self.state in ("walk_left", "walk_right"):
            self.energy = max(0.0, self.energy - 0.025)
        elif self.state == "pet":
            self.energy = min(100.0, self.energy + 0.05) # Dielus memulihkan energi sedikit demi sedikit
        else:
            self.energy = max(0.0, self.energy - 0.005) # Diam tetap mengurangi energi sedikit
            
        # Jika energi habis, kucing langsung tertidur karena kecapean ya Putri cantik
        if self.energy <= 0.0:
            self.energy = 0.0
            self.change_state("sleep")
            self.update_hearts()
            self.update()
            if self.dashboard:
                self.dashboard.update_dashboard_data()
            return
        
        # 1. Jika fitur ikuti kursor dinonaktifkan oleh Putri cantik, kucing jalan mondar-mandir sendiri
        if not self.follow_cursor:
            # Pastikan posisi kucing selalu ada di dalam area layar ya Putri cantik
            x = max(min_x, min(x, max_x))
            y = max(min_y, min(y, max_y))
            
            # Update posisi berdasarkan status jalan mondar-mandirnya
            if self.is_hovered:
                self.state = "pet"
            else:
                if self.state == "walk_left":
                    x -= self.walk_speed
                    if x <= min_x:
                        x = min_x
                        self.change_state("walk_right")
                    self.move(x, y)
                elif self.state == "walk_right":
                    x += self.walk_speed
                    if x >= max_x:
                        x = max_x
                        self.change_state("walk_left")
                    self.move(x, y)
                else:
                    # Mode diam (idle)
                    self.move(x, y)
            
            self.update_hearts()
            self.update()
            if self.dashboard:
                self.dashboard.update_dashboard_data()
            return
            
        # 2. Hitung koordinat target (Kursor mouse di tengah-tengah tubuh kucingnya ya Putri cantik)
        cursor_pos = QCursor.pos()
        target_x = cursor_pos.x() - self.mascot_size.width() // 2
        # Target y dihitung dari bawah jendela karena kucing digambar di bagian bawah ya Putri cantik
        target_y = cursor_pos.y() - self.mascot_size.height()
        
        dx = target_x - x
        dy = target_y - y
        distance = (dx**2 + dy**2) ** 0.5
        
        # 3. Jika jarak kursor masih jauh, meluncur mendekatinya
        if distance > 12: # Toleransi jarak biar kucing gak gemetar pas nyampe kursor
            x_step = int(dx / distance * self.glide_speed)
            y_step = int(dy / distance * self.glide_speed)
            
            new_x = max(min_x, min(x + x_step, max_x))
            new_y = max(min_y, min(y + y_step, max_y))
            self.move(new_x, new_y)
            
            # Ubah gaya animasi hadap kiri/kanan sesuai gerakan horizontalnya
            if dx < 0:
                self.state = "walk_left"
                self.direction = "left"
            else:
                self.state = "walk_right"
                self.direction = "right"
        else:
            # 4. Jika sudah dekat sekali dengan kursor, kucing akan diam atau dielus
            if self.is_hovered:
                self.state = "pet"
            else:
                self.state = "idle"
                self.direction = "left" if dx < 0 else "right"
                
        # 5. Update partikel hatinya ya Putri cantik
        self.update_hearts()
        self.update()
        if self.dashboard:
            self.dashboard.update_dashboard_data()

    def update_hearts(self):
        """Update partikel hati melayang pas dielus ya Putri cantik"""
        if self.state == "pet":
            if random.random() < 0.20:
                self.spawn_heart()
                
        active_hearts = []
        for heart in self.hearts:
            heart['x'] += heart['speed_x']
            heart['y'] -= heart['speed_y']
            heart['alpha'] -= 6.0
            # Hati terhapus jika sudah pudar atau terbang melewati batas atas jendela (y <= 0) ya Putri cantik
            if heart['alpha'] > 0 and heart['y'] > 0:
                active_hearts.append(heart)
        self.hearts = active_hearts

    def spawn_heart(self):
        """Fungsi ini buat bikin efek hati kecil melayang pas dielus ya Putri cantik"""
        w = self.mascot_size.width()
        h = self.mascot_size.height()
        vertical_padding = h // 2
        
        # Batasan spawn horizontal (sekitar kepala kucing) menyesuaikan ukuran ya Putri cantik
        hx = random.uniform(w * 0.25, w * 0.75)
        # Batasan spawn vertikal (dekat telinga/kepala kucing)
        hy = vertical_padding + random.uniform(h * 0.1, h * 0.3)
        
        # Ukuran hati menyesuaikan ukuran kucingnya ya Putri cantik
        pixel_size = max(1, w // 50)
        
        # Kecepatan melayang menyesuaikan ukuran kucing biar natural ya Putri cantik
        speed_x = random.uniform(-0.005 * w, 0.005 * w)
        speed_y = random.uniform(0.012 * h, 0.024 * h)
        
        self.hearts.append({
            'x': float(hx),
            'y': float(hy),
            'pixel_size': pixel_size,
            'alpha': 255.0,
            'speed_x': speed_x,
            'speed_y': speed_y
        })

    def make_decision(self):
        """Biar kucingnya keliatan hidup pas gak ngikutin kursor, dia bisa milih mau jalan atau diam sendiri ya Putri cantik"""
        if self.is_dragging or self.is_hovered or self.follow_cursor or self.state in ("sleep", "sleep_roll", "exhausted", "exhausted_transition", "eat", "scroll", "sad"):
            return
            
        # Pilih status acak: 15% diam, 20% jalan kiri, 20% jalan kanan, 25% main emoji hati, 20% sedih minta patpat
        rand = random.random()
        if rand < 0.15:
            self.change_state("idle")
        elif rand < 0.35:
            self.change_state("walk_left")
        elif rand < 0.55:
            self.change_state("walk_right")
        elif rand < 0.80:
            self.change_state("play_heart")
        else:
            self.change_state("sad")
            
        # Ubah jeda waktu keputusan acak biar natural (3-8 detik)
        self.decision_timer.setInterval(random.randint(3000, 8000))

    # --- Sensor Mouse Hover saat kucingnya dielus ya Putri cantik ---
    def enterEvent(self, event):
        self.is_hovered = True
        if self.state != "sleep": # Jangan ganggu kucing tidur ya Putri cantik
            self.change_state("pet")
        event.accept()
        
    def leaveEvent(self, event):
        self.is_hovered = False
        self.hearts = []
        if self.state != "sleep":
            if self.follow_cursor:
                self.change_state("idle")
            else:
                self.make_decision()
        event.accept()

    # --- Sensor Mouse Klik & Geser (Drag & Drop) / Klik Kiri Biasa ya Putri cantik ---
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Hanya ijinkan seret (drag) jika klik berada di area tubuh kucing ya Putri cantik
            vertical_padding = self.mascot_size.height() // 2
            if event.position().y() >= vertical_padding:
                self.is_dragging = True
                # Simpan posisi awal klik untuk mendeteksi apakah ini klik biasa atau seret ya Putri cantik
                self.press_pos = event.globalPosition().toPoint()
                self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
                event.accept()
            else:
                event.ignore()
            
    def mouseMoveEvent(self, event):
        if self.is_dragging and event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
            
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_dragging = False
            
            # Hitung seberapa jauh mouse digeser ya Putri cantik
            release_pos = event.globalPosition().toPoint()
            drag_distance = (release_pos - self.press_pos).manhattanLength()
            
            if drag_distance < 5:
                if self.alarm_firing:
                    self.stop_alarm()
                    if self.dashboard:
                        self.dashboard.stop_alarm_btn.setEnabled(False)
                else:
                    # Jika mouse tidak digeser (hanya klik kiri biasa), tampilkan menu opsi ya Putri cantik!
                    self.context_menu.exec(QCursor.pos())
            else:
                # Jika digeser, sesuaikan statusnya ya Putri cantik
                if self.state != "sleep":
                    if self.is_hovered:
                        self.change_state("pet")
                    else:
                        if self.follow_cursor:
                            self.change_state("idle")
                        else:
                            self.make_decision()
            event.accept()
            
    def contextMenuEvent(self, event):
        self.context_menu.exec(event.globalPos())

    # --- Bagian menggambar kucing sama hati merahnya langsung ke layar ya Putri cantik ---
    def paintEvent(self, event):
        painter = QPainter(self)
        
        # 1. Gambar badan kucingnya di bagian bawah jendela biar ada sisa transparan di atas untuk hati melayang ya Putri cantik
        sprite_name = self.get_current_sprite_name()
        pixmap = self.sprites.get(sprite_name)
        vertical_padding = self.mascot_size.height() // 2
        if pixmap:
            painter.drawPixmap(0, vertical_padding, pixmap)
            
        # 2. Gambar tag nama di atas kepala kucing ya Putri cantik
        if hasattr(self, 'pet_name') and self.pet_name:
            painter.save()
            font = painter.font()
            font.setFamily("'Comic Sans MS', 'Segoe UI', sans-serif")
            font.setBold(True)
            font.setPointSize(9) # Ukuran font yang pas dan imut
            painter.setFont(font)
            
            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.pet_name)
            text_height = fm.height()
            
            w = self.width()
            rect_w = text_width + 16
            rect_h = text_height + 4
            rect_x = (w - rect_w) // 2
            # Letakkan lebih rendah agar berada tepat di atas kepala kucing (diturunkan sebesar 15% dari tinggi maskot)
            rect_y = vertical_padding + int(self.mascot_size.height() * 0.15) - rect_h
            
            # Gambar bubble nama dengan border pink & background putih transparan
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setPen(QColor("#FF69B4"))
            painter.setBrush(QColor(255, 240, 245, 220)) # LavenderBlush transparan
            painter.drawRoundedRect(rect_x, rect_y, rect_w, rect_h, 6, 6)
            
            # Tulis teks nama kucing
            painter.setPen(QColor("#C71585"))
            painter.drawText(rect_x + 8, rect_y + fm.ascent() + 2, self.pet_name)
            painter.restore()
            
        # 3. Gambar pesan alarm jika sedang berbunyi/firing ya Putri cantik
        if self.alarm_firing and self.alarm_message:
            painter.save()
            font = painter.font()
            font.setFamily("'Comic Sans MS', 'Segoe UI', sans-serif")
            font.setBold(True)
            font.setPointSize(10)
            painter.setFont(font)
            
            fm = painter.fontMetrics()
            msg_text = f"🔔 {self.alarm_message}"
            text_width = fm.horizontalAdvance(msg_text)
            text_height = fm.height()
            
            w = self.width()
            rect_w = text_width + 20
            rect_h = text_height + 8
            rect_x = (w - rect_w) // 2
            # Letakkan di atas tag nama
            name_tag_height = fm.height() + 4
            rect_y = vertical_padding + int(self.mascot_size.height() * 0.15) - name_tag_height - rect_h - 10
            
            # Gambar bubble pesan alarm (background kuning cerah / border pink)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            from PyQt6.QtGui import QPen
            pen = QPen(QColor("#FF1493"))
            pen.setWidth(2)
            painter.setPen(pen)
            painter.setBrush(QColor(255, 255, 224, 240)) # LightYellow cerah
            painter.drawRoundedRect(rect_x, rect_y, rect_w, rect_h, 8, 8)
            
            # Tulis pesan alarm
            painter.setPen(QColor("#FF1493"))
            painter.drawText(rect_x + 10, rect_y + fm.ascent() + 4, msg_text)
            painter.restore()
        elif self.state == "sad":
            painter.save()
            font = painter.font()
            font.setFamily("'Comic Sans MS', 'Segoe UI', sans-serif")
            font.setBold(True)
            font.setPointSize(9)
            painter.setFont(font)
            
            fm = painter.fontMetrics()
            msg_text = "🥺 Pat pat aku dong..."
            text_width = fm.horizontalAdvance(msg_text)
            text_height = fm.height()
            
            w = self.width()
            rect_w = text_width + 16
            rect_h = text_height + 4
            rect_x = (w - rect_w) // 2
            # Letakkan di atas tag nama
            name_tag_height = fm.height() + 4
            rect_y = vertical_padding + int(self.mascot_size.height() * 0.15) - name_tag_height - rect_h - 10
            
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            from PyQt6.QtGui import QPen
            pen = QPen(QColor("#FF69B4"))
            pen.setWidth(1)
            painter.setPen(pen)
            painter.setBrush(QColor(255, 240, 245, 220)) # LavenderBlush transparan
            painter.drawRoundedRect(rect_x, rect_y, rect_w, rect_h, 6, 6)
            
            painter.setPen(QColor("#C71585"))
            painter.drawText(rect_x + 8, rect_y + fm.ascent() + 2, msg_text)
            painter.restore()

        # 4. Gambar partikel hati merah pixel art melayang ya Putri cantik
        for heart in self.hearts:
            color = QColor(255, 60, 60, int(heart['alpha']))
            self.draw_pixel_heart(painter, heart['x'], heart['y'], heart['pixel_size'], color)

    def draw_keyboard_and_paws(self, painter, w, h, vertical_padding):
        """Gambar keyboard pixel art lucu dan cakar bergerak mengetik ya Putri cantik"""
        painter.save()
        painter.setPen(Qt.PenStyle.NoPen)
        
        # 1. Gambar Keyboard (Kotak abu-abu retro pixel)
        kb_w = int(w * 0.55)
        kb_h = int(h * 0.08)
        kb_x = int((w - kb_w) // 2)
        kb_y = int(vertical_padding + h * 0.72)
        
        # Gambar border keyboard hitam
        painter.setBrush(QColor(0, 0, 0))
        painter.drawRect(kb_x, kb_y, kb_w, kb_h)
        # Gambar isi keyboard abu-abu
        painter.setBrush(QColor(190, 190, 190))
        painter.drawRect(kb_x + 2, kb_y + 2, kb_w - 4, kb_h - 4)
        
        # Gambar tuts/keys keyboard (garis-garis kecil gelap)
        painter.setBrush(QColor(100, 100, 100))
        key_size = max(1, w // 64)
        for i in range(kb_x + 6, kb_x + kb_w - 6, key_size * 3):
            painter.drawRect(i, kb_y + 4, key_size, kb_h - 8)
            
        # 2. Gambar Cakar Kucing (White circles dengan pink pads)
        paw_radius = int(w * 0.08)
        
        # Tentukan posisi cakar kiri dan kanan bergantian naik turun
        if self.anim_frame == 1:
            left_paw_y = kb_y - int(h * 0.04) # Kiri naik
            right_paw_y = kb_y + int(h * 0.01) # Kanan nempel
        else:
            left_paw_y = kb_y + int(h * 0.01) # Kiri nempel
            right_paw_y = kb_y - int(h * 0.04) # Kanan naik
            
        # Posisikan relatif agar pas di depan tubuh kucing
        left_paw_x = int(w * 0.35)
        right_paw_x = int(w * 0.53)
        
        # Gambar cakar kiri
        painter.setBrush(QColor(0, 0, 0)) # Outline hitam
        painter.drawEllipse(left_paw_x - 1, left_paw_y - 1, paw_radius + 2, paw_radius + 2)
        painter.setBrush(QColor(255, 255, 255)) # Bulu putih
        painter.drawEllipse(left_paw_x, left_paw_y, paw_radius, paw_radius)
        # Tapak pink lucu
        painter.setBrush(QColor(255, 182, 193)) 
        painter.drawEllipse(left_paw_x + paw_radius // 4, left_paw_y + paw_radius // 4, paw_radius // 2, paw_radius // 2)
        
        # Gambar cakar kanan
        painter.setBrush(QColor(0, 0, 0))
        painter.drawEllipse(right_paw_x - 1, right_paw_y - 1, paw_radius + 2, paw_radius + 2)
        painter.setBrush(QColor(255, 255, 255))
        painter.drawEllipse(right_paw_x, right_paw_y, paw_radius, paw_radius)
        painter.setBrush(QColor(255, 182, 193))
        painter.drawEllipse(right_paw_x + paw_radius // 4, right_paw_y + paw_radius // 4, paw_radius // 2, paw_radius // 2)
        
        painter.restore()

    def draw_pixel_anger(self, painter, x, y, px):
        """Simbol marah merah ala anime menggunakan pixel art ya Putri cantik"""
        painter.save()
        painter.setBrush(QColor(255, 30, 30))
        painter.setPen(Qt.PenStyle.NoPen)
        
        grid = [
            [0, 1, 0, 0, 1, 0],
            [1, 1, 1, 1, 1, 1],
            [0, 1, 0, 0, 1, 0],
            [0, 1, 0, 0, 1, 0],
            [1, 1, 1, 1, 1, 1],
            [0, 1, 0, 0, 1, 0]
        ]
        for row_idx, row in enumerate(grid):
            for col_idx, val in enumerate(row):
                if val:
                    painter.drawRect(
                        int(x + col_idx * px),
                        int(y + row_idx * px),
                        px,
                        px
                    )
        painter.restore()

    def draw_pixel_heart(self, painter, x, y, px, color):
        """Ini rumus buat ngegambar hati merah pixel art-nya ya Putri cantik"""
        painter.save()
        painter.setBrush(color)
        painter.setPen(Qt.PenStyle.NoPen)
        
        grid = [
            [0, 1, 1, 0, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 1, 0],
            [0, 0, 1, 1, 1, 0, 0],
            [0, 0, 0, 1, 0, 0, 0]
        ]
        
        for row_idx, row in enumerate(grid):
            for col_idx, val in enumerate(row):
                if val:
                    painter.drawRect(
                        int(x + col_idx * px),
                        int(y + row_idx * px),
                        px,
                        px
                    )
        painter.restore()

def main():
    os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)
    
    # Inisialisasi mascot dan dashboard panel ya Putri cantik
    mate = DesktopMate()
    dashboard = CatDashboard(mate)
    
    # Tampilkan keduanya ke layar ya Putri cantik
    mate.show()
    dashboard.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
