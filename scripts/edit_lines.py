import os, sys
import fileinput

i = 1
for line in fileinput.input(['postProcessor.py'], inplace=True):
    if i > 21 and i < 189: sys.stdout.write("'nanoAOD_files/tt2017/{l}".format(l=line))
    else: sys.stdout.write("{l}".format(l=line))
    i += 1
