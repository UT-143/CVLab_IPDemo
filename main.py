import cv2
import caputure as cap
import openpifpaf

# cpuで処理してます

predictor = openpifpaf.Predictor(checkpoint='shufflenetv2k16')


cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FPS, 10)
cv2.namedWindow("press space to take a photo", cv2.WINDOW_NORMAL)
cv2.resizeWindow("press space to take a photo", 500, 300)

while True:
    ret, frame = cam.read()
    
    if not ret:
        print("failed to grab frame")
        break
    # パフォーマンスを向上させるために、画像を書き込みを不可にして参照渡しとします。
    frame.flags.writeable = False

    # BGR画像をRGBに変換します。
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    data = cap.frame(frame, predictor)
    # 画像への書き込みを許可します。
    frame.flags.writeable = True

    # RGB画像をBGRに変換します。
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    # lineの描画
    if len(data) != 0: # 人が写っている時
        for d in data:
            if d[0][0] and d[1][0]: # 鼻と左目
                cv2.line(frame, (d[0][1], d[0][2]), (d[1][1], d[1][2]), (255, 0, 0), thickness=2)
            if d[0][0] and d[2][0]: # 鼻と右目
                cv2.line(frame, (d[0][1], d[0][2]), (d[2][1], d[2][2]), (255, 0, 0), thickness=2)
    
    cv2.imshow("press space to take a photo", frame)

    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break

cam.release()

cv2.destroyAllWindows()