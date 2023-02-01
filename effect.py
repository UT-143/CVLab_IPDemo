import cv2

def effect(frame, data):
    main_frame = frame
    alpha_frame = cv2.imread("nc234071.png", cv2.IMREAD_UNCHANGED)  # アルファチャンネル込みで読み込む
    position = (data[0][1]-250, data[0][2]-280)

    #貼り付け座標の調整
    x1, y1 = max(position[0], 0), max(position[1], 0)
    x2 = min(position[0] + alpha_frame.shape[1], main_frame.shape[1])
    y2 = min(position[1] + alpha_frame.shape[0], main_frame.shape[0])
    ax1, ay1 = x1 - position[0], y1 - position[1]
    ax2, ay2 = ax1 + x2 - x1, ay1 + y2 - y1

    #透過素材と描画
    main_frame[y1:y2, x1:x2] = main_frame[y1:y2, x1:x2] * (1 - alpha_frame[ay1:ay2, ax1:ax2, 3:] / 255) + \
                          alpha_frame[ay1:ay2, ax1:ax2, :3] * (alpha_frame[ay1:ay2, ax1:ax2, 3:] / 255)