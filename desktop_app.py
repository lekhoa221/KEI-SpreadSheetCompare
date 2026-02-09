import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QSplashScreen
from PyQt6.QtGui import QPixmap, QPainter, QColor, QPen, QPainterPath, QBitmap
from PyQt6.QtCore import Qt
import qdarktheme

# Import MainWindow inside main() to allow splash screen to show first
# from ui.main_window import MainWindow 

def main():
    # Create the Application
    app = QApplication(sys.argv)

    # ---------------------------
    # Splash Screen Logic
    # ---------------------------
    splash = None
    
    # Determine logo path
    if getattr(sys, 'frozen', False):
        base_path = Path(sys._MEIPASS)
        logo_path = base_path / "ui" / "logo.png"
    else:
        base_path = Path(__file__).resolve().parent
        logo_path = base_path / "ui" / "logo.png"

    if logo_path.exists():
        raw_pixmap = QPixmap(str(logo_path))
        if not raw_pixmap.isNull():
            # 1. Scale logo down (User requested bigger logo)
            logo_w = 600
            if raw_pixmap.width() > logo_w:
                raw_pixmap = raw_pixmap.scaledToWidth(logo_w, Qt.TransformationMode.SmoothTransformation)
            
            # 2. Prepare Canvas (Logo size + thin padding)
            padding = 4  # Very thin white border
            w = raw_pixmap.width() + padding * 2
            h = raw_pixmap.height() + padding * 2
            
            canvas = QPixmap(w, h)
            canvas.fill(Qt.GlobalColor.transparent)
            
            painter = QPainter(canvas)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            # 3. Draw Background: Rounded Rect, White
            bg_path = QPainterPath()
            bg_path.addRoundedRect(0, 0, w, h, 10, 10)
            painter.fillPath(bg_path, Qt.GlobalColor.white)
            
            # 4. Draw Logo Shadow (Simple offset silhouette with opacity)
            # Create a shadow image from alpha channel
            shadow_offset = 4
            shadow_color = QColor(0, 0, 0, 40) # Black with low opacity
            
            # Drawing shadow manually:
            # Save state
            painter.save()
            painter.translate(padding + shadow_offset, padding + shadow_offset)
            
            # Create a silhouette for shadow
            shadow_pixmap = raw_pixmap.copy()
            # Use CompositionMode to turn it black
            sp = QPainter(shadow_pixmap)
            sp.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
            sp.fillRect(shadow_pixmap.rect(), shadow_color)
            sp.end()
            
            painter.drawPixmap(0, 0, shadow_pixmap)
            painter.restore()
            
            # 5. Draw Logo
            painter.drawPixmap(padding, padding, raw_pixmap)
            
            # 6. Draw Border (Grey line) - Optional if padding is very thin, maybe skip or keep very subtle
            pen = QPen(QColor("#e2e8f0"))
            pen.setWidth(1)
            painter.setPen(pen)
            painter.drawPath(bg_path)
            
            painter.end()
            
            # 7. Apply to Splash Screen
            splash = QSplashScreen(canvas, Qt.WindowType.WindowStaysOnTopHint)
            # Mask needed for rounded corners transparency
            splash.setMask(canvas.mask())
            splash.show()
            app.processEvents()

    # ---------------------------
    # Global Cleanup / Theme
    # ---------------------------
    
    # Apply Excel-like Light Theme
    try:
        if hasattr(qdarktheme, 'setup_theme'):
             qdarktheme.setup_theme("light", custom_colors={"primary": "#107c41"}) # Excel Green
        else:
             app.setStyleSheet(qdarktheme.load_stylesheet("light"))
    except Exception as e:
        print(f"Warning: Could not apply theme fully: {e}")
    
    # ---------------------------
    # Load Main Application
    # ---------------------------
    # Move import here to allow splash to display while importing
    from ui.main_window import MainWindow

    # Create and Show Main Window
    window = MainWindow()
    window.show()
    
    # Close splash when main window is ready
    if splash:
        splash.finish(window)
    
    # Run Event Loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
