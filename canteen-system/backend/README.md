# 南航食堂信息管理系统（功能扩展版）

## 简介
这一版在基础 CRUD（员工、菜品、窗口信息）的功能之上，增加了：
- 用户管理：注册、登录、权限校验（管理员 vs 普通用户）
- 订单管理：用户下单、查询、统计报表
- 库存管理：手动或自动更新库存数量、库存报警

## 环境准备
1. 安装 Python 3.8+
2. 创建并激活虚拟环境（可选）：
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\\Scripts\\activate  # Windows
   ```
3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
4. 配置 MySQL：
   - 确保本地已安装 MySQL，并创建一个名为 `canteen` 的数据库。
   - 创建用户 `canteen_user` 并授予权限：
     ```sql
     CREATE DATABASE canteen CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
     CREATE USER 'canteen_user'@'localhost' IDENTIFIED BY 'myRan20041118@';
     GRANT ALL PRIVILEGES ON canteen.* TO 'canteen_user'@'localhost';
     FLUSH PRIVILEGES;
     ```
   - 在 `canteen` 数据库中执行以下建表语句：
     ```sql
     -- 员工、菜品、窗口信息表（与上一版相同）
     CREATE TABLE emp (
         ENO VARCHAR(10) PRIMARY KEY,
         ENAME VARCHAR(50) NOT NULL,
         ESEX CHAR(1) NOT NULL,
         EJOB VARCHAR(50),
         ESAL INT
     );

     CREATE TABLE dish (
         DNO VARCHAR(10) PRIMARY KEY,
         DNAME VARCHAR(100) NOT NULL,
         DPRICE INT,
         STOCK INT DEFAULT 0  -- 新增库存字段
     );

     CREATE TABLE dsc (
         DNO VARCHAR(10),
         DWIN INT,
         DTIME ENUM('mor', 'aft', 'eve'),
         PRIMARY KEY (DNO, DWIN, DTIME),
         FOREIGN KEY (DNO) REFERENCES dish(DNO)
     );

     -- 用户表：存储登录信息，密码使用简单哈希（生产可换更安全方案）
     CREATE TABLE user (
         UID INT AUTO_INCREMENT PRIMARY KEY,
         USERNAME VARCHAR(50) UNIQUE NOT NULL,
         PASSWORD_HASH VARCHAR(128) NOT NULL,
         ROLE ENUM('admin','customer') DEFAULT 'customer'
     );

     -- 订单表：一张订单对应多个菜品，可简化为“订单主表 + 订单项表”
     CREATE TABLE orders (
         OID INT AUTO_INCREMENT PRIMARY KEY,
         UID INT,
         ORDER_TIME DATETIME DEFAULT CURRENT_TIMESTAMP,
         TOTAL_AMOUNT INT,
         FOREIGN KEY (UID) REFERENCES user(UID)
     );

     CREATE TABLE order_item (
         OID INT,
         DNO VARCHAR(10),
         QUANTITY INT,
         PRICE_AT_ORDER INT,
         PRIMARY KEY (OID, DNO),
         FOREIGN KEY (OID) REFERENCES orders(OID),
         FOREIGN KEY (DNO) REFERENCES dish(DNO)
     );
     ```

## 依赖
```
# requirements.txt
pymysql
tabulate
bcrypt              # 用于密码哈希
```

## 主要功能说明
1. **用户注册/登录**：
   - 支持管理员(admin)与普通用户(customer)角色。只有管理员可进行员工、菜品、窗口信息、库存等管理；普通用户只能下单、查看订单、查询菜品。
2. **订单管理**：
   - 普通用户可浏览所有菜品、提交订单，系统会扣减对应库存。
   - 管理员可查看所有订单、导出简易报表（统计某时间段销售总额）。
3. **库存管理**：
   - 每次下单成功后，自动减少相应菜品库存。
   - 管理员可手动调整库存；当库存低于阈值时，系统会在查询时给出报警提示。

## 运行方式
```bash
python main.py
```

### 演示示例
1. 启动后首先出现登录/注册界面：
```
1. 注册
2. 登录
请选择: 
```
2. 普通用户注册并登录后：
```
登录成功！角色：customer

食堂信息管理系统
1. 浏览菜品
2. 下单
3. 查看我的订单
4. 退出系统
请选择操作: 
```
3. 管理员登录后：
```
登录成功！角色：admin

食堂信息管理系统
1. 员工管理
2. 菜品管理
3. 窗口管理
4. 库存管理
5. 订单报表
6. 注销
请选择操作: 
```
