import madmom
import os
import json

downbeatsExtention = '-downbeats.csv'

class MadmomDownbeatAnalyzer:

    rnndbp = RNNDownBeatProcessor()
    dbndbtp = DBNDownBeatTrackingProcessor(beats_per_bar=[4],fps=100)
    
    def processDownbeats(mp3path):
        mp3Filename, mp3Extension = os.path.splitext(mp3path)
        downbeatsPath = mp3Filename + downbeatsExtension
        if(os.path.exists(downbeatsPath)):
            print("opening existing downbeats file at " + downbeatsPath)
            with open(downbeatsPath, 'r') as downbeatsFile:
                downbeatsList = json.load(downbeatsFile)
                return downbeatsList
            #handle exception
        else:
            print("processing downbeats for "+mp3path)
            rnndbpResults = rnndbp(mp3path)
            #does the above line return the correct input for the below line
            dbndbtpResults = dbndbtp(rnndbpResults)
            print("processing complete")
            with open(downbeatsPath, 'w') as downbeatsFile:
                json.dump(dbndbtpResults,downbeatsFile)
            return dbndbtpResults 
