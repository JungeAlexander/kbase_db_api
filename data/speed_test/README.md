# Speed test with wrk

## Sync

```
wrk -t4 -c50 -d60s -spost.lua http://127.0.0.1:8000/api/v1/token
```

```
Running 1m test @ http://127.0.0.1:8000/api/v1/token
  4 threads and 50 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.44s   224.24ms   1.83s    75.00%
    Req/Sec     3.49      6.78    40.00     97.56%
  62 requests in 1.00m, 12.00KB read
  Socket errors: connect 0, read 12, write 0, timeout 46
  Non-2xx or 3xx responses: 62
Requests/sec:      1.03
Transfer/sec:     204.48B
```


## Async

```
wrk -t4 -c50 -d60s -spost.lua http://127.0.0.1:8000/api/v1/token
```

```
Running 1m test @ http://127.0.0.1:8000/api/v1/token
  4 threads and 50 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   629.18ms  132.98ms   1.65s    89.67%
    Req/Sec    19.77     10.88    80.00     86.04%
  4565 requests in 1.00m, 0.89MB read
  Non-2xx or 3xx responses: 4565
Requests/sec:     75.96
Transfer/sec:     15.13KB
```
