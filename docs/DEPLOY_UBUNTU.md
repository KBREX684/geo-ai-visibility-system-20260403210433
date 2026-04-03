# Ubuntu 22.04 部署 SOP（手动部署）

## 1. 服务器准备

```bash
sudo apt update
sudo apt install -y docker.io docker-compose-plugin git
sudo usermod -aG docker $USER
```

重新登录后继续。

## 2. 拉取代码

```bash
git clone <YOUR_GITHUB_REPO_URL> geo-ai-visibility-system
cd geo-ai-visibility-system
cp .env.example .env
```

编辑 `.env`，至少修改：
- `SECRET_KEY`
- `ADMIN_PASSWORD`
- `POSTGRES_PASSWORD`

## 3. 启动服务

```bash
docker compose up --build -d
docker compose ps
```

## 4. 验证

- `curl http://localhost/healthz`
- 浏览器访问 `http://<SERVER_IP>/`

## 5. HTTPS（建议）

生产建议加一层证书管理（如 Certbot/Caddy），并把 `infra/nginx/default.conf` 升级为 TLS 配置。

## 6. 更新发布

```bash
git pull
docker compose up --build -d
```

