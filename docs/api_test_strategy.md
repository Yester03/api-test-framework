# API Test Strategy（接口测试策略）

## 1. Scope（范围）
- Target API: JSONPlaceholder
- Base URL: https://jsonplaceholder.typicode.com
- Endpoint in focus: `GET /posts/{id}`

## 2. Test Levels（测试层级）
- Smoke Test（冒烟）：核心接口 1~3 条，确保可用（200 + 关键字段）
- Functional（功能）：正常/异常/边界/参数组合
- Non-functional（非功能）：性能、并发、限流、稳定性（尽量用脚本或工具验证）

## 3. Coverage Template（覆盖模板）
### 3.1 Happy Path（正常）
- 正确参数 -> 正确返回（200）
- 返回体字段完整、类型正确、业务规则满足

### 3.2 Negative（异常）
- 参数缺失/非法类型/非法取值 -> 4xx
- 资源不存在 -> 404
- 服务端异常模拟 -> 5xx（如可控环境）

### 3.3 Boundary（边界）
- 极小/极大值
- 空字符串/超长字符串
- 特殊字符、中文、emoji（如适用）

### 3.4 Security / Auth（权限/安全）
- 无 token / token 过期 / 权限不足 -> 401/403
- 注入类（SQLi/XSS）在 API 场景：主要验证服务端有输入校验（返回 4xx，不崩溃）

### 3.5 Idempotency（幂等）
- 重复请求是否产生重复副作用（PUT/DELETE/部分 POST）
- 幂等 key（如有）校验

### 3.6 Concurrency（并发）
- 同一资源并发读写一致性（如涉及写）
- 是否出现脏数据、覆盖写、重复创建

### 3.7 Rate Limit（限流）
- 超阈值是否返回 429
- 是否有 Retry-After / 限流窗口提示

## 4. Assertions（断言维度）
- Status code
- Response headers（Content-Type/Cache/RateLimit）
- Response time（例如 < 1s 在测试环境）
- JSON schema / 字段类型校验
- Business rules（业务规则）
- Logging & Trace（日志与链路：traceId/requestId）

## 5. Test Data（测试数据）
- 正常数据：id=1
- 不存在：id=0 或 999999（视系统规则）
- 非法：id=abc、id=-1、id=1.5

## 6. Deliverables（交付物）
- `docs/api_test_strategy.md`
- Test cases list（20 cases for one endpoint）
- Automated tests（pytest + requests，逐步覆盖）