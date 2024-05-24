#!/bin/zsh

while read file event; do
   echo $file
   filename=$file:t:r
   filepath=$file:h
   python -m pixyverse.pixy -p $file -o $filepath/$filename.py
done
