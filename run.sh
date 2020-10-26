#!/bin/bash

pouet=$(ifconfig | grep "inet " | grep -Fv 127.0.0.1 | grep 192 | awk '{print $2}')
echo "[?] LOCAL IP ADDRESS: ${pouet}"

echo "[?] Now running the local development server..."
echo "[?] Open your browser at http://${pouet}:1234/"
echo ""

otree devserver $pouet:1234
