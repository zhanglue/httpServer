#!/bin/bash

################################################################################
# Feature  : Main.
# Author   : zhanglue
# Date     : 2019.01.24
################################################################################

_usage()
{
    echo '
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
'
}

_echo_info()
{
    local dateString=$( date +"%N" )
    dateString=${dateString:0:3}

    echo $( date +"[%Y-%m-%d %k:%M:%S,")"${dateString}] [INFO] $1"
}

_clean()
{
    local dataToDelete=(\
        "temp" \
        )
    for d in ${dataToDelete[@]}
    do
        if [[ -e "${SCRIPT_LOCATION}/${d}" ]]; then
            echo "rm -rf \"${SCRIPT_LOCATION}/${d}\""
            rm -rf "${SCRIPT_LOCATION}/${d}"
        fi
    done

    find ${SCRIPT_LOCATION} \
        -regex ".*\/__pycache__" \
        -type d -print0 | \
        xargs -0 -l1 -i -t rm -rf {}

    find ${SCRIPT_LOCATION} \
        -regex ".+\.py[cod]$" \
        -type f -print0 | \
        xargs -0 -l1 -i -t rm -f {}
}

_start()
{
    _echo_info "Clean up former data."
    _clean > /dev/null 2>&1

    $PYTHON ${SCRIPT_LOCATION}/src/server.py \
        "start" \
        $serverPort &
}

_terminate()
{
    local pid=""
    local cmdPattern="python[3]\? ${SCRIPT_LOCATION}/src/server.py"
    pid=$(ps aux | grep "$cmdPattern" | grep -v grep | sed 's/[[:space:]]\+/ /g' | cut -d ' ' -f 2)
    if [[ -n $pid ]]; then
        kill -9 $pid
    fi
}

_restart()
{
    _terminate
    _start
}

_get_response_pattern()
{
    $PYTHON ${SCRIPT_LOCATION}/src/server.py \
        "get_response_pattern"
}

_set_response_pattern()
{
    $PYTHON ${SCRIPT_LOCATION}/src/server.py \
        "set_response_pattern" \
        $pathDataFile \
        $flagAddData
}

builtin cd "$(dirname "${BASH_SOURCE-$0}")"
SCRIPT_LOCATION=$(pwd -P)
builtin cd ${SCRIPT_LOCATION}

LOG_LEVEL_DEBUG=0
PYTHON=python
exec_mode=''
serverHost='127.0.0.1'
serverPort='9100'
pathDataFile=''
flagAddData=0

while (( $# ))
do
    case $1 in
        -c | --clean )
            exec_mode='_clean'
            ;;
        --debug)
            LOG_LEVEL_DEBUG=1
            ;;
        -s)
            exec_mode='_start'
            ;;
        -p)
            shift
            serverPort=$1
            ;;
        -t)
            exec_mode='_terminate'
            ;;
        -r)
            exec_mode='_restart'
            ;;
        -dg)
            exec_mode='_get_response_pattern'
            LOG_LEVEL_DEBUG=1
            ;;
        -d)
            shift
            exec_mode='_set_response_pattern'
            pathDataFile=$1
            flagAddData=0
            ;;
        -da)
            shift
            exec_mode='_set_response_pattern'
            pathDataFile=$1
            flagAddData=1
            ;;
        --python3)
            PYTHON='python3'
            ;;
        *)
            _usage
            exit 1
            ;;
    esac

    shift
done

export LOG_LEVEL_DEBUG
$exec_mode
