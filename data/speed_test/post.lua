-- example HTTP POST script which demonstrates setting the
-- HTTP method, body, and adding a header

wrk.method = "POST"
wrk.body   = "grant_type=&username=one&password=two&scope=&client_id=&client_secret="
wrk.headers["accept"] = "application/json"
wrk.headers["Content-Type"] = "application/x-www-form-urlencoded"
