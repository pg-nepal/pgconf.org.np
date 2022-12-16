#!/usr/bin/bash

ARGS=(
    --recursive
    --adjust-extension
    --convert-links
    --no-host-directories
    --directory-prefix=dist
)


wget "${ARGS[@]}" http://localhost:5000
