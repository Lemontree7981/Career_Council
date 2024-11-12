import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QPushButton, QLineEdit, QLabel,
                             QFrame, QStackedWidget)
from PyQt6.QtCore import Qt, QSize, QTimer
from PyQt6.QtGui import (QPainter, QColor, QPainterPath, QLinearGradient,
                         QIcon, QFont, QPalette)
import subprocess
import secrets


class LogoWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(100, 100)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Create gradient for first C
        gradient1 = QLinearGradient(0, 0, self.width(), self.height())
        gradient1.setColorAt(0, QColor("#2196F3"))
        gradient1.setColorAt(1, QColor("#1976D2"))

        # Create gradient for second C
        gradient2 = QLinearGradient(0, 0, self.width(), self.height())
        gradient2.setColorAt(0, QColor("#4CAF50"))
        gradient2.setColorAt(1, QColor("#388E3C"))

        # Draw first C
        path1 = QPainterPath()
        path1.arcMoveTo(10, 10, 60, 60, 45)
        path1.arcTo(10, 10, 60, 60, 45, 270)
        painter.fillPath(path1, gradient1)

        # Draw second C
        path2 = QPainterPath()
        path2.arcMoveTo(30, 10, 60, 60, 45)
        path2.arcTo(30, 10, 60, 60, 45, 270)
        painter.fillPath(path2, gradient2)


class PasswordLineEdit(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Container widget for centering
        container = QWidget()
        container.setFixedWidth(300)
        container_layout = QHBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)

        # Password input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 8px 40px 8px 8px;  /* Increased right padding for larger button */
                border: 2px solid #BDBDBD;
                border-radius: 4px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #2196F3;
            }
        """)

        # Create SVG for visible and hidden states
        self.eye_visible = """
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z" fill="#555555"/>
        </svg>
        """

        self.eye_hidden = """
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 7c2.76 0 5 2.24 5 5 0 .65-.13 1.26-.36 1.83l2.92 2.92c1.51-1.26 2.7-2.89 3.43-4.75-1.73-4.39-6-7.5-11-7.5-1.4 0-2.74.25-3.98.7l2.16 2.16C10.74 7.13 11.35 7 12 7zM2 4.27l2.28 2.28.46.46C3.08 8.3 1.78 10.02 1 12c1.73 4.39 6 7.5 11 7.5 1.55 0 3.03-.3 4.38-.84l.42.42L19.73 22 21 20.73 3.27 3 2 4.27zM7.53 9.8l1.55 1.55c-.05.21-.08.43-.08.65 0 1.66 1.34 3 3 3 .22 0 .44-.03.65-.08l1.55 1.55c-.67.33-1.41.53-2.2.53-2.76 0-5-2.24-5-5 0-.79.2-1.53.53-2.2zm4.31-.78l3.15 3.15.02-.16c0-1.66-1.34-3-3-3l-.17.01z" fill="#555555"/>
        </svg>
        """

        # Toggle button with better styling
        self.toggle_btn = QPushButton()
        self.toggle_btn.setFixedSize(34, 34)
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                border: none;
                background-color: transparent;
                padding: 5px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 0.05);
            }
            QPushButton:pressed {
                background-color: rgba(0, 0, 0, 0.1);
            }
        """)
        self.toggle_btn.setIcon(QIcon(self.create_icon(self.eye_hidden)))
        self.toggle_btn.setIconSize(QSize(24, 24))

        # Add widgets to container
        container_layout.addWidget(self.password_input)

        # Center the container
        layout.addStretch()
        layout.addWidget(container)
        layout.addStretch()

        # Position the toggle button over the password input
        self.toggle_btn.setParent(self.password_input)
        self.toggle_btn.move(self.password_input.width() - 38, 3)

        # Connect signals
        self.password_input.textChanged.connect(self.update_toggle_position)
        self.toggle_btn.clicked.connect(self.toggle_password)
        self.is_password_visible = False

    def create_icon(self, svg_data):
        from PyQt6.QtCore import QByteArray
        from PyQt6.QtGui import QIcon, QPixmap
        pixmap = QPixmap()
        pixmap.loadFromData(QByteArray(svg_data.encode()))
        return QIcon(pixmap)

    def toggle_password(self):
        self.is_password_visible = not self.is_password_visible
        if self.is_password_visible:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
            self.toggle_btn.setIcon(QIcon(self.create_icon(self.eye_visible)))
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            self.toggle_btn.setIcon(QIcon(self.create_icon(self.eye_hidden)))

    def update_toggle_position(self):
        self.toggle_btn.move(self.password_input.width() - 38, 3)

    def text(self):
        return self.password_input.text()

    def clear(self):
        self.password_input.clear()

    def setFocus(self):
        self.password_input.setFocus()

    def selectAll(self):
        self.password_input.selectAll()
class StyleSheet:
    MAIN_STYLE = """
        QMainWindow {
            background-color: #f5f5f5;
        }
        QLabel {
            color: #333333;
        }
        QPushButton {
            background-color: #2196F3;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 10px;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #1976D2;
        }
        QPushButton:pressed {
            background-color: #0D47A1;
        }
        QPushButton#secondary {
            background-color: #4CAF50;
        }
        QPushButton#secondary:hover {
            background-color: #388E3C;
        }
        QPushButton#back {
            background-color: #9E9E9E;
        }
        QPushButton#back:hover {
            background-color: #757575;
        }
    """


class ModernLoginApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.login_password = "admin123"  # In production, use proper security
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Career Council Login")
        self.setMinimumSize(450, 600)
        self.setStyleSheet(StyleSheet.MAIN_STYLE)

        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(40, 40, 40, 40)

        # Create stacked widget for different pages
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        # Create main menu page
        self.create_main_menu_page()

        # Create admin login page
        self.create_admin_login_page()

        # Status bar
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.status_label)

        # Show main menu initially
        self.stacked_widget.setCurrentIndex(0)
        self.center_window()

    def create_main_menu_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        # Logo
        logo = LogoWidget()
        layout.addWidget(logo, alignment=Qt.AlignmentFlag.AlignCenter)

        # Title
        title = QLabel("Career Council")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Subtitle
        subtitle = QLabel("Your path to success starts here")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)

        # Spacer
        layout.addSpacing(20)

        # Login type label
        type_label = QLabel("Select your login type")
        type_label.setFont(QFont("Segoe UI", 12))
        type_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(type_label)

        # Admin button
        admin_btn = QPushButton("Administrator Access")
        admin_btn.clicked.connect(self.show_admin_login)
        layout.addWidget(admin_btn)

        # User button
        user_btn = QPushButton("Student Access")
        user_btn.setObjectName("secondary")
        user_btn.clicked.connect(self.open_user)
        layout.addWidget(user_btn)

        self.stacked_widget.addWidget(page)

    def create_admin_login_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        # Logo
        logo = LogoWidget()
        layout.addWidget(logo, alignment=Qt.AlignmentFlag.AlignCenter)

        # Title
        title = QLabel("Administrator Login")
        title.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Custom password input with centered alignment
        self.password_widget = PasswordLineEdit()
        self.password_widget.password_input.returnPressed.connect(self.verify_admin)
        layout.addWidget(self.password_widget)

        # Login button with fixed width and center alignment
        login_btn = QPushButton("Login")
        login_btn.setFixedWidth(300)
        login_btn.clicked.connect(self.verify_admin)
        layout.addWidget(login_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        # Back button with fixed width and center alignment
        back_btn = QPushButton("Back")
        back_btn.setFixedWidth(300)
        back_btn.setObjectName("back")
        back_btn.clicked.connect(self.show_main_menu)
        layout.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.stacked_widget.addWidget(page)

    def show_admin_login(self):
        self.stacked_widget.setCurrentIndex(1)
        self.password_widget.setFocus()
        self.status_label.setText("Enter administrator credentials")

    def show_main_menu(self):
        self.stacked_widget.setCurrentIndex(0)
        self.password_widget.clear()
        self.status_label.setText("")

    def verify_admin(self):
        password = self.password_widget.text()
        if password == self.login_password:
            self.status_label.setText("Access granted")
            QTimer.singleShot(500, self.open_admin)
        else:
            self.status_label.setText("Access denied - Invalid credentials")
            self.password_widget.selectAll()
            self.password_widget.setFocus()

    def open_admin(self):
        token = secrets.token_hex(16)
        self.close()
        subprocess.run(["python", "college_manager.py", token])

    def open_user(self):
        token = secrets.token_hex(16)
        self.close()
        subprocess.run(["python", "college_recommender.py", token])

    def center_window(self):
        frame_geometry = self.frameGeometry()
        screen_center = self.screen().availableGeometry().center()
        frame_geometry.moveCenter(screen_center)
        self.move(frame_geometry.topLeft())


def main():
    app = QApplication(sys.argv)

    # Set application-wide font
    app.setFont(QFont("Segoe UI", 10))

    # Try to load icon
    try:
        app.setWindowIcon(QIcon('icon.ico'))
    except:
        pass

    window = ModernLoginApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()