""" 40 - 59 for deck 1 """
""" 64 - 83 for deck 2 """
dj_buttons = {
    'load_track': {
        'deck_1': {
            'note_on': [0x90, 3, 127],
            'note_off': [0x80, 3, 127]
        },
        'deck_2': {
            'note_on': [0x91, 4, 127],
            'note_off': [0x81, 4, 127]
        }
    },
    'play_pause': {
        'deck_1': {
            'note_on': [0x90, 37, 127],
            'note_off': [0x80, 37, 127]
        },
        'deck_2': {
            'note_on': [0x91, 38, 127],
            'note_off': [0x81, 38, 127]
        }
    },
    'fast_rewind': {
        'deck_1': {
            'note_on': [0x90, 39, 127],
            'note_off': [0x80, 39, 127]
        },
        'deck_2': {
            'note_on': [0x91, 40, 127],
            'note_off': [0x81, 40, 127]
        }
    },
    'fast_forward': {
        'deck_1': {
            'note_on': [0x90, 41, 0],
            'note_off': [0x80, 41, 0]
        },
        'deck_2': {
            'note_on': [0x91, 42, 127],
            'note_off': [0x81, 42, 127]
        }
    },
    'adjust_speed_slower': {
        'deck_1': {
            'note_on': [0x90, 43, 127],
            'note_off': [0x80, 43, 127]
        },
        'deck_2': {
            'note_on': [0x91, 44, 127],
            'note_off': [0x81, 44, 127]
        }
    },
    'adjust_speed_faster': {
        'deck_1': {
            'note_on': [0x90, 45, 127],
            'note_off': [0x80, 45, 127]
        },
        'deck_2': {
            'note_on': [0x91, 46, 127],
            'note_off': [0x81, 46, 127]
        }
    },
    'temp_decrease_speed': {
        'deck_1': {
            'note_on': [0x90, 47, 127],
            'note_off': [0x80, 47, 127]
        },
        'deck_2': {
            'note_on': [0x91, 48, 127],
            'note_off': [0x81, 48, 127]
        }
    },
    'temp_increase_speed': {
        'deck_1': {
            'note_on': [0x90, 49, 127],
            'note_off': [0x80, 49, 127]
        },
        'deck_2': {
            'note_on': [0x91, 50, 127],
            'note_off': [0x81, 50, 127]
        }
    },
    'cue': {
        'deck_1': {
            'note_on': [0x90, 51, 127],
            'note_off': [0x80, 51, 127]
        },
        'deck_2': {
            'note_on': [0x91, 52, 127],
            'note_off': [0x81, 52, 127]
        }
    },
    'jump_to_start': {
        'deck_1': {
            'note_on': [0x90, 53, 127],
            'note_off': [0x80, 53, 127]
        },
        'deck_2': {
            'note_on': [0x91, 54, 127],
            'note_off': [0x81, 54, 127]
        }
    },
    'play_reverse': {
        'deck_1': {
            'note_on': [0x90, 55, 127],
            'note_off': [0x80, 55, 127]
        },
        'deck_2': {
            'note_on': [0x91, 56, 127],
            'note_off': [0x81, 56, 127]
        }
    },
    'stop_and_jump_to_start': {
        'deck_1': {
            'note_on': [0x90, 57, 127],
            'note_off': [0x80, 57, 127]
        },
        'deck_2': {
            'note_on': [0x91, 58, 127],
            'note_off': [0x81, 58, 127]
        }
    },
    'strip_search': {
        'deck_1': {
            'control_change': [0xB0, 59, 127],
            'note_on': [0x90, 59, 63],
            'note_off': [0x80, 59, 63]
        },
        'deck_2': {
            'control_change': [0xB1, 60, 127],
            'note_on': [0x91, 60, 63],
            'note_off': [0x81, 60, 63]
        }
    },
    'bpm_plus_0.1': {
        'deck_1': {
            'note_on': [0x90, 61, 127],
            'note_off': [0x80, 61, 127]
        },
        'deck_2': {
            'note_on': [0x91, 62, 127],
            'note_off': [0x81, 62, 127]
        }
    },
    'bpm_minus_0.1': {
        'deck_1': {
            'note_on': [0x90, 63, 127],
            'note_off': [0x80, 63, 127]
        },
        'deck_2': {
            'note_on': [0x91, 64, 127],
            'note_off': [0x81, 64, 127]
        }
    },
    'sync': {
        'deck_1': {
            'note_on': [0x90, 65, 127],
            'note_off': [0x80, 65, 127]
        },
        'deck_2': {
            'note_on': [0x91, 66, 127],
            'note_off': [0x81, 66, 127]
        }
    },
    'key_lock': {  # needs to be mapped
        'deck_1': {
            'note_on': [0x90, 67, 127],
            'note_off': [0x80, 67, 127]
        },
        'deck_2': {
            'note_on': [0x91, 68, 127],
            'note_off': [0x81, 68, 127]
        }
    },
    'match_key': {
        'deck_1': {
            'note_on': [0x90, 69, 127],
            'note_off': [0x80, 69, 127]
        },
        'deck_2': {
            'note_on': [0x91, 70, 127],
            'note_off': [0x81, 70, 127]
        }
    },
    'reset_key': {
        'deck_1': {
            'note_on': [0x90, 71, 127],
            'note_off': [0x80, 71, 127]
        },
        'deck_2': {
            'note_on': [0x91, 72, 127],
            'note_off': [0x81, 72, 127]
        }
    },
    'beat_sync': {
        'deck_1': {
            'note_on': [0x90, 73, 127],
            'note_off': [0x80, 73, 127]
        },
        'deck_2': {
            'note_on': [0x91, 74, 127],
            'note_off': [0x81, 74, 127]
        }
    },
    'beat_loop_16': {
        'deck_1': {
            'note_on': [0x90, 75, 127],
            'note_off': [0x80, 75, 127]
        },
        'deck_2': {
            'note_on': [0x91, 76, 127],
            'note_off': [0x81, 76, 127]
        }
    },
    'quantize': {
        'deck_1': {
            'note_on': [0x90, 77, 127],
            'note_off': [0x80, 77, 127]
        },
        'deck_2': {
            'note_on': [0x91, 78, 127],
            'note_off': [0x81, 78, 127]
        }
    },
    'reset_speed': {  # Refers to pitch slider
        'deck_1': {
            'note_on': [0x90, 79, 127],
            'note_off': [0x80, 79, 127]
        },
        'deck_2': {
            'note_on': [0x91, 80, 127],
            'note_off': [0x81, 80, 127]
        }
    },
    'go_to_cue_and_play': {
        'deck_1': {
            'note_on': [0x90, 81, 127],
            'note_off': [0x80, 81, 127]
        },
        'deck_2': {
            'note_on': [0x91, 82, 127],
            'note_off': [0x81, 82, 127]
        }
    }
}
""",
    'blank': {
        'deck_1': {
            'note_on': 0,
            'note_off': 1
        },
        'deck_2': {
            'note_on': 0,
            'note_off': 1
        }
"""

""" 1 - 7 for library buttons"""
library_buttons = {
    'move_down': {
        'master': {
            'note_on': [0x92, 1, 127],
            'note_off': [0x82, 1, 127]
        }
    },
    'move_up': {
        'master': {
            'note_on': [0x92, 2, 127],
            'note_off': [0x82, 2, 127]
        }
    },
    'move_focus_left_pane': {
        'master': {
            'note_on': [0x92, 5, 127],
            'note_off': [0x82, 5, 127]
        }
    },
    'move_focus_right_pane': {
        'master': {
            'note_on': [0x92, 6, 127],
            'note_off': [0x82, 6, 127]
        }
    },
    'move_focus': {
        'master': {
            'note_on': [0x92, 7, 127],
            'note_off': [0x82, 7, 127]
        }
    }
}

""" 4 - 13 for knobs """
knobs = {
    'gain': {
        'channel_1': {
            'control_change': [0xB0, 4, 64]
        },
        'channel_2': {
            'control_change': [0xB1, 5, 64]
        }
    },
    'hi_eq': {
        'channel_1': {
            'control_change': [0xB0, 6, 64]
        },
        'channel_2': {
            'control_change': [0xB1, 7, 64]
        }
    },
    'mid_eq': {
        'channel_1': {
            'control_change': [0xB0, 8, 64]
        },
        'channel_2': {
            'control_change': [0xB1, 9, 64]
        }
    },
    'low_eq': {
        'channel_1': {
            'control_change': [0xB0, 10, 64]
        },
        'channel_2': {
            'control_change': [0xB1, 11, 64]
        }
    },
    'filter': {
        'channel_1': {
            'control_change': [0xB0, 12, 64]
        },
        'channel_2': {
            'control_change': [0xB1, 13, 64]
        }
    },
    'blank': {
        'channel_1': {
            'control_change': 1
        },
        'channel_2': {
            'control_change': 1
        }
    }
}

""" 1 - 3 for faders """
faders = {
    'crossfader': {
        'master': {
            'control_change': [0xB2, 1, 64]
        }
    },
    'fader': {
        'channel_1': {
            'control_change': [0xB0, 2, 127]
        },
        'channel_2': {
            'control_change': [0xB1, 3, 127]
        }
    }
}
