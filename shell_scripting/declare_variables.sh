#!/bin/bash

#Simple use of declare
declare FOO=22

#Read only variables
declare -r PWDFILE=/etc/passwd
echo $PWDFILE

