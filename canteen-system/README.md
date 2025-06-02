# 南航智慧食堂管理系统

## 简介

这是一个基于 Python 和 Vue 的智慧食堂信息管理系统，主要用于南航食堂的信息管理。系统支持管理员和普通用户两种角色，具备以下功能：
- **用户管理**：支持用户注册、登录和权限校验（管理员 vs 普通用户）。
- **订单管理**：用户可以浏览菜品、下单并查看自己的订单，管理员可以查看所有订单、生成统计报表。
- **库存管理**：系统支持手动或自动更新库存，并提供库存报警功能。
- **菜品管理**：管理员可以管理菜品、员工信息、窗口信息等。

## 系统架构

本系统包含前端和后端两部分，前端使用 Vue 3 和 Vite 构建，后端使用 Python 的 Flask 框架开发。

- **前端**：Vue 3 + Vite
- **后端**：Flask + MySQL

## 项目结构

```
├── backend # 后端文件夹
│ ├── models # 数据库模型
│ ├── services # 业务逻辑
│ ├── main.py # 后端主文件
│ └── pycache # Python 编译文件
├── frontend # 前端文件夹
│ ├── images # 图片资源
│ ├── node_modules # 前端依赖
│ └── src # 前端源代码
│ ├── components # Vue 组件
│ ├── views # 页面视图
│ ├── App.vue # 主入口组件
│ └── router # 路由配置
└── README.md # 项目说明文件
```


## 功能说明

### 1. 用户管理
- 支持 **管理员** 和 **普通用户** 角色。
- **管理员** 可进行员工、菜品、窗口信息、库存管理等。
- **普通用户** 可浏览菜品、下单并查看自己的订单。

### 2. 订单管理
- **普通用户** 可以浏览菜品、提交订单，系统会自动扣减库存。
- **管理员** 可以查看所有订单、生成统计报表（按时间段统计销售总额）。

### 3. 库存管理
- 每次下单后，系统会自动减少相应菜品的库存。
- **管理员** 可以手动调整库存，并且当库存低于阈值时会有报警提示。

### 4. 菜品管理
- **管理员** 可以管理菜品的名称、价格、库存等信息。
- 菜品信息可以与窗口进行关联，确保窗口的菜品按时供应。

## 环境准备

### 1. 安装依赖

#### 后端环境
- 安装 Python 3.8 或更高版本。
- 安装后端依赖：
```bash
  pip install -r requirements.txt
```
#### 前端环境
- 安装 Node.js 和 npm。
- 安装前端依赖：
```bash
npm install
```

### 2. 配置 MySQL

确保本地已安装 MySQL，并创建一个名为 canteen 的数据库。执行以下 SQL 语句来创建数据库和用户：

```sql
CREATE DATABASE canteen CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'canteen_user'@'localhost' IDENTIFIED BY 'yourpassword';
GRANT ALL PRIVILEGES ON canteen.* TO 'canteen_user'@'localhost';
FLUSH PRIVILEGES;
```

在 canteen 数据库中执行以下建表语句：
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

-- 用户表：存储登录信息，密码使用简单哈希
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

## 启动项目

### 启动前端

在 frontend 目录下，运行以下命令启动前端：
```bash
npm run dev
```
这会启动 Vite 开发服务器，默认访问地址为 http://localhost:3000

### 启动后端
在 backend 目录下，运行以下命令启动后端：
```bash
python3 main.py
```
后端会运行在 http://127.0.0.1:5000

可以在 frontend/package.json 中配置 concurrently，使用以下命令同时启动前后端：
```bash
npm run dev
```

## TODO
- 完善前端页面的样式，增加更多交互功能。

- 优化后端 API，增加数据验证和错误处理。

- 完善库存报警系统，增加邮件或短信通知功能。