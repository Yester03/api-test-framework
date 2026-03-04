# Linux 接口排障 SOP（Troubleshooting SOP）

> 目标：遇到接口异常/慢，能快速判断问题在「客户端/网关/上游服务/日志/数据」哪一层，并用证据闭环。

---

## 0. 排障总流程（Evidence Chain）

1. **复现（Reproduce）**：`curl -i` / `curl -v` 获取状态码、响应头、响应体
2. **量化（Measure）**：`curl -w "%{http_code} %{time_total}\n"` 记录耗时
3. **端口（Port）**：`ss -lntp` / `lsof -i :PORT` 确认是否监听、谁在监听
4. **进程（Process）**：`ps -p PID -o pid,user,cmd` / `systemctl status SERVICE`
5. **日志（Logs）**：`journalctl -u SERVICE` / `grep` 定位 error/warn、关键报错
6. **修复（Fix）**：重启服务/修正配置/恢复依赖
7. **回归（Verify）**：本机回环 + 域名访问 + 关键接口验证

---

## 1. 常用命令速查（Minimal Set）

### 1.1 复现与耗时

- `curl -i URL`
- `curl -v URL`
- `curl -s -o /dev/null -w "%{http_code} %{time_total}\n" URL`

### 1.2 端口与进程

- `ss -lntp | head -n 50`
- `ss -lntp | grep ':PORT '`
- `sudo lsof -i :PORT | head`
- `ps -p PID -o pid,user,cmd --no-headers`
- `systemctl status SERVICE --no-pager -n 60`

### 1.3 日志

- `sudo journalctl -u SERVICE -n 120 --no-pager`
- `sudo journalctl -u SERVICE --since "today" --no-pager | grep -nEi "error|warn|tls|handshake" | tail -n 120`

---

## 2. Case A：Reverse Proxy 502（上游连接被拒绝）

### 2.1 现象与影响

- 现象：访问 `https://api.<domain>/` 返回 **502**
- 影响：API 不可用，网关正常但无法转发到上游（upstream）

### 2.2 复现证据

```bash
curl -I https://api.<domain>/
```

### 2.3 关键日志证据（网关侧）

典型报错：dial tcp 127.0.0.1:8000: connect: connection refused

```bash
sudo journalctl -u caddy --since "today" --no-pager | grep -nEi "connect: connection refused|dial tcp|reverse_proxy|502" | tail -n 50
```

### 2.4 端口证据（上游未监听）

```bash
ss -lntp | grep ':8000 ' || echo "8000 not listening"
curl -s -o /dev/null -w "%{http_code} %{time_total}\n" http://127.0.0.1:8000/ || true
```

### 2.5 结论（Root Cause）

根因：上游 FastAPI 服务未启动/崩溃/端口不一致 → 8000 未监听 → Caddy 反代失败 → 502

### 2.6 修复步骤（Fix）

systemd 服务（推荐）

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now fastapi-demo
sudo systemctl status fastapi-demo --no-pager -n 60
```

回归验证（Verify）

```bash
ss -lntp | grep ':8000 '
curl -s -o /dev/null -w "%{http_code} %{time_total}\n" http://127.0.0.1:8000/
curl -s -o /dev/null -w "%{http_code} %{time_total}\n" https://api.<domain>/ || true
```

## 3. Case B：本机 curl https://127.0.0.1 失败（TLS SNI / Host 误区）

### 3.1 现象与影响

现象：本机执行 `curl -Iv https://127.0.0.1` 或 `https://localhost` 报错：

```bash
TLS alert, internal error (592)
```

影响：误以为 TLS 配置坏了，但外网域名访问可能是正常的

### 3.2 错误示范（Important）

`-H "Host: ..."` 只影响 HTTP 层 `Host header`，不会改变 `TLS` 的 `SNI`
因此下面这种方式无法模拟真实域名 TLS：

```bash
curl -Ik https://127.0.0.1 -H "Host: www.<domain>"
```

### 3.3 正确验证方式：用 --resolve 改 SNI（关键技巧）

这会让 SNI=域名，并把连接指向 127.0.0.1

```bash
curl -Iv --resolve www.<domain>:443:127.0.0.1 https://www.<domain>/
curl -Iv --resolve api.<domain>:443:127.0.0.1 https://api.<domain>/
```

### 3.4 结论（Root Cause）

根因：直接访问 https://127.0.0.1 时 SNI=127.0.0.1，Caddy 只为域名站点签发证书

正确做法：使用 --resolve 用域名作为 SNI 做本机验证

### 3.5 可选修复（本地也想直接 https）

若你希望 https://localhost / https://127.0.0.1 也能用，可在 Caddyfile 增加：

```bash
localhost, 127.0.0.1 {
  tls internal
  respond "OK local tls" 200
}
```
