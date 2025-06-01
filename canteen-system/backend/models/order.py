class Order:
    """订单主表模型"""
    def __init__(self, oid, uid, order_time, total_amount):
        self.OID = oid
        self.UID = uid
        self.ORDER_TIME = order_time
        self.TOTAL_AMOUNT = total_amount

class OrderItem:
    """订单项表模型"""
    def __init__(self, oid, dno, quantity, price_at_order):
        self.OID = oid
        self.DNO = dno
        self.QUANTITY = quantity
        self.PRICE_AT_ORDER = price_at_order