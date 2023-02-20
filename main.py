import cv2
import merge

# cpuで処理してます

f = float(5)
me = merge.merge(f)
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

    # pifpafで処理する画素値を下げている ※取得座標を変化させないといけない
    frame2 = cv2.resize(frame, dsize=None, fx=1/f , fy=1/f)
    frame2.flags.writeable = False
    frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
    
    # RGB画像をBGRに変換します。
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    frame = me.drow(frame, frame2)
    # 画像への書き込みを許可します。
    frame.flags.writeable = True

    frame = cv2.flip(frame, 1)
    cv2.imshow("press space to take a photo", frame)

    k = cv2.waitKey(1)
    if k == ord('q'):
        frame = me.switchFlag()
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break

cam.release()

cv2.destroyAllWindows()