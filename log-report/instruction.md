An Apache-style access log is at `/app/access.log`. Parse it and write a JSON summary
report to `/app/report.json`. Do not modify `/app/access.log`.

`/app/report.json` must be a single JSON object with exactly these three keys:

1. `total_requests` (integer): the total number of requests in the log — one per
   non-empty line.
2. `unique_ips` (integer): the number of distinct client IP addresses. The client IP is
   the first whitespace-separated field on each line.
3. `top_path` (string): the request path that appears in the most requests, taken from
   the request line (for example, `"GET /index.html HTTP/1.1"` has the path
   `/index.html`). Exactly one path is the most frequent in this log.

You have 120 seconds to complete this task. Do not cheat by using online solutions or hints specific to this task.
