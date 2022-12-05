#!/bin/bash

CSRF_PATH='/var/www/html/dvwa/includes/dvwaPage.inc.php'

CSRF=$(cat $CSRF_PATH | grep md5 | cut -d " " -f6)

if [ $CSRF = "uniqid()" ];then
    sed -i 's/uniqid()/"1234"/g' $CSRF_PATH
    echo 'CHANGE CSRF_TOKEN'
fi

python3 attack.py

sed -i 's/"1234"/uniqid()/g' $CSRF_PATH
echo 'RESET CSRF_TOKEN'
