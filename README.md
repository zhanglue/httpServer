### General
It is used to set a HTTP server, while set response data manually. (Compitable with both python2/3)

### Usage
```
./main.sh MODE [MODE_PARAMS] [-p SERVER_PORT] [--debug]

    MODE: 
        -c: Clean up former data.
        -s: Start a HTTP server.
        -t: Terminate all HTTP servers.
        -r: Restart HTTP server.
        -d: Set server behaviou and data.
        -da: Set server behaviou and data(add mode).
        -dg: Get currnet response pattern.
    -p: Set HTTP server port(work in -s mode, 9100 as default).
    --python3: Python as python3.
    --debug: Show debug messages in stdout.
    
    Response patterns are record as json:
    {
        "urlPath_A": {
            "headers": {
                ...
            },
            "respData": respString
        },
        "urlPath_B": {
            "headers": {
                ...
            },
            "respData": respString
        }
    }
```

### Example
```
./main.sh -s -p 9200
./main.sh -d ./data/demo_pattern.json

curl 127.0.0.1:9200
curl 127.0.0.1:9200/try
curl 127.0.0.1:9200/try_another
curl 127.0.0.1:9200/try_bad
```
