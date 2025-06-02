from db_manager import DBManager
from flask import Blueprint, request, jsonify

class DishService:
    def __init__(self, db: DBManager):
        self.db = db

    def add_dish(self, dish):
        sql = "INSERT INTO dish (DNO, DNAME, DPRICE, DIMAGE, STOCK) VALUES (%s, %s, %s, %s, %s)"
        self.db.execute(sql, (dish["DNO"], dish["DNAME"], dish["DPRICE"], dish["DIMAGE"], dish["STOCK"]))
        print("菜品添加成功!")

    def delete_dish(self, dno):
        sql = "DELETE FROM dish WHERE DNO = %s"
        cursor = self.db.execute(sql, (dno,))
        print(f"删除{cursor.rowcount}条记录")

    def update_price(self, dno, new_price):
        sql = "UPDATE dish SET DPRICE = %s WHERE DNO = %s"
        self.db.execute(sql, (new_price, dno))
        print("菜品价格更新成功!")

    def query_all(self):
        # 查询时包含库存字段
        sql = "SELECT DNO, DNAME, DPRICE, DIMAGE, STOCK FROM dish"
        cursor = self.db.execute(sql)
        # 将查询结果转换为字典格式
        result = cursor.fetchall() if cursor else []
        # 确保返回的结果是字典格式
        return [
            {
                "DNO": row["DNO"],
                "DNAME": row["DNAME"],
                "DPRICE": row["DPRICE"],
                "DIMAGE": row["DIMAGE"],
                "STOCK": row["STOCK"]
            }
            for row in result
        ]

# =========== Flask 蓝图 ===========
dish_bp = Blueprint("dish", __name__)
dish_service = DishService(DBManager())

@dish_bp.route("/add", methods=["POST"])
def add_dish():
    dish = request.get_json()
    if not all(k in dish for k in ["DNO", "DNAME", "DPRICE", "DIMAGE", "STOCK"]):
        return jsonify({"error": "参数不完整"}), 400
    dish_service.add_dish(dish)
    return jsonify({"message": "菜品添加成功"}), 200


@dish_bp.route("/delete/<int:dno>", methods=["DELETE"])
def delete_dish(dno):
    dish_service.delete_dish(dno)
    return jsonify({"message": "删除成功"}), 200

@dish_bp.route("/update_price", methods=["PUT"])
def update_price():
    data = request.get_json()
    dno = data.get("DNO")
    price = data.get("DPRICE")
    if dno is None or price is None:
        return jsonify({"error": "缺少参数"}), 400
    dish_service.update_price(dno, price)
    return jsonify({"message": "价格更新成功"}), 200

@dish_bp.route("/all", methods=["GET"])
def get_all_dishes():
    data = dish_service.query_all()
    return jsonify(data), 200
