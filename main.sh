#!/bin/bash

################################################################################
# Feature  : Main.
# Author   : lucuszhang
# Date     : 2019.01.24
################################################################################

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

    export LOG_LEVEL_DEBUG
    python ${SCRIPT_LOCATION}/src/server.py \
        $serverHost \
        $serverPort \
        $serverLogPath
}

builtin cd "$(dirname "${BASH_SOURCE-$0}")"
SCRIPT_LOCATION=$(pwd -P)
builtin cd ${SCRIPT_LOCATION}

LOG_LEVEL_DEBUG=0
exec_mode='_start'

serverHost='127.0.0.1'
serverPort='9100'
serverLogPath="${SCRIPT_LOCATION}/temp"

while (( $# ))
do
    case $1 in
        -c | --clean )
            exec_mode='_clean'
            ;;
        -d)
            LOG_LEVEL_DEBUG=1
            ;;
        -p)
            shift
            serverPort=$1
            ;;
    esac

    shift
done

$exec_mode
