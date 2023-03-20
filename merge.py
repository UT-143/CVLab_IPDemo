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
        self.effects = [[["null", 0, 0, [], [], False] for i in range(3)] for i in range(10)]
        # マーカーのフラグ
        self.flag = False
        # スクショカウントのフラグ
        self.shot = False
        # カウントが開始してるかどうかのフラグ
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
                            try:
                                effect.effect(frame, d, "./effect/" + effectData[0] + ".png", effectData[1], effectData[2], effectData[4][0], effectData[4][1], effectData[5])
                            except:
                                print()
                at += 1
        
        return frame
    
    # 付与するエフェクトの判定する関数
    def selectEffects(self, d, at):
        #案１の検出
        if d[5][0] and d[6][0] and d[7][0] and d[8][0] and d[9][0] and d[10][0]:
            far_sholder = abs(d[5][1] - d[6][1])
            if d[9][1] > d[5][1] and d[9][2] > d[5][2] and d[9][1] < d[5][1] + far_sholder * 1.5 and d[10][1] < d[6][1] and d[10][2] > d[6][2] and d[10][1] > d[6][1] - far_sholder * 1.5 and d[9][1] > d[7][1] and d[9][2] < d[7][2]and d[10][1] < d[8][1] and d[10][2] < d[8][2]:
                self.clearEffects(at)
                self.effects[at][0] = ["power", 0, 8, [0, 5, 6], [5, 6], True]
        #案2の検出
        if d[1][0] and d[2][0] and d[5][0] and d[6][0] and d[9][0] and d[10][0] and d[11][0] and d[12][0]:
            if d[10][1] > d[9][1] and d[5][1]-d[2][1]+d[1][1] > d[9][1] and d[6][1]+d[2][1]-d[1][1] < d[10][1] and d[5][2] < d[9][2] and d[6][2] < d[10][2] and d[11][2] > d[9][2] and d[12][2] > d[10][2]:
                self.clearEffects(at)
                self.effects[at][0] = ["don", 0, 5, [0, 5, 6], [5, 6], True]
        #案3の検出
        if d[1][0] and d[2][0] and d[9][0] and d[10][0]:
            radius_R = math.sqrt(pow(d[9][1] - d[0][1], 2) + pow(d[9][2] - d[0][2], 2))
            radius_L = math.sqrt(pow(d[10][1] - d[0][1], 2) + pow(d[10][2] - d[0][2], 2))
            if radius_R < 5 * abs(d[1][1] - d[2][1]) and radius_L < 5 * abs(d[1][1] - d[2][1]) and d[9][2] > d[10][2]:
                self.clearEffects(at)
                self.effects[at][0] = ["cat_ear", 0, 6, [0, 1, 2], [1, 2], False]
                self.effects[at][1] = ["cat_tail", 11, 2.5, [11, 12], [11, 12], False]
        # #案4の検出
        if d[0][0] and d[5][0] and d[6][0] and d[9][0] and d[10][0] and d[13][0] and d[14][0]:
            far_hand = abs(d[9][1] - d[10][1])
            far_sholder = abs(d[5][1] - d[6][1])
            far_knees = abs(d[13][1] - d[14][1])
            if far_hand > far_sholder * 2 and far_knees > far_sholder * 1.5 and d[9][2] < d[0][2] and d[10][2] < d[0][2] and d[9][2] > d[0][2] - far_sholder and d[10][2] > d[0][2] - far_sholder:
                self.clearEffects(at)
                self.effects[at][1] = ["grab_L", 9, 1.5, [7, 9], [7, 9], False]
                self.effects[at][2] = ["grab_R", 10, 1.5, [8, 10], [8, 10], False]
        #案5の検出
        if d[1][0] and d[2][0] and d[9][0] and d[10][0] and d[11][0] and d[12][0]:
            radius_R = math.sqrt(pow(d[9][1] - d[11][1], 2) + pow(d[9][2] - d[11][2], 2))
            radius_L = math.sqrt(pow(d[10][1] - d[12][1], 2) + pow(d[10][2] - d[12][2], 2))
            if radius_R < 3 * abs(d[1][1] - d[2][1]) and radius_L < 3 * abs(d[1][1] - d[2][1]):
                self.clearEffects(at)
                self.effects[at][0] = ["kirakira", 0, 5, [0, 5, 6], [5, 6], True]
                self.effects[at][1] = ["kirakira", 0, 8, [0, 1, 2], [1, 2], True]
        # エフェクトのクリア
        if d[5][0] and d[6][0] and d[9][0] and d[10][0]:
            if  abs(d[9][2] - d[10][2]) < 50 and abs(d[9][1] - d[10][1] > 3 * abs(d[5][1] - d[6][1])) and d[9][2] > d[5][2]:
                # cv2.line(frame, (d[9][1], d[9][2]), (d[10][1], d[10][2]), (0, 255, 0), thickness=5)
                self.clearEffects(at)

    # エフェクトをクリアする関数
    def clearEffects(self, at):
        for i in range(3):
            self.effects[at][i] = ["null", 0, 0, [0], [0, 0], False]

    # マーカーオンオフを判定する関数
    def switchFlag(self):
        if self.flag:
            self.flag = False
        else:
            self.flag = True
        return

    # マーカーを取得座標に描画するクラス
    def drowPoint(self, frame, d):
        for i in range(17):
            if d[i][0]:
                cv2.drawMarker(frame, (d[i][1], d[i][2]), (0, 0, 255), markerSize=30)
    # 画像を出力するクラス
    def printImg(self, frame):
        dt_now = datetime.datetime.now()
        src = str(dt_now.day) + "_" +  str(dt_now.hour) + "_" +  str(dt_now.minute) + "_" + str(dt_now.second)
        cv2.imwrite('./img/' + src + '.jpg', frame)
        print('./img/' + src + '.jpg')
        return
    
    # スクショカウントのオンオフ関数
    def switchShotOn(self):
        if not self.shot and not self.countFlag:
            print("shot on")
            self.shot = True
