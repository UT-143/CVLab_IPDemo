
def test():
    print("ok")
    print("finish")

def frame(frame, predictor):
    data = []
    predictions, gt_anns, meta = predictor.numpy_image(frame)
    for prediction in predictions:
        d = []
        for info in prediction.data:
            ret = False
            if int(info[0]) !=0 and int(info[1]) != 0:
                ret = True
            # 0番目：存在するかどうかのタグ、1番目：x座標、2番目：y座標
            d.append([ret, int(info[0]), int(info[1])])
        data.append(d)

    return data # data[0]に1人目の情報、data[0][0]に鼻の情報、data[0][0][1]に鼻のx座標