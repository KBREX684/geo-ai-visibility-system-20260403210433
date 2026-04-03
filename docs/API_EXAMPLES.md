# API 调用示例

## 登录

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

## 创建客户

```bash
curl -X POST http://localhost:8000/api/v1/clients \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "brand_name":"杭州星火少儿编程",
    "industry":"少儿编程培训",
    "city":"杭州",
    "core_services":["Scratch","Python"],
    "target_persona":"6-15岁孩子家长",
    "competitors":["编程猫","小码王"],
    "promise_scope":"visibility_only"
  }'
```

## 合规检查

```bash
curl -X POST http://localhost:8000/api/v1/reports/compliance-check \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"client_id":1}'
```

