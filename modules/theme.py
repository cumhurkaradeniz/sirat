import os, subprocess
from PyQt5.QtWidgets import QApplication

def is_dark_mode(mode="auto"):
    if mode == "dark": return True
    if mode == "light": return False
    cf = os.path.expanduser("~/.config/cutefish/services.conf")
    if os.path.exists(cf) and "darkmode=true" in open(cf).read().lower().replace(" ", ""):
        return True
    try:
        out = subprocess.check_output(["gsettings", "get", "org.gnome.desktop.interface", "color-scheme"], stderr=subprocess.DEVNULL, text=True)
        if "dark" in out.lower(): return True
    except Exception:
        pass
    return QApplication.palette().window().color().lightness() < 128

def get_stylesheet(dark, fsize=14):
    if dark:
        bg, side, card, txt, sub, brd, inp = "#111318", "#181B22", "#1C2029", "#F3F4F6", "#9CA3AF", "#2A2F3D", "#222631"
        hover, sel_bg, sel_txt = "#252A36", "rgba(16, 185, 129, 0.18)", "#34D399"
        scroll_bg, scroll_hdl = "transparent", "#374151"
        hero_bg, hero_brd = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #132A24, stop:1 #1C2029)", "#10B981"
    else:
        bg, side, card, txt, sub, brd, inp = "#F3F5F8", "#FFFFFF", "#FFFFFF", "#111827", "#6B7280", "#E5E7EB", "#F9FAFB"
        hover, sel_bg, sel_txt = "#F3F4F6", "rgba(16, 185, 129, 0.12)", "#059669"
        scroll_bg, scroll_hdl = "transparent", "#D1D5DB"
        hero_bg, hero_brd = "qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #ECFDF5, stop:1 #FFFFFF)", "#10B981"

    return f"""
    QMainWindow, QWidget {{ background: {bg}; color: {txt}; font-family: 'Inter', 'Segoe UI', sans-serif; font-size: {fsize}px; }}
    QLabel {{ background: transparent; }}
    
    QFrame#Sidebar {{ background: {side}; border-right: 1px solid {brd}; }}
    QPushButton#NavBtn {{
        background: transparent; color: {sub}; text-align: left;
        padding: 11px 16px; border-radius: 10px; font-size: {fsize}px; font-weight: 500; border: none;
    }}
    QPushButton#NavBtn:hover {{ background: {hover}; color: {txt}; }}
    QPushButton#NavBtn[active="true"] {{ background: #10B981; color: #FFFFFF; font-weight: bold; }}

    QFrame#Card {{ background: {card}; border: 1px solid {brd}; border-radius: 14px; }}
    QFrame#HeroCard {{ background: {hero_bg}; border: 1.5px solid {hero_brd}; border-radius: 16px; }}
    QFrame#ActivePrayerCard {{ background: {sel_bg}; border: 1.5px solid #10B981; border-radius: 14px; }}

    QPushButton#ActionBtn {{
        background: #10B981; color: #FFFFFF; border: none;
        border-radius: 10px; padding: 8px 16px; font-weight: bold;
    }}
    QPushButton#ActionBtn:hover {{ background: #059669; }}

    QPushButton#MiniBtn {{
        background: {inp}; color: {txt}; border: 1px solid {brd};
        border-radius: 8px; padding: 6px 8px; font-weight: 600;
    }}
    QPushButton#MiniBtn:hover {{ background: {hover}; border-color: #10B981; }}

    QLineEdit, QComboBox {{
        background: {inp}; color: {txt}; border: 1px solid {brd};
        border-radius: 10px; padding: 8px 12px; selection-background-color: #10B981;
    }}
    QLineEdit:focus, QComboBox:focus {{ border: 1.5px solid #10B981; }}
    QComboBox::drop-down {{ border: none; width: 24px; }}
    QComboBox QAbstractItemView {{
        background: {card}; color: {txt}; border: 1px solid {brd};
        border-radius: 8px; selection-background-color: {sel_bg}; selection-color: {sel_txt};
    }}

    QListWidget {{ background: {card}; border: 1px solid {brd}; border-radius: 12px; padding: 6px; outline: none; }}
    QListWidget::item {{ padding: 9px 12px; border-radius: 8px; margin-bottom: 2px; color: {txt}; }}
    QListWidget::item:hover {{ background: {hover}; }}
    QListWidget::item:selected {{ background: {sel_bg}; color: {sel_txt}; font-weight: bold; }}

    QTextBrowser {{ background: {card}; border: 1px solid {brd}; border-radius: 14px; padding: 14px; }}

    QScrollBar:vertical {{ background: {scroll_bg}; width: 7px; margin: 4px 2px 4px 0px; border-radius: 3px; }}
    QScrollBar::handle:vertical {{ background: {scroll_hdl}; min-height: 30px; border-radius: 3px; }}
    QScrollBar::handle:vertical:hover {{ background: #10B981; }}
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0px; }}

    QScrollBar:horizontal {{ background: {scroll_bg}; height: 7px; margin: 0px 4px 2px 4px; border-radius: 3px; }}
    QScrollBar::handle:horizontal {{ background: {scroll_hdl}; min-width: 30px; border-radius: 3px; }}
    QScrollBar::handle:horizontal:hover {{ background: #10B981; }}
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0px; }}
    """
