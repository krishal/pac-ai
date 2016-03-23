from PIL import ImageGrab
import win32gui
import numpy as np

def takeScreenshot():
	toplist, winlist = [], []

	def enum_cb(hwnd, results):
	    winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

	win32gui.EnumWindows(enum_cb, toplist)

	jnes = [(hwnd, title) for hwnd, title in winlist if 'jnes 1.1' in title.lower()]

	if(len(jnes) == 0):
		raise Exception('Pacman not running')

	jnes = jnes[0]
	hwnd = jnes[0]

	win32gui.SetForegroundWindow(hwnd)
	bbox = win32gui.GetWindowRect(hwnd)
	img = ImageGrab.grab(bbox)

	mat = np.array(img) 
	mat = mat[:, :, ::-1].copy()

	return mat

def main():
	mat = takeScreenshot()

if __name__ == '__main__':
	main()