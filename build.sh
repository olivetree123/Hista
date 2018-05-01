#! /bin/bash

tar -cvzf  hista.tar.gz  * --exclude="__pycache__" --exclude="*.pyc"
docker build -t hista .