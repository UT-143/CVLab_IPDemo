import cv2
import openpifpaf
import caputure
import effect


class merge():
    def __init__(self, f):
        self.predictor = openpifpaf.Predictor(checkpoint='shufflenetv2k16')
        self.cap = caputure.caputure(self.predictor, f)
        pass

    def drow(self, frame, detectionFrame):
        data = self.cap.frame(detectionFrame)
        if len(data) != 0: # 人が写っている時
            for d in data:
                if d[0][0] and d[1][0]: # 鼻と左目
                    cv2.line(frame, (d[0][1], d[0][2]), (d[1][1], d[1][2]), (255, 0, 0), thickness=2)
                if d[0][0] and d[2][0]: # 鼻と右目
                    cv2.line(frame, (d[0][1], d[0][2]), (d[2][1], d[2][2]), (255, 0, 0), thickness=2)
                if d[1][0] and d[5][0] and d[6][0] and d[9][0] and d[10][0] and d[2][0]:
                    if d[1][2] > d[9][2] and d[1][2] > d[10][2] and d[5][1]-d[2][1]+d[1][1] > d[9][1] and d[6][1]+d[2][1]-d[1][1] < d[10][1]:
                        # print("pose")
                        cv2.line(frame, (d[1][1], d[1][2]+d[2][1]-d[1][1]), (d[1][1], d[1][2]-50), (255, 255, 255), thickness=5)
                        cv2.line(frame, (d[2][1], d[2][2]+d[2][1]-d[1][1]), (d[2][1], d[2][2]-50), (255, 255, 255), thickness=5)
                        effect.effect(frame, d, "13.png")
                if d[9][0] and d[10][0]: # 左右手首検出できたら
                    if  d[9][1] < d[10][1]: # 重ならないクロスだったら
                        cv2.line(frame, (d[9][1], d[9][2]), (d[10][1], d[10][2]), (0, 255, 0), thickness=5)
                
        return frame

