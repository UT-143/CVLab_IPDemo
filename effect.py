import cv2
import math
import numpy as np
# エフェクトの付与を行うクラス
def effect(frame, data, imgPath, centerPoint, size, startLine, endLine, rotable):
    main_frame = frame
    alpha_frame = cv2.imread(imgPath, cv2.IMREAD_UNCHANGED)  # アルファチャンネル込みで読み込む
    w = alpha_frame.shape[1]
    lineX = data[startLine][1] - data[endLine][1]
    lineY = data[startLine][2] - data[endLine][2]
    f = math.sqrt(pow(lineX, 2) + pow(lineY, 2)) * size / w
    if f == 0:
        return
    if f < 0.5:
        f = 0.5
    alpha_frame = cv2.resize(alpha_frame, dsize=None, fx=f , fy=f)
    h = alpha_frame.shape[0]
    w = alpha_frame.shape[1]
    position = (data[centerPoint][1] - int(w/2), data[centerPoint][2]-int(h/2))
    # position = (data[0][1] - int(w/2), data[0][2]-h+data[2][1]-data[1][1])

    lineX = np.where(lineX == 0, 1, lineX)
    angle = math.degrees(math.atan2(-1 * lineY, lineX))
    if rotable:
        angle = 0
    trans = cv2.getRotationMatrix2D(center=(int(w/2), int(h/2)), angle=angle , scale=1.0)
    alpha_frame = cv2.warpAffine(src=alpha_frame, M=trans, dsize=(w,h))

    #貼り付け座標の調整
    x1, y1 = max(position[0], 0), max(position[1], 0)
    x2 = min(position[0] + alpha_frame.shape[1], main_frame.shape[1])
    y2 = min(position[1] + alpha_frame.shape[0], main_frame.shape[0])
    ax1, ay1 = x1 - position[0], y1 - position[1]
    ax2, ay2 = ax1 + x2 - x1, ay1 + y2 - y1

    #透過素材と描画
    main_frame[y1:y2, x1:x2] = main_frame[y1:y2, x1:x2] * (1 - alpha_frame[ay1:ay2, ax1:ax2, 3:] / 255) + \
                          alpha_frame[ay1:ay2, ax1:ax2, :3] * (alpha_frame[ay1:ay2, ax1:ax2, 3:] / 255)