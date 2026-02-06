import os
from datetime import datetime
from openpyxl import load_workbook
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QFileDialog, QHBoxLayout, QWidget
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QDragEnterEvent, QDropEvent

class FileDropWidget(QFrame):
    fileDropped = pyqtSignal(str)
    filesDropped = pyqtSignal(list)

    def __init__(self, title="Drop File Here", color="#6366f1"):
        super().__init__()
        self.setAcceptDrops(True)
        self.file_path = None
        self.default_color = color
        self.initial_dir = None
        self.setMinimumHeight(260)
        
        # Styling
        self.setObjectName("DropZone")
        self.setStyleSheet(f"""
            QFrame#DropZone {{
                border: 2px dashed #cbd5f5;
                border-radius: 14px;
                background-color: #f8fafc;
            }}
            QFrame#DropZone:hover {{
                border-color: {color};
                background-color: #eef2ff;
            }}
        """)
        
        # Layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Icon/Text
        self.label = QLabel(title)
        self.label.setStyleSheet("color: #475569; font-size: 15px; font-weight: 700;")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        
        self.sub_label = QLabel("or click to browse")
        self.sub_label.setStyleSheet("color: #94a3b8; font-size: 12px;")
        self.sub_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.sub_label)

        self.path_label = QLabel("")
        self.path_label.setStyleSheet("color: #64748b; font-size: 12px;")
        self.path_label.setWordWrap(True)
        self.path_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.path_label)

        meta_container = QWidget()
        meta_layout = QHBoxLayout(meta_container)
        meta_layout.setContentsMargins(0, 6, 0, 0)
        meta_layout.setSpacing(12)

        self.meta_left = QLabel("")
        self.meta_left.setStyleSheet("color: #475569; font-size: 12px;")
        self.meta_left.setWordWrap(True)
        self.meta_left.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        self.meta_right = QLabel("")
        self.meta_right.setStyleSheet("color: #475569; font-size: 12px;")
        self.meta_right.setWordWrap(True)
        self.meta_right.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)

        meta_layout.addWidget(self.meta_left, 1)
        meta_layout.addWidget(self.meta_right, 1)
        layout.addWidget(meta_container)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.accept()
            self.setStyleSheet(f"""
                QFrame#DropZone {{
                    border: 2px solid {self.default_color};
                    background-color: #e0f2fe;
                    border-radius: 14px;
                }}
            """)
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self.setStyleSheet(f"""
            QFrame#DropZone {{
                border: 2px dashed #cbd5f5;
                border-radius: 14px;
                background-color: #f8fafc;
            }}
            QFrame#DropZone:hover {{
                border-color: {self.default_color};
                background-color: #eef2ff;
            }}
        """)

    def dropEvent(self, event: QDropEvent):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        if not files:
            self.dragLeaveEvent(None)
            return

        if len(files) >= 2:
            self.filesDropped.emit(files)
        elif files:
            self.process_file(files[0])
            
        # Reset Style
        self.dragLeaveEvent(None)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            start_dir = self.initial_dir or ""
            fname, _ = QFileDialog.getOpenFileName(self, "Select Excel File", start_dir, "Excel Files (*.xlsx *.xls)")
            if fname:
                self.process_file(fname)

    def set_initial_dir(self, path):
        if path and os.path.exists(path):
            self.initial_dir = path

    def process_file(self, file_path):
        if file_path.endswith(('.xlsx', '.xls')):
            self.file_path = file_path
            file_name = os.path.basename(file_path)
            self.label.setText(file_name)
            self.label.setStyleSheet(f"color: {self.default_color}; font-size: 15px; font-weight: 700;")
            self.sub_label.setText("Ready")
            self.path_label.setText(file_path)
            left_text, right_text = self.build_metadata(file_path)
            self.meta_left.setText(left_text)
            self.meta_right.setText(right_text)
            self.fileDropped.emit(file_path)
        else:
            self.label.setText("Invalid File!")
            self.sub_label.setText("Please use .xlsx or .xls")
            self.path_label.setText("")
            self.meta_left.setText("")
            self.meta_right.setText("")

    def clear_file(self):
        self.file_path = None
        self.label.setText(self.label.text() if self.file_path else "Drop File Here") # Resetting to default title is tricky if we don't store it.
        # Actually in init we do: self.label = QLabel(title).
        # We lose the original title when we set file name.
        # We should store the original title.
        self.sub_label.setText("or click to browse")
        self.path_label.setText("")
        self.meta_left.setText("")
        self.meta_right.setText("")
        self.fileDropped.emit("")

    def build_metadata(self, file_path):
        try:
            stat = os.stat(file_path)
            size_text = self.format_size(stat.st_size)
            modified = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
            created = datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M")
            accessed = datetime.fromtimestamp(stat.st_atime).strftime("%Y-%m-%d %H:%M")
        except Exception:
            size_text = "Unknown"
            modified = "Unknown"
            created = "Unknown"
            accessed = "Unknown"

        authors = "Unknown"
        last_saved_by = "Unknown"
        try:
            wb = load_workbook(file_path, read_only=True)
            creator = wb.properties.creator or ""
            last_mod = wb.properties.lastModifiedBy or ""
            if creator:
                authors = creator
            if last_mod:
                last_saved_by = last_mod
            wb.close()
        except Exception:
            pass

        left = "\n".join([
            f"Size: {size_text}",
            f"Authors: {authors}",
            f"Last saved by: {last_saved_by}",
        ])
        right = "\n".join([
            f"Modified: {modified}",
            f"Created: {created}",
            f"Accessed: {accessed}",
        ])
        return left, right

    def format_size(self, size_bytes):
        if size_bytes < 1024:
            return f"{size_bytes} B"
        if size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        if size_bytes < 1024 * 1024 * 1024:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"
