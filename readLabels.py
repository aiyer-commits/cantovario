import glob
from itertools import cycle

def dGetTimestamps(filename):
    labelFile = open(filename,"r")
    lines = labelFile.readlines()
    timestamps = [float(line.split("\t")[0]) for line in lines]
    timestampsAndNumbers = list(zip(timestamps,cycle([1,2,3,4])))
    labelFile.close()
    #print(timestampsAndNumbers)
    return [i[0] for i in timestampsAndNumbers],[i[1] for i in timestampsAndNumbers]

allLabelPaths = glob.glob('./dd/labels/*.txt')

for labelPath in allLabelPaths:
    timestamps,numbers = dGetTimestamps(labelPath)
    print(timestamps)
    print(numbers)
