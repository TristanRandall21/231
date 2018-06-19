CONFIG = '''
# one-room map

# the room
room 20 10 30 7 Welcome to The Room!

# greetz, yo
char 2 10 5
char C 5 5
char C 8 5
char 3 11 5
char S 7 5
char P 6 5
char 1 12 5

## This is a comment too.

# now add some overlapping rooms

# a room without a visible symbol
room 24 14 3 3 A room is nigh! Alert the media!

# single-char "room"
room 25 15 1 1 I'm a room too...
# and symbol that marks it, which needs to be preserved when player moves past
char * 25 15

# aaaaaaaand add some room weirdness

# antechamber of commerce
room 23 5 1 5 THE HALLWAY... OF DOOM
room 21 2 5 3 THE ANTECHAMBER... OF DOOM

# make a Life Savers room extension
room 48 8 10 3 Welcome to The Room!
room 54 8 10 7 Welcome to The Room!
room 48 14 10 2 Welcome to The Room!

# I'm a people person
char O 60 10
char | 60 11
char | 60 12
char / 59 13
char \ 61 13
char / 61 11
char \ 59 11

# now add a corridor that reaches all four edges, for bounds testing
room 0 21 70 1 The outer limits... of doom.
room 0 17 1 5 The outer limits... of doom.
room 79 17 1 5 This should never be seen!
room 0 17 21 1 The outer limits... of doom.
room 70 0 1 22 The outer limits... of doom.
room 70 0 10 1 The outer limits... of doom.
room 79 0 1 3 The outer limits... of doom.
'''
