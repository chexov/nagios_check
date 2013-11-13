#!/bin/sh
to=$1; shift
e=$1; shift
subj=$1; shift

echo $* | mail -s "[checkalive] $subj $e" $to

