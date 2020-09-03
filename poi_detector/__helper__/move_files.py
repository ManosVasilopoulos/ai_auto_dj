# Move from "POIs WAV" to original directory
import os

current_dir = 'D:/Documents/Thesis/POIs WAV/'
pitch_1 = 'D:/Documents/Thesis/Cue Point Detection Dataset WAV - Pitch Shifted/+3/'
pitch_2 = 'D:/Documents/Thesis/Cue Point Detection Dataset WAV - Pitch Shifted/-3/'

tracks_list = os.listdir(current_dir)
for track in tracks_list:
    try:
        if '-pitch-3' in track:
            os.rename(current_dir+track, pitch_1+track)
            print(track)
        if '-pitch--3' in track:
            os.rename(current_dir+track, pitch_2+track)
            print(track)
    except Exception as e:
        print (e)
# Move a file by renaming it's path
#os.rename('/Users/billy/d1/xfile.txt', '/Users/billy/d2/xfile.txt')
