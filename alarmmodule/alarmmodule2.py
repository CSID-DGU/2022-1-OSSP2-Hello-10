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

    def transform_obj(self, classes):
        c = '장애물'
        if classes == 0:
            c = '자전거'
        elif classes == 1:
            c = '스쿠터'
        elif classes == 2:
            c = '커리어'
        elif classes == 3:
            c = '버스'
        elif classes == 4:
            c = '자동차'
        elif classes == 5:
            c = '트럭'
        elif classes == 6:
            c = '오토바이'
        elif classes == 7:
            c = '사람'
        elif classes == 8:
            c = '방책'
        elif classes == 9:
            c = '소화전'
        elif classes == 10:
            c = '가로수'
        elif classes == 11:
            c = '밴치'
        elif classes == 12:
            c = '의자'
        elif classes == 13:
            c = '전봇대'
        elif classes == 14:
            c = '신호등'
        elif classes == 15:
            c = '표지판'
        return c

    def transform_dist(self, direction):
        d = "방향"
        if direction[0] and direction[1] and (not direction[2]):
            d = "좌측 전방에"
        elif (not direction[0]) and direction[1] and direction[2]:
            d = "우측 전방에"
        elif (not direction[0]) and (not direction[1]) and direction[2]:
            d = "우측에"
        elif (not direction[0]) and direction[1] and (not direction[2]):
            d = "전방에"
        elif direction[0] and (not direction[1]) and (not direction[2]):
            d = "좌측에"
        elif direction[0] and direction[1] and direction[2]:
            d = "전방위에"
        return d

    def runmodule(self, classes, direction):
        if classes == -1:
            playsound.playsound('beep.wav')
            self.speak("인도 벗어남")
        elif classes == -2:
            playsound.playsound('beep.wav')
            self.speak("전방에" + ",," + "횡단보도")
        else:
            d = self.transform_dist(direction)
            c = self.transform_obj(classes)
            playsound.playsound('beep.wav')
            self.speak(d + ",," + c)


