from Player import Player
import keyboard
import time

p = Player()


def main():
    for _ in range(5):
        p.clickButton("Left", "Door")
        # time.sleep(1)
        p.clickButton("Left", "Light")
        # time.sleep(1)
        p.clickButton("Right", "Door")
        # time.sleep(1)
        p.clickButton("Right", "Light")
        # time.sleep(1)


if __name__ == "__main__":
    main()
