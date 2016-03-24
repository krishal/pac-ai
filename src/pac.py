from PIL import ImageGrab
import win32gui
import numpy as np
import win32com.client as comclt
import ctypes
import time

SendInput = ctypes.windll.user32.SendInput

SC_UP = 0xC8
SC_LEFT = 0x4B 
SC_RIGHT = 0x4D
SC_DOWN = 0x50

# C struct redefinitions 
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))



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
	
	wsh= comclt.Dispatch("WScript.Shell")
	wsh.AppActivate("jnes 1.1") # select another application
	
	PressKey(SC_UP)
	time.sleep(0.2)
	ReleaseKey(SC_UP)

if __name__ == '__main__':
	main()