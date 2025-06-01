from db_manager import DBManager
from tabulate import tabulate
from flask import Blueprint, request, jsonify

class EmpService:
    def __init__(self, db: DBManager):
        self.db = db

    def add_employee(self, emp):
        sql = "INSERT INTO emp (ENO, ENAME, ESEX, EJOB, ESAL) VALUES (%s, %s, %s, %s, %s)"
        self.db.execute(sql, (emp["ENO"], emp["ENAME"], emp["ESEX"], emp["EJOB"], emp["ESAL"]))
        print("员工添加成功!")

    def delete_employee(self, eno):
        sql = "DELETE FROM emp WHERE ENO = %s"
        cursor = self.db.execute(sql, (eno,))
        print(f"删除{cursor.rowcount}条记录")

    def update_salary(self, eno, new_sal):
        sql = "UPDATE emp SET ESAL = %s WHERE ENO = %s"
        self.db.execute(sql, (new_sal, eno))
        print("员工薪水更新成功!")

    def update_job(self, eno, new_job):
        sql = "UPDATE emp SET EJOB = %s WHERE ENO = %s"
        self.db.execute(sql, (new_job, eno))
        print("员工岗位更新成功!")

    def query_all(self):
        sql = "SELECT * FROM emp"
        cursor = self.db.execute(sql)
        rows = cursor.fetchall() if cursor else []
        if rows:
            data_list = [list(r.values()) for r in rows]
            headers = ["员工编号", "姓名", "性别", "岗位", "薪水"]
            print(tabulate(data_list, headers=headers, tablefmt='grid'))
        else:
            print("没有员工信息")

    # Web API 版本
    def get_all_employees(self):
        sql = "SELECT * FROM emp"
        cursor = self.db.execute(sql)
        return cursor.fetchall() if cursor else []

    def add_employee_api(self, emp):
        self.add_employee(emp)

    def delete_employee_api(self, eno):
        self.delete_employee(eno)

    def update_salary_api(self, eno, new_sal):
        self.update_salary(eno, new_sal)

    def update_job_api(self, eno, new_job):
        self.update_job(eno, new_job)


# ============ Flask 蓝图 ================
emp_bp = Blueprint("emp", __name__)
emp_service = EmpService(DBManager())

@emp_bp.route("/all", methods=["GET"])
def get_all():
    data = emp_service.get_all_employees()
    return jsonify(data), 200

@emp_bp.route("/add", methods=["POST"])
def add():
    emp = request.get_json()
    print(emp)  # 打印请求体
    required_keys = ["ENO", "ENAME", "ESEX", "EJOB", "ESAL"]
    if not all(k in emp for k in required_keys):
        return jsonify({"error": "参数不完整"}), 400
    emp_service.add_employee_api(emp)
    return jsonify({"message": "添加成功"}), 200


@emp_bp.route("/delete", methods=["DELETE"])
def delete():
    eno = request.args.get("eno")
    if not eno:
        return jsonify({"error": "缺少 eno 参数"}), 400
    emp_service.delete_employee_api(eno)
    return jsonify({"message": "删除成功"}), 200

@emp_bp.route("/update_salary", methods=["POST"])
def update_salary():
    data = request.get_json()
    eno = data.get("ENO")  # 前端传递的员工编号
    new_sal = data.get("ESAL")  # 前端传递的新薪水
    if not eno or new_sal is None:
        return jsonify({"error": "参数错误"}), 400
    
    # 通过员工编号（ENO）更新薪水
    emp_service.update_salary_api(eno, new_sal)
    
    return jsonify({"message": "薪水更新成功"}), 200


@emp_bp.route("/update_job", methods=["POST"])
def update_job():
    data = request.get_json()
    eno = data.get("ENO")
    new_job = data.get("EJOB")
    if not eno or not new_job:
        return jsonify({"error": "参数错误"}), 400
    emp_service.update_job_api(eno, new_job)
    return jsonify({"message": "岗位更新成功"}), 200