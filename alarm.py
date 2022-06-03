#pip install pyttsx3
#pip install playsound == 1.2.2

import playsound
import pyttsx3

class Alarm:
    def __init__(self) -> None:
        pass

    def speak(self, text):
        engine = pyttsx3.init()
        engine.setProperty('rate', 250)
        engine.setProperty('volume', 1)
        engine.say(text)
        engine.runAndWait()

    def runmodule(self, classes, distance):
        d = "방향"
        if distance[0] and distance[1] and (not distance[2]):
            d = "좌측 전방"
        elif (not distance[0]) and distance[1] and distance[2]:
            d = "우측 전방"
        elif (not distance[0]) and (not distance[1]) and distance[2]:
            d = "우측"
        elif (not distance[0]) and distance[1] and (not distance[2]):
            d = "전방"
        elif distance[0] and (not distance[1]) and (not distance[2]):
            d = "좌측"
        elif distance[0] and distance[1] and distance[2]:
            d = "전방위에"

        if classes == '차도':
            playsound.playsound('beep.wav')
            self.speak("인도 벗어남")
        else:
            playsound.playsound('beep.wav')
            self.speak(d + ",," + classes)


