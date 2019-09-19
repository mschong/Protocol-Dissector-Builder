#/bin/bash
# this bash script will start the gui
# it is not complete yet, but will be done this week, sorry :(
# evazquez 9/9/2019

python3 ./Backend/pyro_run.py & 
python3 ./UI/MainPane/mainwindow.py &