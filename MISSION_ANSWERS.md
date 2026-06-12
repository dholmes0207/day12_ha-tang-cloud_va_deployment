# Day 12 Lab - Mission Answers

> **Student Name:** Lưu Tiến Duy
> **Student ID:** 2A202600729  
> **Date:** 12-06-2026

---

## Part 1: Localhost vs Production

### Exercise 1.1: Anti-patterns found
1. Hardcoded API keys và database URL trực tiếp trong file code (`OPENAI_API_KEY`, `DATABASE_URL`), rất nguy hiểm nếu đẩy code lên GitHub.
2. Cấu hình cứng, không đọc từ Environment Variables (như `DEBUG`, `MAX_TOKENS`).
3. Sử dụng `print()` thay vì thư viện logging chuẩn, ngoài ra log cả thông tin nhạy cảm (`print(f"[DEBUG] Using key: {OPENAI_API_KEY}")`).
4. Không có `/health` endpoint, khiến hệ thống giám sát (orchestrators) không thể biết ứng dụng đang sống hay đã crash.
5. Hardcode IP và Port (`localhost:8000`) nên không truy cập được từ bên ngoài và khó tuỳ biến. Chế độ `reload=True` được dùng sai khi chạy production.

### Exercise 1.3: Comparison table
| Feature | Develop | Production | Tại sao quan trọng? |
|---------|---------|------------|----------------|
| Config | Hardcode | Env vars (`pydantic_settings`) | Bảo mật secret key, dễ thay đổi cấu hình giữa dev/prod. |
| Health check | Không có | Có (`/health`, `/ready`) | Kubernetes/Load balancer cần điểm này để restart container lỗi hoặc route traffic. |
| Logging | `print()` | JSON Structured logging | Dễ parse, tìm kiếm lỗi tập trung trong Elasticsearch / Datadog. |
| Shutdown | Đột ngột | Graceful Shutdown | Xử lý xong nốt các request đang dang dở trước khi tắt hẳn container. |

## Part 2: Docker

### Exercise 2.1: Dockerfile questions
1. Base image: `python:3.11-slim`
2. Working directory: `/app`
3. Tại sao COPY requirements.txt trước: Tối ưu hoá Docker Cache, layer cài requirements chỉ build lại nếu file này thay đổi.
4. CMD vs ENTRYPOINT: `ENTRYPOINT` định nghĩa tiến trình chính (container), `CMD` dùng làm default parameters hoặc truyền thêm biến cho ENTRYPOINT.

### Exercise 2.3: Image size comparison
- Develop: ~1660 MB
- Production: ~236 MB (Do sử dụng multi-stage build, chỉ copy runtime dependencies).
- Difference: ~85.8%

## Part 3: Cloud Deployment

### Exercise 3.1: Railway deployment
- URL: https://day12-agent.up.railway.app
- Screenshot: [Link to screenshot in repo]

## Part 4: API Security

### Exercise 4.1-4.3: Test results
- Không có khóa API: `401 Unauthorized`
- Nhập sai token JWT / Token hết hạn: `401 Unauthorized`
- Gửi quá nhiều (20 requests): `429 Too Many Requests - Rate limit exceeded`

### Exercise 4.4: Cost guard implementation
Ghi nhận mức độ tiêu thụ của user trong tháng sử dụng Redis. Mã key Redis có định dạng `budget:user_id:YYYY-MM`. Khi có một request gửi tới, kiểm tra nếu `current_usage + estimated_cost > LIMIT (10$)` thì block và trả về lỗi 402 Payment Required. Ngược lại, tiếp tục xử lý và dùng `r.incrbyfloat` để cộng tiền vào usage tháng đó kèm `expire(32 days)`.

## Part 5: Scaling & Reliability

### Exercise 5.1-5.5: Implementation notes
- Health check (`/health` và `/ready`) chia thành Liveness và Readiness Probe.
- Bắt signal `SIGTERM` bằng `signal.signal()` để ngừng nhận traffic và đợi process xong queue trước khi tắt (Graceful Shutdown).
- Không lưu conversation history tại memory nội bộ. Mọi requests dùng `redis.lrange()` và `redis.rpush()` để lấy và cất state. Điều này giúp chạy nhiều containers song song được tải đều bởi Nginx balancer.
