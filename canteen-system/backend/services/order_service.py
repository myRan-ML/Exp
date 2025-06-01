from db_manager import DBManager
from tabulate import tabulate
import datetime
from flask import Blueprint, request, jsonify

class OrderService:
    def __init__(self, db: DBManager):
        self.db = db

    def place_order(self, uid, cart_items):
        total = 0
        for dno, qty in cart_items:
            cursor = self.db.execute("SELECT DPRICE, STOCK FROM dish WHERE DNO = %s", (dno,))
            row = cursor.fetchone()
            if not row:
                return {"success": False, "message": f"菜品 {dno} 不存在"}
            if row['STOCK'] < qty:
                return {"success": False, "message": f"菜品 {dno} 库存不足，仅剩 {row['STOCK']}"}
            total += row['DPRICE'] * qty

        cursor = self.db.execute("INSERT INTO orders (UID, TOTAL_AMOUNT) VALUES (%s, %s)", (uid, total))
        oid = cursor.lastrowid

        for dno, qty in cart_items:
            cursor = self.db.execute("SELECT DPRICE, STOCK FROM dish WHERE DNO = %s", (dno,))
            row = cursor.fetchone()
            price = row['DPRICE']
            self.db.execute(
                "INSERT INTO order_item (OID, DNO, QUANTITY, PRICE_AT_ORDER) VALUES (%s, %s, %s, %s)",
                (oid, dno, qty, price)
            )
            self.db.execute(
                "UPDATE dish SET STOCK = %s WHERE DNO = %s",
                (row['STOCK'] - qty, dno)
            )

        return {"success": True, "oid": oid, "total": total}

    def view_orders_by_user(self, uid):
        sql = "SELECT * FROM orders WHERE UID = %s"
        cursor = self.db.execute(sql, (uid,))
        orders = cursor.fetchall() if cursor else []
        result = []
        for order in orders:
            cursor = self.db.execute(
                "SELECT oi.DNO, d.DNAME, oi.QUANTITY, oi.PRICE_AT_ORDER "
                "FROM order_item oi JOIN dish d ON oi.DNO=d.DNO WHERE oi.OID = %s", (order['OID'],))
            items = cursor.fetchall()
            result.append({
                "oid": order["OID"],
                "order_time": order["ORDER_TIME"],
                "total": order["TOTAL_AMOUNT"],
                "items": items
            })
        return result

    def generate_sales_report(self, start_date, end_date):
        sql = "SELECT * FROM orders WHERE ORDER_TIME BETWEEN %s AND %s"
        cursor = self.db.execute(sql, (start_date, end_date))
        orders = cursor.fetchall() if cursor else []
        total_sum = sum(o['TOTAL_AMOUNT'] for o in orders)
        return {
            "total_sales": total_sum,
            "orders": orders
        }

# ========= 蓝图接口 ============
order_bp = Blueprint("order", __name__)
order_svc = OrderService(DBManager())

@order_bp.route("/place", methods=["POST"])
def place_order_api():
    data = request.get_json()
    uid = data.get("uid")
    cart = data.get("cart")  # 格式: [{ "dno": 1, "quantity": 2 }, ...]
    cart_items = [(item["dno"], item["quantity"]) for item in cart]
    result = order_svc.place_order(uid, cart_items)
    if result["success"]:
        return jsonify({
            "message": "下单成功",
            "oid": result["oid"],
            "total": result["total"]
        }), 201
    else:
        return jsonify({"error": result["message"]}), 400

@order_bp.route("/user/<int:uid>", methods=["GET"])
def get_user_orders_api(uid):
    orders = order_svc.view_orders_by_user(uid)
    return jsonify(orders), 200

@order_bp.route("/report", methods=["POST"])
def sales_report_api():
    data = request.get_json()
    start_date = data.get("start")
    end_date = data.get("end")
    report = order_svc.generate_sales_report(start_date, end_date)
    return jsonify(report), 200
# 生成销售报表的API
# @order_bp.route("/report", methods=["POST"])