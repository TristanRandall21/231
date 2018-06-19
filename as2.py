import curses
import config
stdscr=curses.initscr()
curses.noecho()
MAPROWS = 22
MAPCOLS = 80
MAPWALL = '.'

# initialize map #http://pages.cpsc.ucalgary.ca/~aycock/231/as2.html
map = []
for i in range(MAPROWS):
        map.append([MAPWALL] * MAPCOLS)
#player start
roomNub=1
startx=0
starty=0

rooms = []
n = 0
#Read in configuration
#room read-in/implementation
line = config.CONFIG.split('\n')               
for L in (line):            #reversed so player starts in "first room defined in map"-Under Just like Rogue section of assignment
    if '#' in L:
        continue
    if 'room' in L:
        L_=L.split(' ')
        n=n+1
        location=str(L_[5:])       
        L_[1:5] = [int(v) for v in L_[1:5]] #adamk #http://stackoverflow.com/questions/3371269/call-int-function-on-every-list-element
        x=L_[1]
        y=L_[2]
        W=L_[3]
        H=L_[4]

        rooms.append(x)
        rooms.append(y)
        rooms.append(W)
        rooms.append(H)
        rooms.append(location)
        for i in range(y,y+H):
            for j in range(x,x+W):
                map[i][j] = ' '                
                
                if roomNub ==1:
                    startx=x
                    starty=y
                    pl=x+W//2,y+H//2
                    roomNub +=2
                        
#char read-in/implementation    
    if 'char' in L:
        L_=L.split(' ')
        L_[2:4] = [int(v) for v in L_[2:4]]
        ch=L_[1]
        x=L_[2]
        y=L_[3]
        map[y][x]=ch
stdscr.refresh()

map_=' '
for i in range(MAPROWS):
    for j in range(MAPCOLS):
        stdscr.addstr(i, j, map[i][j])
      
stdscr.refresh()

#Main Loop

Move = True
x,y = pl #room 1 location 
#My Player
# k(key) is the input
while Move == True:
    stdscr.addch(y, x, '@')
    stdscr.refresh()
    k = stdscr.getch()
    if k == ord('w') and stdscr.inch(y-1,x) != ord('.') and y>0:                        
        y -= 1
        stdscr.addch(y+1,x, map[y+1][x])
    elif k == ord('a') and stdscr.inch(y,x-1) != ord('.') and x>0: 
       x -= 1
       stdscr.addch(y,x+1, map[y][x+1])       
    elif k == ord('s') and stdscr.inch(y+1,x) != ord('.') and y<21:
       y += 1
       stdscr.addch(y-1, x, map[y-1][x])
    elif k == ord('d') and stdscr.inch(y,x+1) != ord('.') and x<79:
       x += 1
       stdscr.addch(y, x-1,map[y][x-1])
    elif k == ord('i') and stdscr.inch(y-1,x) != ord('.') and y>0:    
        y -= 1
        stdscr.addch(y+1, x, map[y+1][x])
    elif k == ord('j') and stdscr.inch(y,x-1) != ord('.') and x>0:
        x -= 1
        stdscr.addch(y, x+1, map[y][x+1])
    elif k == ord('k') and stdscr.inch(y+1,x) != ord('.') and y<21:
        y += 1
        stdscr.addch(y-1, x, map[y-1][x])
    elif k == ord('l') and stdscr.inch(y,x+1) != ord('.') and x <79:
        x += 1
        stdscr.addch(y, x-1, map[y][x-1])
    for i in range(n):
#Room chech for location label
        if ( x >= rooms[5 * i] and x < rooms[5 * i] + rooms[5 * i + 2] and y >= rooms[5 * i + 1] and y < rooms[5 * i + 1] + rooms[5 * i + 3]):
            location = None
            location = str(rooms[5 * i + 4])
            j=" " * 79
            stdscr.addstr(23,0,j)
            stdscr.addstr(23,0, location)
            
    curses.endwin()
