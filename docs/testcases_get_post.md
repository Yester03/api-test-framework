# Test Cases - GET /posts/{id}

## Basic / Happy Path
1. id=1 -> 200，JSON 中 `id==1`，包含 userId/title/body
2. id=2 -> 200，JSON 中 `id==2`
3. id=100 -> 200（边界：已知最大有效 id）字段完整

## Not Found / Resource
4. id=0 -> 404（或空返回，按实际观察记录）
5. id=101 -> 404（超出有效范围）
6. id=999999 -> 404

## Parameter Validation
7. id=-1 -> 404 或 400（记录实际行为）
8. id=1.5 -> 404 或 400（小数）
9. id=abc -> 404 或 400（非数字）
10. id=空字符串 -> 404（路径缺失场景：请求 /posts/）
11. id=空格 " " -> 404（编码后）
12. id=01 -> 200 且 id==1（前导零的处理，记录实际）

## Headers / Content Negotiation
13. Accept: application/json -> 200 且 Content-Type 是 JSON
14. Accept: text/plain -> 仍返回 JSON 或 406（记录实际）
15. 不带 Accept -> 200

## Robustness（健壮性）
16. 超时设置：timeout=0.001 -> 客户端超时异常（测试用例应捕获异常并标记为预期）
17. 重试策略（如果后续实现 retry）：临时网络错误 -> 重试成功（可在可控环境做）

## Performance / Stability（轻量即可）
18. 连续请求 50 次 id=1 -> 全部 200，失败率 0（记录耗时均值/最大值）
19. 并发 20（线程/进程）请求 id=1 -> 全部 200（记录耗时分布）

## Security (light)
20. id=1%27%20or%201%3D1 -> 应该 404/400（输入不应导致服务异常）