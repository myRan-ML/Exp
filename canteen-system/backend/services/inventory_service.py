from db_manager import DBManager
from tabulate import tabulate
from flask import Blueprint, request, jsonify

class InventoryService:
    def __init__(self, db: DBManager):
        self.db = db
        self.ALERT_THRESHOLD = 10  # 库存低于该值时报警

    def view_inventory(self):
        sql = "SELECT DNO, DNAME, STOCK FROM dish"
        cursor = self.db.execute(sql)
        rows = cursor.fetchall() if cursor else []
        if rows:
            headers = ["菜品编号", "菜名", "库存"]
            data_list = [list(r.values()) for r in rows]
            print(tabulate(data_list, headers=headers, tablefmt='grid'))
            low = [r for r in rows if r['STOCK'] < self.ALERT_THRESHOLD]
            if low:
                print("\n库存报警提醒：以下菜品库存低于阈值：")
                for r in low:
                    print(f"{r['DNO']} - {r['DNAME']} 当前库存: {r['STOCK']}")
        else:
            print("没有菜品库存信息。")

    def update_stock(self, dno, new_stock):
        sql = "UPDATE dish SET STOCK = %s WHERE DNO = %s"
        self.db.execute(sql, (new_stock, dno))
        print("库存更新成功！")

    # 供 Web API 用的版本
    def get_inventory_list(self):
        cursor = self.db.execute("SELECT DNO, DNAME, STOCK FROM dish")
        return cursor.fetchall() if cursor else []

    def update_stock_api(self, dno, stock):
        self.db.execute("UPDATE dish SET STOCK = %s WHERE DNO = %s", (stock, dno))
        return True


# ========= 蓝图接口 ============
inventory_bp = Blueprint("inventory", __name__)
inventory_svc = InventoryService(DBManager())

@inventory_bp.route("/view", methods=["GET"])
def view_inventory_api():
    items = inventory_svc.get_inventory_list()
    low_stock = [item for item in items if item["STOCK"] < inventory_svc.ALERT_THRESHOLD]
    return jsonify({
        "inventory": items,
        "low_stock_alert": low_stock
    }), 200

@inventory_bp.route("/update", methods=["POST"])
def update_stock_api():
    data = request.get_json()
    dno = data.get("dno")
    new_stock = data.get("stock")
    if dno is None or new_stock is None:
        return jsonify({"error": "参数缺失"}), 400
    inventory_svc.update_stock_api(dno, new_stock)
    return jsonify({"message": "库存更新成功"}), 200

@inventory_bp.route("/all", methods=["GET"])
def get_all_inventory():
    items = inventory_svc.get_inventory_list()
    return jsonify(items), 200



