import os, sys

directory = 'outputHists/2017/'

for filename in os.listdir(directory):
    sample = filename.split('_')[1]
    selection = filename.split('_')[2]
    os.rename(directory+filename, directory+'histOut_'+sample+'2017_'+selection+'.root')
    print directory+filename, '  --->  ', directory+'histOut_'+sample+'2017_'+selection+'.root'
