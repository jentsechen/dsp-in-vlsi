#!/bin/bash

ZIP_FILE="$1"

unzip "$ZIP_FILE"
FOLDER="${ZIP_FILE%.zip}"
cd "$FOLDER/01_RTL"
chmod +x 01_run
./01_run