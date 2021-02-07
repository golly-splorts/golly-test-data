#!/bin/bash

find . \( -name "bracket*" -o -name "postseason*" \) -not -path "./vp/*" | xargs -n1 -I% gsed -i -e 's/World Series/Hellmouth Cup/g' %
