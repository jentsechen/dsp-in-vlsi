#!/bin/bash
tar -czf "$2.tar.gz" --transform "s|^$(basename $1)|$(basename $2)|" -C "$(dirname $1)" "$(basename $1)"