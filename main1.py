import sys
import sqlite3
from datetime import datetime, timedelta
import hashlib
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class ModernCard(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFrameStyle(QFrame.NoFrame)
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #e0e6ed;
            }
        """)
        self.setGraphicsEffect(self.create_shadow())
    
    def create_shadow(self):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 4)
        return shadow

class AnimatedButton(QPushButton):
    def __init__(self, text, primary=True, parent=None):
        super().__init__(text, parent)
        self.primary = primary
        self.setMinimumHeight(45)
        self.setCursor(Qt.PointingHandCursor)
        self.original_pos = None
        self.current_animation = None
        self.setup_style()
        
        # Add animation
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(150)
        
    def setup_style(self):
        if self.primary:
            self.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #4f46e5, stop:1 #7c3aed);
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-size: 14px;
                    font-weight: 600;
                    padding: 12px 24px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #4338ca, stop:1 #6d28d9);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #3730a3, stop:1 #581c87);
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #f8fafc;
                    color: #64748b;
                    border: 2px solid #e2e8f0;
                    border-radius: 8px;
                    font-size: 14px;
                    font-weight: 600;
                    padding: 12px 24px;
                }
                QPushButton:hover {
                    background-color: #f1f5f9;
                    border-color: #cbd5e1;
                    color: #475569;
                }
                QPushButton:pressed {
                    background-color: #e2e8f0;
                }
            """)
    def showEvent(self, event):
        """Store initial position when widget is first shown"""
        if self.original_pos is None:
            self.original_pos = self.pos()
        super().showEvent(event)

    def store_position(self):
        """Store the current position as original position"""
        if self.parent() and self.isVisible():
            self.original_pos = self.pos()
    
    


    def enterEvent(self, event):
        """Triggered when mouse enters the button"""
        if not self.original_pos:
            self.original_pos = self.pos()
            
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(150)
        self.animation.setEndValue(self.original_pos - QPoint(0, 2))  # Move up 2 pixels
        self.animation.setEasingCurve(QEasingCurve.OutQuad)
        self.animation.start()

    def leaveEvent(self, event):
        """Triggered when mouse leaves the button"""
        if self.current_animation:
            self.current_animation.stop()
            
        if not self.original_pos:
            self.store_position()
            
        self.current_animation = QPropertyAnimation(self, b"pos")
        self.current_animation.setDuration(150)
        self.current_animation.setEndValue(self.original_pos)  # Return to original position
        self.current_animation.setEasingCurve(QEasingCurve.OutQuad)
        self.current_animation.start()
        
    def moveEvent(self, event):
        """Update original position if the button is moved programmatically"""
        super().moveEvent(event)
        self.store_position()

class ModernInput(QLineEdit):
    def __init__(self, placeholder="", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setMinimumHeight(45)
        self.setStyleSheet("""
            QLineEdit {
                background-color: #f8fafc;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 14px;
                color: #1e293b;
            }
            QLineEdit:focus {
                border-color: #4f46e5;
                background-color: white;
            }
            QLineEdit:hover {
                border-color: #cbd5e1;
            }
        """)

class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("College Leave Management System")
        self.setFixedSize(800, 500)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        
        # Center the window
        screen = QApplication.desktop().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)
        
        # Create layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Background with gradient
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #667eea, stop:0.5 #764ba2, stop:1 #f093fb);
            }
        """)
        
        # Content container
        content = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setAlignment(Qt.AlignCenter)
        content_layout.setSpacing(30)
        
        # Logo/Icon placeholder
        icon_label = QLabel("🎓")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("""
            font-size: 72px;
            color: white;
            margin-bottom: 20px;
        """)
        
        # Title
        title_label = QLabel("College Leave Management System")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 36px;
            font-weight: 700;
            color: white;
            margin-bottom: 10px;
        """)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(2, 2)
        title_label.setGraphicsEffect(shadow)
        # Subtitle
        subtitle_label = QLabel("Streamlined Leave Processing for Students and Faculty")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("""
            font-size: 18px;
            color: rgba(255, 255, 255, 0.9);
            font-weight: 400;
            margin-bottom: 40px;
        """)
        
        # Loading animation
        loading_label = QLabel("Loading...")
        loading_label.setAlignment(Qt.AlignCenter)
        loading_label.setStyleSheet("""
            font-size: 16px;
            color: rgba(255, 255, 255, 0.8);
            font-weight: 300;
        """)
        
        # Progress bar
        self.progress = QProgressBar()
        self.progress.setMaximum(100)
        self.progress.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 10px;
                background-color: rgba(255, 255, 255, 0.2);
                height: 20px;
                text-align: center;
                color: white;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #ff9a9e, stop:1 #fecfef);
                border-radius: 10px;
            }
        """)
        
        content_layout.addWidget(icon_label)
        content_layout.addWidget(title_label)
        content_layout.addWidget(subtitle_label)
        content_layout.addWidget(loading_label)
        content_layout.addWidget(self.progress)
        
        content.setLayout(content_layout)
        layout.addWidget(content)
        self.setLayout(layout)
        
        # Animate progress bar
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(10)
        self.progress_value = 0
        
    def update_progress(self):
        self.progress_value += 1
        self.progress.setValue(self.progress_value)
        if self.progress_value >= 100:
            self.timer.stop()

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.db_path =r"D:\miniproject\leave_management\leave_management.db"
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Login - College Leave Management System")
        self.resize(900, 600)
        
        # Center the window
        screen = QApplication.desktop().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)
        
        # Set background
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #f8fafc, stop:1 #e2e8f0);
            }
        """)
        
        # Main layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Left side - Branding
        left_panel = QWidget()
        left_panel.setFixedWidth(400)
        left_panel.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #4f46e5, stop:1 #7c3aed);
            }
        """)
        
        left_layout = QVBoxLayout()
        left_layout.setAlignment(Qt.AlignCenter)
        left_layout.setSpacing(30)
        
        # Branding content
        brand_icon = QLabel("🎓")
        brand_icon.setAlignment(Qt.AlignCenter)
        brand_icon.setStyleSheet("font-size: 64px; color: white;")
        
        brand_title = QLabel("Welcome Back!")
        brand_title.setAlignment(Qt.AlignCenter)
        brand_title.setStyleSheet("""
            font-size: 32px;
            font-weight: 700;
            color: white;
            margin-bottom: 10px;
        """)
        
        brand_subtitle = QLabel("Access your leave management dashboard")
        brand_subtitle.setAlignment(Qt.AlignCenter)
        brand_subtitle.setStyleSheet("""
            font-size: 16px;
            color: rgba(255, 255, 255, 0.8);
            font-weight: 300;
        """)
        
        left_layout.addWidget(brand_icon)
        left_layout.addWidget(brand_title)
        left_layout.addWidget(brand_subtitle)
        left_panel.setLayout(left_layout)
        
        # Right side - Login form
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignCenter)
        right_layout.setContentsMargins(60, 60, 60, 60)
        right_layout.setSpacing(30)
        
        # Login card
        login_card = ModernCard()
        login_card.resize(350, 450)
        
        card_layout = QVBoxLayout()
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(25)
        
        # Title
        title = QLabel("Sign In")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 10px;
        """)
        
        subtitle = QLabel("Enter your credentials to access your account")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("""
            font-size: 14px;
            color: #64748b;
            margin-bottom: 20px;
        """)
        
        # Form fields
        self.username_input = ModernInput("Roll Number / Faculty ID / Admin ID")
        self.password_input = ModernInput("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        
        # Login button
        self.login_btn = AnimatedButton("Sign In", primary=True)
        self.login_btn.clicked.connect(self.authenticate_user)
        
        # Status label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("""
            color: #ef4444;
            font-weight: 500;
            font-size: 14px;
            margin-top: 10px;
        """)
        
        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)
        card_layout.addWidget(self.username_input)
        card_layout.addWidget(self.password_input)
        card_layout.addWidget(self.login_btn)
        card_layout.addWidget(self.status_label)
        
        login_card.setLayout(card_layout)
        right_layout.addWidget(login_card)
        right_panel.setLayout(right_layout)
        
        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel)
        self.setLayout(main_layout)
        
        # Connect Enter key to login
        self.password_input.returnPressed.connect(self.authenticate_user)
        
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate_user(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username or not password:
            self.show_error("Please enter both username and password")
            return
            
        # Show loading state
        self.login_btn.setText("Signing in...")
        self.login_btn.setEnabled(False)
        QApplication.processEvents()
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if admin
            cursor.execute('''
                SELECT Admin_id, Name, E_mail
                FROM Admin 
                WHERE Admin_id = ? AND Password = ?
            ''', (username, self.hash_password(password)))
            
            admin = cursor.fetchone()
            
            if admin:
                self.open_admin_dashboard({
                    'admin_id': admin[0],
                    'name': admin[1],
                    'email': admin[2]
                })
                conn.close()
                return
            
            # Check if student
            cursor.execute('''
                SELECT s.Roll_no, s.Name, s.Dept, s.Tutor_id, f.Name 
                FROM student s
                JOIN Faculty f ON s.Tutor_id = f.Tutor_id
                WHERE s.Roll_no = ? AND s.password = ?
            ''', (username, self.hash_password(password)))
            
            student = cursor.fetchone()
            
            if student:
                self.open_student_dashboard({
                    'roll_no': student[0],
                    'name': student[1],
                    'dept': student[2],
                    'tutor_id': student[3],
                    'tutor_name': student[4]
                })
                conn.close()
                return
            
            # Check if faculty
            cursor.execute('''
                SELECT Tutor_id, Name, Dept, E_mail
                FROM Faculty 
                WHERE Tutor_id = ? AND Password = ?
            ''', (username, self.hash_password(password)))
            
            faculty = cursor.fetchone()
            
            if faculty:
                self.open_faculty_dashboard({
                    'tutor_id': faculty[0],
                    'name': faculty[1],
                    'dept': faculty[2],
                    'email': faculty[3]
                })
                conn.close()
                return
                
            self.show_error("Invalid username or password")
            conn.close()
            
        except sqlite3.Error as e:
            self.show_error(f"Database error: {str(e)}")
        finally:
            self.login_btn.setText("Sign In")
            self.login_btn.setEnabled(True)
    
    def show_error(self, message):
        self.status_label.setText(message)
        # Auto-clear error after 5 seconds
        QTimer.singleShot(5000, lambda: self.status_label.setText(""))
    
    def open_student_dashboard(self, student_info):
        self.student_dashboard = StudentDashboard(student_info, self.db_path)
        self.student_dashboard.showMaximized()
        self.close()
    
    def open_faculty_dashboard(self, faculty_info):
        self.faculty_dashboard = FacultyDashboard(faculty_info, self.db_path)
        self.faculty_dashboard.showMaximized()
        self.close()

    def open_admin_dashboard(self, admin_info):
        self.admin_dashboard = AdminDashboard(admin_info, self.db_path)
        self.admin_dashboard.showMaximized()
        self.close()



class StudentDashboard(QWidget):
    def __init__(self, student_info, db_path):
        super().__init__()
        self.student_info = student_info
        self.db_path = db_path
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Student Dashboard - College Leave Management System")
        self.resize(1200, 800)
        
        # Center the window
        screen = QApplication.desktop().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)
        
        # Set background
        self.setStyleSheet("""
            QWidget {
                background-color: #f8fafc;
            }
        """)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(30)
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Stats cards
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)
        
        # Quick stats
        total_requests = self.get_total_requests()
        pending_requests = self.get_pending_requests()
        approved_requests = self.get_approved_requests()
        
        stats_layout.addWidget(self.create_stat_card("Total Requests", str(total_requests), "#3b82f6", "📊"))
        stats_layout.addWidget(self.create_stat_card("Pending", str(pending_requests), "#f59e0b", "⏳"))
        stats_layout.addWidget(self.create_stat_card("Approved", str(approved_requests), "#10b981", "✅"))
        
        main_layout.addLayout(stats_layout)
        
        # Action buttons
        action_layout = QHBoxLayout()
        action_layout.setSpacing(20)
        
        new_leave_btn = AnimatedButton("📝 New Leave Application", primary=True)
        new_leave_btn.setMinimumHeight(60)
        new_leave_btn.clicked.connect(self.open_new_leave_form)
        
        check_status_btn = AnimatedButton("📋 Check Status", primary=False)
        check_status_btn.setMinimumHeight(60)
        check_status_btn.clicked.connect(self.show_leave_status)
        
        action_layout.addWidget(new_leave_btn)
        action_layout.addWidget(check_status_btn)
        
        main_layout.addLayout(action_layout)
        
        # Content area
        self.content_area = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_area.setLayout(self.content_layout)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidget(self.content_area)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: #f1f5f9;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #cbd5e1;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #94a3b8;
            }
        """)
        
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)
        
    def create_header(self):
        header = ModernCard()
        header.setMinimumHeight(120)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)
        
        # Student info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(5)
        
        welcome_label = QLabel(f"Welcome back, {self.student_info['name']}! 👋")
        welcome_label.setStyleSheet("""
            font-size: 24px;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 5px;
        """)
        
        details_layout = QHBoxLayout()
        details_layout.setSpacing(30)
        
        roll_label = QLabel(f"🎓 Roll No: {self.student_info['roll_no']}")
        dept_label = QLabel(f"🏛️ Department: {self.student_info['dept']}")
        tutor_label = QLabel(f"👨‍🏫 Tutor: {self.student_info['tutor_name']}")
        
        for label in [roll_label, dept_label, tutor_label]:
            label.setStyleSheet("""
                font-size: 14px;
                font-weight: 500;
                color: #64748b;
            """)
            details_layout.addWidget(label)
        
        info_layout.addWidget(welcome_label)
        info_layout.addLayout(details_layout)
        
        # Logout button
        logout_btn = AnimatedButton("Logout", primary=False)
        logout_btn.setFixedSize(100, 40)
        logout_btn.clicked.connect(self.logout)

        logout_btn.enterEvent = lambda event: None
        logout_btn.leaveEvent = lambda event: None
        
        layout.addLayout(info_layout)
        layout.addStretch()
        layout.addWidget(logout_btn)
        
        header.setLayout(layout)
        return header
    
    def create_stat_card(self, title, value, color, icon):
        card = ModernCard()
        card.setFixedHeight(120)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(10)
        
        # Icon and value
        top_layout = QHBoxLayout()
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"""
            font-size: 32px;
            color: {color};
        """)
        
        value_label = QLabel(value)
        value_label.setAlignment(Qt.AlignRight)
        value_label.setStyleSheet(f"""
            font-size: 32px;
            font-weight: 700;
            color: {color};
        """)
        
        top_layout.addWidget(icon_label)
        top_layout.addStretch()
        top_layout.addWidget(value_label)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-size: 14px;
            font-weight: 600;
            color: #64748b;
        """)
        
        layout.addLayout(top_layout)
        layout.addWidget(title_label)
        
        card.setLayout(layout)
        return card
    
    def get_total_requests(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM leave_requests WHERE student_id = ?', (self.student_info['roll_no'],))
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except:
            return 0
    
    def get_pending_requests(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM leave_requests WHERE student_id = ? AND status = "Pending"', (self.student_info['roll_no'],))
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except:
            return 0
    
    def get_approved_requests(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM leave_requests WHERE student_id = ? AND status = "Approved"', (self.student_info['roll_no'],))
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except:
            return 0
    
    def clear_content(self):
        """Clear the content area"""
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
    def logout(self):
        reply = QMessageBox.question(self, 'Logout', 'Are you sure you want to logout?',
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.login_window = LoginWindow()
            self.login_window.showMaximized()
            self.close()
        
    def open_new_leave_form(self):
        self.clear_content()
        
        # Title
        title = QLabel("📝 New Leave Request")
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 30px;
        """)
        title.setAlignment(Qt.AlignCenter)
        self.content_layout.addWidget(title)
        
        # Form card
        form_card = ModernCard()
        form_card.setMaximumWidth(600)
        
        form_layout = QVBoxLayout()
        form_layout.setContentsMargins(40, 40, 40, 40)
        form_layout.setSpacing(25)
        
        # Form fields
        fields_layout = QFormLayout()
        fields_layout.setSpacing(20)
        
        # Start date
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate())
        self.start_date.setCalendarPopup(True)
        self.start_date.setMinimumHeight(45)
        self.start_date.setStyleSheet("""
            QDateEdit {
                background-color: #f8fafc;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 14px;
                color: #1e293b;
            }
            QDateEdit:focus {
                border-color: #4f46e5;
                background-color: white;
            }
        """)
        
        # Number of days
        self.days_input = QSpinBox()
        self.days_input.setMinimum(1)
        self.days_input.setMaximum(365)
        self.days_input.setValue(1)
        self.days_input.setMinimumHeight(45)
        self.days_input.setStyleSheet("""
            QSpinBox {
                background-color: #f8fafc;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 14px;
                color: #1e293b;
            }
            QSpinBox:focus {
                border-color: #4f46e5;
                background-color: white;
            }
        """)
        
        # Leave type
        self.leave_type = QComboBox()
        self.leave_type.addItems(["🤒 Sick", "👤 Personal", "📋 Other"])
        self.leave_type.setMinimumHeight(45)
        self.leave_type.setStyleSheet("""
            QComboBox {
                background-color: #f8fafc;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 14px;
                color: #1e293b;
            }
            QComboBox:focus {
                border-color: #4f46e5;
                background-color: white;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border: none;
            }
        """)
        
        # Description
        self.description = QTextEdit()
        self.description.setMaximumHeight(100)
        self.description.setPlaceholderText("Brief description (optional)")
        self.description.setStyleSheet("""
            QTextEdit {
                background-color: #f8fafc;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 14px;
                color: #1e293b;
            }
            QTextEdit:focus {
                border-color: #4f46e5;
                background-color: white;
            }
        """)
        
        # Create stylized labels
        start_label = QLabel("📅 Start Date")
        days_label = QLabel("📊 Number of Days")
        type_label = QLabel("📋 Leave Type")
        desc_label = QLabel("📝 Description")
        
        for label in [start_label, days_label, type_label, desc_label]:
            label.setStyleSheet("""
                font-size: 14px;
                font-weight: 600;
                color: #374151;
                margin-bottom: 5px;
            """)
        
        fields_layout.addRow(start_label, self.start_date)
        fields_layout.addRow(days_label, self.days_input)
        fields_layout.addRow(type_label, self.leave_type)
        fields_layout.addRow(desc_label, self.description)
        
        # Submit button
        submit_btn = AnimatedButton("🚀 Submit Leave Request", primary=True)
        submit_btn.setMinimumHeight(50)
        submit_btn.clicked.connect(self.submit_leave_request)
        
        form_layout.addLayout(fields_layout)
        form_layout.addWidget(submit_btn)
        
        form_card.setLayout(form_layout)
        
        # Center the form
        center_layout = QHBoxLayout()
        center_layout.addStretch()
        center_layout.addWidget(form_card)
        center_layout.addStretch()
        
        self.content_layout.addLayout(center_layout)
        
    def submit_leave_request(self):
        start_date = self.start_date.date().toPyDate()
        days = self.days_input.value()
        leave_type = self.leave_type.currentText().split(' ', 1)[1]  # Remove emoji
        description = self.description.toPlainText().strip()
        
        # Validate date
        if start_date < datetime.now().date():
            self.show_error_message("Error", "Start date cannot be in the past!")
            return
        
        # Calculate end date
        end_date = start_date + timedelta(days=days-1)
        
        # Show confirmation dialog
        self.show_confirmation_dialog(start_date, end_date, days, leave_type, description)
        
    def show_confirmation_dialog(self, start_date, end_date, days, leave_type, description):
        """Show confirmation dialog with all details"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Confirm Leave Request")
        dialog.setFixedSize(500, 400)
        dialog.setStyleSheet("""
            QDialog {
                background-color: white;
                border-radius: 12px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("📋 Confirm Your Leave Request")
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 10px;
        """)
        title.setAlignment(Qt.AlignCenter)
        
        # Details
        details_text = f"""
        <div style="background-color: #f8fafc; padding: 20px; border-radius: 8px; border: 1px solid #e2e8f0;">
            <p><strong>📅 Start Date:</strong> {start_date.strftime('%Y-%m-%d')}</p>
            <p><strong>📅 End Date:</strong> {end_date.strftime('%Y-%m-%d')}</p>
            <p><strong>📊 Number of Days:</strong> {days}</p>
            <p><strong>📋 Leave Type:</strong> {leave_type}</p>
            <p><strong>📝 Description:</strong> {description if description else 'Not provided'}</p>
        </div>
        """
        
        details_label = QLabel(details_text)
        details_label.setWordWrap(True)
        details_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #374151;
                line-height: 1.5;
            }
        """)
        
        # Warning message
        warning = QLabel("⚠️ Please review all details carefully before submitting.")
        warning.setStyleSheet("""
            font-size: 12px;
            color: #f59e0b;
            font-weight: 500;
            padding: 10px;
            background-color: #fef3c7;
            border-radius: 6px;
            border: 1px solid #fcd34d;
        """)
        warning.setAlignment(Qt.AlignCenter)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        cancel_btn = AnimatedButton("❌ Cancel", primary=False)
        cancel_btn.clicked.connect(dialog.reject)
        
        confirm_btn = AnimatedButton("✅ Confirm & Submit", primary=True)
        confirm_btn.clicked.connect(lambda: self.confirm_submission(dialog, start_date, end_date, days, leave_type, description))
        
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(confirm_btn)
        
        layout.addWidget(title)
        layout.addWidget(details_label)
        layout.addWidget(warning)
        layout.addLayout(button_layout)
        
        dialog.setLayout(layout)
        dialog.exec_()

    def send_leave_request_email(self, student_name, student_roll, tutor_email, tutor_name, 
                           start_date, end_date, leave_type, description):
        """Send email notification to the tutor"""
        try:
            # Email configuration
            SMTP_SERVER = "smtp.gmail.com"
            SMTP_PORT = 587
            SENDER_EMAIL = "leavemanagement13@gmail.com"
            SENDER_PASSWORD = "cvtu yils lqtc dyzf"  # Consider using environment variables in production
            
            print(f"Attempting to send email to: {tutor_email}")

            # Validate email
            if not tutor_email or "@" not in tutor_email:
                print("Invalid tutor email address")
                return False

            # Create email message
            msg = MIMEMultipart()
            msg['From'] = SENDER_EMAIL
            msg['To'] = tutor_email
            msg['Subject'] = f"Leave Request from {student_name} ({student_roll})"
            
            body = f"""
            <html>
                <body>
                    <p>Dear Prof. {tutor_name},</p>
                    <p>You have a new leave request from your student:</p>
                    <ul>
                        <li><strong>Student:</strong> {student_name} ({student_roll})</li>
                        <li><strong>Dates:</strong> {start_date} to {end_date}</li>
                        <li><strong>Type:</strong> {leave_type}</li>
                        <li><strong>Reason:</strong> {description if description else 'No reason provided'}</li>
                    </ul>
                    <p>Please review this in the Leave Management System.</p>
                    <p>Regards,<br>College Leave System</p>
                </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))

            # Send email
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
                server.starttls()
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                server.send_message(msg)
            
            print("Email successfully sent!")
            return True
        
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
                server.ehlo()
                server.starttls()
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                
                # Add delivery status check
                response = server.sendmail(SENDER_EMAIL, tutor_email, msg.as_string())
                
                if not response:
                    print(f"Email successfully delivered to {tutor_email}")
                else:
                    print(f"Delivery issues: {response}")
                
            return True
            
        except smtplib.SMTPAuthenticationError:
            print("Error: Authentication failed - check your email credentials")
            return False
        except smtplib.SMTPException as e:
            print(f"SMTP error occurred: {str(e)}")
            return False
        except Exception as e:
            print(f"Unexpected error sending email: {str(e)}")
            return False
        
    def confirm_submission(self, dialog, start_date, end_date, days, leave_type, description):
        """Submit the leave request to database and send email to tutor"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO leave_requests (student_id, tutor_id, from_date, to_date, reason, description, status)
                VALUES (?, ?, ?, ?, ?, ?, 'Pending')
            ''', (self.student_info['roll_no'], self.student_info['tutor_id'], 
                start_date, end_date, leave_type, description))
            
            conn.commit()
            
            # Get tutor's email from database
            cursor.execute('''
                SELECT E_mail FROM Faculty WHERE Tutor_id = ?
            ''', (self.student_info['tutor_id'],))
            
            tutor_email = cursor.fetchone()[0]
            conn.close()
            
            # Send email to tutor
            email_sent = self.send_leave_request_email(
                student_name=self.student_info['name'],
                student_roll=self.student_info['roll_no'],
                tutor_email=tutor_email,
                tutor_name=self.student_info['tutor_name'],
                start_date=start_date.strftime('%Y-%m-%d'),
                end_date=end_date.strftime('%Y-%m-%d'),
                leave_type=leave_type,
                description=description
            )
            
            if email_sent:
                dialog.accept()
                self.show_success_message("Success", 
                    "Leave request submitted successfully!\nAn email has been sent to your tutor.")
            else:
                dialog.accept()
                self.show_success_message("Success", 
                    "Leave request submitted successfully!\nBut failed to send email notification.")
            
            # Clear form
            self.start_date.setDate(QDate.currentDate())
            self.days_input.setValue(1)
            self.leave_type.setCurrentIndex(0)
            self.description.clear()
            
        except sqlite3.Error as e:
            self.show_error_message("Database Error", f"Failed to submit leave request: {str(e)}")
        
    def show_leave_status(self):
        """Display all leave requests with status"""
        self.clear_content()
        
        # Title
        title = QLabel("📋 Leave Request Status")
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 30px;
        """)
        title.setAlignment(Qt.AlignCenter)
        self.content_layout.addWidget(title)
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT from_date, to_date, reason, description, status, created_at
                FROM leave_requests 
                WHERE student_id = ?
                ORDER BY created_at DESC
            ''', (self.student_info['roll_no'],))
            
            requests = cursor.fetchall()
            conn.close()
            
            if not requests:
                # No requests found
                no_requests = QLabel("📭 No leave requests found")
                no_requests.setStyleSheet("""
                    font-size: 18px;
                    color: #64748b;
                    font-weight: 500;
                    padding: 40px;
                """)
                no_requests.setAlignment(Qt.AlignCenter)
                self.content_layout.addWidget(no_requests)
                return
            
            # Display requests
            for request in requests:
                request_card = self.create_request_card(request)
                self.content_layout.addWidget(request_card)
                
        except sqlite3.Error as e:
            self.show_error_message("Database Error", f"Failed to fetch leave requests: {str(e)}")
    
    def create_request_card(self, request_data):
        """Create a card for each leave request"""
        from_date, to_date, reason, description, status, created_at = request_data
        
        # Determine card color based on status
        if status == "Approved":
            border_color = "#10b981"
            bg_color = "#f0fdf4"
            status_color = "#10b981"
            status_icon = "✅"
        elif status == "Rejected":
            border_color = "#ef4444"
            bg_color = "#fef2f2"
            status_color = "#ef4444"
            status_icon = "❌"
        else:  # Pending
            border_color = "#f59e0b"
            bg_color = "#fefbf0"
            status_color = "#f59e0b"
            status_icon = "⏳"
        
        card = QFrame()
        card.setFrameStyle(QFrame.NoFrame)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border: 2px solid {border_color};
                border-radius: 12px;
                margin: 5px;
            }}
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(15)
        
        # Header with status
        header_layout = QHBoxLayout()
        
        # Request info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(5)
        
        title_text = f"📅 {from_date} to {to_date}"
        title_label = QLabel(title_text)
        title_label.setStyleSheet("""
            font-size: 16px;
            font-weight: 600;
            color: #1e293b;
        """)
        
        reason_text = f"📋 {reason}"
        reason_label = QLabel(reason_text)
        reason_label.setStyleSheet("""
            font-size: 14px;
            color: #64748b;
            font-weight: 500;
        """)
        
        info_layout.addWidget(title_label)
        info_layout.addWidget(reason_label)
        
        # Status badge
        status_label = QLabel(f"{status_icon} {status}")
        status_label.setStyleSheet(f"""
            font-size: 14px;
            font-weight: 600;
            color: {status_color};
            padding: 8px 16px;
            background-color: white;
            border-radius: 20px;
            border: 1px solid {border_color};
        """)
        status_label.setAlignment(Qt.AlignCenter)
        status_label.setFixedHeight(35)
        
        header_layout.addLayout(info_layout)
        header_layout.addStretch()
        header_layout.addWidget(status_label)
        
        # Description (if provided)
        if description:
            desc_label = QLabel(f"📝 {description}")
            desc_label.setStyleSheet("""
                font-size: 13px;
                color: #6b7280;
                font-style: italic;
                padding: 10px;
                background-color: rgba(255, 255, 255, 0.7);
                border-radius: 6px;
            """)
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label)
        
        # Footer with submission date
        footer_label = QLabel(f"📅 Submitted: {created_at}")
        footer_label.setStyleSheet("""
            font-size: 12px;
            color: #9ca3af;
            font-weight: 400;
        """)
        
        # Status message
        if status == "Pending":
            message = "⏳ Waiting for confirmation from your tutor"
        elif status == "Approved":
            message = "✅ Your leave request has been approved"
        else:
            message = "❌ Your leave request has been rejected"
            
        message_label = QLabel(message)
        message_label.setStyleSheet(f"""
            font-size: 13px;
            color: {status_color};
            font-weight: 500;
            padding: 8px;
            text-align: center;
        """)
        message_label.setAlignment(Qt.AlignCenter)
        
        layout.addLayout(header_layout)
        layout.addWidget(message_label)
        layout.addWidget(footer_label)
        
        card.setLayout(layout)
        return card
    
    def show_error_message(self, title, message):
        """Show error message dialog"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
                color: #1e293b;
            }
            QMessageBox QPushButton {
                background-color: #ef4444;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: 500;
            }
            QMessageBox QPushButton:hover {
                background-color: #dc2626;
            }
        """)
        msg.exec_()
    
    def show_success_message(self, title, message):
        """Show success message dialog"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
                color: #1e293b;
            }
            QMessageBox QPushButton {
                background-color: #10b981;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: 500;
            }
            QMessageBox QPushButton:hover {
                background-color: #059669;
            }
        """)
        msg.exec_()

class FacultyDashboard(QWidget):
    def __init__(self, faculty_info, db_path):
        super().__init__()
        self.faculty_info = faculty_info
        self.db_path = db_path
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Faculty Dashboard - College Leave Management System")
        self.resize(1200, 800)
        
        # Center the window
        screen = QApplication.desktop().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)
        
        # Set background
        self.setStyleSheet("""
            QWidget {
                background-color: #f8fafc;
            }
        """)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(30)
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Stats cards
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)
        
        # Quick stats
        total_requests = self.get_total_requests()
        pending_requests = self.get_pending_requests()
        approved_requests = self.get_approved_requests()
        rejected_requests = self.get_rejected_requests()
        
        stats_layout.addWidget(self.create_stat_card("Total Requests", str(total_requests), "#3b82f6", "📊"))
        stats_layout.addWidget(self.create_stat_card("Pending", str(pending_requests), "#f59e0b", "⏳"))
        stats_layout.addWidget(self.create_stat_card("Approved", str(approved_requests), "#10b981", "✅"))
        stats_layout.addWidget(self.create_stat_card("Rejected", str(rejected_requests), "#ef4444", "❌"))
        
        main_layout.addLayout(stats_layout)
        
        # Action buttons
        action_layout = QHBoxLayout()
        action_layout.setSpacing(20)
        
        review_requests_btn = AnimatedButton("📋 Review Leave Requests", primary=True)
        review_requests_btn.setMinimumHeight(60)
        review_requests_btn.clicked.connect(self.show_leave_requests)
        
        request_leave_btn = AnimatedButton("📝 Request Leave", primary=False)
        request_leave_btn.setMinimumHeight(60)
        request_leave_btn.clicked.connect(self.open_new_leave_form)
        
        refresh_btn = AnimatedButton("🔄 Refresh Data", primary=False)
        refresh_btn.setMinimumHeight(60)
        refresh_btn.clicked.connect(self.refresh_data)
        
        action_layout.addWidget(review_requests_btn)
        action_layout.addWidget(request_leave_btn)
        action_layout.addWidget(refresh_btn)
        
        main_layout.addLayout(action_layout)
        
        # Content area
        self.content_area = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_area.setLayout(self.content_layout)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidget(self.content_area)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: #f1f5f9;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #cbd5e1;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #94a3b8;
            }
        """)
        
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)
        
        # Load initial data
        self.show_leave_requests()
        
    def create_header(self):
        header = ModernCard()
        header.setMinimumHeight(120)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)
        
        # Faculty info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(5)
        
        welcome_label = QLabel(f"Welcome, Prof. {self.faculty_info['name']}! 👨‍🏫")
        welcome_label.setStyleSheet("""
            font-size: 24px;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 5px;
        """)
        
        details_layout = QHBoxLayout()
        details_layout.setSpacing(30)
        
        id_label = QLabel(f"🆔 Faculty ID: {self.faculty_info['tutor_id']}")
        dept_label = QLabel(f"🏛️ Department: {self.faculty_info['dept']}")
        email_label = QLabel(f"📧 Email: {self.faculty_info['email']}")
        
        for label in [id_label, dept_label, email_label]:
            label.setStyleSheet("""
                font-size: 14px;
                font-weight: 500;
                color: #64748b;
            """)
            details_layout.addWidget(label)
        
        info_layout.addWidget(welcome_label)
        info_layout.addLayout(details_layout)
        
        # Logout button
        logout_btn = AnimatedButton("Logout", primary=False)
        logout_btn.setFixedSize(100, 40)
        logout_btn.clicked.connect(self.logout)
        
        layout.addLayout(info_layout)
        layout.addStretch()
        layout.addWidget(logout_btn)
        
        header.setLayout(layout)
        return header
    
    def create_stat_card(self, title, value, color, icon):
        card = ModernCard()
        card.setFixedHeight(120)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(10)
        
        # Icon and value
        top_layout = QHBoxLayout()
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"""
            font-size: 32px;
            color: {color};
        """)
        
        value_label = QLabel(value)
        value_label.setAlignment(Qt.AlignRight)
        value_label.setStyleSheet(f"""
            font-size: 32px;
            font-weight: 700;
            color: {color};
        """)
        
        top_layout.addWidget(icon_label)
        top_layout.addStretch()
        top_layout.addWidget(value_label)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-size: 14px;
            font-weight: 600;
            color: #64748b;
        """)
        
        layout.addLayout(top_layout)
        layout.addWidget(title_label)
        
        card.setLayout(layout)
        return card
    
    def get_total_requests(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM leave_requests WHERE tutor_id = ?', (self.faculty_info['tutor_id'],))
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except:
            return 0
    
    def get_pending_requests(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM leave_requests WHERE tutor_id = ? AND status = "Pending"', (self.faculty_info['tutor_id'],))
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except:
            return 0
    
    def get_approved_requests(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM leave_requests WHERE tutor_id = ? AND status = "Approved"', (self.faculty_info['tutor_id'],))
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except:
            return 0
    
    def get_rejected_requests(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM leave_requests WHERE tutor_id = ? AND status = "Rejected"', (self.faculty_info['tutor_id'],))
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except:
            return 0
    
    def clear_content(self):
        """Clear the content area"""
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    
    def logout(self):
        reply = QMessageBox.question(self, 'Logout', 'Are you sure you want to logout?',
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.login_window = LoginWindow()
            self.login_window.showMaximized()
            self.close()
    
    def refresh_data(self):
        """Refresh the dashboard data"""
        # Update stats
        total_requests = self.get_total_requests()
        pending_requests = self.get_pending_requests()
        approved_requests = self.get_approved_requests()
        rejected_requests = self.get_rejected_requests()
        
        # Refresh the current view
        self.show_leave_requests()
        
        # Show success message
        self.show_success_message("Refreshed", "Data has been refreshed successfully!")
    
    def show_leave_requests(self):
        """Display all leave requests assigned to this faculty"""
        self.clear_content()
        
        # Title
        title = QLabel("📋 Leave Requests for Review")
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 30px;
        """)
        title.setAlignment(Qt.AlignCenter)
        self.content_layout.addWidget(title)
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get leave requests with student information
            cursor.execute('''
                SELECT lr.student_id, s.Name, lr.from_date, lr.to_date, lr.reason, 
                       lr.description, lr.status, lr.created_at, s.Dept
                FROM leave_requests lr
                JOIN student s ON lr.student_id = s.Roll_no
                WHERE lr.tutor_id = ?
                ORDER BY 
                    CASE 
                        WHEN lr.status = 'Pending' THEN 1
                        WHEN lr.status = 'Approved' THEN 2
                        WHEN lr.status = 'Rejected' THEN 3
                        ELSE 4
                    END,
                    lr.created_at DESC
            ''', (self.faculty_info['tutor_id'],))
            
            requests = cursor.fetchall()
            conn.close()
            
            if not requests:
                # No requests found
                no_requests = QLabel("📭 No leave requests found")
                no_requests.setStyleSheet("""
                    font-size: 18px;
                    color: #64748b;
                    font-weight: 500;
                    padding: 40px;
                """)
                no_requests.setAlignment(Qt.AlignCenter)
                self.content_layout.addWidget(no_requests)
                return
            
            # Separate requests by status
            pending_requests = [req for req in requests if req[6] == 'Pending']
            processed_requests = [req for req in requests if req[6] != 'Pending']
            
            # Show pending requests first
            if pending_requests:
                pending_title = QLabel("⏳ Pending Requests (Require Action)")
                pending_title.setStyleSheet("""
                    font-size: 20px;
                    font-weight: 600;
                    color: #f59e0b;
                    margin: 20px 0 15px 0;
                    padding: 10px;
                    background-color: #fef3c7;
                    border-radius: 8px;
                    border: 1px solid #fcd34d;
                """)
                pending_title.setAlignment(Qt.AlignCenter)
                self.content_layout.addWidget(pending_title)
                
                for request in pending_requests:
                    request_card = self.create_request_card(request, actionable=True)
                    self.content_layout.addWidget(request_card)
            
            # Show processed requests
            if processed_requests:
                processed_title = QLabel("📋 Processed Requests")
                processed_title.setStyleSheet("""
                    font-size: 18px;
                    font-weight: 600;
                    color: #64748b;
                    margin: 30px 0 15px 0;
                    padding: 8px;
                    background-color: #f1f5f9;
                    border-radius: 6px;
                """)
                processed_title.setAlignment(Qt.AlignCenter)
                self.content_layout.addWidget(processed_title)
                
                for request in processed_requests:
                    request_card = self.create_request_card(request, actionable=False)
                    self.content_layout.addWidget(request_card)
                    
        except sqlite3.Error as e:
            self.show_error_message("Database Error", f"Failed to fetch leave requests: {str(e)}")
    
    def send_faculty_leave_request_email(self, faculty_name, faculty_id, admin_email, 
                                   start_date, end_date, leave_type, description):
        """Send email notification to admin about faculty leave request"""
        try:
            # Email configuration (same as student notification)
            SMTP_SERVER = "smtp.gmail.com"
            SMTP_PORT = 587
            SENDER_EMAIL = "leavemanagement13@gmail.com"
            SENDER_PASSWORD = "cvtu yils lqtc dyzf"  # Consider using environment variables in production
            
            print(f"Attempting to send email to admin: {admin_email}")

            # Validate email
            if not admin_email or "@" not in admin_email:
                print("Invalid admin email address")
                return False

            # Create email message
            msg = MIMEMultipart()
            msg['From'] = SENDER_EMAIL
            msg['To'] = admin_email
            msg['Subject'] = f"Faculty Leave Request from {faculty_name} ({faculty_id})"
            
            body = f"""
            <html>
                <body>
                    <p>Dear Admin,</p>
                    <p>You have a new faculty leave request:</p>
                    <ul>
                        <li><strong>Faculty:</strong> {faculty_name} ({faculty_id})</li>
                        <li><strong>Dates:</strong> {start_date} to {end_date}</li>
                        <li><strong>Type:</strong> {leave_type}</li>
                        <li><strong>Reason:</strong> {description if description else 'No reason provided'}</li>
                    </ul>
                    <p>Please review this in the Leave Management System.</p>
                    <p>Regards,<br>College Leave System</p>
                </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))

            # Send email
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
                server.starttls()
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                server.send_message(msg)
            
            print("Email to admin successfully sent!")
            return True
            
        except smtplib.SMTPAuthenticationError:
            print("Error: Authentication failed - check your email credentials")
            return False
        except smtplib.SMTPException as e:
            print(f"SMTP error occurred: {str(e)}")
            return False
        except Exception as e:
            print(f"Unexpected error sending email: {str(e)}")
            return False


    def open_new_leave_form(self):
        """Open form for faculty to request leave"""
        self.clear_content()
        
        # Title
        title = QLabel("📝 New Leave Request")
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 30px;
        """)
        title.setAlignment(Qt.AlignCenter)
        self.content_layout.addWidget(title)
        
        # Form card
        form_card = ModernCard()
        form_card.setMaximumWidth(600)
        
        form_layout = QVBoxLayout()
        form_layout.setContentsMargins(40, 40, 40, 40)
        form_layout.setSpacing(25)
        
        # Form fields
        fields_layout = QFormLayout()
        fields_layout.setSpacing(20)
        
        # Start date
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate())
        self.start_date.setCalendarPopup(True)
        self.start_date.setMinimumHeight(45)
        self.start_date.setStyleSheet("""
            QDateEdit {
                background-color: #f8fafc;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 14px;
                color: #1e293b;
            }
            QDateEdit:focus {
                border-color: #4f46e5;
                background-color: white;
            }
        """)
        
        # Number of days
        self.days_input = QSpinBox()
        self.days_input.setMinimum(1)
        self.days_input.setMaximum(365)
        self.days_input.setValue(1)
        self.days_input.setMinimumHeight(45)
        self.days_input.setStyleSheet("""
            QSpinBox {
                background-color: #f8fafc;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 14px;
                color: #1e293b;
            }
            QSpinBox:focus {
                border-color: #4f46e5;
                background-color: white;
            }
        """)
        
        # Leave type
        self.leave_type = QComboBox()
        self.leave_type.addItems(["🤒 Sick", "👤 Personal", "📋 Other"])
        self.leave_type.setMinimumHeight(45)
        self.leave_type.setStyleSheet("""
            QComboBox {
                background-color: #f8fafc;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 14px;
                color: #1e293b;
            }
            QComboBox:focus {
                border-color: #4f46e5;
                background-color: white;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border: none;
            }
        """)
        
        # Description
        self.description = QTextEdit()
        self.description.setMaximumHeight(100)
        self.description.setPlaceholderText("Brief description (optional)")
        self.description.setStyleSheet("""
            QTextEdit {
                background-color: #f8fafc;
                border: 2px solid #e2e8f0;
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 14px;
                color: #1e293b;
            }
            QTextEdit:focus {
                border-color: #4f46e5;
                background-color: white;
            }
        """)
        
        # Create stylized labels
        start_label = QLabel("📅 Start Date")
        days_label = QLabel("📊 Number of Days")
        type_label = QLabel("📋 Leave Type")
        desc_label = QLabel("📝 Description")
        
        for label in [start_label, days_label, type_label, desc_label]:
            label.setStyleSheet("""
                font-size: 14px;
                font-weight: 600;
                color: #374151;
                margin-bottom: 5px;
            """)
        
        fields_layout.addRow(start_label, self.start_date)
        fields_layout.addRow(days_label, self.days_input)
        fields_layout.addRow(type_label, self.leave_type)
        fields_layout.addRow(desc_label, self.description)
        
        # Submit button
        submit_btn = AnimatedButton("🚀 Submit Leave Request", primary=True)
        submit_btn.setMinimumHeight(50)
        submit_btn.clicked.connect(self.submit_leave_request)
        
        form_layout.addLayout(fields_layout)
        form_layout.addWidget(submit_btn)
        
        form_card.setLayout(form_layout)
        
        # Center the form
        center_layout = QHBoxLayout()
        center_layout.addStretch()
        center_layout.addWidget(form_card)
        center_layout.addStretch()
        
        self.content_layout.addLayout(center_layout)
    
    def submit_leave_request(self):
        """Submit faculty leave request to admin"""
        start_date = self.start_date.date().toPyDate()
        days = self.days_input.value()
        leave_type = self.leave_type.currentText().split(' ', 1)[1]  # Remove emoji
        description = self.description.toPlainText().strip()
        
        # Validate date
        if start_date < datetime.now().date():
            self.show_error_message("Error", "Start date cannot be in the past!")
            return
        
        # Calculate end date
        end_date = start_date + timedelta(days=days-1)
        
        # Show confirmation dialog
        self.show_confirmation_dialog(start_date, end_date, days, leave_type, description)

    def show_my_leave_requests(self):
        """Display faculty's own leave requests"""
        self.clear_content()
        
        # Title
        title = QLabel("📋 My Leave Requests")
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 30px;
        """)
        title.setAlignment(Qt.AlignCenter)
        self.content_layout.addWidget(title)
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT from_date, to_date, reason, description, status, created_at
                FROM faculty_leave_requests 
                WHERE faculty_id = ?
                ORDER BY created_at DESC
            ''', (self.faculty_info['tutor_id'],))
            
            requests = cursor.fetchall()
            conn.close()
            
            if not requests:
                no_requests = QLabel("📭 No leave requests found")
                no_requests.setStyleSheet("""
                    font-size: 18px;
                    color: #64748b;
                    font-weight: 500;
                    padding: 40px;
                """)
                no_requests.setAlignment(Qt.AlignCenter)
                self.content_layout.addWidget(no_requests)
                return
            
            # Display requests
            for request in requests:
                request_card = self.create_faculty_request_card(request)
                self.content_layout.addWidget(request_card)
                
        except sqlite3.Error as e:
            self.show_error_message("Database Error", f"Failed to fetch leave requests: {str(e)}")
    
    def create_faculty_request_card(self, request_data):
        """Create a card for each faculty leave request"""
        from_date, to_date, reason, description, status, created_at = request_data
        
        # Determine card color based on status
        if status == "Approved":
            border_color = "#10b981"
            bg_color = "#f0fdf4"
            status_color = "#10b981"
            status_icon = "✅"
        elif status == "Rejected":
            border_color = "#ef4444"
            bg_color = "#fef2f2"
            status_color = "#ef4444"
            status_icon = "❌"
        else:  # Pending
            border_color = "#f59e0b"
            bg_color = "#fefbf0"
            status_color = "#f59e0b"
            status_icon = "⏳"
        
        card = QFrame()
        card.setFrameStyle(QFrame.NoFrame)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border: 2px solid {border_color};
                border-radius: 12px;
                margin: 5px;
            }}
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(15)
        
        # Header with status
        header_layout = QHBoxLayout()
        
        # Request info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(5)
        
        title_text = f"📅 {from_date} to {to_date}"
        title_label = QLabel(title_text)
        title_label.setStyleSheet("""
            font-size: 16px;
            font-weight: 600;
            color: #1e293b;
        """)
        
        reason_text = f"📋 Reason: {reason}"
        reason_label = QLabel(reason_text)
        reason_label.setStyleSheet("""
            font-size: 14px;
            color: #64748b;
            font-weight: 500;
        """)
        
        info_layout.addWidget(title_label)
        info_layout.addWidget(reason_label)
        
        # Status badge
        status_label = QLabel(f"{status_icon} {status}")
        status_label.setStyleSheet(f"""
            font-size: 14px;
            font-weight: 600;
            color: {status_color};
            padding: 8px 16px;
            background-color: white;
            border-radius: 20px;
            border: 1px solid {border_color};
        """)
        status_label.setAlignment(Qt.AlignCenter)
        status_label.setFixedHeight(35)
        
        header_layout.addLayout(info_layout)
        header_layout.addStretch()
        header_layout.addWidget(status_label)
        
        # Description (if provided)
        if description:
            desc_label = QLabel(f"📝 Description: {description}")
            desc_label.setStyleSheet("""
                font-size: 13px;
                color: #6b7280;
                font-style: italic;
                padding: 10px;
                background-color: rgba(255, 255, 255, 0.7);
                border-radius: 6px;
            """)
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label)
        
        # Footer with submission date
        footer_label = QLabel(f"📅 Submitted: {created_at}")
        footer_label.setStyleSheet("""
            font-size: 12px;
            color: #9ca3af;
            font-weight: 400;
        """)
        
        # Status message
        if status == "Pending":
            message = "⏳ Waiting for confirmation from admin"
        elif status == "Approved":
            message = "✅ Your leave request has been approved"
        else:
            message = "❌ Your leave request has been rejected"
            
        message_label = QLabel(message)
        message_label.setStyleSheet(f"""
            font-size: 13px;
            color: {status_color};
            font-weight: 500;
            padding: 8px;
            text-align: center;
        """)
        message_label.setAlignment(Qt.AlignCenter)
        
        layout.addLayout(header_layout)
        layout.addWidget(message_label)
        layout.addWidget(footer_label)
        
        card.setLayout(layout)
        return card


    def show_confirmation_dialog(self, start_date, end_date, days, leave_type, description):
        """Show confirmation dialog with all details"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Confirm Leave Request")
        dialog.setFixedSize(500, 400)
        dialog.setStyleSheet("""
            QDialog {
                background-color: white;
                border-radius: 12px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # Title
        title = QLabel("📋 Confirm Your Leave Request")
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 10px;
        """)
        title.setAlignment(Qt.AlignCenter)
        
        # Details
        details_text = f"""
        <div style="background-color: #f8fafc; padding: 20px; border-radius: 8px; border: 1px solid #e2e8f0;">
            <p><strong>📅 Start Date:</strong> {start_date.strftime('%Y-%m-%d')}</p>
            <p><strong>📅 End Date:</strong> {end_date.strftime('%Y-%m-%d')}</p>
            <p><strong>📊 Number of Days:</strong> {days}</p>
            <p><strong>📋 Leave Type:</strong> {leave_type}</p>
            <p><strong>📝 Description:</strong> {description if description else 'Not provided'}</p>
        </div>
        """
        
        details_label = QLabel(details_text)
        details_label.setWordWrap(True)
        details_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #374151;
                line-height: 1.5;
            }
        """)
        
        # Warning message
        warning = QLabel("⚠️ Please review all details carefully before submitting.")
        warning.setStyleSheet("""
            font-size: 12px;
            color: #f59e0b;
            font-weight: 500;
            padding: 10px;
            background-color: #fef3c7;
            border-radius: 6px;
            border: 1px solid #fcd34d;
        """)
        warning.setAlignment(Qt.AlignCenter)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        cancel_btn = AnimatedButton("❌ Cancel", primary=False)
        cancel_btn.clicked.connect(dialog.reject)
        
        confirm_btn = AnimatedButton("✅ Confirm & Submit", primary=True)
        confirm_btn.clicked.connect(lambda: self.confirm_submission(dialog, start_date, end_date, days, leave_type, description))
        
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(confirm_btn)
        
        layout.addWidget(title)
        layout.addWidget(details_label)
        layout.addWidget(warning)
        layout.addLayout(button_layout)
        
        dialog.setLayout(layout)
        dialog.exec_()
        
    def confirm_submission(self, dialog, start_date, end_date, days, leave_type, description):
        """Submit the faculty leave request to database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Insert into faculty_leave_requests table
            cursor.execute('''
                INSERT INTO faculty_leave_requests (faculty_id, from_date, to_date, reason, description, status)
                VALUES (?, ?, ?, ?, ?, 'Pending')
            ''', (self.faculty_info['tutor_id'], start_date, end_date, leave_type, description))
            
            conn.commit()
            
            # Get admin email from database
            cursor.execute('''
                SELECT E_mail FROM Admin LIMIT 1
            ''')
            
            admin_email = cursor.fetchone()[0]
            conn.close()
            
            # Send email to admin
            email_sent = self.send_faculty_leave_request_email(
                faculty_name=self.faculty_info['name'],
                faculty_id=self.faculty_info['tutor_id'],
                admin_email=admin_email,
                start_date=start_date.strftime('%Y-%m-%d'),
                end_date=end_date.strftime('%Y-%m-%d'),
                leave_type=leave_type,
                description=description
            )
            
            if email_sent:
                dialog.accept()
                self.show_success_message("Success", 
                    "Leave request submitted successfully!\nAn email has been sent to admin.")
            else:
                dialog.accept()
                self.show_success_message("Success", 
                    "Leave request submitted successfully!\nBut failed to send email notification.")
            
            # Clear form
            self.start_date.setDate(QDate.currentDate())
            self.days_input.setValue(1)
            self.leave_type.setCurrentIndex(0)
            self.description.clear()
            
        except sqlite3.Error as e:
            self.show_error_message("Database Error", f"Failed to submit leave request: {str(e)}")

    def create_request_card(self, request_data, actionable=True):
        """Create a card for each leave request"""
        student_id, student_name, from_date, to_date, reason, description, status, created_at, dept = request_data
        
        # Determine card color based on status
        if status == "Approved":
            border_color = "#10b981"
            bg_color = "#f0fdf4"
            status_color = "#10b981"
            status_icon = "✅"
        elif status == "Rejected":
            border_color = "#ef4444"
            bg_color = "#fef2f2"
            status_color = "#ef4444"
            status_icon = "❌"
        else:  # Pending
            border_color = "#f59e0b"
            bg_color = "#fefbf0"
            status_color = "#f59e0b"
            status_icon = "⏳"
        
        card = QFrame()
        card.setFrameStyle(QFrame.NoFrame)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border: 2px solid {border_color};
                border-radius: 12px;
                margin: 5px;
            }}
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(15)
        
        # Header with student info and status
        header_layout = QHBoxLayout()
        
        # Student info
        student_info_layout = QVBoxLayout()
        student_info_layout.setSpacing(5)
        
        student_label = QLabel(f"👤 {student_name} ({student_id})")
        student_label.setStyleSheet("""
            font-size: 16px;
            font-weight: 600;
            color: #1e293b;
        """)
        
        dept_label = QLabel(f"🏛️ Department: {dept}")
        dept_label.setStyleSheet("""
            font-size: 14px;
            color: #64748b;
            font-weight: 500;
        """)
        
        student_info_layout.addWidget(student_label)
        student_info_layout.addWidget(dept_label)
        
        # Status badge
        status_label = QLabel(f"{status_icon} {status}")
        status_label.setStyleSheet(f"""
            font-size: 14px;
            font-weight: 600;
            color: {status_color};
            padding: 8px 16px;
            background-color: white;
            border-radius: 20px;
            border: 1px solid {border_color};
        """)
        status_label.setAlignment(Qt.AlignCenter)
        status_label.setFixedHeight(35)
        
        header_layout.addLayout(student_info_layout)
        header_layout.addStretch()
        header_layout.addWidget(status_label)
        
        # Leave details
        details_layout = QGridLayout()
        details_layout.setSpacing(10)
        
        # Calculate number of days
        from_date_obj = datetime.strptime(from_date, '%Y-%m-%d').date()
        to_date_obj = datetime.strptime(to_date, '%Y-%m-%d').date()
        num_days = (to_date_obj - from_date_obj).days + 1
        
        date_label = QLabel(f"📅 Duration: {from_date} to {to_date} ({num_days} day{'s' if num_days > 1 else ''})")
        reason_label = QLabel(f"📋 Reason: {reason}")
        submitted_label = QLabel(f"📅 Submitted: {created_at}")
        
        for label in [date_label, reason_label, submitted_label]:
            label.setStyleSheet("""
                font-size: 14px;
                color: #374151;
                font-weight: 500;
                padding: 5px;
            """)
        
        details_layout.addWidget(date_label, 0, 0)
        details_layout.addWidget(reason_label, 0, 1)
        details_layout.addWidget(submitted_label, 1, 0, 1, 2)
        
        layout.addLayout(header_layout)
        layout.addLayout(details_layout)
        
        # Description (if provided)
        if description and description.strip():
            desc_label = QLabel(f"📝 Description: {description}")
            desc_label.setStyleSheet("""
                font-size: 13px;
                color: #6b7280;
                font-style: italic;
                padding: 10px;
                background-color: rgba(255, 255, 255, 0.7);
                border-radius: 6px;
                margin: 5px 0;
            """)
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label)
        
        # Action buttons (only for pending requests)
        if actionable and status == "Pending":
            button_layout = QHBoxLayout()
            button_layout.setSpacing(15)
            
            reject_btn = AnimatedButton("❌ Reject", primary=False)
            reject_btn.setStyleSheet("""
                QPushButton {
                    background-color: #fef2f2;
                    color: #ef4444;
                    border: 2px solid #ef4444;
                    border-radius: 8px;
                    font-size: 14px;
                    font-weight: 600;
                    padding: 12px 24px;
                    min-height: 40px;
                }
                QPushButton:hover {
                    background-color: #ef4444;
                    color: white;
                }
                QPushButton:pressed {
                    background-color: #dc2626;
                }
            """)
            reject_btn.clicked.connect(lambda: self.update_request_status(student_id, from_date, "Rejected"))
            
            approve_btn = AnimatedButton("✅ Approve", primary=True)
            approve_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #10b981, stop:1 #059669);
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-size: 14px;
                    font-weight: 600;
                    padding: 12px 24px;
                    min-height: 40px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #059669, stop:1 #047857);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #047857, stop:1 #065f46);
                }
            """)
            approve_btn.clicked.connect(lambda: self.update_request_status(student_id, from_date, "Approved"))
            
            button_layout.addWidget(reject_btn)
            button_layout.addWidget(approve_btn)
            
            layout.addLayout(button_layout)
        
        # Status message for processed requests
        elif not actionable:
            if status == "Approved":
                message = "✅ This leave request has been approved"
                color = "#10b981"
            else:
                message = "❌ This leave request has been rejected"
                color = "#ef4444"
                
            message_label = QLabel(message)
            message_label.setStyleSheet(f"""
                font-size: 13px;
                color: {color};
                font-weight: 500;
                padding: 8px;
                text-align: center;
            """)
            message_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(message_label)
        
        card.setLayout(layout)
        return card
    
    def update_request_status(self, student_id, from_date, new_status):
         
        """Update the status of a leave request"""
        # Show confirmation dialog
        action = "approve" if new_status == "Approved" else "reject"
        reply = QMessageBox.question(
            self, 
            f'Confirm {action.title()}', 
            f'Are you sure you want to {action} this leave request?',
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )
        
        if reply != QMessageBox.Yes:
            return
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get student email and details before updating
            cursor.execute('''
                SELECT s.E_mail, s.Name, lr.from_date, lr.to_date, lr.reason
                FROM leave_requests lr
                JOIN student s ON lr.student_id = s.Roll_no
                WHERE lr.student_id = ? AND lr.from_date = ? AND lr.tutor_id = ?
            ''', (student_id, from_date, self.faculty_info['tutor_id']))
            
            student_data = cursor.fetchone()
            
            if not student_data:
                self.show_error_message("Error", "Leave request not found!")
                conn.close()
                return
                
            student_email = student_data[0]
            student_name = student_data[1]
            start_date = student_data[2]
            end_date = student_data[3]
            reason = student_data[4]
            
            # Update the request status
            cursor.execute('''
                UPDATE leave_requests 
                SET status = ? 
                WHERE student_id = ? AND from_date = ? AND tutor_id = ?
            ''', (new_status, student_id, from_date, self.faculty_info['tutor_id']))
            
            conn.commit()
            conn.close()
            
            # Send email to student
            email_sent = self.send_student_leave_response_email(
                student_email=student_email,
                student_name=student_name,
                faculty_name=self.faculty_info['name'],
                start_date=start_date,
                end_date=end_date,
                reason=reason,
                status=new_status
            )
            
            if email_sent:
                self.show_success_message(
                    "Success", 
                    f"Leave request has been {new_status.lower()} successfully!\nNotification sent to student."
                )
            else:
                self.show_success_message(
                    "Success", 
                    f"Leave request has been {new_status.lower()} successfully!\nBut failed to send email notification."
                )
            
            # Refresh the view
            self.show_leave_requests()
            
        except sqlite3.Error as e:
            self.show_error_message("Database Error", f"Failed to update request status: {str(e)}")
    def send_student_leave_response_email(self, student_email, student_name, faculty_name, 
                                start_date, end_date, reason, status):
        """Send email notification to student about their leave request response"""
        try:
            # Email configuration
            SMTP_SERVER = "smtp.gmail.com"
            SMTP_PORT = 587
            SENDER_EMAIL = "leavemanagement13@gmail.com"
            SENDER_PASSWORD = "cvtu yils lqtc dyzf"
            
            print(f"Attempting to send response email to student: {student_email}")

            # Validate email
            if not student_email or "@" not in student_email:
                print("Invalid student email address")
                return False

            # Create email message
            msg = MIMEMultipart()
            msg['From'] = SENDER_EMAIL
            msg['To'] = student_email
            msg['Subject'] = f"Your Leave Request has been {status}"
            
            body = f"""
            <html>
                <body>
                    <p>Dear {student_name},</p>
                    <p>Your leave request has been processed by your faculty tutor:</p>
                    <ul>
                        <li><strong>Dates:</strong> {start_date} to {end_date}</li>
                        <li><strong>Reason:</strong> {reason}</li>
                        <li><strong>Status:</strong> {status}</li>
                    </ul>
                    <p>Processed by: Prof. {faculty_name}</p>
                    <p>Regards,<br>College Leave System</p>
                </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))

            # Send email
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
                server.starttls()
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                server.send_message(msg)
            
            print("Response email to student successfully sent!")
            return True
            
        except smtplib.SMTPAuthenticationError:
            print("Error: Authentication failed - check your email credentials")
            return False
        except smtplib.SMTPException as e:
            print(f"SMTP error occurred: {str(e)}")
            return False
        except Exception as e:
            print(f"Unexpected error sending email: {str(e)}")
            return False
        

    def show_error_message(self, title, message):
        """Show error message dialog"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
                color: #1e293b;
            }
            QMessageBox QPushButton {
                background-color: #ef4444;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: 500;
            }
            QMessageBox QPushButton:hover {
                background-color: #dc2626;
            }
        """)
        msg.exec_()
    
    def show_success_message(self, title, message):
        """Show success message dialog"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
                color: #1e293b;
            }
            QMessageBox QPushButton {
                background-color: #10b981;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: 500;
            }
            QMessageBox QPushButton:hover {
                background-color: #059669;
            }
        """)
        msg.exec_()

class AdminDashboard(QWidget):
    def __init__(self, admin_info, db_path):
        super().__init__()
        self.admin_info = admin_info
        self.db_path = db_path
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Admin Dashboard - College Leave Management System")
        self.resize(1200, 800)
        
        # Center the window
        screen = QApplication.desktop().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)
        
        # Set background
        self.setStyleSheet("""
            QWidget {
                background-color: #f8fafc;
            }
        """)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(30)
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Stats cards
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)
        
        # Quick stats
        total_faculty = self.get_total_faculty()
        total_students = self.get_total_students()
        total_requests = self.get_total_requests()
        
        stats_layout.addWidget(self.create_stat_card("Total Faculty", str(total_faculty), "#3b82f6", "👨‍🏫"))
        stats_layout.addWidget(self.create_stat_card("Total Students", str(total_students), "#7c3aed", "🎓"))
        stats_layout.addWidget(self.create_stat_card("Total Requests", str(total_requests), "#10b981", "📋"))
        
        main_layout.addLayout(stats_layout)
        
        # Action buttons
        action_layout = QHBoxLayout()
        action_layout.setSpacing(20)
        
        view_faculty_btn = AnimatedButton("👨‍🏫 View Faculty", primary=True)
        view_faculty_btn.setMinimumHeight(60)
        view_faculty_btn.clicked.connect(self.show_faculty_details)
        
        view_students_btn = AnimatedButton("🎓 View Students", primary=False)
        view_students_btn.setMinimumHeight(60)
        view_students_btn.clicked.connect(self.show_student_details)
        
        faculty_requests_btn = AnimatedButton("📋 Faculty Leave Requests", primary=False)
        faculty_requests_btn.setMinimumHeight(60)
        faculty_requests_btn.clicked.connect(self.show_faculty_leave_requests)
        
        action_layout.addWidget(view_faculty_btn)
        action_layout.addWidget(view_students_btn)
        action_layout.addWidget(faculty_requests_btn)
        
        main_layout.addLayout(action_layout)
        
        # Content area
        self.content_area = QWidget()
        self.content_layout = QVBoxLayout()
        self.content_area.setLayout(self.content_layout)
        
        # Scroll area
        scroll = QScrollArea()
        scroll.setWidget(self.content_area)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: #f1f5f9;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #cbd5e1;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #94a3b8;
            }
        """)
        
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)
        
    def create_header(self):
        header = ModernCard()
        header.setMinimumHeight(120)
        
        layout = QHBoxLayout()
        layout.setContentsMargins(30, 20, 30, 20)
        
        # Admin info
        info_layout = QVBoxLayout()
        info_layout.setSpacing(5)
        
        welcome_label = QLabel(f"Welcome, Admin {self.admin_info['name']}! 👑")
        welcome_label.setStyleSheet("""
            font-size: 24px;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 5px;
        """)
        
        details_layout = QHBoxLayout()
        details_layout.setSpacing(30)
        
        id_label = QLabel(f"🆔 Admin ID: {self.admin_info['admin_id']}")
        email_label = QLabel(f"📧 Email: {self.admin_info['email']}")
        
        for label in [id_label, email_label]:
            label.setStyleSheet("""
                font-size: 14px;
                font-weight: 500;
                color: #64748b;
            """)
            details_layout.addWidget(label)
        
        info_layout.addWidget(welcome_label)
        info_layout.addLayout(details_layout)
        
        # Logout button
        logout_btn = AnimatedButton("Logout", primary=False)
        logout_btn.setFixedSize(100, 40)
        logout_btn.clicked.connect(self.logout)
        
        layout.addLayout(info_layout)
        layout.addStretch()
        layout.addWidget(logout_btn)
        
        header.setLayout(layout)
        return header
    
    def create_stat_card(self, title, value, color, icon):
        card = ModernCard()
        card.setFixedHeight(120)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(10)
        
        # Icon and value
        top_layout = QHBoxLayout()
        
        icon_label = QLabel(icon)
        icon_label.setStyleSheet(f"""
            font-size: 32px;
            color: {color};
        """)
        
        value_label = QLabel(value)
        value_label.setAlignment(Qt.AlignRight)
        value_label.setStyleSheet(f"""
            font-size: 32px;
            font-weight: 700;
            color: {color};
        """)
        
        top_layout.addWidget(icon_label)
        top_layout.addStretch()
        top_layout.addWidget(value_label)
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-size: 14px;
            font-weight: 600;
            color: #64748b;
        """)
        
        layout.addLayout(top_layout)
        layout.addWidget(title_label)
        
        card.setLayout(layout)
        return card
    
    def get_total_faculty(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM Faculty')
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except:
            return 0
    
    def get_total_students(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM student')
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except:
            return 0
    
    def get_total_requests(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM leave_requests')
            count = cursor.fetchone()[0]
            conn.close()
            return count
        except:
            return 0
    
    def clear_content(self):
        """Clear the content area"""
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    
    def logout(self):
        reply = QMessageBox.question(self, 'Logout', 'Are you sure you want to logout?',
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.login_window = LoginWindow()
            self.login_window.showMaximized()
            self.close()
    
    def show_faculty_details(self):
        """Display all faculty details"""
        self.clear_content()
        
        # Title
        title = QLabel("👨‍🏫 Faculty Details")
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 30px;
        """)
        title.setAlignment(Qt.AlignCenter)
        self.content_layout.addWidget(title)
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT Tutor_id, Name, Dept, E_mail
                FROM Faculty
                ORDER BY Dept, Name
            ''')
            
            faculty_list = cursor.fetchall()
            conn.close()
            
            if not faculty_list:
                no_faculty = QLabel("👨‍🏫 No faculty found")
                no_faculty.setStyleSheet("""
                    font-size: 18px;
                    color: #64748b;
                    font-weight: 500;
                    padding: 40px;
                """)
                no_faculty.setAlignment(Qt.AlignCenter)
                self.content_layout.addWidget(no_faculty)
                return
            
            # Group by department
            dept_groups = {}
            for faculty in faculty_list:
                dept = faculty[2]
                if dept not in dept_groups:
                    dept_groups[dept] = []
                dept_groups[dept].append(faculty)
            
            # Create cards for each department
            for dept, faculty_members in dept_groups.items():
                # Department header
                dept_label = QLabel(f"🏛️ {dept} Department")
                dept_label.setStyleSheet("""
                    font-size: 20px;
                    font-weight: 600;
                    color: #3b82f6;
                    margin: 20px 0 10px 0;
                    padding: 8px;
                """)
                self.content_layout.addWidget(dept_label)
                
                # Faculty cards
                for faculty in faculty_members:
                    faculty_card = self.create_faculty_card(faculty)
                    self.content_layout.addWidget(faculty_card)
                    
        except sqlite3.Error as e:
            self.show_error_message("Database Error", f"Failed to fetch faculty details: {str(e)}")
    def show_faculty_leave_requests(self):
        """Display all faculty leave requests for admin review"""
        self.clear_content()
        
        # Title
        title = QLabel("📋 Faculty Leave Requests")
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 30px;
        """)
        title.setAlignment(Qt.AlignCenter)
        self.content_layout.addWidget(title)
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get leave requests with faculty information
            cursor.execute('''
                SELECT flr.faculty_id, f.Name, f.Dept, flr.from_date, flr.to_date, 
                       flr.reason, flr.description, flr.status, flr.created_at
                FROM faculty_leave_requests flr
                JOIN Faculty f ON flr.faculty_id = f.Tutor_id
                ORDER BY 
                    CASE 
                        WHEN flr.status = 'Pending' THEN 1
                        WHEN flr.status = 'Approved' THEN 2
                        WHEN flr.status = 'Rejected' THEN 3
                        ELSE 4
                    END,
                    flr.created_at DESC
            ''')
            
            requests = cursor.fetchall()
            conn.close()
            
            if not requests:
                no_requests = QLabel("📭 No faculty leave requests found")
                no_requests.setStyleSheet("""
                    font-size: 18px;
                    color: #64748b;
                    font-weight: 500;
                    padding: 40px;
                """)
                no_requests.setAlignment(Qt.AlignCenter)
                self.content_layout.addWidget(no_requests)
                return
            
            # Separate requests by status
            pending_requests = [req for req in requests if req[7] == 'Pending']
            processed_requests = [req for req in requests if req[7] != 'Pending']
            
            # Show pending requests first
            if pending_requests:
                pending_title = QLabel("⏳ Pending Requests (Require Action)")
                pending_title.setStyleSheet("""
                    font-size: 20px;
                    font-weight: 600;
                    color: #f59e0b;
                    margin: 20px 0 15px 0;
                    padding: 10px;
                    background-color: #fef3c7;
                    border-radius: 8px;
                    border: 1px solid #fcd34d;
                """)
                pending_title.setAlignment(Qt.AlignCenter)
                self.content_layout.addWidget(pending_title)
                
                for request in pending_requests:
                    request_card = self.create_faculty_request_card(request, actionable=True)
                    self.content_layout.addWidget(request_card)
            
            # Show processed requests
            if processed_requests:
                processed_title = QLabel("📋 Processed Requests")
                processed_title.setStyleSheet("""
                    font-size: 18px;
                    font-weight: 600;
                    color: #64748b;
                    margin: 30px 0 15px 0;
                    padding: 8px;
                    background-color: #f1f5f9;
                    border-radius: 6px;
                """)
                processed_title.setAlignment(Qt.AlignCenter)
                self.content_layout.addWidget(processed_title)
                
                for request in processed_requests:
                    request_card = self.create_faculty_request_card(request, actionable=False)
                    self.content_layout.addWidget(request_card)
                    
        except sqlite3.Error as e:
            self.show_error_message("Database Error", f"Failed to fetch faculty leave requests: {str(e)}")
    


    def show_error_message(self, title, message):
            """Show error message dialog"""
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle(title)
            msg.setText(message)
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: white;
                    color: #1e293b;
                }
                QMessageBox QPushButton {
                    background-color: #ef4444;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-weight: 500;
                }
                QMessageBox QPushButton:hover {
                    background-color: #dc2626;
                }
            """)
            msg.exec_()
    
    def show_success_message(self, title, message):
        """Show success message dialog"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
                color: #1e293b;
            }
            QMessageBox QPushButton {
                background-color: #10b981;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: 500;
            }
            QMessageBox QPushButton:hover {
                background-color: #059669;
            }
        """)
        msg.exec_()

    def create_faculty_request_card(self, request_data, actionable=True):
        """Create a card for each faculty leave request"""
        faculty_id, faculty_name, dept, from_date, to_date, reason, description, status, created_at = request_data
        
        # Determine card color based on status
        if status == "Approved":
            border_color = "#10b981"
            bg_color = "#f0fdf4"
            status_color = "#10b981"
            status_icon = "✅"
        elif status == "Rejected":
            border_color = "#ef4444"
            bg_color = "#fef2f2"
            status_color = "#ef4444"
            status_icon = "❌"
        else:  # Pending
            border_color = "#f59e0b"
            bg_color = "#fefbf0"
            status_color = "#f59e0b"
            status_icon = "⏳"
        
        card = QFrame()
        card.setFrameStyle(QFrame.NoFrame)
        card.setStyleSheet(f"""
            QFrame {{
                background-color: {bg_color};
                border: 2px solid {border_color};
                border-radius: 12px;
                margin: 5px;
            }}
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(25, 20, 25, 20)
        layout.setSpacing(15)
        
        # Header with faculty info and status
        header_layout = QHBoxLayout()
        
        # Faculty info
        faculty_info_layout = QVBoxLayout()
        faculty_info_layout.setSpacing(5)
        
        faculty_label = QLabel(f"👨‍🏫 {faculty_name} ({faculty_id})")
        faculty_label.setStyleSheet("""
            font-size: 16px;
            font-weight: 600;
            color: #1e293b;
        """)
        
        dept_label = QLabel(f"🏛️ Department: {dept}")
        dept_label.setStyleSheet("""
            font-size: 14px;
            color: #64748b;
            font-weight: 500;
        """)
        
        faculty_info_layout.addWidget(faculty_label)
        faculty_info_layout.addWidget(dept_label)
        
        # Status badge
        status_label = QLabel(f"{status_icon} {status}")
        status_label.setStyleSheet(f"""
            font-size: 14px;
            font-weight: 600;
            color: {status_color};
            padding: 8px 16px;
            background-color: white;
            border-radius: 20px;
            border: 1px solid {border_color};
        """)
        status_label.setAlignment(Qt.AlignCenter)
        status_label.setFixedHeight(35)
        
        header_layout.addLayout(faculty_info_layout)
        header_layout.addStretch()
        header_layout.addWidget(status_label)
        
        # Leave details
        details_layout = QGridLayout()
        details_layout.setSpacing(10)
        
        # Calculate number of days
        from_date_obj = datetime.strptime(from_date, '%Y-%m-%d').date()
        to_date_obj = datetime.strptime(to_date, '%Y-%m-%d').date()
        num_days = (to_date_obj - from_date_obj).days + 1
        
        date_label = QLabel(f"📅 Duration: {from_date} to {to_date} ({num_days} day{'s' if num_days > 1 else ''})")
        reason_label = QLabel(f"📋 Reason: {reason}")
        submitted_label = QLabel(f"📅 Submitted: {created_at}")
        
        for label in [date_label, reason_label, submitted_label]:
            label.setStyleSheet("""
                font-size: 14px;
                color: #374151;
                font-weight: 500;
                padding: 5px;
            """)
        
        details_layout.addWidget(date_label, 0, 0)
        details_layout.addWidget(reason_label, 0, 1)
        details_layout.addWidget(submitted_label, 1, 0, 1, 2)
        
        layout.addLayout(header_layout)
        layout.addLayout(details_layout)
        
        # Description (if provided)
        if description and description.strip():
            desc_label = QLabel(f"📝 Description: {description}")
            desc_label.setStyleSheet("""
                font-size: 13px;
                color: #6b7280;
                font-style: italic;
                padding: 10px;
                background-color: rgba(255, 255, 255, 0.7);
                border-radius: 6px;
                margin: 5px 0;
            """)
            desc_label.setWordWrap(True)
            layout.addWidget(desc_label)
        
        # Action buttons (only for pending requests)
        if actionable and status == "Pending":
            button_layout = QHBoxLayout()
            button_layout.setSpacing(15)
            
            reject_btn = AnimatedButton("❌ Reject", primary=False)
            reject_btn.setStyleSheet("""
                QPushButton {
                    background-color: #fef2f2;
                    color: #ef4444;
                    border: 2px solid #ef4444;
                    border-radius: 8px;
                    font-size: 14px;
                    font-weight: 600;
                    padding: 12px 24px;
                    min-height: 40px;
                }
                QPushButton:hover {
                    background-color: #ef4444;
                    color: white;
                }
                QPushButton:pressed {
                    background-color: #dc2626;
                }
            """)
            reject_btn.clicked.connect(lambda: self.update_faculty_request_status(faculty_id, from_date, "Rejected"))
            
            approve_btn = AnimatedButton("✅ Approve", primary=True)
            approve_btn.setStyleSheet("""
                QPushButton {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #10b981, stop:1 #059669);
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-size: 14px;
                    font-weight: 600;
                    padding: 12px 24px;
                    min-height: 40px;
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #059669, stop:1 #047857);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #047857, stop:1 #065f46);
                }
            """)
            approve_btn.clicked.connect(lambda: self.update_faculty_request_status(faculty_id, from_date, "Approved"))
            
            button_layout.addWidget(reject_btn)
            button_layout.addWidget(approve_btn)
            
            layout.addLayout(button_layout)
        
        # Status message for processed requests
        elif not actionable:
            if status == "Approved":
                message = "✅ This leave request has been approved"
                color = "#10b981"
            else:
                message = "❌ This leave request has been rejected"
                color = "#ef4444"
                
            message_label = QLabel(message)
            message_label.setStyleSheet(f"""
                font-size: 13px;
                color: {color};
                font-weight: 500;
                padding: 8px;
                text-align: center;
            """)
            message_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(message_label)
        
        card.setLayout(layout)
        return card
    
    def update_faculty_request_status(self, faculty_id, from_date, new_status):
        """Update the status of a faculty leave request"""
        # Show confirmation dialog
        action = "approve" if new_status == "Approved" else "reject"
        reply = QMessageBox.question(
            self, 
            f'Confirm {action.title()}', 
            f'Are you sure you want to {action} this leave request?',
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No
        )
        
        if reply != QMessageBox.Yes:
            return
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get faculty email and name before updating
            cursor.execute('''
                SELECT f.E_mail, f.Name, flr.from_date, flr.to_date 
                FROM faculty_leave_requests flr
                JOIN Faculty f ON flr.faculty_id = f.Tutor_id
                WHERE faculty_id = ? AND from_date = ?
            ''', (faculty_id, from_date))
            
            faculty_data = cursor.fetchone()
            faculty_email = faculty_data[0]
            faculty_name = faculty_data[1]
            start_date = faculty_data[2]
            end_date = faculty_data[3]
            
            # Update the request status
            cursor.execute('''
                UPDATE faculty_leave_requests 
                SET status = ? 
                WHERE faculty_id = ? AND from_date = ?
            ''', (new_status, faculty_id, from_date))
            
            conn.commit()
            conn.close()
            
            # Send email to faculty
            email_sent = self.send_faculty_leave_response_email(
                faculty_email=faculty_email,
                faculty_name=faculty_name,
                admin_name=self.admin_info['name'],
                start_date=start_date,
                end_date=end_date,
                status=new_status
            )
            
            if email_sent:
                self.show_success_message(
                    "Success", 
                    f"Faculty leave request has been {new_status.lower()} successfully!\nNotification sent to faculty."
                )
            else:
                self.show_success_message(
                    "Success", 
                    f"Faculty leave request has been {new_status.lower()} successfully!\nBut failed to send email notification."
                )
            
            # Refresh the view
            self.show_faculty_leave_requests()
            
        except sqlite3.Error as e:
            self.show_error_message("Database Error", f"Failed to update request status: {str(e)}")
    
    def create_faculty_card(self, faculty_data):
        """Create a card for each faculty member"""
        tutor_id, name, dept, email = faculty_data
        
        card = ModernCard()
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 15, 20, 15)
        layout.setSpacing(10)
        
        # Name and ID
        name_label = QLabel(f"👨‍🏫 {name}")
        name_label.setStyleSheet("""
            font-size: 18px;
            font-weight: 600;
            color: #1e293b;
        """)
        
        id_label = QLabel(f"🆔 ID: {tutor_id}")
        id_label.setStyleSheet("""
            font-size: 14px;
            color: #64748b;
        """)
        
        # Department and Email
        dept_label = QLabel(f"🏛️ Department: {dept}")
        email_label = QLabel(f"📧 Email: {email}")
        
        for label in [dept_label, email_label]:
            label.setStyleSheet("""
                font-size: 14px;
                color: #64748b;
            """)
        
        layout.addWidget(name_label)
        layout.addWidget(id_label)
        layout.addWidget(dept_label)
        layout.addWidget(email_label)
        
        card.setLayout(layout)
        return card
    def send_faculty_leave_response_email(self, faculty_email, faculty_name, admin_name, 
                                    start_date, end_date, status, reason=""):
        """Send email notification to faculty about their leave request response"""
        try:
            # Email configuration
            SMTP_SERVER = "smtp.gmail.com"
            SMTP_PORT = 587
            SENDER_EMAIL = "leavemanagement13@gmail.com"
            SENDER_PASSWORD = "cvtu yils lqtc dyzf"
            
            print(f"Attempting to send response email to faculty: {faculty_email}")

            # Validate email
            if not faculty_email or "@" not in faculty_email:
                print("Invalid faculty email address")
                return False

            # Create email message
            msg = MIMEMultipart()
            msg['From'] = SENDER_EMAIL
            msg['To'] = faculty_email
            msg['Subject'] = f"Your Leave Request has been {status}"
            
            body = f"""
            <html>
                <body>
                    <p>Dear Prof. {faculty_name},</p>
                    <p>Your leave request has been processed by the admin:</p>
                    <ul>
                        <li><strong>Dates:</strong> {start_date} to {end_date}</li>
                        <li><strong>Status:</strong> {status}</li>
                        {f"<li><strong>Admin Note:</strong> {reason}</li>" if reason else ""}
                    </ul>
                    <p>Processed by: {admin_name}</p>
                    <p>Regards,<br>College Leave System</p>
                </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))

            # Send email
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as server:
                server.starttls()
                server.login(SENDER_EMAIL, SENDER_PASSWORD)
                server.send_message(msg)
            
            print("Response email to faculty successfully sent!")
            return True
            
        except smtplib.SMTPAuthenticationError:
            print("Error: Authentication failed - check your email credentials")
            return False
        except smtplib.SMTPException as e:
            print(f"SMTP error occurred: {str(e)}")
            return False
        except Exception as e:
            print(f"Unexpected error sending email: {str(e)}")
            return False
        
    def show_student_details(self):
        """Display all student details grouped by department"""
        self.clear_content()
        
        # Title
        title = QLabel("🎓 Student Details")
        title.setStyleSheet("""
            font-size: 28px;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 30px;
        """)
        title.setAlignment(Qt.AlignCenter)
        self.content_layout.addWidget(title)
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT s.Roll_no, s.Name, s.Dept, s.Tutor_id, f.Name
                FROM student s
                JOIN Faculty f ON s.Tutor_id = f.Tutor_id
                ORDER BY s.Dept, s.Name
            ''')
            
            students = cursor.fetchall()
            conn.close()
            
            if not students:
                no_students = QLabel("🎓 No students found")
                no_students.setStyleSheet("""
                    font-size: 18px;
                    color: #64748b;
                    font-weight: 500;
                    padding: 40px;
                """)
                no_students.setAlignment(Qt.AlignCenter)
                self.content_layout.addWidget(no_students)
                return
            
            # Group by department
            dept_groups = {}
            for student in students:
                dept = student[2]
                if dept not in dept_groups:
                    dept_groups[dept] = []
                dept_groups[dept].append(student)
            
            # Create cards for each department
            for dept, student_list in dept_groups.items():
                # Department header
                dept_label = QLabel(f"🏛️ {dept} Department")
                dept_label.setStyleSheet("""
                    font-size: 20px;
                    font-weight: 600;
                    color: #3b82f6;
                    margin: 20px 0 10px 0;
                    padding: 8px;
                """)
                self.content_layout.addWidget(dept_label)
                
                # Create a table for students
                table = QTableWidget()
                table.setColumnCount(4)
                table.setHorizontalHeaderLabels(["Roll No", "Name", "Tutor ID", "Tutor Name"])
                table.setRowCount(len(student_list))
                
                # Style the table
                table.setStyleSheet("""
                    QTableWidget {
                        background-color: white;
                        border: 1px solid #e2e8f0;
                        border-radius: 8px;
                    }
                    QHeaderView::section {
                        background-color: #f1f5f9;
                        padding: 8px;
                        border: none;
                        font-weight: 600;
                    }
                    QTableWidget::item {
                        padding: 8px;
                        border-bottom: 1px solid #e2e8f0;
                    }
                """)
                
                # Fill the table
                for row, student in enumerate(student_list):
                    for col in range(4):
                        item = QTableWidgetItem(str(student[col]))
                        table.setItem(row, col, item)
                
                # Resize columns to content
                table.resizeColumnsToContents()
                
                self.content_layout.addWidget(table)
                
        except sqlite3.Error as e:
            self.show_error_message("Database Error", f"Failed to fetch student details: {str(e)}")
    
    def show_error_message(self, title, message):
        """Show error message dialog"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
                color: #1e293b;
            }
            QMessageBox QPushButton {
                background-color: #ef4444;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: 500;
            }
            QMessageBox QPushButton:hover {
                background-color: #dc2626;
            }
        """)
        msg.exec_()


class LeaveManagementApp(QApplication):
    def __init__(self, sys_argv):
        super().__init__(sys_argv)
        
        # Show splash screen
        self.splash = SplashScreen()
        self.splash.showMaximized()
        
        # Timer to show login window after 1 second
        QTimer.singleShot(3000, self.show_login)
        
    def show_login(self):
        self.splash.close()
        self.login_window = LoginWindow()
        self.login_window.showMaximized()

def main():
    app = LeaveManagementApp(sys.argv)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()


