IN=t3.txt
IN=eslpod1k.txt
OUT=1-${IN}.html
rm -vf $OUT
cp a.css $OUT
head  -1000 $IN|./IntensiveRL.py >> $OUT
open $OUT
