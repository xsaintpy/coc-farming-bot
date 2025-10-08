import time
import cv2
import numpy as np
import pyautogui
import pytesseract
from PIL import Image
from attack import attack_with_e_drags, attack_with_dragons
from dotenv import load_dotenv
import os

# --------------------------------------------- DE --------------------------------------------- #
# Die Main Logik hinter der Suchfunktion nach einer Base mit einer bestimmten Menge an Loot.
# Nutzt pytesseract für die OCR-Funktion (Text aus Screenshot vom Loot)
# Screenshot wird von pyautogui gemacht und dann mit cv2 bearbeitet
# Danach wird, je nach Account ("1" oder "2") mit dem "MIN_COMBINED_{ACCOUNT}" abgeglichen
# Ist genügend Loot vorhanden - > Angriff, ansonsten: Nächste Base

# --------------------------------------------- ENG --------------------------------------------- #
# The main logic behind the search function for a base with a certain amount of loot.
# Uses pytesseract for the OCR function (text from screenshot of loot)
# Screenshot is taken by pyautogui and then processed with cv2
# Then, depending on the account (“1” or “2”) is compared with the “MIN_COMBINED_{ACCOUNT}”
# If there is enough loot - > attack, otherwise: next base

LOOKING_FOR_BASE = True
MIN_COMBINED_MAIN_ACCOUNT = 1800000  # 1.8 Million Elixir + Gold Combined
MIN_COMBINED_ALT_ACCOUNT = 900000  # 900K Elixir + Gold Combined
ATTACK_COUNTER = 0

load_dotenv()

# Tesseract configuration (added error handling)
try:
    tesseract_cmd = os.getenv("TESSERACT_CMD") or r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    if not os.path.exists(tesseract_cmd):
        tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
except Exception as e:
    print(f"Error configuring Tesseract: {e}")
    print("Please install Tesseract OCR and set the TESSERACT_CMD environment variable")
    exit(1)


def searchforbase(user_account):
    global LOOKING_FOR_BASE
    LOOKING_FOR_BASE = True
    
    try:
        # Verify Tesseract is working
        pytesseract.get_tesseract_version()
    except Exception as e:
        print(f"Tesseract error: {e}")
        return
        
    time.sleep(1)
    pyautogui.click(100, 1000)
    time.sleep(0.5)
    pyautogui.click(1400, 700)
    time.sleep(5)
    
    # Create screenshot directory if it doesn't exist
    screenshot_dir = os.path.join(os.path.dirname(__file__), "screenshots")
    os.makedirs(screenshot_dir, exist_ok=True)
    
    while LOOKING_FOR_BASE:
        # Set default path if not in env
        path = os.getenv("SCREENSHOT_PATH") or os.path.join(screenshot_dir, "loot_screenshot.png")
        trophy_path = os.path.join(screenshot_dir, "trophy_screenshot.png")
        
        # # Screenshot aufnehmen
        # pyautogui.screenshot(path, region=(30, 120, 250, 130))
        
        # Take screenshot of trophy count
        pyautogui.screenshot(trophy_path, region=(100, 300, 100, 60))

        # # Screenshot laden und bearbeiten (HSV + Maske)
        # cv2_image = cv2.imread(path)
        # hsv = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2HSV)
        lower_white = np.array([0, 0, 200])
        upper_white = np.array([180, 60, 255])
        # mask = cv2.inRange(hsv, lower_white, upper_white)
        # mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))

        # Process trophy screenshot
        trophy_img = cv2.imread(trophy_path)
        trophy_hsv = cv2.cvtColor(trophy_img, cv2.COLOR_BGR2HSV)
        trophy_mask = cv2.inRange(trophy_hsv, lower_white, upper_white)
        trophy_mask = cv2.morphologyEx(trophy_mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))

        # Maske in PIL-Image konvertieren für pytesseract
        # mask_pil = Image.fromarray(mask)
        trophy_mask_pil = Image.fromarray(trophy_mask)
        
        time.sleep(2)

        # # OCR auf bearbeitetem Bild anwenden
        # result = pytesseract.image_to_string(mask_pil, timeout=1, lang='eng',
        #                                      config='--oem 1 --psm 4 -c tessedit_char_whitelist=0123456789')
        # Read trophy count
        trophy_result = pytesseract.image_to_string(trophy_mask_pil, timeout=1, lang='eng',
                                             config='--oem 1 --psm 4 -c tessedit_char_whitelist=0123456789')
        
        # result = result.replace('\n\n', '\n')
        # loot_list = result.splitlines()
        
        try:
            trophy_count = int(trophy_result.strip())
            print(trophy_count)
            high_trophy = trophy_count > 30
        except (ValueError, IndexError):
            high_trophy = False
            
        print(high_trophy)
            
        if user_account == "1":
            try:
                if high_trophy:
                    print(f"Trophies: {trophy_count}")
                    LOOKING_FOR_BASE = False
                    # attack_with_e_drags()  # Angriff starten
                    break  # GANZ WICHTIG: nach Angriff raus aus While-Loop!
                else:
                    pyautogui.click(x=1785, y=820)  # Nächste Base
                    time.sleep(5)
            except (ValueError, IndexError):
                pyautogui.click(x=1785, y=820)
                time.sleep(5)

        elif user_account == "2":
            try:
                if high_trophy:
                    print(f"Trophies: {trophy_count}")
                    LOOKING_FOR_BASE = False
                    # attack_with_dragons()  # Angriff starten
                    break  # GANZ WICHTIG: nach Angriff raus aus While-Loop!
                else:
                    pyautogui.click(x=1785, y=820)  # Nächste Base
                    time.sleep(5)
            except (ValueError, IndexError):
                pyautogui.click(x=1785, y=820)
                time.sleep(5)
                
    LOOKING_FOR_BASE = True
