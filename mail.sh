#!/bin/sh
echo $* | sendmail -f nagioscheck@localhost -t $USER
