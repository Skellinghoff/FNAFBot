# import cv2
import time

import pyautogui
from keyboard import is_pressed
from win32api import mouse_event
from win32con import MOUSEEVENTF_LEFTDOWN, MOUSEEVENTF_LEFTUP

confidence = 0.7


class Player:
    button_states = {
        "Left": {
            "Door": "Open",
            "Light": "Off"
        },
        "Right": {
            "Door": "Open",
            "Light": "Off"
        },
        "Camera": "Down"
    }

    # Window of game in windowed mode
    game_window = {"top": 180,
                   "left": 320,
                   "width": 1280,
                   "height": 720}

    # Center of the cam buttons
    cams = {
        "FLIP": (874, 848),
        "REST": (874, 748),
        "1A": (1304, 534),
        "1B": (1284, 590),
        "1C": (1252, 668),
        "2A": (1304, 784),
        "2B": (1304, 824),
        "3": (1220, 766),
        "4A": (1410, 785),
        "4B": (1410, 825),
        "5": (1178, 617),
        "6": (1507, 749),
        "7": (1516, 618)
    }

    buttons_region = (342, 456, 1232, 284)

    buttonPNG_paths = {
        "Left": {
            "Door": {
                "Open": "Resources/left_door_open.png",
                "Closed": "Resources/left_door_closed.png"
            },
            "Light": {
                "On": "Resources/left_light_on.png",
                "Off": "Resources/left_light_off.png"
            }
        },
        "Right": {
            "Door": {
                "Open": "Resources/right_door_open.png",
                "Closed": "Resources/right_door_closed.png"
            },
            "Light": {
                "On": "Resources/right_light_on.png",
                "Off": "Resources/right_light_off.png"
            }
        }
    }

    def cycleThroughCams(self, cycles=0):
        cams = self.cams
        i = 1
        cycle = True
        while cycle:
            if self.button_states["Camera"] == "Down":
                if is_pressed('q'):
                    cycle = False
                self.flipCam()
            elif self.button_states["Camera"] == "Up":
                for cam in cams:
                    if is_pressed('q'):
                        cycle = False
                    if cam == "FLIP" or cam == "REST":
                        continue
                    else:
                        if is_pressed('q'):
                            cycle = False
                        print(cam)
                        pyautogui.moveTo(cams[cam])
                        self.click()
                        time.sleep(0.075)
                self.flipCam()
                i += 1
                if i == cycles+1:
                    cycle = False

    def checkButtonState(self, side, button):
        buttonPNG_paths = self.buttonPNG_paths
        partial_path = buttonPNG_paths[side][button]
        LDO = LDC = LLON = LLOFF = RDO = RDC = RLON = RLOFF = None
        if side == "Left":
            if button == "Door":
                while LDO is None and LDC is None:
                    print(f"Checking {side} {button}")
                    LDO = pyautogui.locateCenterOnScreen(partial_path["Open"], region=self.buttons_region,
                                                         confidence=confidence)
                    LDC = pyautogui.locateCenterOnScreen(partial_path["Closed"], region=self.buttons_region,
                                                         confidence=confidence)
                    self.moveLeft()
                if LDO is not None:
                    self.button_states["Left"]["Door"] = "Open"
                elif LDC is not None:
                    self.button_states["Left"]["Door"] = "Closed"
            elif button == "Light":
                while LLON is None and LLOFF is None:
                    print(f"Checking {side} {button}")
                    LLON = pyautogui.locateCenterOnScreen(partial_path["On"], region=self.buttons_region,
                                                          confidence=confidence)
                    LLOFF = pyautogui.locateCenterOnScreen(partial_path["Off"], region=self.buttons_region,
                                                           confidence=confidence)
                    self.moveLeft()
                if LLON is not None:
                    self.button_states["Left"]["Light"] = "On"
                elif LLOFF is not None:
                    self.button_states["Left"]["Light"] = "Off"
        elif side == "Right":
            if button == "Door":
                while RDO is None and RDC is None:
                    print(f"Checking {side} {button}")
                    RDO = pyautogui.locateCenterOnScreen(partial_path["Open"], region=self.buttons_region,
                                                         confidence=confidence)
                    RDC = pyautogui.locateCenterOnScreen(partial_path["Closed"], region=self.buttons_region,
                                                         confidence=confidence)
                    self.moveRight()
                if RDO is not None:
                    self.button_states["Right"]["Door"] = "Open"
                elif RDC is not None:
                    self.button_states["Right"]["Door"] = "Closed"
            elif button == "Light":
                while RLON is None and RLOFF is None:
                    print(f"Checking {side} {button}")
                    RLON = pyautogui.locateCenterOnScreen(partial_path["On"], region=self.buttons_region,
                                                          confidence=confidence)
                    RLOFF = pyautogui.locateCenterOnScreen(partial_path["Off"], region=self.buttons_region,
                                                           confidence=confidence)
                    self.moveRight()
                if RLON is not None:
                    self.button_states["Right"]["Light"] = "On"
                elif RLOFF is not None:
                    self.button_states["Right"]["Light"] = "Off"

    def clickButton(self, side, button):
        self.checkButtonState(side, button)
        buttonPNG_paths = self.buttonPNG_paths
        state = self.button_states[side][button]
        path = buttonPNG_paths[side][button][state]
        found = None
        while found is None:
            found = pyautogui.locateCenterOnScreen(
                path,
                region=self.buttons_region,
                confidence=confidence
            )
        pyautogui.moveTo(found)
        self.click()

    # Flips cams up and down
    def flipCam(self):
        cams = self.cams
        pyautogui.moveTo(cams["FLIP"])
        pyautogui.moveTo(cams["REST"])
        time.sleep(0.125)
        if self.button_states["Camera"] == "Down":
            self.button_states["Camera"] = "Up"
        elif self.button_states["Camera"] == "Up":
            self.button_states["Camera"] = "Down"
        print("Camera", self.button_states["Camera"])

    # Clicks where mouse currently is
    @staticmethod
    def click():
        mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0)
        mouse_event(MOUSEEVENTF_LEFTUP, 0, 0)
        time.sleep(0.05)

    def moveRight(self):
        game_window = self.game_window
        pyautogui.moveTo(game_window["left"] + game_window["width"],
                         game_window["top"] + (game_window["height"] / 2))

    def moveLeft(self):
        game_window = self.game_window
        pyautogui.moveTo(game_window["left"],
                         game_window["top"] + (game_window["height"] / 2))
