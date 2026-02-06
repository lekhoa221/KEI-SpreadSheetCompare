from PyQt6.QtWidgets import (
    QHeaderView, QMenu, QWidgetAction, QCheckBox, QLineEdit, 
    QListWidget, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, 
    QLabel, QListWidgetItem, QApplication
)
from PyQt6.QtCore import Qt, pyqtSignal, QAbstractTableModel, QModelIndex, QRect
from PyQt6.QtGui import QAction, QIcon, QPainter, QColor, QPixmap
import os

class FilterHeader(QHeaderView):
    # Signal emitted when filter changes: col_idx, set_of_values (or None if cleared)
    filterChanged = pyqtSignal(int, object)

    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent)
        self.setSectionsClickable(True)
        self.setHighlightSections(True)
        
        # Load Icon
        icon_path = os.path.join(os.path.dirname(__file__), "..", "assets", "icons", "filter.svg")
        self._filter_icon = QIcon(icon_path)
        
        # Track active filters: col_idx -> set of allowed values
        self._active_filters = {} 
        self._hover_index = -1

    def paintSection(self, painter, rect, logicalIndex):
        painter.save()
        super().paintSection(painter, rect, logicalIndex)
        painter.restore()

        # Check if this column is filtered
        is_filtered = logicalIndex in self._active_filters
        
        # Draw Icon if filtered or hovered
        # We'll draw it on the right side of the header section
        if is_filtered:
            icon_size = 14
            padding = 4
            
            # Position: Right side, vertically centered
            img_rect = QRect(
                rect.right() - icon_size - padding,
                rect.top() + (rect.height() - icon_size) // 2,
                icon_size,
                icon_size
            )
            
            # If section is too small, don't draw
            if rect.width() > icon_size + padding * 2:
                # Tint icon based on state
                mode = QIcon.Mode.Normal
                if is_filtered:
                    mode = QIcon.Mode.Active # Or use a specific color painter
                    
                # To force a specific color (e.g. Blue if filtered), we might need to paint pixmap manually
                pixmap = self._filter_icon.pixmap(icon_size, icon_size, mode=mode)
                
                if is_filtered:
                    # Paint a small indicator background or just the icon
                    painter.save()
                    # painter.setOpacity(0.2)
                    # painter.fillRect(img_rect.adjusted(-2, -2, 2, 2), QColor("#0ea5e9"))
                    painter.restore()
                
                painter.drawPixmap(img_rect, pixmap)

    def mousePressEvent(self, event):
        # Right click to show filter, or click on the "icon area" if we had one.
        # For simplicity: Right Click on Header triggers Filter Menu
        if event.button() == Qt.MouseButton.RightButton:
            idx = self.logicalIndexAt(event.pos())
            if idx >= 0:
                self.show_filter_menu(idx)
        else:
            super().mousePressEvent(event)

    def show_filter_menu(self, col_idx):
        table = self.parent()
        if not table: return
        
        # Gather unique values
        # Note: This scans all rows used. For huge data, might be slow, but ok for typical spreadsheet usage.
        values = set()
        for r in range(table.rowCount()):
            item = table.item(r, col_idx)
            val = item.text() if item else ""
            values.add(val)
            
        sorted_values = sorted(list(values))
        
        # Menu Setup
        menu = QMenu(self)
        menu.setStyleSheet("QMenu { background-color: white; border: 1px solid #ccc; }")
        
        # 1. Search Box
        search_widget = QWidget()
        vbox = QVBoxLayout(search_widget)
        vbox.setContentsMargins(4, 4, 4, 4)
        vbox.setSpacing(4)
        
        search_input = QLineEdit()
        search_input.setPlaceholderText("Search...")
        vbox.addWidget(search_input)
        
        # 2. List Widget
        list_widget = QListWidget()
        list_widget.setFixedHeight(200)
        
        # Select All Item
        item_all = QListWidgetItem("(Select All)")
        item_all.setCheckState(Qt.CheckState.Checked)
        list_widget.addItem(item_all)
        
        # Determine items to check (if filter exists)
        current_filter = self._active_filters.get(col_idx)
        
        items_map = {} # value -> item
        
        for val in sorted_values:
            item = QListWidgetItem(str(val))
            is_checked = True
            if current_filter is not None:
                is_checked = val in current_filter
            
            item.setCheckState(Qt.CheckState.Checked if is_checked else Qt.CheckState.Unchecked)
            list_widget.addItem(item)
            items_map[val] = item
            
        # Update "Select All" state based on items
        if current_filter is not None and len(current_filter) < len(sorted_values):
            item_all.setCheckState(Qt.CheckState.Unchecked)
            
        vbox.addWidget(list_widget)
        
        # Logic: Filter list based on search
        def on_search(text):
            text = text.lower()
            for i in range(1, list_widget.count()): # Skip select all
                item = list_widget.item(i)
                item.setHidden(text not in item.text().lower())
                
        search_input.textChanged.connect(on_search)
        
        # Logic: Select All toggle
        def on_item_changed(item):
            if item == item_all:
                state = item.checkState()
                list_widget.blockSignals(True)
                for i in range(1, list_widget.count()):
                    list_widget.item(i).setCheckState(state)
                list_widget.blockSignals(False)
            
        list_widget.itemChanged.connect(on_item_changed)

        # 3. Buttons
        btn_layout = QHBoxLayout()
        btn_ok = QPushButton("OK")
        btn_cancel = QPushButton("Cancel")
        btn_layout.addWidget(btn_ok)
        btn_layout.addWidget(btn_cancel)
        vbox.addLayout(btn_layout)
        
        action = QWidgetAction(menu)
        action.setDefaultWidget(search_widget)
        menu.addAction(action)
        
        # Execution
        # Calculate global position
        # sectionViewportPosition returns relative to viewport
        header_pos = self.mapToGlobal(self.viewport().mapToParent(self.pixel_pos_of_section(col_idx)))
        
        # Allow menu to process events
        # We need to capture the button clicks
        
        def apply_filter():
            # Gather checked items
            checked_values = set()
            all_checked = item_all.checkState() == Qt.CheckState.Checked
            
            # If select all is checked and search is empty, usually means clear filter
            # But here "Select All" behaves as "Include All"
            
            # Count actual checked
            checked_count = 0
            total_items = list_widget.count() - 1
            
            for i in range(1, list_widget.count()):
                item = list_widget.item(i)
                if item.checkState() == Qt.CheckState.Checked:
                    checked_values.add(sorted_values[i-1]) # Use index mapping carefully
            
            if len(checked_values) == total_items:
                # All selected -> No Filter
                if col_idx in self._active_filters:
                    del self._active_filters[col_idx]
                self.filterChanged.emit(col_idx, None)
            else:
                self._active_filters[col_idx] = checked_values
                self.filterChanged.emit(col_idx, checked_values)
            
            menu.close()
            self.viewport().update()

        btn_ok.clicked.connect(apply_filter)
        btn_cancel.clicked.connect(menu.close)
        
        # Run
        menu.exec(header_pos)

    def pixel_pos_of_section(self, logical_index):
        # Helper to get position relative to header widget
        # visualIndex = self.visualIndex(logical_index) 
        # But sectionViewportPosition gives x coord
        x = self.sectionViewportPosition(logical_index)
        from PyQt6.QtCore import QPoint
        return QPoint(x, 0)
