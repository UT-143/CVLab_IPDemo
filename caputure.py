# pifpafで座標を取得し返すクラス
class caputure():
    def __init__(self, predictor, f):
        self.predictor = predictor
        self.f = f
        pass

    def frame(self, frame):
        data = []
        predictions, gt_anns, meta = self.predictor.numpy_image(frame)
        for prediction in predictions:
            d = []
            for info in prediction.data:
                ret = False
                if int(info[0]) !=0 and int(info[1]) != 0:
                    ret = True
                # 0番目：存在するかどうかのタグ、1番目：x座標、2番目：y座標
                d.append([ret, int(info[0]*self.f), int(info[1]*self.f)])
            data.append(d)
        return data # data[0]に1人目の情報、data[0][0]に鼻の情報、data[0][0][1]に鼻のx座標
