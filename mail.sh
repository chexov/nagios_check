#!/bin/sh
e=$1; shift
to=$1; shift
subj=$1; shift

echo $* | mail -s "[checkalive] $subj $e" $to

