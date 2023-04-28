#!/bin/bash

DOCS_USER_GUIDE_PATH=docs/user_guide/

DOCSGAME_PATH=docsgame_dist/game/docs/

mkdir -p -m 755 $DOCSGAME_PATH

for filename in "$DOCS_USER_GUIDE_PATH"**/*.rst
do
  base="${filename#*/}"
  docsgame_path="${DOCSGAME_PATH}""${base%/*}"
  mkdir -p "$docsgame_path"

  html_name="$(basename "$filename" .rst).html"
  html_path="$docsgame_path/$html_name"

  rst2html5.py --stylesheet='' --no-xml-declaration "$filename" > "$html_path"

done


rst2html5.py --stylesheet='' --no-xml-declaration "docs/development.rst" ""$DOCSGAME_PATH"development.html"

rst2html5.py --stylesheet='' --no-xml-declaration "docs/encyclopaedia.rst" ""$DOCSGAME_PATH"encyclopaedia.html"
