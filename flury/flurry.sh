#! /usr/bin/bash
echo "Please choose the type: Network = n OR DVWA = d"
read VAR

if [ "$VAR" = "d" ]; then
    python3 webserver.py
elif [ "$VAR" = "n" ]; then
    python3 networkhost.py
else
    echo "Wrong Choice"
fi