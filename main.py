from src.layout import make_layout
from ctypes import windll

timeBeginPeriod = windll.winmm.timeBeginPeriod
timeBeginPeriod(1)

window, pm = make_layout()
window.mainloop()
