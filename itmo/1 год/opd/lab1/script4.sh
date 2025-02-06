#!/bin/bash

# 4

cd ~/lab0

echo "- 4.1:"
wc -l $(ls -R . | grep '^l') 2>/dev/null | sort -n
#find . -type f -name "l*" -exec wc -l {} + | sort -n
echo "- 4.2:"
ls -lur | tail -2 2>/dev/null
echo "- 4.3:"
cat $(ls -Rp hydreigon6/**/*) 2>/dev/null | grep -iv "lle" 2>&1
#echo "- 4.3:"
cat $(ls -Rp hydreigon6/*/*/* hydreigon6/*/* | grep -v "/$") 2>/dev/null | grep -iv "lle" 2>&1
#find hydreigon6 -type f -exec cat {} + | grep -iv "lle" 2>&1
echo "- 4.4:"
ls -Rlt |  grep " c.*$" | head -3 2>/tmp/errors.log
echo "- 4.5:"
ls -Rlu |  grep " m.*$" 2>/dev/null
echo "- 4.6:"
wc -l $(ls -Rdp **/*p | grep -v "/$") | sort -n 2>/tmp/errors.log

echo "====Step 4 done===="