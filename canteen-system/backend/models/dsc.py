class Dsc:
    """窗口信息模型"""
    def __init__(self, dno, dwin, dtime):
        self.DNO = dno
        self.DWIN = dwin
        self.DTIME = dtime  # 'mor', 'aft', 'eve'