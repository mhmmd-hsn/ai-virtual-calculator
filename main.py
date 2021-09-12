import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import cvzone
from pynput.keyboard import Controller

wCam, hCam = 1800, 1200

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = HandDetector(detectionCon=0.8)
keys = [["7", "8", "9", "*", "+", "0"],
        ["4", "5", "6", "/", "-"],
        ["1", "2", "3", "=", "c"]]
finalText = ""

keyboard = Controller()


def draw_all(img,buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(img, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
                          20, rt=0)
        cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65),
                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return img


class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text


buttonList = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList, bboxInfo = detector.findPosition(img)
    img = draw_all(img, buttonList)

    if lmList:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size

            if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (175, 0, 175), cv2.FILLED)
                cv2.putText(img, button.text, (x + 20, y + 65),
                            cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                l, _, _ = detector.findDistance(8, 12, img, draw=False)
                print(l)

                ## when clicked
                if l < 20:
                    keyboard.press(button.text)
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65),
                                cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    if button.text == '=':
                        #divide
                        if '/' in finalText:
                            try:
                                numbers = finalText.split("/")
                                num1 = int(numbers[0])
                                num2 = int(numbers[1])
                                result = num1 / num2
                                finalText += '=' + str(result)
                                sleep(1)
                            except ZeroDivisionError:
                                finalText = 'ZeroDivisionError'
                        #sum
                        if '+' in finalText:
                            numbers = finalText.split("+")
                            num1 = int(numbers[0])
                            num2 = int(numbers[1])
                            result = num1 + num2
                            finalText += '=' + str(result)
                            sleep(1)
                        #time
                        if '*' in finalText:
                            numbers = finalText.split("*")
                            num1 = int(numbers[0])
                            num2 = int(numbers[1])
                            result = num1 * num2
                            finalText += '=' + str(result)
                            sleep(1)
                        #mines
                        if '-' in finalText:
                            numbers = finalText.split("-")
                            num1 = int(numbers[0])
                            num2 = int(numbers[1])
                            result = num1 - num2
                            finalText += '=' + str(result)
                            sleep(1)
                    if button.text == 'c':
                        finalText = ''
                    if button.text != '=' and button.text != 'c':
                        finalText += button.text
                        sleep(1)

    cv2.rectangle(img, (50, 350), (700, 450), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finalText, (60, 430),
                cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    cv2.imshow("Image", img)
    cv2.waitKey(1)

