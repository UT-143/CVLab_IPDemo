import cv2
import openpifpaf
import caputure
import effect


class merge():
    def __init__(self, f):
        self.predictor = openpifpaf.Predictor(checkpoint='shufflenetv2k16')
        self.cap = caputure.caputure(self.predictor, f)
        # 画像名, 中心番地, サイズ, 必要検出, 基準ライン
        self.effects = [[["null", 0, 0, [], []] for i in range(3)] for i in range(10)]
        self.flag = False
        pass

    def drow(self, frame, detectionFrame):
        data = self.cap.frame(detectionFrame)
        if len(data) != 0: # 人が写っている時
            at = 0
            for d in data:
                if self.flag:
                    self.drowPoint(frame, d)
                if d[1][0] and d[5][0] and d[6][0] and d[9][0] and d[10][0] and d[2][0]:
                    if d[1][2] > d[9][2] and d[1][2] > d[10][2] and d[5][1]-d[2][1]+d[1][1] > d[9][1] and d[6][1]+d[2][1]-d[1][1] < d[10][1]:
                        self.clearEffects(at)
                        self.effects[at][0] = ["rabit_ear", 0, 6, [0, 1, 2], [1, 2]]
                        self.effects[at][1] = ["13", 9, 1, [7, 9], [7, 9]]
                        self.effects[at][2] = ["12", 10, 1, [8, 10], [8, 10]]
                if d[1][0] and d[5][0] and d[6][0] and d[9][0] and d[10][0] and d[2][0]:
                    if d[1][2] < d[9][2] and d[1][2] < d[10][2] and d[5][1]-d[2][1]+d[1][1] > d[9][1] and d[6][1]+d[2][1]-d[1][1] < d[10][1]:
                        self.clearEffects(at)
                        self.effects[at][0] = ["cat_ear", 0, 5, [0, 1, 2], [1, 2]]
                        self.effects[at][1] = ["cat_tail", 11, 3, [11, 12], [11, 12]]
                if d[1][0] and d[5][0] and d[6][0] and d[9][0] and d[10][0] and d[2][0]:
                    if d[1][2] < d[9][2] and d[5][2] > d[9][2] and d[2][2] < d[10][2] and d[6][2] > d[10][2] and d[5][1]-d[2][1]+d[1][1] < d[9][1] and d[9][1] < d[5][1]-(3*d[2][1])+(3*d[1][1]) and d[6][1]+d[2][1]-d[1][1] > d[10][1] and d[6][1]+(3*d[2][1])-(3*d[1][1]) < d[10][1]:
                        self.clearEffects(at)
                        # self.effects[at][0] = ["gogogo", 5, 5, [5, 6], [5, 6]]
                        self.effects[at][0] = ["tenshi_ring", 0, 5, [0, 1, 2], [1, 2]]
                        self.effects[at][1] = ["tenshi_hane_R", 6, 3, [5, 6], [5, 6]]
                        self.effects[at][2] = ["tenshi_hane_L", 5, 3, [5, 6], [5, 6]]
                if d[1][0] and d[5][0] and d[6][0] and d[9][0] and d[10][0] and d[2][0]:
                    if d[1][2] > d[9][2] and d[2][2] > d[10][2]and d[5][1]-d[2][1]+d[1][1] < d[9][1] and d[9][1] < d[5][1]-(3*d[2][1])+(3*d[1][1]) and d[6][1]+d[2][1]-d[1][1] > d[10][1] and d[6][1]+(3*d[2][1])-(3*d[1][1]) < d[10][1]:
                        self.clearEffects(at)
                        self.effects[at][0] = ["don", 0, 5, [0, 5, 6], [5, 6]]

                if d[9][0] and d[10][0]: # 左右手首検出できたら
                    if  d[9][1] < d[10][1]: # 重ならないクロスだったら
                        cv2.line(frame, (d[9][1], d[9][2]), (d[10][1], d[10][2]), (0, 255, 0), thickness=5)
                        self.clearEffects(at)
                for effectData in self.effects[at]:
                    if effectData[0] != "null":
                        flag = False
                        for t in effectData[3]:
                            if d[t][0]:
                                flag = True
                            else:
                                flag = False
                                break
                        if flag:
                            effect.effect(frame, d, effectData[0] + ".png", effectData[1], effectData[2], effectData[4][0], effectData[4][1])
                at += 1
                
        return frame

    def clearEffects(self, at):
        for i in range(3):
            self.effects[at][i] = ["null", 0, 5, [], []]

    def switchFlag(self):
        if self.flag:
            self.flag = False
        else:
            self.flag = True
        return

    def drowPoint(self, frame, d):
        if d[0][0]: # 鼻
            cv2.drawMarker(frame, (d[0][1], d[0][2]), (0, 0, 255), markerSize=30)
        if d[1][0]: # 左目
            cv2.drawMarker(frame, (d[1][1], d[1][2]), (0, 0, 255), markerSize=30)
        if d[2][0]: # 右目
            cv2.drawMarker(frame, (d[2][1], d[2][2]), (0, 0, 255), markerSize=30)
        if d[3][0]: # 左耳
            cv2.drawMarker(frame, (d[3][1], d[3][2]), (0, 0, 255), markerSize=30)
        if d[4][0]: # 右耳
            cv2.drawMarker(frame, (d[4][1], d[4][2]), (0, 0, 255), markerSize=30)
        if d[5][0]: # 左肩
            cv2.drawMarker(frame, (d[5][1], d[5][2]), (0, 0, 255), markerSize=30)
        if d[6][0]: # 右肩
            cv2.drawMarker(frame, (d[6][1], d[6][2]), (0, 0, 255), markerSize=30)
        if d[7][0]: # 左肘
            cv2.drawMarker(frame, (d[7][1], d[7][2]), (0, 0, 255), markerSize=30)
        if d[8][0]: # 右肘
            cv2.drawMarker(frame, (d[8][1], d[8][2]), (0, 0, 255), markerSize=30)
        if d[9][0]: # 左手首
            cv2.drawMarker(frame, (d[9][1], d[9][2]), (0, 0, 255), markerSize=30)
        if d[10][0]: # 右手首
            cv2.drawMarker(frame, (d[10][1], d[10][2]), (0, 0, 255), markerSize=30)
        if d[11][0]: # 左股関節
            cv2.drawMarker(frame, (d[11][1], d[11][2]), (0, 0, 255), markerSize=30)
        if d[12][0]: # 右股関節
            cv2.drawMarker(frame, (d[12][1], d[12][2]), (0, 0, 255), markerSize=30)
        if d[13][0]: # 左膝
            cv2.drawMarker(frame, (d[13][1], d[13][2]), (0, 0, 255), markerSize=30)
        if d[14][0]: # 右膝
            cv2.drawMarker(frame, (d[14][1], d[14][2]), (0, 0, 255), markerSize=30)
        if d[15][0]: # 
            cv2.drawMarker(frame, (d[15][1], d[15][2]), (0, 0, 255), markerSize=30)
        if d[16][0]: # 
            cv2.drawMarker(frame, (d[16][1], d[16][2]), (0, 0, 255), markerSize=30)
        

