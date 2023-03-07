
dic = {1: "a", 2: "b", 3: "c", 4: "d", 5: "e", 6: 6}

import winreg

reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\firefox.exe"
with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
    firefox_path = winreg.QueryValue(key, None)

print(firefox_path)

reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe"
with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path) as key:
    chrome_path = winreg.QueryValue(key, None)

print(chrome_path)

