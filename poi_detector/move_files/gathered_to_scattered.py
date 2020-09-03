# Move from "POIs WAV" to original directory
import os

gathered_dir = 'D:/Documents/Thesis/WAVs/'
wav_dir1 = 'D:/Documents/Thesis/Cue Point Detection Dataset WAV/'
wav_dir2 = 'D:/Documents/Thesis/Cue Point Detection Dataset WAV 2/'
pitch_1 = 'D:/Documents/Thesis/Cue Point Detection Dataset WAV - Pitch Shifted/+3/'
pitch_2 = 'D:/Documents/Thesis/Cue Point Detection Dataset WAV - Pitch Shifted/-3/'
pitch_3 = 'D:/Documents/Thesis/Cue Point Detection Dataset WAV - Pitch Shifted/+6/'
pitch_4 = 'D:/Documents/Thesis/Cue Point Detection Dataset WAV - Pitch Shifted/-6/'
stretch_1 = 'D:/Documents/Thesis/Cue Point Detection Dataset WAV - Time Stretched/-25%/'
stretch_2 = 'D:/Documents/Thesis/Cue Point Detection Dataset WAV - Time Stretched/+25%/'

tracks_list = os.listdir(gathered_dir)
for track in tracks_list:
    try:
        if '-pitch-3' in track:
            os.rename(gathered_dir+track, pitch_1+track)
            print(track)
        if '-pitch--3' in track:
            os.rename(gathered_dir+track, pitch_2+track)
            print(track)
        if '-pitch-6' in track:
            os.rename(gathered_dir+track, pitch_3+track)
            print(track)
        if '-pitch--6' in track:
            os.rename(gathered_dir+track, pitch_4+track)
            print(track)
        if '-stetch0.75' in track:
            os.rename(gathered_dir+track, stretch_1+track)
            print(track)
        if '-stetch1.25' in track:
            os.rename(gathered_dir+track, stretch_2+track)
            print(track)

    except Exception as e:
        print (e)
# Move a file by renaming it's path
#os.rename('/Users/billy/d1/xfile.txt', '/Users/billy/d2/xfile.txt')
