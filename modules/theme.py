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
    bg, side, card, txt, sub, brd, inp = ("#16181D", "#1E2028", "#1E2028", "#F3F4F6", "#9CA3AF", "#2D313D", "#252832") if dark else ("#F4F6F8", "#FFFFFF", "#FFFFFF", "#111827", "#4B5563", "#E5E7EB", "#FFFFFF")
    return f"""
    QMainWindow, QWidget {{ background: {bg}; color: {txt}; font-family: sans-serif; font-size: {fsize}px; }}
    QFrame#Sidebar {{ background: {side}; border-right: 1px solid {brd}; }}
    QFrame#Card {{ background: {card}; border: 1px solid {brd}; border-radius: 12px; }}
    QPushButton#NavBtn {{ background: transparent; color: {sub}; text-align: left; padding: 10px 14px; border-radius: 8px; font-size: {fsize}px; }}
    QPushButton#NavBtn:hover {{ background: {brd}; color: {txt}; }}
    QPushButton#NavBtn[active="true"] {{ background: #10B981; color: #FFFFFF; font-weight: bold; }}
    QPushButton#ActionBtn {{ background: #10B981; color: #FFFFFF; border-radius: 8px; padding: 6px 12px; font-weight: bold; }}
    QPushButton#MiniBtn {{ background: {inp}; color: {txt}; border: 1px solid {brd}; border-radius: 6px; padding: 4px 8px; }}
    QLineEdit, QComboBox {{ background: {inp}; color: {txt}; border: 1px solid {brd}; border-radius: 8px; padding: 6px 10px; }}
    QListWidget {{ background: {card}; border: 1px solid {brd}; border-radius: 8px; }}
    """
