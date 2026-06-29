import ctypes
import ctypes.util
import os

if os.name == 'nt':
    # --- Windows ---
    user32 = ctypes.windll.user32
    
    user32.MessageBoxW.argtypes = [ctypes.c_void_p, ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint]
    user32.MessageBoxW.restype = ctypes.c_int

    print("Вызов MessageBoxW из user32.dll...")
    user32.MessageBoxW(0, "Привет из Python!", "ctypes Демо (Windows)", 0x00000040)
    print("Диалоговое окно закрыто.")

else:
    # --- Linux & macOS ---
    libc_name = ctypes.util.find_library('c')
    if not libc_name:
        print("Ошибка: не могу найти libc. Что-то пошло не так.")
        exit()
        
    libc = ctypes.CDLL(libc_name)
    
    libc.puts.argtypes = [ctypes.c_char_p]
    libc.puts.restype = ctypes.c_int
    
    print(f"Вызов puts из {libc_name}...")
    message = b"Hello from Python! (ctypes Demo, POSIX)"
    libc.puts(message)
