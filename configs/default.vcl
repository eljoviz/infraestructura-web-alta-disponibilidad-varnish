vcl 4.1;

probe backend_probe {
    .url = "/";
    .interval = 3s;
    .timeout = 2s;
    .window = 5;
    .threshold = 3;
}

backend default {
    .host = "172.31.23.225";
    .port = "80";
    .probe = backend_probe;
}

sub vcl_recv {
    set req.grace = 1h;
}

sub vcl_backend_response {
    set beresp.ttl = 10m;
    set beresp.grace = 1h;
}

sub vcl_deliver {
    if (obj.hits > 0) {
        set resp.http.X-Cache = "HIT (desde Varnish)";
    } else {
        set resp.http.X-Cache = "MISS (desde Apache)";
    }
}
