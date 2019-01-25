### General
It is used to set a HTTP server, while set response data manually.

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
