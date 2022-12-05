#!/bin/bash

CSRF=$(cat /var/www/html/dvwa/includes/dvwaPage.inc.php | grep md5 | cut -d " " -f6)

if [ $CSRF = "uniqid()" ];then
    sed -i 's/uniqid()/"1234"/g' /var/www/html/dvwa/includes/dvwaPage.inc.php
    echo 'CHANGE CSRF_TOKEN'
fi

python3 attack.py

