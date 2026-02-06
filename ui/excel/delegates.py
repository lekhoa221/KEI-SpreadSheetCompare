from PyQt6.QtWidgets import QStyledItemDelegate
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen, QColor

class BorderDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        # 1. Draw the standard content (Text, Background, Selection)
        super().paint(painter, option, index)
        
        # 2. Retrieve Border Data stored in UserRole
        # We stored it as a dict: {'top': True, 'bottom': True, ...}
        borders = index.data(Qt.ItemDataRole.UserRole)
        
        if borders and isinstance(borders, dict):
            painter.save()
            
            # Setup Pen for Border (Black, Thin)
            # Future improvement: Extract color/weight from Excel too
            pen = QPen(QColor("#000000")) 
            pen.setWidth(1) 
            painter.setPen(pen)
            
            rect = option.rect
            
            # Draw Lines based on data
            # Use 'adjusted' to ensure lines don't overlap awkwardly
            
            if borders.get('top'):
                painter.drawLine(rect.topLeft(), rect.topRight())
                
            if borders.get('bottom'):
                painter.drawLine(rect.bottomLeft(), rect.bottomRight())
                
            if borders.get('left'):
                painter.drawLine(rect.topLeft(), rect.bottomLeft())
                
            if borders.get('right'):
                # subtract 1 from right so it doesn't get clipped
                painter.drawLine(rect.topRight(), rect.bottomRight())
            
            painter.restore()

        diff_mask = index.data(Qt.ItemDataRole.UserRole + 2)
        if diff_mask:
            painter.save()
            # rect = option.rect.adjusted(1, 1, -2, -2) # No adjustment needed for fill
            rect = option.rect
            if diff_mask == 1:
                color = QColor("#0ea5e9")  # content
            elif diff_mask == 2:
                color = QColor("#f59e0b")  # format
            elif diff_mask == 4:
                color = QColor("#22c55e")  # formula
            else:
                color = QColor("#8b5cf6")  # mixed
            
            # Set transparency (e.g., 20% opacity)
            color.setAlpha(50) 
            painter.fillRect(rect, color)
            painter.restore()

        # Reference Highlight (Excel-like formula view)
        ref_color = index.data(Qt.ItemDataRole.UserRole + 3)
        if ref_color:
            painter.save()
            rect = option.rect.adjusted(1, 1, -1, -1)
            # Use a slightly thicker border for visibility
            pen = QPen(QColor(ref_color))
            pen.setWidth(2)
            painter.setPen(pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawRect(rect)
            
            # Optional: Add corner handles or slight tint? For now just border.
            color = QColor(ref_color)
            color.setAlpha(30) # 10-15% opacity
            painter.fillRect(rect, color)
            
            painter.restore()
