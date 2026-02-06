import sys
from PyQt6.QtWidgets import QApplication
import qdarktheme
from ui.main_window import MainWindow

def main():
    # Create the Application
    app = QApplication(sys.argv)
    
    # Apply Excel-like Light Theme
    try:
        if hasattr(qdarktheme, 'setup_theme'):
             qdarktheme.setup_theme("light", custom_colors={"primary": "#107c41"}) # Excel Green
        else:
             app.setStyleSheet(qdarktheme.load_stylesheet("light"))
    except Exception as e:
        print(f"Warning: Could not apply theme fully: {e}")
    
    # Create and Show Main Window
    window = MainWindow()
    window.show()
    
    # Run Event Loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
