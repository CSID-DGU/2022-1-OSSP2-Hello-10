#pip install pyttsx3
#pip install playsound == 1.2.2

import playsound
import pyttsx3
from time import sleep

class Alarm:
    def __init__(self) -> None:
        pass

    def speak(self, text):
        engine = pyttsx3.init()    # 콜백 에러 방지하기 위함
        engine.setProperty('rate', 150)  # 말하기 속도
        engine.setProperty('volume', 1)  # 볼륨 (min=0, MAX=1)
        playsound.playsound('beep.wav')
        engine.say(text)
        engine.runAndWait()

    def runmodule(self, classes, distance):
        num = len(classes)
        for i in range(num):
            if classes[i] == '차도':
                self.speak("인도를 벗어났습니다 안전에 유의해주세요")
            elif classes[i] == '사람' or classes[i] == '차량' or classes[i] == '소화전':
                self.speak(str(distance[i]) + "미터 앞에 " + classes[i] + "이 있습니다")
            else:
                self.speak(str(distance[i]) + "미터 앞에 " + classes[i] + "가 있습니다")


