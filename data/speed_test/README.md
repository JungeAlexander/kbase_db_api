# Sync

# Async

`wrk -t12 -c400 -d60s -spost.lua http://127.0.0.1:8000/api/v1/token`

Running 1m test @ http://127.0.0.1:8000/api/v1/token
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.17s   512.82ms   1.99s    68.00%
    Req/Sec     5.37     19.42   202.00     95.12%
  522 requests in 1.00m, 95.23KB read
  Socket errors: connect 155, read 284647, write 0, timeout 472
  Non-2xx or 3xx responses: 522
Requests/sec:      8.69
Transfer/sec:      1.58KB
