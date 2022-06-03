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
            c = '사람'
        elif classes == 1:
            c = '전봇대'
        elif classes == 2:
            c = '기둥'
        elif classes == 3:
            c = '가로수'
        elif classes == 4:
            c = '차량'
        elif classes == 5:
            c = '신호등'
        elif classes == 6:
            c = '트럭'
        elif classes == 7:
            c = '버스'
        elif classes == 8:
            c = '신호등'
        elif classes == 9:
            c = '오토바이'
        elif classes == 10:
            c = '표지판'
        elif classes == 11:
            c = '화분'
        elif classes == 12:
            c = '휠체어'
        return c

    def transform_dist(self, distance):
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
        return d

    def runmodule(self, classes, distance):
        if classes == -1:
            playsound.playsound('beep.wav')
            self.speak("인도 벗어남")
        else:
            d = self.transform_dist(distance)
            c = self.transform_obj(classes)
            playsound.playsound('beep.wav')
            self.speak(d + ",," + c)

