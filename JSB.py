from midiutil.MidiFile import MIDIFile
import random

############## some functions that the main program calls ##############

# write major 7 chord to file
def play_maj7_chord(midi, track, channel, pitch, time, duration, volume):
    midi.addNote(track,channel,pitch,time,duration,volume)
    midi.addNote(track,channel,pitch+4,time,duration,volume)
    midi.addNote(track,channel,pitch+7,time,duration,volume)
    midi.addNote(track,channel,pitch+11,time,duration,volume)
 
# write minor 7 chord to file    
def play_min7_chord(midi, track, channel, pitch, time, duration, volume):
    midi.addNote(track,channel,pitch,time,duration,volume)
    midi.addNote(track,channel,pitch+3,time,duration,volume)
    midi.addNote(track,channel,pitch+7,time,duration,volume)
    midi.addNote(track,channel,pitch+10,time,duration,volume)
    
# get the next note in the melody
def get_melody_note(melody_set, cur_melody_note):     
    new_note_index = -1
    while new_note_index < 0 or new_note_index > len(melody_set)-1: # while the index of new note is not in range
        index_diff = random.randint(-1*1,1) # pick the offset of the index of next note
        new_note_index = melody_set.index(cur_melody_note) + index_diff
    new_note = melody_set[new_note_index] # chose new note from the set of possible notes
    return new_note

# write single note to file
def play_melody_note(midi, track, channel, pitch, time, duration, volume):
    midi.addNote(track,channel,pitch,time,duration,volume)


############## the main program ##############
   
MyMIDI = MIDIFile(1) # create the MIDIFile object with 1 track

# set current track and time
track = 0   
time = 0

# add track name and tempo
MyMIDI.addTrackName(track,time,"JSB")
MyMIDI.addTempo(track,time,120) # tempo is actually 60, but I want to be able to play half notes

first_melody_note = 72 # this is the number of the key on a piano
cur_melody_note = first_melody_note
n = first_melody_note
melody_set = [n-5, n-3, n, n+2, n+4, n+7, n+9, n+12, n+14, n+16] # notes in pentatonic scale

for i in range(16*4*2): # loop through half-notes. this is 16 bars, 4 beats each, double time
    
    if i%16==0: # at the start of a bar
        play_maj7_chord(midi=MyMIDI, track=0, channel=0, pitch=48, time=i, duration=8, volume=55)

    if (i+8)%16==0: # at the start of a bar
        play_min7_chord(midi=MyMIDI, track=0, channel=0, pitch=50, time=i, duration=8, volume=55)
        
    cur_melody_note = get_melody_note(melody_set, cur_melody_note) # fetch the next note
    is_rest = random.randint(0,1) > 0 # determine if this note should be a rest
    
    if not is_rest:
        play_melody_note(midi=MyMIDI, track=0, channel=0, pitch=cur_melody_note, time=i, duration=2, volume=70) # play the note

        
# write song to disk.
binfile = open("output.mid", 'wb')
MyMIDI.writeFile(binfile)
binfile.close()