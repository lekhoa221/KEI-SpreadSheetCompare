from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, 
    QCheckBox, QComboBox, QGroupBox, QWidget, QTableWidget, QTableWidgetItem, QHeaderView,
    QTabWidget, QGridLayout
)
from PyQt6.QtCore import Qt, pyqtSignal, QSettings

class FindDialog(QDialog):
    findNext = pyqtSignal(dict)
    findAll = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Find")
        self.setFixedWidth(440)
        self.settings = QSettings("DocCompareAI", "FindHistory")
        
        # Styles
        # Note: Added background color to QComboBox to ensure White text is visible on light theme
        self.setStyleSheet("""
            QPushButton { color: black; }
            QLabel[role="header"] { font-weight: bold; }
            QComboBox { color: black; background-color: white; selection-background-color: #107c41; selection-color: white; }
            QComboBox QAbstractItemView { color: black; background-color: white; selection-background-color: #107c41; selection-color: white; }
            QCheckBox[role="checked"] { font-weight: bold; }
        """)
        
        # Main Layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)

        # 1. Find What Row
        find_row = QHBoxLayout()
        lbl_find = QLabel("Find what:")
        lbl_find.setProperty("role", "header")
        find_row.addWidget(lbl_find)
        
        self.find_input = QComboBox()
        self.find_input.setEditable(True)
        self.find_input.setInsertPolicy(QComboBox.InsertPolicy.InsertAtTop)
        # Load history
        self.load_history()
        
        # Make the line edit of combobox also respect the style
        self.find_input.setStyleSheet("QComboBox { color: black; background-color: white; selection-background-color: #107c41; selection-color: white; }")
        
        find_row.addWidget(self.find_input)
        self.layout.addLayout(find_row)

        # 2. Advanced Options Container
        self.advanced_container = QWidget()
        self.adv_layout = QGridLayout(self.advanced_container)
        self.adv_layout.setContentsMargins(0, 0, 0, 0)
        self.adv_layout.setHorizontalSpacing(16)
        self.adv_layout.setVerticalSpacing(8)

        # Column 1: Labels
        lbl_search = QLabel("Search:")
        lbl_search.setProperty("role", "header")
        self.adv_layout.addWidget(lbl_search, 0, 0)
        
        lbl_look = QLabel("Look in:")
        lbl_look.setProperty("role", "header")
        self.adv_layout.addWidget(lbl_look, 1, 0)

        # Column 2: Combos
        self.search_by = QComboBox()
        self.search_by.addItems(["By Rows", "By Columns"])
        self.adv_layout.addWidget(self.search_by, 0, 1)

        self.look_in = QComboBox()
        self.look_in.addItems(["Formulas", "Values"])
        self.adv_layout.addWidget(self.look_in, 1, 1)

        # Column 3: Checkboxes
        self.match_case = QCheckBox("Match case")
        self.match_entire = QCheckBox("Match entire cell contents")
        
        # Dynamic Bold on Check logic
        self.match_case.toggled.connect(self.update_checkbox_style)
        self.match_entire.toggled.connect(self.update_checkbox_style)
        
        self.adv_layout.addWidget(self.match_case, 0, 2, 1, 2)
        self.adv_layout.addWidget(self.match_entire, 1, 2, 1, 2)

        self.layout.addWidget(self.advanced_container)
        
        # 3. Results List (Find All)
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(5)
        self.results_table.setHorizontalHeaderLabels(["Book", "Sheet", "Cell", "Value", "Formula"])
        self.results_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.results_table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)
        self.results_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.results_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.results_table.hide() 
        self.results_table.cellClicked.connect(self.on_result_clicked)
        self.layout.addWidget(self.results_table)

        # 4. Buttons
        btn_layout = QHBoxLayout()
        
        self.options_btn = QPushButton("Options >>")
        self.options_btn.setCheckable(True)
        self.options_btn.toggled.connect(self.toggle_options)
        
        self.find_all_btn = QPushButton("Find All")
        self.find_next_btn = QPushButton("Find Next")
        self.close_btn = QPushButton("Close")
        
        btn_layout.addWidget(self.options_btn)
        btn_layout.addStretch()
        # In simple mode (default), Find All is hidden?
        # User said: "simple mode ... only find next"
        self.find_all_btn.setVisible(False) 
        
        btn_layout.addWidget(self.find_all_btn)
        btn_layout.addWidget(self.find_next_btn)
        btn_layout.addWidget(self.close_btn)
        
        self.layout.addLayout(btn_layout)
        self.layout.addStretch() # Push buttons up if list hidden
        
        # Connections
        self.find_next_btn.clicked.connect(self.on_find_next)
        self.find_all_btn.clicked.connect(self.on_find_all)
        self.close_btn.clicked.connect(self.close)
        
        # Initial State
        self.advanced_container.setVisible(False)
        self.resize(440, 160)

    def update_checkbox_style(self):
        sender = self.sender()
        if sender:
            # We use a dynamic property + style unpolish/polish or just set font explicitly
            # Since CSS dynamic property updates can be tricky in Qt without repolish:
            f = sender.font()
            f.setBold(sender.isChecked())
            sender.setFont(f)

    def toggle_options(self, checked):
        self.advanced_container.setVisible(checked)
        self.find_all_btn.setVisible(checked) # Show Find All only in Advanced
        self.options_btn.setText("Options <<" if checked else "Options >>")
        
        # If unchecked (Simple), hide results table too? 
        if not checked:
            self.results_table.hide()
        
        self.adjustSize()

    def load_history(self):
        history = self.settings.value("history", [], type=list)
        self.find_input.addItems(history)
        self.find_input.setCurrentIndex(-1)
        self.find_input.setEditText("")

    def save_history_item(self, text):
        if not text: return
        
        # Get current history
        history = []
        for i in range(self.find_input.count()):
            history.append(self.find_input.itemText(i))
        
        # Remove if exists (to move to top)
        if text in history:
            history.remove(text)
        
        # Add to top
        history.insert(0, text)
        
        # Keep max 5
        history = history[:5]
        
        # Update Combo (avoid triggering signals if any)
        self.find_input.blockSignals(True)
        self.find_input.clear()
        self.find_input.addItems(history)
        self.find_input.setEditText(text)
        self.find_input.blockSignals(False)
        
        # Save
        self.settings.setValue("history", history)

    def get_options(self):
        text = self.find_input.currentText()
        # Save history on get_options (which implies action)
        self.save_history_item(text)
        
        return {
            "text": text,
            "search_by": self.search_by.currentText(),
            "look_in": self.look_in.currentText(),
            "match_case": self.match_case.isChecked(),
            "match_entire": self.match_entire.isChecked()
        }

    def on_find_next(self):
        self.findNext.emit(self.get_options())

    def on_find_all(self):
        self.results_table.setRowCount(0)
        self.results_table.hide()
        self.findAll.emit(self.get_options())
        # Show table if we have results is handled by parent, but parent calls show_results?
        # Actually parent class calls add_result_row then show().

    def add_result_row(self, cell_ref, value, sheet_name, user_data):
        row = self.results_table.rowCount()
        self.results_table.insertRow(row)
        
        # Parse sheet/book info if possible, for now just placeholder
        # user_data = (grid_idx, r, c)
        grid_idx = user_data[0]
        book = "Original" if grid_idx == 1 else "Modified"
        
        self.results_table.setItem(row, 0, QTableWidgetItem(book))
        self.results_table.setItem(row, 1, QTableWidgetItem(sheet_name)) # sheet_name passed is actually header label "Original"/"Modified" in current logic
        self.results_table.setItem(row, 2, QTableWidgetItem(cell_ref))
        self.results_table.setItem(row, 3, QTableWidgetItem(str(value)))
        self.results_table.setItem(row, 4, QTableWidgetItem("")) # Formula placeholder
        
        self.results_table.item(row, 0).setData(Qt.ItemDataRole.UserRole, user_data)

    def on_result_clicked(self, row, col):
        data = self.results_table.item(row, 0).data(Qt.ItemDataRole.UserRole)
        if data and self.parent():
            self.parent().navigate_to_find_result(data)
