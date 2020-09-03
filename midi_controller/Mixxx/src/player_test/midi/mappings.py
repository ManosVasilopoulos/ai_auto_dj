dj_buttons = {
    'fast_rewind': {
        'deck_1': {
            'note_on': [0x90, 40, 127],
            'note_off': [0x80, 40, 127]
        },
        'deck_2': {
            'note_on': [0x90, 64, 127],
            'note_off': [0x80, 64, 127]
        }
    },
    'cue': {
        'deck_1': {
            'note_on': [0x90, 47, 127],
            'note_off': [0x80, 47, 127]
        },
        'deck_2': {
            'note_on': [0x90, 71, 127],
            'note_off': [0x80, 71, 127]
        }
    },
    'flanger': {
        'deck_1': {
            'note_on': [0x90, 52, 127],
            'note_off': [0x80, 52, 127]
        },
        'deck_2': {
            'note_on': [0x90, 76, 127],
            'note_off': [0x80, 76, 127]
        }
    },
    'fast_forward': {
        'deck_1': {
            'note_on': [0x90, 41, 127],
            'note_off': [0x80, 41, 127]
        },
        'deck_2': {
            'note_on': [0x90, 65, 127],
            'note_off': [0x80, 65, 127]
        }
    },
    'play_pause': {
        'deck_1': {
            'note_on': [0x90, 36, 127],
            'note_off': [0x80, 36, 127]
        },
        'deck_2': {
            'note_on': [0x90, 60, 127],
            'note_off': [0x80, 60, 127]
        }
    },
    'adjust_speed_slower': {
        'deck_1': {
            'note_on': [0x90, 43, 127],
            'note_off': [0x80, 43, 127]
        },
        'deck_2': {
            'note_on': [0x90, 67, 127],
            'note_off': [0x80, 67, 127]
        }
    },
    'adjust_speed_faster': {
        'deck_1': {
            'note_on': [0x90, 44, 127],
            'note_off': [0x80, 44, 127]
        },
        'deck_2': {
            'note_on': [0x90, 68, 127],
            'note_off': [0x80, 68, 127]
        }
    },
    'temp_decrease_speed': {
        'deck_1': {
            'note_on': [0x90, 45, 127],
            'note_off': [0x80, 45, 127]
        },
        'deck_2': {
            'note_on': [0x90, 69, 127],
            'note_off': [0x80, 69, 127]
        }
    },
    'temp_increase': {
        'deck_1': {
            'note_on': [0x90, 46, 127],
            'note_off': [0x80, 46, 127]
        },
        'deck_2': {
            'note_on': [0x90, 70, 127],
            'note_off': [0x80, 70, 127]
        }
    },
    'play_reverse': {
        'deck_1': {
            'note_on': [0x90, 38, 127],
            'note_off': [0x80, 38, 127]
        },
        'deck_2': {
            'note_on': [0x90, 62, 127],
            'note_off': [0x80, 62, 127]
        }
    },
    'blank': {
        'deck_1': {
            'note_on': 0,
            'note_off': 1
        },
        'deck_2': {
            'note_on': 0,
            'note_off': 1
        }
    }
}

library_buttons = {
    'move_focus': {
        'right_pane': {
            'note_on': [0x90, 5, 127],
            'note_off': [0x80, 5, 127]
        },
        'left_pane': {
            'note_on': [0x90, 6, 127],
            'note_off': [0x80, 6, 127]
        },
        'master': {
            'note_on': [0x90, 7, 127],
            'note_off': [0x80, 7, 127]
        }

    },
    'move_down': {
        'master': {
            'note_on': [0x90, 1, 127],
            'note_off': [0x80, 1, 127]
        }
    },
    'move_up': {
        'master': {
            'note_on': [0x90, 2, 127],
            'note_off': [0x80, 2, 127]
        }
    },
    'load_track': {
        'deck_1': {
            'note_on': [0x90, 3, 127],
            'note_off': [0x80, 3, 127]
        },
        'deck_2': {
            'note_on': [0x90, 4, 127],
            'note_off': [0x80, 4, 127]
        }
    }
}

knobs = {
    'gain': {
        'channel_1': {
            'control_change': [0xB0, 4, 64]
        },
        'channel_2': {
            'control_change': [0xB0, 5, 64]
        }
    },
    'hi_eq': {
        'channel_1': {
            'control_change': [0xB0, 6, 64]
        },
        'channel_2': {
            'control_change': [0xB0, 7, 64]
        }
    },
    'mid_eq': {
        'channel_1': {
            'control_change': [0xB0, 8, 64]
        },
        'channel_2': {
            'control_change': [0xB0, 9, 64]
        }
    },
    'low_eq': {
        'channel_1': {
            'control_change': [0xB0, 10, 64]
        },
        'channel_2': {
            'control_change': [0xB0, 11, 64]
        }
    },
    'filter': {
        'channel_1': {
            'control_change': [0xB0, 12, 64]
        },
        'channel_2': {
            'control_change': [0xB0, 13, 64]
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

faders = {
    'crossfader': {
        'master': {
            'control_change': [0xB0, 1, 64]
        }
    },
    'fader': {
        'channel_1': {
            'control_change': [0xB0, 2, 127]
        },
        'channel_2': {
            'control_change': [0xB0, 3, 127]
        }
    }
}
