#!/bin/bash

DOCS_USER_GUIDE_PATH=docs/user_guide/
DOCSGAME_USER_GUIDE_PATH=docsgame_dist/game/docs/user_guide/

mkdir -p -m 755 $DOCSGAME_USER_GUIDE_PATH

for filename in "$DOCS_USER_GUIDE_PATH"*.rst
do
  rst2html5.py --stylesheet='' --no-xml-declaration "$filename" > ""$DOCSGAME_USER_GUIDE_PATH"$(basename "$filename" .rst).html"
done
