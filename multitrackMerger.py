from pydub import AudioSegment
import os
import glob


def mergeTracks(trackPaths, filename):
    merged = AudioSegment.from_file(
        trackPaths[0]
    )  # this has to be the longest track.. not just the first track...
    mergedFilePath = filename + "-merged.mp3"
    if os.path.exists(mergedFilePath):
        return True
    for trackPath in trackPaths[1:]:
        # print("merging", trackPath)
        track = AudioSegment.from_file(trackPath)
        merged = merged.overlay(track)
        # print("merged", trackPath)
    merged.export(mergedFilePath, format="mp3")
    return True


def mergeAllTracksInFolders(folder):
    paths = [root+'/' for root, dirs, files in os.walk(folder) if not dirs]
    globPaths = glob.glob(folder + "/*/")
    # print(folder, paths)
    print(paths,globPaths)
    for path in paths:
        allPaths = glob.glob(path + "*.wav")
        # print(path + "/*.wav")
        # print(allPaths)
        dirname = os.path.dirname(path)
        mergeTracks(allPaths, dirname + "-master")
        mergeTracksWithPattern(["Vox"], allPaths, dirname + "-vocal")
        mergeTracksWithoutPattern(["Vox"], allPaths, dirname + "-instrumental")
        print("merged")
    return True


def mergeTracksWithPattern(ps, trackpaths, filename):
    matching = []
    for path in trackpaths:
        for p in ps:
            # print(p, path)
            if path.find(p) != -1:
                matching.append(path)
                break

    # print("mergeTracksWithPattern", matching)
    if len(matching) > 0:
        mergeTracks(matching, filename)
    return True


def mergeTracksWithoutPattern(ps, trackpaths, filename):

    matching = []
    for path in trackpaths:
        found = False
        for p in ps:
            if path.find(p) != -1:
                found = True
        if not found:
            matching.append(path)

    # print("mergeTracksWithoutPattern", matching)
    if len(matching) > 0:
        mergeTracks(matching, filename)
    return True


mergeAllTracksInFolders(os.getcwd())
print("multitrackMerger completed")
