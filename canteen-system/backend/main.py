from flask import Flask
from services.user_service import user_bp
from services.dish_service import dish_bp
from services.emp_service import emp_bp
from services.dsc_service import dsc_bp
from services.order_service import order_bp
from services.inventory_service import inventory_bp

from db_manager import DBManager
from models.employee import Employee
from models.dish import Dish
from models.dsc import Dsc
from models.user import User
from services.emp_service import EmpService
from services.dish_service import DishService
from services.dsc_service import DscService
from services.user_service import UserService
from services.order_service import OrderService
from services.inventory_service import InventoryService
import getpass
import datetime

app = Flask(__name__)
# 注册蓝图
app.register_blueprint(user_bp, url_prefix='/api/user')
app.register_blueprint(dish_bp, url_prefix='/api/dish')
app.register_blueprint(emp_bp, url_prefix='/api/employee')
app.register_blueprint(dsc_bp, url_prefix='/api/window')
app.register_blueprint(order_bp, url_prefix='/api/order')
app.register_blueprint(inventory_bp, url_prefix='/api/inventory')

def initial_prompt():
    print("1. 注册")
    print("2. 登录")
    print("3. 退出")
    return input("请选择: ")


def admin_menu():
    print("\n食堂信息管理系统（管理员）")
    print("1. 员工管理")
    print("2. 菜品管理")
    print("3. 窗口管理")
    print("4. 库存管理")
    print("5. 订单报表")
    print("6. 注销")
    return input("请选择操作: ")


def customer_menu():
    print("\n食堂信息管理系统（用户）")
    print("1. 浏览菜品")
    print("2. 下单")
    print("3. 查看我的订单")
    print("4. 注销")
    return input("请选择操作: ")


def emp_submenu(emp_svc):
    print("\n员工管理")
    print("1. 增加员工")
    print("2. 删除员工")
    print("3. 更新员工信息")
    print("4. 查询所有员工")
    print("5. 返回上级菜单")
    choice = input("请选择: ")
    if choice == '1':
        eno = input("员工编号: ")
        ename = input("姓名: ")
        esex = input("性别(M/F): ").upper()
        ejob = input("岗位: ")
        esal = int(input("薪水: "))
        emp = Employee(eno, ename, esex, ejob, esal)
        emp_svc.add_employee(emp)
    elif choice == '2':
        eno = input("输入要删除的员工编号: ")
        emp_svc.delete_employee(eno)
    elif choice == '3':
        print("1. 更新薪水 2. 更新岗位")
        c = input("请选择: ")
        if c == '1':
            eno = input("员工编号: ")
            new_sal = int(input("新薪水: "))
            emp_svc.update_salary(eno, new_sal)
        elif c == '2':
            eno = input("员工编号: ")
            new_job = input("新岗位: ")
            emp_svc.update_job(eno, new_job)
    elif choice == '4':
        emp_svc.query_all()
    # 5 -> 返回


def dish_submenu(dish_svc):
    print("\n菜品管理")
    print("1. 增加菜品")
    print("2. 删除菜品")
    print("3. 更新价格")
    print("4. 查询所有菜品")
    print("5. 返回上级菜单")
    choice = input("请选择: ")
    if choice == '1':
        dno = input("菜品编号: ")
        dname = input("菜品名称: ")
        dprice = int(input("价格: "))
        stock = int(input("初始库存: "))
        dish = Dish(dno, dname, dprice)
        dish_svc.add_dish(dish)
        # 紧接着更新库存
        dish_svc.db.execute("UPDATE dish SET STOCK=%s WHERE DNO=%s", (stock, dno))
        print("初始库存已设置。")
    elif choice == '2':
        dno = input("输入要删除的菜品编号: ")
        dish_svc.delete_dish(dno)
    elif choice == '3':
        dno = input("菜品编号: ")
        new_price = int(input("新价格: "))
        dish_svc.update_price(dno, new_price)
    elif choice == '4':
        dish_svc.query_all()
    # 5 -> 返回


def dsc_submenu(dsc_svc):
    print("\n窗口管理")
    print("1. 增加窗口信息")
    print("2. 删除窗口信息")
    print("3. 按窗口查询菜品")
    print("4. 返回上级菜单")
    choice = input("请选择: ")
    if choice == '1':
        dno = input("菜品编号: ")
        dwin = int(input("窗口号(1-6): "))
        dtime = input("上架时间(mor/aft/eve): ")
        dsc = Dsc(dno, dwin, dtime)
        dsc_svc.add_dsc(dsc)
    elif choice == '2':
        dno = input("菜品编号: ")
        dwin = int(input("窗口号: "))
        dtime = input("上架时间: ")
        dsc_svc.delete_dsc(dno, dwin, dtime)
    elif choice == '3':
        win = input("输入窗口号(1-6): ")
        dsc_svc.query_by_win(win)
    # 4 -> 返回


def inventory_submenu(inv_svc):
    print("\n库存管理")
    print("1. 查看库存")
    print("2. 更新库存")
    print("3. 返回上级菜单")
    choice = input("请选择: ")
    if choice == '1':
        inv_svc.view_inventory()
    elif choice == '2':
        dno = input("菜品编号: ")
        new_stock = int(input("新库存数量: "))
        inv_svc.update_stock(dno, new_stock)
    # 3 -> 返回


def order_report_submenu(order_svc):
    print("\n订单报表")
    start = input("起始日期 (YYYY-MM-DD): ")
    end = input("结束日期 (YYYY-MM-DD): ")
    # 转换为 datetime
    try:
        start_dt = datetime.datetime.strptime(start, "%Y-%m-%d")
        end_dt = datetime.datetime.strptime(end, "%Y-%m-%d") + datetime.timedelta(days=1)
        order_svc.generate_sales_report(start_dt, end_dt)
    except:
        print("日期格式不正确。")


def main():
    db = DBManager()
    if not db.cursor:
        print("无法连接数据库，系统退出!")
        return

    # 初始化各服务
    emp_svc = EmpService(db)
    dish_svc = DishService(db)
    dsc_svc = DscService(db)
    user_svc = UserService(db)
    order_svc = OrderService(db)
    inv_svc = InventoryService(db)

    while True:
        c = initial_prompt()
        if c == '1':  # 注册
            username = input("用户名: ")
            password = getpass.getpass("密码: ")
            role = input("角色 (admin/customer, 默认 customer): ") or 'customer'
            if role not in ('admin', 'customer'):
                role = 'customer'
            user_svc.register(username, password, role)
        elif c == '2':  # 登录
            username = input("用户名: ")
            password = getpass.getpass("密码: ")
            user = user_svc.login(username, password)
            if user:
                role = user['ROLE']
                uid = user['UID']
                # 管理员界面
                if role == 'admin':
                    while True:
                        choice = admin_menu()
                        if choice == '1':
                            emp_submenu(emp_svc)
                        elif choice == '2':
                            dish_submenu(dish_svc)
                        elif choice == '3':
                            dsc_submenu(dsc_svc)
                        elif choice == '4':
                            inventory_submenu(inv_svc)
                        elif choice == '5':
                            order_report_submenu(order_svc)
                        elif choice == '6':
                            print("已注销。")
                            break
                        else:
                            print("无效选项。")
                # 普通用户界面
                else:
                    while True:
                        choice = customer_menu()
                        if choice == '1':
                            dish_svc.query_all()
                        elif choice == '2':
                            # 简易购物车：输入多条 DNO:qty，以逗号分隔
                            cart_input = input("请输入购物车（格式 DNO:数量, 如 D001:2,D002:1）: ")
                            try:
                                cart_items = []
                                for part in cart_input.split(','):
                                    dno, qty = part.split(':')
                                    cart_items.append((dno, int(qty)))
                                order_svc.place_order(uid, cart_items)
                            except:
                                print("购物车格式不正确。")
                        elif choice == '3':
                            order_svc.view_orders_by_user(uid)
                        elif choice == '4':
                            print("已注销。")
                            break
                        else:
                            print("无效选项。")
        elif c == '3':
            print("系统已退出。")
            db.close()
            break
        else:
            print("无效选项，请重新输入！")


if __name__ == '__main__':
    # main()
    app.run(host='0.0.0.0', port=5000, debug=True)