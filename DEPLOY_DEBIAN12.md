# Debian 12 部署文档

本文档说明如何将课程管理系统部署到 Debian 12 服务器。部署方式为：

- Nginx 托管前端静态文件
- Nginx 将 `/api` 反向代理到 FastAPI
- FastAPI 通过 systemd 常驻运行
- MySQL 保存课程和管理员数据

示例域名使用 `course.example.com`，请替换为你的真实域名或服务器 IP。

## 1. 环境准备

使用 root 用户或具备 sudo 权限的用户执行。

```bash
sudo apt update
sudo apt install -y nginx mysql-server python3 python3-venv python3-pip curl git build-essential
```

安装 Node.js 20：

```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
node -v
npm -v
```

## 2. 创建数据库

登录 MySQL：

```bash
sudo mysql
```

创建数据库和用户：

```sql
CREATE DATABASE cms DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'cms_user'@'localhost' IDENTIFIED BY '请修改为强密码';
GRANT ALL PRIVILEGES ON cms.* TO 'cms_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

## 3. 上传代码

推荐部署目录：

```bash
sudo mkdir -p /opt/course-cms
sudo chown -R $USER:$USER /opt/course-cms
```

将项目代码上传到：

```text
/opt/course-cms
```

目录结构应类似：

```text
/opt/course-cms/
  backend/
  frontend/
  database/
  README.md
```

## 4. 配置后端

进入后端目录：

```bash
cd /opt/course-cms/backend
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

创建环境变量文件：

```bash
cp .env.example .env
nano .env
```

示例配置：

```env
APP_NAME=Course Management System
APP_SECRET_KEY=请修改为随机长字符串
DATABASE_URL=mysql+pymysql://cms_user:请修改为强密码@127.0.0.1:3306/cms?charset=utf8mb4
CORS_ORIGINS=http://course.example.com,https://course.example.com
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

初始化数据库表和默认管理员：

```bash
python -m app.init_db
```

默认管理员：

```text
用户名：admin
密码：admin123
```

部署完成后请立即登录后台修改默认密码。

## 5. 配置 systemd 后端服务

创建服务文件：

```bash
sudo nano /etc/systemd/system/course-cms-backend.service
```

写入：

```ini
[Unit]
Description=Course CMS FastAPI Backend
After=network.target mysql.service

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/opt/course-cms/backend
Environment="PATH=/opt/course-cms/backend/.venv/bin"
ExecStart=/opt/course-cms/backend/.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

调整目录权限：

```bash
sudo chown -R www-data:www-data /opt/course-cms
```

启动后端：

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now course-cms-backend
sudo systemctl status course-cms-backend
```

检查接口：

```bash
curl http://127.0.0.1:8000/api/health
```

## 6. 构建前端

进入前端目录：

```bash
cd /opt/course-cms/frontend
sudo -u www-data npm install
sudo -u www-data npm run build
```

构建产物位于：

```text
/opt/course-cms/frontend/dist
```

## 7. 配置 Nginx

创建站点配置：

```bash
sudo nano /etc/nginx/sites-available/course-cms
```

写入：

```nginx
server {
    listen 80;
    server_name course.example.com;

    root /opt/course-cms/frontend/dist;
    index index.html;

    client_max_body_size 10m;

    location /api/ {
        proxy_pass http://127.0.0.1:8000/api/;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location / {
        try_files $uri $uri/ /index.html;
    }

    location ~* \.(js|css|png|jpg|jpeg|gif|svg|ico|woff2?)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
        try_files $uri =404;
    }
}
```

启用站点：

```bash
sudo ln -s /etc/nginx/sites-available/course-cms /etc/nginx/sites-enabled/course-cms
sudo nginx -t
sudo systemctl reload nginx
```

访问：

```text
前台首页：http://course.example.com/
后台登录：http://course.example.com/login
后台管理：http://course.example.com/admin/courses
```

## 8. HTTPS 配置

如果域名已解析到服务器，可以使用 Certbot 配置 HTTPS：

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d course.example.com
```

完成后访问：

```text
https://course.example.com/
```

同时将 `backend/.env` 中的 `CORS_ORIGINS` 改为 HTTPS 域名：

```env
CORS_ORIGINS=https://course.example.com
```

重启后端：

```bash
sudo systemctl restart course-cms-backend
```

## 9. 日常运维

查看后端日志：

```bash
sudo journalctl -u course-cms-backend -f
```

重启后端：

```bash
sudo systemctl restart course-cms-backend
```

重载 Nginx：

```bash
sudo nginx -t
sudo systemctl reload nginx
```

重新构建前端：

```bash
cd /opt/course-cms/frontend
sudo -u www-data npm run build
```

## 10. 更新部署

如果代码通过 Git 管理：

```bash
cd /opt/course-cms
sudo -u www-data git pull
```

更新后端依赖并重启：

```bash
cd /opt/course-cms/backend
sudo -u www-data .venv/bin/pip install -r requirements.txt
sudo systemctl restart course-cms-backend
```

更新前端依赖并构建：

```bash
cd /opt/course-cms/frontend
sudo -u www-data npm install
sudo -u www-data npm run build
sudo systemctl reload nginx
```

## 11. 数据备份

备份数据库：

```bash
mysqldump -u cms_user -p cms > cms_backup_$(date +%F).sql
```

恢复数据库：

```bash
mysql -u cms_user -p cms < cms_backup_2026-05-20.sql
```

## 12. 常见问题

### 后台接口 502

检查 FastAPI 服务是否运行：

```bash
sudo systemctl status course-cms-backend
sudo journalctl -u course-cms-backend -n 100
```

### 前端页面刷新后 404

确认 Nginx 中存在：

```nginx
try_files $uri $uri/ /index.html;
```

这是 Vue Router history 路由必须的配置。

### 数据库连接失败

检查 `backend/.env`：

```env
DATABASE_URL=mysql+pymysql://cms_user:密码@127.0.0.1:3306/cms?charset=utf8mb4
```

然后重启：

```bash
sudo systemctl restart course-cms-backend
```

### 登录后请求失败

检查 `CORS_ORIGINS` 是否包含当前访问域名。如果使用同域 Nginx 反代，一般配置为：

```env
CORS_ORIGINS=https://course.example.com
```

## 13. 部署验收清单

- `curl http://127.0.0.1:8000/api/health` 返回正常
- `sudo systemctl status course-cms-backend` 为 active
- `sudo nginx -t` 通过
- 前台首页可打开
- 后台登录页可打开
- 管理员可登录
- 课程列表可查询
- 课程可新增、编辑、删除、批量删除
- 管理员密码可修改
