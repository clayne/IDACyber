from PyQt5.QtGui import qRgb
from PyQt5.QtCore import Qt
from idacyber import ColorFilter
from ida_kernwin import ask_str, warning

class xpression(ColorFilter):
    name = "expression"
    help = """Specify expression for RGB color values.
Press right mousebutton in order to change expression."""

    def __init__(self):
        self.xpr = "r, g, b"

    def _set_user_expr(self):
        while True:
            xpr = ask_str(self.xpr, 0, "Please enter expression")
            if xpr is None:
                break
            
            try:
                r = g = b = 0
                r, g, b = eval(xpr)
                self.xpr = xpr
                break
            except:
                warning("Invalid expression!")
                continue

    def on_mb_click(self, event, addr, size, mouse_offs):
        if event.button() == Qt.RightButton:
            self._set_user_expr()

    def on_process_buffer(self, buffers, addr, size, mouse_offs):
        colors = []
        for mapped, buf in buffers:
            if mapped:
                for c in buf:
                    r = g = b = c & 0xFF
                    r, g, b = eval(self.xpr)
                    colors.append((True, qRgb(r&0xFF, g&0xFF, b&0xFF)))
            else:
                colors += [(False, None)]*len(buf)
        return colors

def FILTER_INIT(pw):
    return xpression()
    
def FILTER_EXIT():
    return