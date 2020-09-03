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

"""     DONT MOVE THE ORIGINAL WAVs. THEY ARE READ BY REKORDBOX AS WELL.   
# WAV 1
wav_list1 = os.listdir(wav_dir1)
for track in wav_list1:
    if 'wav' in track:
        try:
            os.rename(wav_dir1 + track, gathered_dir + track)
            print(track)
        except Exception as e:
            print(e)

# WAV 2
wav_list2 = os.listdir(wav_dir2)
for track in wav_list2:
    if 'wav' in track:
        try:
            os.rename(wav_dir2 + track, gathered_dir + track)
            print(track)
        except Exception as e:
            print(e)
"""
# PITCH 1
pitch_1_list = os.listdir(pitch_1)
for track in pitch_1_list:
    if 'wav' in track:
        try:
            os.rename(pitch_1 + track, gathered_dir + track)
            print(track)
        except Exception as e:
            print(e)

# PITCH 2
pitch_2_list = os.listdir(pitch_2)
for track in pitch_2_list:
    if 'wav' in track:
        try:
            os.rename(pitch_2 + track, gathered_dir + track)
            print(track)
        except Exception as e:
            print(e)

# PITCH 3
pitch_3_list = os.listdir(pitch_3)
for track in pitch_3_list:
    if 'wav' in track:
        try:
            os.rename(pitch_3 + track, gathered_dir + track)
            print(track)
        except Exception as e:
            print(e)

# PITCH 4
pitch_4_list = os.listdir(pitch_4)
for track in pitch_4_list:
    if 'wav' in track:
        try:
            os.rename(pitch_4 + track, gathered_dir + track)
            print(track)
        except Exception as e:
            print(e)

# STRETCH 1
stretch_1_list = os.listdir(stretch_1)
for track in stretch_1_list:
    if 'wav' in track:
        try:
            os.rename(stretch_1 + track, gathered_dir + track)
            print(track)
        except Exception as e:
            print(e)

# STRETCH 2
stretch_2_list = os.listdir(stretch_2)
for track in stretch_2_list:
    if 'wav' in track:
        try:
            os.rename(stretch_2 + track, gathered_dir + track)
            print(track)
        except Exception as e:
            print(e)
