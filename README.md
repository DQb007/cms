# 课程管理系统

一个基于 `FastAPI + MySQL + Vue 3` 的课程管理系统。前台用于公开浏览和检索课程，后台用于管理员登录后维护课程数据，并支持管理员修改密码。

## 功能概览

- 前台课程检索：课程编码、课程名称、课程类型、价格区间筛选
- 前台课程展示：桌面端表格展示，手机端自动切换为课程卡片
- 分页浏览：支持每页条数切换、页码跳转
- 后台登录：Bearer Token 登录态
- 后台课程管理：新增、编辑、删除、查询、分页
- 管理员改密：登录后可修改当前管理员密码
- MySQL 数据库：兼容指定的 `course`、`user` 表结构
- 响应式适配：兼容桌面、平板、手机

## 技术栈

- 后端：Python、FastAPI、SQLAlchemy、PyMySQL、Uvicorn
- 前端：Vue 3、Vite、TypeScript、Element Plus、Pinia、Vue Router、Axios
- 数据库：MySQL

## 目录结构

```text
cms/
  backend/              FastAPI 后端
    app/
      routers/          API 路由
      config.py         环境配置
      database.py       数据库连接
      init_db.py        初始化表和默认数据
      main.py           应用入口
      models.py         SQLAlchemy 模型
      schemas.py        Pydantic 请求/响应模型
      security.py       密码哈希和 Token 逻辑
    .env.example        后端环境变量示例
    requirements.txt    后端依赖
  database/
    schema.sql          MySQL 建表与示例数据 SQL
  frontend/             Vue 3 前端
    src/
      api/              Axios API 封装
      router/           前端路由
      stores/           Pinia 状态
      styles/           全局样式和响应式样式
      views/            页面
    package.json
  README.md
```

## 环境要求

- Python 3.11+
- Node.js 20+
- MySQL 5.7+ 或 MySQL 8+

MySQL 8 默认认证方式可能需要 `cryptography`，项目依赖中已包含。

## 数据库初始化

方式一：使用 SQL 脚本创建数据库、表和默认数据。

```bash
mysql -uroot -p < database/schema.sql
```

方式二：使用后端初始化脚本。先完成后端 `.env` 配置，再执行：

```bash
cd backend
python -m app.init_db
```

默认管理员：

```text
用户名：admin
密码：admin123
```

首次部署后建议登录后台立即修改默认密码。

## 后端启动

进入后端目录：

```bash
cd backend
```

创建并启用虚拟环境：

```bash
python3 -m venv .venv
source venv/bin/activate
```

安装依赖：

```bash
pip install -r requirements.txt
```

复制环境变量文件：

```bash
copy .env.example .env
```

编辑 `backend/.env`：

```text
APP_NAME=Course Management System
APP_SECRET_KEY=请改成随机长字符串
DATABASE_URL=mysql+pymysql://root:password@127.0.0.1:3306/cms?charset=utf8mb4
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

如果 MySQL 账号没有密码：

```text
DATABASE_URL=mysql+pymysql://root:@127.0.0.1:3306/cms?charset=utf8mb4
```

初始化数据库：

```bash
python -m app.init_db
```

启动服务：

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

如果 8000 端口被占用：

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

接口文档：

```text
http://127.0.0.1:8000/docs
```

## 前端启动

进入前端目录：

```bash
cd frontend
```

安装依赖：

```bash
npm install
```

启动开发服务：

```bash
npm run dev
```

如果后端不是 8000 端口，例如后端运行在 8001：

```bash
set VITE_API_PROXY_TARGET=http://127.0.0.1:8001
npm run dev
```

访问地址：

```text
前台首页：http://127.0.0.1:5173/
后台登录：http://127.0.0.1:5173/login
后台管理：http://127.0.0.1:5173/admin
```

## 前端构建

```bash
cd frontend
npm run build
```

构建产物位于：

```text
frontend/dist/
```

## 后台使用

1. 访问 `http://127.0.0.1:5173/login`
2. 使用管理员账号登录
3. 进入课程管理页面后，可新增、编辑、删除课程
4. 点击右上角管理员菜单，可修改密码或退出登录

修改密码成功后会自动退出登录，需要使用新密码重新登录。

## 响应式适配

- 桌面端：课程列表以表格展示，适合横向信息对比
- 平板端：筛选区自动换行，表格保持可读宽度
- 手机端：前台课程列表自动切换为卡片列表，避免表格被压缩
- 手机端后台：头部、筛选表单、弹窗宽度和表格横向滚动做了适配

## 主要 API

认证：

```text
POST /api/auth/login
GET  /api/auth/me
PUT  /api/auth/password
```

课程：

```text
GET    /api/courses
GET    /api/courses/categories
POST   /api/courses
PUT    /api/courses/{course_id}
DELETE /api/courses/{course_id}
```

健康检查：

```text
GET /api/health
```

## 课程查询参数

`GET /api/courses` 支持：

```text
code        课程编码，模糊匹配
name        课程名称，模糊匹配
category    课程类型，精确匹配
price_min   最低价格
price_max   最高价格
page        页码，默认 1
page_size   每页条数，默认 10，最大 100
```

## 数据表

`course` 表字段：

```text
id, code, name, url, price, category,
create_time, creator, modify_time, modifier
```

`user` 表字段：

```text
id, username, password, age, salt,
create_time, creator, modify_time, modifier
```

密码存储方式为：

```text
sha256(salt + password)
```

## 常见问题

### 1. MySQL 连接失败

检查 `backend/.env` 中的 `DATABASE_URL` 是否正确，重点确认用户名、密码、端口和数据库名。

### 2. 端口被占用

后端可以换端口：

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

前端同步设置代理：

```bash
set VITE_API_PROXY_TARGET=http://127.0.0.1:8001
npm run dev
```

### 3. 前端请求 404 或 500

先确认后端健康检查是否正常：

```text
http://127.0.0.1:8000/api/health
```

如果后端使用 8001，请访问：

```text
http://127.0.0.1:8001/api/health
```

### 4. 中文显示乱码

浏览器页面和 API 使用 UTF-8。若 PowerShell 输出乱码，通常是终端编码显示问题，不代表接口返回内容乱码。

## 验证命令

后端语法检查：

```bash
python -m compileall backend\app
```

前端构建检查：

```bash
cd frontend
npm run build
```
