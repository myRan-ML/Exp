from db_manager import DBManager
from flask import Blueprint, request, jsonify

class DscService:
    def __init__(self, db: DBManager):
        self.db = db

    def add_dsc(self, dsc):
        sql = "INSERT INTO dsc (DNO, DWIN, DTIME) VALUES (%s, %s, %s)"
        self.db.execute(sql, (dsc["DNO"], dsc["DWIN"], dsc["DTIME"]))
        print("窗口信息添加成功!")

    def delete_dsc(self, dno, dwin, dtime):
        sql = "DELETE FROM dsc WHERE DNO=%s AND DWIN=%s AND DTIME=%s"
        cursor = self.db.execute(sql, (dno, dwin, dtime))
        print(f"删除{cursor.rowcount}条记录")

    def query_by_win(self, win):
        sql = """
            SELECT d.DNO, d.DNAME, d.DPRICE, s.DWIN, s.DTIME 
            FROM dish d 
            JOIN dsc s ON d.DNO = s.DNO 
            WHERE s.DWIN = %s
        """
        cursor = self.db.execute(sql, (win,))
        return cursor.fetchall() if cursor else []

# ============ Flask 蓝图 ============
dsc_bp = Blueprint("dsc", __name__)
dsc_service = DscService(DBManager())

@dsc_bp.route("/add", methods=["POST"])
def add_dsc():
    dsc = request.get_json()
    if not all(k in dsc for k in ["DNO", "DWIN", "DTIME"]):
        return jsonify({"error": "参数不完整"}), 400
    dsc_service.add_dsc(dsc)
    return jsonify({"message": "添加成功"}), 200

@dsc_bp.route("/delete", methods=["DELETE"])
def delete_dsc():
    dno = request.args.get("dno")
    dwin = request.args.get("dwin")
    dtime = request.args.get("dtime")
    if not all([dno, dwin, dtime]):
        return jsonify({"error": "缺少参数"}), 400
    dsc_service.delete_dsc(dno, dwin, dtime)
    return jsonify({"message": "删除成功"}), 200

@dsc_bp.route("/by_window", methods=["GET"])
def query_by_window():
    win = request.args.get("win")
    if not win:
        return jsonify({"error": "缺少窗口号"}), 400
    data = dsc_service.query_by_win(win)
    return jsonify(data), 200

@dsc_bp.route('/api/window/all', methods=['GET'])
def get_all_windows():
    try:
        # 假设数据库中窗口号存储在 `window` 表中的 `DWIN` 列
        query = "SELECT DWIN FROM window"
        db = DBManager()
        cursor = db.execute(query)
        windows = cursor.fetchall() if cursor else []
        return jsonify(windows), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



