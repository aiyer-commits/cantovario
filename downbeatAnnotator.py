import pydub
import os
import madmomDownbeatAnalyzer
class DownbeatAnnotator:

    measureClick = AudioSegment.from_file("./measureClick.wav",format="wav")
    beatClick = AudioSegment.from_file("./beatClick.wav",format="wav")

    def overlayDownbeats(mp3Path,downbeatsArray):
        annotatedPath = os.path.splitext(mp3Path)[0] + "-annotated.mp3"
        mp3Segment = AudioSegment.from_file(mp3Path,format="mp3")
        annotated = AudioSegment.empty()
        dIndex = 0
        dLength = len(downbeatsArray)
        for downbeat,number in downbeatsArray:
            nextIndex = dIndex + 1
            if( nextIndex < dLength):
                begin = downbeat*1000
                end = downbeatsArray[nextIndex]*1000
                original = mp3Segment[begin:end]
                if number == 1:
                    overlaid = original.overlay(measureClick)
                else:
                    overlaid = original.overlay(beatClick)
                annotated += overlaid
            dIndex += 1
        annotated.export(annotatedPath,format="mp3")
        return annotatedPath
