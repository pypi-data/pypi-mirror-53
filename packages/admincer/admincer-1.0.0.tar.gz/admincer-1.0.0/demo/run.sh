#!/bin/bash

rm -Rf out
admincer pl -f ad=banners:sides -f label=labels -n 100 src out

echo "<html><body>" > out/index.html
for a in 0 1 2 3 4 5 6 7 8 9; do
    for b in 0 1 2 3 4 5 6 7 8 9 0; do
        echo "<img src='000${a}${b}.png' style='border:1px solid black' />" >> out/index.html
    done
    echo "<br/>" >> out/index.html
done
echo "</body></html>" >> out/index.html
