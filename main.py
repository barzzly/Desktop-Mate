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


def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class CatDashboard(QWidget):
    def __init__(self, mascot):
        super().__init__()
        self.mascot = mascot
        self.mascot.dashboard = self

        self.setWindowTitle("Dashboard Kucing Pixel")
        self.setWindowIcon(QIcon(get_resource_path("assets/idle_left.png")))

        self.setStyleSheet("""
            QWidget {
                background-color:
                font-family: 'Comic Sans MS', 'Segoe UI', sans-serif;
            }
            QLabel {
                color:
                font-weight: bold;
                font-size: 13px;
            }
                font-size: 18px;
                color:
                margin-bottom: 10px;
            }
            QProgressBar {
                border: 2px solid
                border-radius: 8px;
                text-align: center;
                color:
                font-weight: bold;
                background-color:
            }
            QProgressBar::chunk {
                background-color:
                border-radius: 6px;
            }
            QPushButton {
                background-color:
                color: white;
                border: 2px solid
                border-radius: 12px;
                padding: 6px 12px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color:
            }
            QPushButton:pressed {
                background-color:
            }
            QCheckBox {
                color:
                font-weight: bold;
                font-size: 13px;
            }
            QComboBox {
                border: 2px solid
                border-radius: 6px;
                padding: 4px;
                background-color: white;
                color:
                font-weight: bold;
            }
            QLineEdit, QTimeEdit {
                border: 2px solid
                border-radius: 6px;
                padding: 4px;
                background-color: white;
                color:
                font-weight: bold;
            }
            QSlider::groove:horizontal {
                border: 1px solid
                height: 8px;
                background: white;
                border-radius: 4px;
            }
            QSlider::handle:horizontal {
                background:
                border: 1px solid
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

        title = QLabel("🐾 DASHBOARD KUCING PUTERI IMUP 🐾")
        title.setObjectName("TitleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        status_layout = QHBoxLayout()
        status_layout.addWidget(QLabel("Status Kucing:"))
        self.status_val = QLabel("🧍 Diam Santai")
        status_layout.addWidget(self.status_val)
        layout.addLayout(status_layout)

        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Nama Mascot:"))
        self.name_input = QLineEdit()
        self.name_input.setText(self.mascot.pet_name)
        self.name_input.textChanged.connect(self.update_pet_name)
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)

        layout.addWidget(QLabel("Tingkat Energi Kucing (Bisa Capek):"))
        self.energy_bar = QProgressBar()
        self.energy_bar.setRange(0, 100)
        self.energy_bar.setValue(int(self.mascot.energy))
        layout.addWidget(self.energy_bar)

        layout.addSpacing(10)

        self.follow_chk = QCheckBox("Ikuti Kursor Mouse (Chase Mode)")
        self.follow_chk.setChecked(self.mascot.follow_cursor)
        self.follow_chk.stateChanged.connect(self.toggle_follow)
        layout.addWidget(self.follow_chk)

        layout.addSpacing(10)

        layout.addWidget(QLabel("Ukuran Kucing:"))
        self.size_combo = QComboBox()
        self.size_combo.addItems(["128 x 128", "256 x 256"])
        self.size_combo.setCurrentText(f"{self.mascot.mascot_size.width()} x {self.mascot.mascot_size.height()}")
        self.size_combo.currentTextChanged.connect(self.change_size)
        layout.addWidget(self.size_combo)

        layout.addWidget(QLabel("Kecepatan Mengejar Kursor:"))
        self.glide_slider = QSlider(Qt.Orientation.Horizontal)
        self.glide_slider.setRange(2, 15)
        self.glide_slider.setValue(self.mascot.glide_speed)
        self.glide_slider.valueChanged.connect(self.change_glide_speed)
        layout.addWidget(self.glide_slider)

        layout.addSpacing(10)

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
        is_checked = (state == 2)
        self.mascot.follow_cursor = is_checked
        self.mascot.follow_action.setChecked(is_checked)
        if not is_checked:
            self.mascot.make_decision()

    def change_size(self, size_str):
        w, h = map(int, size_str.split(" x "))
        self.mascot.mascot_size = QSize(w, h)
        self.mascot.load_sprites()
        self.mascot.resize(w * 2, h * 2)
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
        self.mascot.start_eating()
        self.status_val.setText("😋 Nyam Nyam Enak!")

    def call_cat(self):
        screen_geometry = QGuiApplication.primaryScreen().availableGeometry()
        start_x = screen_geometry.width() // 2 - self.mascot.mascot_size.width() // 2
        start_y = screen_geometry.height() // 2 - self.mascot.mascot_size.height() // 2
        self.mascot.move(start_x, start_y)
        self.mascot.change_state("idle")

    def update_dashboard_data(self):
        """Update data energi dan status kucing di layar Dashboard Putri cantik"""
        self.energy_bar.setValue(int(self.mascot.energy))

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

        self.mascot_size = QSize(128, 128)
        self.pet_name = "Putri"

        self.glide_speed = 6
        self.walk_speed = 2
        self.tick_interval = 30

        self.alarm_active = False
        self.alarm_firing = False
        self.alarm_message = "Waktunya Istirahat! 🐾"
        self.alarm_time = QTime(12, 0)

        self.anim_tick_interval = 200

        self.energy = 100.0

        self.state = "idle"
        self.direction = "left"
        self.anim_frame = 1

        self.follow_cursor = False

        self.is_dragging = False
        self.drag_position = QPoint()
        self.press_pos = QPoint()
        self.is_hovered = False

        self.dashboard = None

        self.hearts = []

        self.load_sprites()

        self.init_ui()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_behavior)
        self.timer.start(self.tick_interval)

        self.anim_timer = QTimer(self)
        self.anim_timer.timeout.connect(self.update_animation)
        self.anim_timer.start(self.anim_tick_interval)

        self.decision_timer = QTimer(self)
        self.decision_timer.timeout.connect(self.make_decision)
        self.decision_timer.start(5000)

        screen_geometry = QGuiApplication.primaryScreen().availableGeometry()
        start_x = screen_geometry.width() // 2 - self.width() // 2
        start_y = screen_geometry.height() // 2 - self.height() // 2
        self.move(start_x, start_y)

        self.typing_streak = 0
        self.typing_timer = QTimer(self)
        self.typing_timer.setSingleShot(True)
        self.typing_timer.timeout.connect(self.stop_typing)

        self.eat_timer = QTimer(self)
        self.eat_timer.setSingleShot(True)
        self.eat_timer.timeout.connect(self.stop_eating)

        self.exhausted_timer = QTimer(self)
        self.exhausted_timer.setSingleShot(True)
        self.exhausted_timer.timeout.connect(self.start_transition_idle)

        self.transition_timer = QTimer(self)
        self.transition_timer.setSingleShot(True)
        self.transition_timer.timeout.connect(self.stop_exhausted)

        self.sleep_duration_ticks = 0
        self.roll_frame_idx = 0
        self.roll_timer = QTimer(self)
        self.roll_timer.timeout.connect(self.advance_sleep_roll)

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
        self.keyboard_poll_timer.start(50)

    def setup_mouse_hook(self):
        """Setup Windows low-level mouse hook to capture mouse scroll events globally with fixed ctypes signatures"""
        self.mouse_hook = None

        LRESULT = ctypes.c_int64
        HOOKPROC = ctypes.WINFUNCTYPE(LRESULT, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM)

        user32 = ctypes.windll.user32
        kernel32 = ctypes.windll.kernel32

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
                if wParam == 0x020A:
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
            14,
            self.mouse_hook_callback,
            h_module,
            0
        )
        if not self.mouse_hook:
            print(f"Warning: Low-level mouse hook failed with code {ctypes.GetLastError()}")

    def on_mouse_scroll(self, delta):
        if self.state in ("sleep", "sleep_roll") or self.is_dragging or self.alarm_firing:
            return

        self.scroll_streak += 1

        self.scroll_timer.start(300)

        if self.state != "scroll":
            self.anim_frame = 1
            self.change_state("scroll")
        else:
            self.anim_frame = 2 if self.anim_frame == 1 else 1
            self.update()

    def stop_scroll(self):
        if self.state == "scroll":
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
        if self.state == "sleep" or self.alarm_firing:
            return

        GetAsyncKeyState = ctypes.windll.user32.GetAsyncKeyState
        any_key = False

        for vk in (8, 9, 13, 32):
            if GetAsyncKeyState(vk) & 0x8000:
                any_key = True
                break

        if not any_key:
            for vk in range(48, 58):
                if GetAsyncKeyState(vk) & 0x8000:
                    any_key = True
                    break

        if not any_key:
            for vk in range(65, 91):
                if GetAsyncKeyState(vk) & 0x8000:
                    any_key = True
                    break

        if not any_key:
            for vk in range(96, 106):
                if GetAsyncKeyState(vk) & 0x8000:
                    any_key = True
                    break

        if not any_key:
            for vk in (186, 187, 188, 189, 190, 191, 192, 219, 220, 221, 222):
                if GetAsyncKeyState(vk) & 0x8000:
                    any_key = True
                    break

        if any_key:
            self.on_key_press()

    def on_key_press(self):
        if self.state == "sleep":
            return

        self.typing_timer.start(800)

        self.typing_streak += 1

        drain = 0.45 if self.typing_streak >= 50 else 0.18
        self.energy = max(0.0, self.energy - drain)

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
        was_angry = (self.state == "angry")
        self.typing_streak = 0
        if self.state in ("typing", "angry"):
            if was_angry:
                self.change_state("exhausted")
                self.exhausted_timer.start(3000)
            else:
                if self.follow_cursor:
                    self.change_state("idle")
                else:
                    self.make_decision()

    def start_transition_idle(self):
        if self.state == "exhausted":
            self.change_state("exhausted_transition")
            self.transition_timer.start(500)

    def stop_exhausted(self):
        if self.state == "exhausted_transition":
            if self.follow_cursor:
                self.change_state("idle")
            else:
                self.make_decision()

    def start_sleep_roll(self):
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
            self.roll_timer.stop()
            self.change_state("sleep")
            self.sleep_duration_ticks = 0

    def start_eating(self):
        self.energy = min(100.0, self.energy + 35.0)
        self.change_state("eat")
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
        if hasattr(self, 'mouse_hook') and self.mouse_hook:
            ctypes.windll.user32.UnhookWindowsHookEx(self.mouse_hook)
            self.mouse_hook = None
        event.accept()

    def init_ui(self):
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.SubWindow
        )

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.resize(self.mascot_size.width() * 2, self.mascot_size.height() * 2)

        self.setMouseTracking(True)

        self.context_menu = QMenu(self)

        status_action = QAction("Desktop Mate: Kucing Putih", self)
        status_action.setEnabled(False)
        self.context_menu.addAction(status_action)
        self.context_menu.addSeparator()

        self.follow_action = QAction("Ikuti Kursor Mouse", self, checkable=True)
        self.follow_action.setChecked(self.follow_cursor)
        self.follow_action.triggered.connect(self.toggle_follow_cursor)
        self.context_menu.addAction(self.follow_action)

        show_db_action = QAction("Tampilkan Dashboard", self)
        show_db_action.triggered.connect(self.show_dashboard_panel)
        self.context_menu.addAction(show_db_action)
        self.context_menu.addSeparator()

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
            return f"sleep_{self.direction}_{f2}"
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
                self.anim_frame = 2
                self.is_blinking = False
            else:
                self.anim_frame = 1
                self.idle_ticks_since_blink += 1
                if self.idle_ticks_since_blink > 15 and random.random() < 0.25:
                    self.is_blinking = True
                    self.idle_ticks_since_blink = 0
        elif self.state in ("scroll", "typing", "angry"):
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

        screen_geometry = QGuiApplication.primaryScreen().availableGeometry()
        horizontal_padding = (self.width() - self.mascot_size.width()) // 2
        min_x = screen_geometry.left() - horizontal_padding
        max_x = screen_geometry.right() - self.width() + horizontal_padding
        min_y = screen_geometry.top()
        max_y = screen_geometry.bottom() - self.height()

        if self.alarm_active and not self.alarm_firing:
            if self.dashboard:
                self.alarm_time = self.dashboard.alarm_time_edit.time()
                self.alarm_message = self.dashboard.alarm_msg_edit.text()
            curr_time = QTime.currentTime()
            if curr_time.hour() == self.alarm_time.hour() and curr_time.minute() == self.alarm_time.minute():
                self.start_alarm()

        if self.state == "reminder":
            if not hasattr(self, 'reminder_bounce_tick'):
                self.reminder_bounce_tick = 0
            self.reminder_bounce_tick += 1

            import math
            bounce = abs(math.sin(self.reminder_bounce_tick * 0.15)) * 60
            target_y = max_y - int(bounce)

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

        screen_geometry = QGuiApplication.primaryScreen().availableGeometry()
        horizontal_padding = (self.width() - self.mascot_size.width()) // 2
        min_x = screen_geometry.left() - horizontal_padding
        max_x = screen_geometry.right() - self.width() + horizontal_padding
        min_y = screen_geometry.top()
        max_y = screen_geometry.bottom() - self.height()

        if self.state == "sleep":
            self.energy = min(100.0, self.energy + 0.02)

            x = max(min_x, min(x, max_x))
            y = max(min_y, min(y, max_y))
            self.move(x, y)

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

        if self.state in ("typing", "angry", "eat", "play_heart", "exhausted", "exhausted_transition", "sleep_roll", "scroll"):
            if self.state == "sleep_roll":
                self.energy = min(100.0, self.energy + 0.02)
            self.update_hearts()
            self.update()
            if self.dashboard:
                self.dashboard.update_dashboard_data()
            return

        if self.state in ("walk_left", "walk_right"):
            self.energy = max(0.0, self.energy - 0.025)
        elif self.state == "pet":
            self.energy = min(100.0, self.energy + 0.05)
        else:
            self.energy = max(0.0, self.energy - 0.005)

        if self.energy <= 0.0:
            self.energy = 0.0
            self.change_state("sleep")
            self.update_hearts()
            self.update()
            if self.dashboard:
                self.dashboard.update_dashboard_data()
            return

        if not self.follow_cursor:
            x = max(min_x, min(x, max_x))
            y = max(min_y, min(y, max_y))

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
                    self.move(x, y)

            self.update_hearts()
            self.update()
            if self.dashboard:
                self.dashboard.update_dashboard_data()
            return

        cursor_pos = QCursor.pos()
        target_x = cursor_pos.x() - self.width() // 2
        target_y = cursor_pos.y() - self.height()

        dx = target_x - x
        dy = target_y - y
        distance = (dx**2 + dy**2) ** 0.5

        if distance > 12:
            x_step = int(dx / distance * self.glide_speed)
            y_step = int(dy / distance * self.glide_speed)

            new_x = max(min_x, min(x + x_step, max_x))
            new_y = max(min_y, min(y + y_step, max_y))
            self.move(new_x, new_y)

            if dx < 0:
                self.state = "walk_left"
                self.direction = "left"
            else:
                self.state = "walk_right"
                self.direction = "right"
        else:
            if self.is_hovered:
                self.state = "pet"
            else:
                self.state = "idle"
                self.direction = "left" if dx < 0 else "right"

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
            if heart['alpha'] > 0 and heart['y'] > 0:
                active_hearts.append(heart)
        self.hearts = active_hearts

    def spawn_heart(self):
        """Fungsi ini buat bikin efek hati kecil melayang pas dielus ya Putri cantik"""
        w = self.width()
        h = self.height()
        vertical_padding = h - self.mascot_size.height()
        horizontal_padding = (w - self.mascot_size.width()) // 2

        hx = horizontal_padding + random.uniform(self.mascot_size.width() * 0.25, self.mascot_size.width() * 0.75)
        hy = vertical_padding + random.uniform(self.mascot_size.height() * 0.1, self.mascot_size.height() * 0.3)

        pixel_size = max(1, self.mascot_size.width() // 50)

        speed_x = random.uniform(-0.005 * self.mascot_size.width(), 0.005 * self.mascot_size.width())
        speed_y = random.uniform(0.012 * self.mascot_size.height(), 0.024 * self.mascot_size.height())

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

        self.decision_timer.setInterval(random.randint(3000, 8000))

    def enterEvent(self, event):
        self.is_hovered = True
        if self.state != "sleep" and not self.alarm_firing:
            self.change_state("pet")
        event.accept()

    def leaveEvent(self, event):
        self.is_hovered = False
        self.hearts = []
        if self.state != "sleep" and not self.alarm_firing:
            if self.follow_cursor:
                self.change_state("idle")
            else:
                self.make_decision()
        event.accept()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            vertical_padding = self.height() - self.mascot_size.height()
            horizontal_padding = (self.width() - self.mascot_size.width()) // 2
            x = event.position().x()
            y = event.position().y()
            if horizontal_padding <= x <= horizontal_padding + self.mascot_size.width() and y >= vertical_padding:
                self.is_dragging = True
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

            release_pos = event.globalPosition().toPoint()
            drag_distance = (release_pos - self.press_pos).manhattanLength()

            if drag_distance < 5:
                if self.alarm_firing:
                    self.stop_alarm()
                    if self.dashboard:
                        self.dashboard.stop_alarm_btn.setEnabled(False)
                else:
                    self.context_menu.exec(QCursor.pos())
            else:
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

    def paintEvent(self, event):
        painter = QPainter(self)

        sprite_name = self.get_current_sprite_name()
        pixmap = self.sprites.get(sprite_name)
        vertical_padding = self.height() - self.mascot_size.height()
        horizontal_padding = (self.width() - self.mascot_size.width()) // 2
        if pixmap:
            painter.drawPixmap(horizontal_padding, vertical_padding, pixmap)

        if hasattr(self, 'pet_name') and self.pet_name:
            painter.save()
            font = painter.font()
            font.setFamily("'Comic Sans MS', 'Segoe UI', sans-serif")
            font.setBold(True)
            font.setPointSize(9)
            painter.setFont(font)

            fm = painter.fontMetrics()
            text_width = fm.horizontalAdvance(self.pet_name)
            text_height = fm.height()

            w = self.width()
            rect_w = text_width + 16
            rect_h = text_height + 4
            rect_x = (w - rect_w) // 2
            rect_y = vertical_padding + int(self.mascot_size.height() * 0.15) - rect_h

            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            painter.setPen(QColor("#FF69B4"))
            painter.setBrush(QColor(255, 240, 245, 220))
            painter.drawRoundedRect(rect_x, rect_y, rect_w, rect_h, 6, 6)

            painter.setPen(QColor("#C71585"))
            painter.drawText(rect_x + 8, rect_y + fm.ascent() + 2, self.pet_name)
            painter.restore()

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
            name_tag_height = fm.height() + 4
            rect_y = vertical_padding + int(self.mascot_size.height() * 0.15) - name_tag_height - rect_h - 10

            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            from PyQt6.QtGui import QPen
            pen = QPen(QColor("#FF1493"))
            pen.setWidth(2)
            painter.setPen(pen)
            painter.setBrush(QColor(255, 255, 224, 240))
            painter.drawRoundedRect(rect_x, rect_y, rect_w, rect_h, 8, 8)

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
            name_tag_height = fm.height() + 4
            rect_y = vertical_padding + int(self.mascot_size.height() * 0.15) - name_tag_height - rect_h - 10

            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            from PyQt6.QtGui import QPen
            pen = QPen(QColor("#FF69B4"))
            pen.setWidth(1)
            painter.setPen(pen)
            painter.setBrush(QColor(255, 240, 245, 220))
            painter.drawRoundedRect(rect_x, rect_y, rect_w, rect_h, 6, 6)

            painter.setPen(QColor("#C71585"))
            painter.drawText(rect_x + 8, rect_y + fm.ascent() + 2, msg_text)
            painter.restore()

        for heart in self.hearts:
            color = QColor(255, 60, 60, int(heart['alpha']))
            self.draw_pixel_heart(painter, heart['x'], heart['y'], heart['pixel_size'], color)

    def draw_keyboard_and_paws(self, painter, w, h, vertical_padding):
        """Gambar keyboard pixel art lucu dan cakar bergerak mengetik ya Putri cantik"""
        painter.save()
        painter.setPen(Qt.PenStyle.NoPen)

        kb_w = int(w * 0.55)
        kb_h = int(h * 0.08)
        kb_x = int((w - kb_w) // 2)
        kb_y = int(vertical_padding + h * 0.72)

        painter.setBrush(QColor(0, 0, 0))
        painter.drawRect(kb_x, kb_y, kb_w, kb_h)
        painter.setBrush(QColor(190, 190, 190))
        painter.drawRect(kb_x + 2, kb_y + 2, kb_w - 4, kb_h - 4)

        painter.setBrush(QColor(100, 100, 100))
        key_size = max(1, w // 64)
        for i in range(kb_x + 6, kb_x + kb_w - 6, key_size * 3):
            painter.drawRect(i, kb_y + 4, key_size, kb_h - 8)

        paw_radius = int(w * 0.08)

        if self.anim_frame == 1:
            left_paw_y = kb_y - int(h * 0.04)
            right_paw_y = kb_y + int(h * 0.01)
        else:
            left_paw_y = kb_y + int(h * 0.01)
            right_paw_y = kb_y - int(h * 0.04)

        left_paw_x = int(w * 0.35)
        right_paw_x = int(w * 0.53)

        painter.setBrush(QColor(0, 0, 0))
        painter.drawEllipse(left_paw_x - 1, left_paw_y - 1, paw_radius + 2, paw_radius + 2)
        painter.setBrush(QColor(255, 255, 255))
        painter.drawEllipse(left_paw_x, left_paw_y, paw_radius, paw_radius)
        painter.setBrush(QColor(255, 182, 193))
        painter.drawEllipse(left_paw_x + paw_radius // 4, left_paw_y + paw_radius // 4, paw_radius // 2, paw_radius // 2)

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

    mate = DesktopMate()
    dashboard = CatDashboard(mate)

    mate.show()
    dashboard.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()