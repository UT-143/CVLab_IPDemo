import cv2
import asyncio
import time
import merge

# cpuで処理してます

f = float(5)
me = merge.merge(f)
t = None
cam = cv2.VideoCapture(0)
cam.set(cv2.CAP_PROP_FPS, 10)
cv2.namedWindow("capture a photo", cv2.WINDOW_NORMAL)
cv2.resizeWindow("capture a photo", 1920, 1080)


while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    # pifpafで処理する画素値を下げている ※取得座標を変化させないといけない
    frame2 = cv2.resize(frame, dsize=None, fx=1/f , fy=1/f)
    frame2.flags.writeable = False
    frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
    

    frame = me.drow(frame, frame2)
    # 画像への書き込みを許可します。
    frame.flags.writeable = True

    frame = cv2.flip(frame, 1)
    # スクリーンショットの処理を開始
    if me.shot:
        t = time.time()
        print("count on")
        me.countFlag = True
        me.shot = False
    # スクリーンショットカウントが開始
    if me.countFlag:
        c = time.time()
        if c - t >= 3:
            me.printImg(frame)
            me.countFlag = False
        else:
            cv2.circle(frame, (100, 100), 80, (0, 255, 0), thickness=6)
            cv2.putText(frame,
                text=str(3 - int(c - t)),
                org=(70, 130),
                fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                fontScale=3.0,
                color=(0, 255, 0),
                thickness=3,
                lineType=cv2.LINE_4)


    cv2.imshow("capture a photo", frame)



    k = cv2.waitKey(1)
    # マーカーを表示
    if k == ord('q'):
        frame = me.switchFlag()
    # スクショカウントオン
    if k == ord('s'):
        me.switchShotOn()
    # 終了
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break

cam.release()

cv2.destroyAllWindows()
