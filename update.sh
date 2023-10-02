#!/bin/bash

git remote -v update > /dev/null 2>&1
output="$(git status -uno)"

if [[ $output == *"Your branch is behind"* ]]; then
	echo "Time to update!"
	git pull
	pkill -f Lewdie.py
	python3 Lewdie.py
fi
