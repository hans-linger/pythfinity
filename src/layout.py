import tkinter as tk
from tkinter import ttk

from src.core.polymom import Polymom

DELAY = 12


def x(win: tk.Tk, pm: Polymom):
	pm.draw_poly()
	win.after(DELAY, x, win, pm)


def make_layout():
	win = tk.Tk()
	win.title("Draw me")

	mainframe = ttk.Frame(win, height=1000)
	mainframe.grid(column=0, row=0)
	win.columnconfigure(0, weight=1)
	win.rowconfigure(0, weight=1)
	draw_region = tk.Frame(mainframe, width=200, height=200)
	canvas = tk.Canvas(draw_region, width=200, height=200, bg="white")
	canvas.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
	pm = Polymom(canvas, 5)
	pm.draw()
	draw_region.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
	mainframe.pack()
	x(win, pm)
	return win, pm
