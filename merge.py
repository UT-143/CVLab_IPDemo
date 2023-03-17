import cv2
import openpifpaf
import datetime
import math
import caputure
import effect


class merge():
    def __init__(self, f):
        self.predictor = openpifpaf.Predictor(checkpoint='shufflenetv2k16')
        self.cap = caputure.caputure(self.predictor, f)
        # 画像名, 中心番地, サイズ, 必要検出, 基準ライン
        self.effects = [[["null", 0, 0, [], []] for i in range(3)] for i in range(10)]
        self.flag = False
        self.shot = False
        self.countFlag = False
        pass

    def drow(self, frame, detectionFrame):
        data = self.cap.frame(detectionFrame)
        if len(data) != 0: # 人が写っている時
            at = 0
            for d in data:
                if at == 10:
                    break
                if self.flag:
                    self.drowPoint(frame, d)
                self.selectEffects(d, at)
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
                            effect.effect(frame, d, "./effect/" + effectData[0] + ".png", effectData[1], effectData[2], effectData[4][0], effectData[4][1])
                at += 1
        
        return frame
    
    def selectEffects(self, d, at):
        #案１の検出
        # if d[5][0] and d[6][0] and d[7][0] and d[8][0] and d[9][0] and d[10][0] and d[15][0] and d[16][0]:
        #     if d[9][2] < d[7][2] and d[10][2] < d[8][2] and d[5][2] < d[9][2] and d[6][2] < d[10][2] and d[15][1]-d[16][1] > 50:
        #         self.clearEffects(at)
        #         self.effects[at][0] = ["1", 0, 5, [0, 1, 2], [1, 2]]
        #案2の検出
        if d[1][0] and d[2][0] and d[5][0] and d[6][0] and d[9][0] and d[10][0] and d[11][0] and d[12][0]:
            if d[10][1] > d[9][1] and d[5][1]-d[2][1]+d[1][1] > d[9][1] and d[6][1]+d[2][1]-d[1][1] < d[10][1] and d[5][2] < d[9][2] and d[6][2] < d[10][2] and d[11][2] > d[9][2] and d[12][2] > d[10][2]:
                self.clearEffects(at)
                self.effects[at][0] = ["don", 0, 5, [0, 5, 6], [5, 6]]
        # #案3の検出
        if d[1][0] and d[2][0] and d[9][0] and d[10][0]:
            radius_R = math.sqrt(pow(d[9][1] - d[0][1], 2) + pow(d[9][2] - d[0][2], 2))
            radius_L = math.sqrt(pow(d[10][1] - d[0][1], 2) + pow(d[10][2] - d[0][2], 2))
            if radius_R < 5 * abs(d[1][1] - d[2][1]) and radius_L < 5 * abs(d[1][1] - d[2][1]) and d[9][2] > d[10][2]:
                self.clearEffects(at)
                self.effects[at][0] = ["cat_ear", 0, 6, [0, 1, 2], [1, 2]]
                self.effects[at][1] = ["cat_tail", 11, 2.5, [11, 12], [11, 12]]
        # #案4の検出
        if d[1][0] and d[5][0] and d[6][0] and d[9][0] and d[10][0] and d[13][0] and d[14][0]:
            far_hand = abs(d[9][1] - d[10][1])
            far_sholder = abs(d[5][1] - d[6][1])
            far_knees = abs(d[13][1] - d[14][1])
            if far_hand > far_sholder * 2 and far_knees > far_sholder * 1.5 and d[9][2] < d[1][2]:
                self.clearEffects(at)
                self.effects[at][1] = ["grab_L", 9, 1.5, [7, 9], [7, 9]]
                self.effects[at][2] = ["grab_R", 10, 1.5, [8, 10], [8, 10]]
        #案5の検出
        if d[1][0] and d[2][0] and d[9][0] and d[10][0] and d[11][0] and d[12][0]:
            radius_R = math.sqrt(pow(d[9][1] - d[11][1], 2) + pow(d[9][2] - d[11][2], 2))
            radius_L = math.sqrt(pow(d[10][1] - d[12][1], 2) + pow(d[10][2] - d[12][2], 2))
            if radius_R < 3 * abs(d[1][1] - d[2][1]) and radius_L < 3 * abs(d[1][1] - d[2][1]):
                self.clearEffects(at)
                self.effects[at][0] = ["kirakira", 0, 5, [0, 5, 6], [5, 6]]
                self.effects[at][1] = ["kirakira", 0, 8, [0, 1, 2], [1, 2]]
        # エフェクトのクリア
        if d[5][0] and d[6][0] and d[9][0] and d[10][0]:
            if  abs(d[9][2] - d[10][2]) < 50 and abs(d[9][1] - d[10][1] > 3.5 * abs(d[5][1] - d[6][1])) and d[9][2] > d[5][2]:
                # cv2.line(frame, (d[9][1], d[9][2]), (d[10][1], d[10][2]), (0, 255, 0), thickness=5)
                self.clearEffects(at)

    def clearEffects(self, at):
        for i in range(3):
            self.effects[at][i] = ["null", 0, 0, [0], [0, 0]]

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

    def printImg(self, frame):
        dt_now = datetime.datetime.now()
        src = str(dt_now.day) + "_" +  str(dt_now.hour) + "_" +  str(dt_now.minute) + "_" + str(dt_now.second)
        cv2.imwrite('./img/' + src + '.jpg', frame)
        print('./img/' + src + '.jpg')
        return
    
    def switchShotOn(self):
        if not self.shot and not self.countFlag:
            print("shot on")
            self.shot = True
