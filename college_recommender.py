import sys
import logging
from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt
from database_operations import DatabaseManager, College


class ModernButton(QtWidgets.QPushButton):
    def __init__(self, text, primary=True):
        super().__init__(text)
        self.setFixedHeight(40)
        self.setCursor(QtGui.QCursor(Qt.CursorShape.PointingHandCursor))

        # Modern styling
        if primary:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #2563eb;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 8px 16px;
                    font-weight: bold;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #1d4ed8;
                }
                QPushButton:pressed {
                    background-color: #1e40af;
                }
            """)
        else:
            self.setStyleSheet("""
                QPushButton {
                    background-color: #f3f4f6;
                    color: #4b5563;
                    border: 1px solid #d1d5db;
                    border-radius: 8px;
                    padding: 8px 16px;
                    font-weight: bold;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #e5e7eb;
                }
                QPushButton:pressed {
                    background-color: #d1d5db;
                }
            """)


class ModernComboBox(QtWidgets.QComboBox):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(40)
        self.setStyleSheet("""
            QComboBox {
                border: 1px solid #d1d5db;
                border-radius: 8px;
                padding: 8px 16px;
                background-color: white;
                font-size: 14px;
            }
            QComboBox:hover {
                border-color: #2563eb;
            }
            QComboBox:drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border: none;
            }
        """)


class ModernLineEdit(QtWidgets.QLineEdit):
    def __init__(self, placeholder=""):
        super().__init__()
        self.setFixedHeight(40)
        self.setPlaceholderText(placeholder)
        self.setStyleSheet("""
            QLineEdit {
                border: 1px solid #d1d5db;
                border-radius: 8px;
                padding: 8px 16px;
                background-color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #2563eb;
                outline: none;
            }
            QLineEdit::placeholder {
                color: #9ca3af;
            }
        """)


class CollegeRecommenderApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.font_family = QtWidgets.QApplication.instance().font().family()
        self.db_manager = DatabaseManager('career_counseling.db')
        self.setWindowTitle("College Recommender System")
        self.setGeometry(100, 100, 1200, 900)  # Increased window size
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8fafc;
            }
            QLabel {
                color: #1e293b;
            }
        """)

        # Main container widget with margins
        main_widget = QtWidgets.QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QtWidgets.QVBoxLayout(main_widget)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)

        # Header
        header_container = QtWidgets.QWidget()
        header_container.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 16px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            }
        """)
        header_layout = QtWidgets.QVBoxLayout(header_container)
        header_layout.setContentsMargins(30, 30, 30, 30)

        header_label = QtWidgets.QLabel("College Recommender System")
        header_label.setFont(QtGui.QFont(self.font_family, 32, QtGui.QFont.Weight.Bold))
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_label.setStyleSheet("color: #0f172a;")
        header_layout.addWidget(header_label)

        subtitle_label = QtWidgets.QLabel("Find the best colleges based on your exam scores")
        subtitle_label.setFont(QtGui.QFont(self.font_family, 16))
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet("color: #64748b;")
        header_layout.addWidget(subtitle_label)

        main_layout.addWidget(header_container)

        # Form container
        form_container = QtWidgets.QWidget()
        form_container.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 16px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            }
        """)
        form_layout = QtWidgets.QVBoxLayout(form_container)
        form_layout.setContentsMargins(30, 30, 30, 30)
        form_layout.setSpacing(20)

        # Form grid
        grid_layout = QtWidgets.QGridLayout()
        grid_layout.setSpacing(20)

        # Add form elements with labels
        labels = ["Select Exam:", "Your Score:", "Category:", "Field:", "Max Budget (₹):"]
        self.exam_combo = ModernComboBox()
        self.exam_combo.addItems(self.db_manager.get_exam_types())
        self.score_input = ModernLineEdit("Enter your score")
        self.category_combo = ModernComboBox()
        self.category_combo.addItems(["General", "OBC", "SC", "ST"])
        self.field_combo = ModernComboBox()
        self.field_combo.addItems(["Engineering", "Medicine", "Architecture"])
        self.budget_input = ModernLineEdit("Enter maximum budget")

        widgets = [self.exam_combo, self.score_input, self.category_combo,
                   self.field_combo, self.budget_input]

        for i, (label, widget) in enumerate(zip(labels, widgets)):
            label_widget = QtWidgets.QLabel(label)
            label_widget.setFont(QtGui.QFont(self.font_family, 12))
            label_widget.setStyleSheet("color: #475569;")
            grid_layout.addWidget(label_widget, i, 0)
            grid_layout.addWidget(widget, i, 1)

        form_layout.addLayout(grid_layout)

        # Buttons layout
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(15)

        self.search_button = ModernButton("Find Colleges", primary=True)
        self.search_button.clicked.connect(self.search_colleges)

        self.clear_button = ModernButton("Clear Form", primary=False)
        self.clear_button.clicked.connect(self.clear_form)

        button_layout.addWidget(self.search_button)
        button_layout.addWidget(self.clear_button)
        form_layout.addLayout(button_layout)

        main_layout.addWidget(form_container)

        # Search bar for filtering results
        search_container = QtWidgets.QWidget()
        search_container.setStyleSheet("""
            QWidget {
                background-color: white;
                border-radius: 16px;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            }
        """)
        search_layout = QtWidgets.QHBoxLayout(search_container)
        search_layout.setContentsMargins(20, 20, 20, 20)

        self.search_input = ModernLineEdit("Search colleges by name or location...")
        self.search_input.textChanged.connect(self.filter_results)
        search_layout.addWidget(self.search_input)

        main_layout.addWidget(search_container)

        # Results area
        self.results_area = QtWidgets.QTextEdit()
        self.results_area.setReadOnly(True)
        self.results_area.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: none;
                border-radius: 16px;
                padding: 20px;
                font-size: 14px;
                line-height: 1.6;
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            }
        """)
        main_layout.addWidget(self.results_area)

        # Store the full results for filtering
        self.current_colleges = []

        # Status bar
        self.statusBar().setStyleSheet("""
            QStatusBar {
                background-color: white;
                color: #64748b;
                padding: 8px;
                font-size: 13px;
            }
        """)
        self.statusBar().showMessage("Ready to search")

    def filter_results(self):
        search_text = self.search_input.text().lower()
        filtered_colleges = [
            college for college in self.current_colleges
            if search_text in college.name.lower() or
               search_text in college.location.lower()
        ]
        self.display_colleges(filtered_colleges)

    def display_colleges(self, colleges):
        results_html = """
            <style>
                .college-card {
                    background-color: #f8fafc;
                    border-radius: 12px;
                    padding: 25px;
                    margin-bottom: 25px;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
                    transition: transform 0.2s, box-shadow 0.2s;
                }
                .college-card:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                }
                .college-name {
                    font-size: 20px;
                    font-weight: bold;
                    color: #0f172a;
                    margin-bottom: 12px;
                    border-bottom: 2px solid #e2e8f0;
                    padding-bottom: 8px;
                }
                .college-info {
                    color: #475569;
                    margin: 8px 0;
                    font-size: 15px;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                }
                .badge {
                    display: inline-block;
                    padding: 4px 8px;
                    border-radius: 6px;
                    font-size: 13px;
                    font-weight: 500;
                    background-color: #e2e8f0;
                    color: #475569;
                    margin-right: 8px;
                }
            </style>
        """

        for college in colleges:
            results_html += f"""
                <div class='college-card'>
                    <div class='college-name'>{college.name}</div>
                    <div class='college-info'>
                        <span class='badge'>Location</span>
                        📍 {college.location}
                    </div>
                    <div class='college-info'>
                        <span class='badge'>Field</span>
                        🎓 {college.field}
                    </div>
                    <div class='college-info'>
                        <span class='badge'>Cutoff Score</span>
                        📊 {college.cutoff_score:.2f}
                    </div>
                    <div class='college-info'>
                        <span class='badge'>Annual Fee</span>
                        💰 ₹{college.tuition_fee:,.2f}
                    </div>
                </div>
            """

        self.results_area.setHtml(results_html)

    def search_colleges(self):
        try:
            exam = self.exam_combo.currentText()
            score = float(self.score_input.text())
            category = self.category_combo.currentText()
            field = self.field_combo.currentText()
            budget = float(self.budget_input.text()) if self.budget_input.text() else None

            logging.debug(f"Exam: {exam}, Field: {field}, Category: {category}, Score: {score}, Budget: {budget}")

            colleges = self.db_manager.search_colleges(
                exam_name=exam,
                field=field,
                category=category,
                score=score,
                budget=budget
            )

            self.results_area.clear()
            if not colleges:
                QMessageBox.information(self, "No Results", "No colleges found matching your criteria.")
                self.statusBar().showMessage("No colleges found")
                return

            self.current_colleges = colleges
            self.display_colleges(colleges)
            self.statusBar().showMessage(f"Found {len(colleges)} colleges matching your criteria")

        except ValueError:
            QMessageBox.warning(self, "Input Error", "Please enter valid numerical values for score and budget.")
        except Exception as e:
            logging.error(f"Error during college search: {e}")
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")
            self.statusBar().showMessage("Search failed")

    def clear_form(self):
        self.exam_combo.setCurrentIndex(0)
        self.score_input.clear()
        self.category_combo.setCurrentIndex(0)
        self.field_combo.setCurrentIndex(0)
        self.budget_input.clear()
        self.search_input.clear()
        self.results_area.clear()
        self.current_colleges = []
        self.statusBar().showMessage("Form cleared")


def main():
    app = QtWidgets.QApplication(sys.argv)

    # Set modern system fonts based on the operating system
    if sys.platform.startswith('win'):  # Windows
        default_font = QtGui.QFont('Segoe UI', 10)
    elif sys.platform.startswith('darwin'):  # macOS
        default_font = QtGui.QFont('SF Pro Display', 10)
    else:  # Linux and others
        default_font = QtGui.QFont('Ubuntu', 10)

    app.setFont(default_font)

    recommender = CollegeRecommenderApp()
    recommender.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()