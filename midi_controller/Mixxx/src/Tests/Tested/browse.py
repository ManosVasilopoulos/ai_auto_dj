import time
from midi_out_port import get_midi_port
from mappings import library_buttons


move_down_note_on = library_buttons['move_down']['master']['note_on']
move_down_note_off = library_buttons['move_down']['master']['note_off']

move_focus_master_note_on = library_buttons['move_focus']['master']['note_on']
move_focus_master_note_off = library_buttons['move_focus']['master']['note_off']

move_focus_right_note_on = library_buttons['move_focus']['right_pane']['note_on']
move_focus_right_note_off = library_buttons['move_focus']['right_pane']['note_off']

midiout, port_name = get_midi_port()
print('Midi Out Port:', port_name)

time.sleep(5)
print('Moving focus on right or left pane...')
midiout.send_message(move_focus_master_note_on)
time.sleep(0.001)
midiout.send_message(move_focus_master_note_off)
time.sleep(0.001)

time.sleep(5)
print('Moving focus on right pane...')
midiout.send_message(move_focus_right_note_on)
time.sleep(0.001)
midiout.send_message(move_focus_right_note_off)
time.sleep(0.001)

input('Press ENTER to move vertically in the current music library...')
for i in range(5):
    midiout.send_message(move_down_note_on)
    time.sleep(0.001)
    midiout.send_message(move_down_note_off)
    print('Moved ', i + 1, 'times.')
    time.sleep(1)

midiout.close_port()
