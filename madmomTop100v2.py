import madmom
import numpy as np
import os
from scipy.signal import argrelextrema
from pydub import AudioSegment
import glob
from itertools import cycle

def overlayForTimestamps(timestamps,numbers,original,clickPath,firstBeatPath):
    click = AudioSegment.from_file(clickPath)
    firstBeat = AudioSegment.from_file(firstBeatPath)
    withBeats = AudioSegment.empty()
    numberOfTimestamps = len(timestamps)
    #print(numberOfTimestamps)
    timestampIndex = 0
    for timestamp in timestamps:
        #print(timestamp)
        if timestampIndex > numberOfTimestamps-2:
            break
        begin = timestamp*1000.0
        end = timestamps[timestampIndex+1]*1000.0
        measure = original[begin:end]
        if numbers[timestampIndex] == 1:
            measure.overlay(firstBeat)
        else:
            measure.overlay(click)
        withBeats += measure
        timestampIndex += 1
    return withBeats


def dGetTimestamps(filename):
    labelFile = open(filename,"r")
    lines = labelFile.readlines()
    timestamps = [float(line.split("\t")[0]) for line in lines]
    timestampsAndNumbers = list(zip(timestamps,cycle([1,2,3,4])))
    labelFile.close()
    #print(timestampsAndNumbers)
    return [i[0] for i in timestampsAndNumbers],[i[1] for i in timestampsAndNumbers]


def madmomSynthesize(fileName,labelFilename):
    mergedFilePath = os.path.splitext(fileName)[0]+'-madmom-merged.mp3'
    dMergedFilePath = os.path.splitext(fileName)[0]+'-d-merged.mp3'
    downbeatTrackingProcessor = madmom.features.downbeats.DBNDownBeatTrackingProcessor(beats_per_bar=[4],fps=100)
    
    songProcessor = madmom.features.downbeats.RNNDownBeatProcessor()(fileName)
    
    downbeatProcessorResults = downbeatTrackingProcessor(songProcessor)
    #an array of type [P(beat),P(downbeat)]
    
    downbeatNumbers = [child[1] for child in downbeatProcessorResults]
    downbeatTimestamps = [child[0] for child in downbeatProcessorResults]
    #print(type(PDownbeat),len(PDownbeat))
    
    original = AudioSegment.from_file(fileName)
    madmomMerged = AudioSegment.empty()

    click = AudioSegment.from_file('./MetroBeat1-right.wav')
    firstBeat = AudioSegment.from_file('./MetroBeat2-right.wav')
    numberOfTimestamps = len(downbeatTimestamps)
    #print(numberOfTimestamps)
    timestampIndex = 0
    for timestamp in downbeatTimestamps:
        #print(timestamp)
        if timestampIndex > numberOfTimestamps-2:
            break
        begin = timestamp*1000.0
        end = downbeatTimestamps[timestampIndex+1]*1000.0
        measure = original[begin:end]
        if downbeatNumbers[timestampIndex] == 1:
            merged = measure.overlay(firstBeat)
            #print("firstBeat")
        else:
            merged = measure.overlay(click)
            #print("click")
        madmomMerged += merged
        timestampIndex += 1

    #madmomMerged.export(mergedFilePath,format='wav')
    dClick = AudioSegment.from_file('./MetroBeat1-left.wav')
    dFirstBeat = AudioSegment.from_file('./MetroBeat2-left.wav')
    dTimestamps, dNumbers = dGetTimestamps(labelFilename)
    dModified = AudioSegment.empty()
    numberOfTimestamps = len(dTimestamps)
    #print(numberOfTimestamps)
    timestampIndex = 0
    for timestamp in dTimestamps:
        #print(timestamp)
        if timestampIndex > numberOfTimestamps-2:
            break
        begin = timestamp*1000.0
        end = dTimestamps[timestampIndex+1]*1000.0
        measure = madmomMerged[begin:end]
        if dNumbers[timestampIndex] == 1:
            merged = measure.overlay(dFirstBeat)
        else:
            merged = measure.overlay(dClick)
        dModified += merged
        timestampIndex += 1

    
    dModified.export(dMergedFilePath,format='mp3')
    #write resulting wav to new file 
    
    return True


#for all files in this directory
allPaths = glob.glob('./dd/*.mp3')
allLabelPaths = glob.glob('./dd/labels/*.txt')
zippedPaths = zip(allPaths,allLabelPaths)
#print(list(zippedPaths))
for wavPath,labelPath in zippedPaths:
    print(wavPath,labelPath)
    madmomSynthesize(wavPath,labelPath)
    print(wavPath)

print("madmom completed synthesis")












    





    
