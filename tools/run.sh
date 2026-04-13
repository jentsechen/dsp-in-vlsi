#!/bin/bash

MODE="$1"
ZIP_FILE="$2.zip"
FOLDER="$2"

if [ "$MODE" != "rtl_sim" ] && [ "$MODE" != "syn" ] && [ "$MODE" != "gl_sim" ]; then
    echo "Usage: $0 <rtl_sim|syn|gl_sim> <folder>"
    exit 1
fi

if [ -d "$FOLDER" ]; then
    if [ "$ZIP_FILE" -nt "$FOLDER" ]; then
        rm -rf "$FOLDER"
        unzip "$ZIP_FILE"
    fi
else
    unzip "$ZIP_FILE"
fi

if [ "$MODE" = "rtl_sim" ]; then
    cd "$FOLDER/01_RTL"
    chmod +x 01_run
    ./01_run
elif [ "$MODE" = "syn" ]; then
    cd "$FOLDER/02_SYN"
    chmod +x 01_syn
    ./01_syn
else
    cd "$FOLDER/03_GATESIM"
    chmod +x 01_run
    ./01_run
fi