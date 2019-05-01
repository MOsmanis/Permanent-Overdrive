import subprocess
import curses
import time
import random
from random import randint

Y = 50
X = 100

def main():
    
    curses_controller = CursesController(0)
    curses_controller.initCurses()
    try:
        game(curses_controller)
    except KeyboardInterrupt:
        curses_controller.closeCurses()
        exit()

class O():
    def  __init__(self, **kwargs):
        self.location = (17, 2)
        self.level = 0
    def move(self, direction, data):
        newdata = data
        if direction == "left":
            x, y = self.location
            if y <= -1:
                return list("dead")
            newPOS = newdata[34*y + x-1]
            if newPOS == ' ':
                self.location = (x - 1, y)
                newdata[34 * y + x] = ' '
                newdata[34 * y + x - 1] = 'O'
            elif newPOS == 'I':
                return list("dead")
            elif newPOS == 'U':
                return list("next")
        if direction == "up":
            x, y = self.location
            if y <= -1:
                return list("dead")
            newPOS = newdata[34*(y-1) + x]
            if newPOS == ' ':
                self.location = (x, y - 1)
                newdata[34 * y + x] = ' '
                newdata[34 * (y-1) + x] = 'O'
            elif newPOS == 'I':
                return list("dead")
            elif newPOS == 'U':
                return list("next")
        if direction == "right":
            x, y = self.location
            if y <= -1:
                return list("dead")
            newPOS = newdata[34 * y + x + 1]
            if newPOS == ' ':
                self.location = (x + 1, y)
                newdata[34 * y + x] = ' '
                newdata[34 * y + x + 1] = 'O'
            elif newPOS == 'I':
                return list("dead")
            elif newPOS =='U':
                return list("next")
        if direction == "down":
            x, y = self.location
            if y <= -1:
                y = 0
            newPOS = newdata[34*(y+1) + x]
            if newPOS == ' ':
                self.location = (x, y + 1)
                newdata[34 * y + x] = ' '
                newdata[34 * (y+1) + x] = 'O'
            elif newPOS == 'I':
                return list("dead")
            elif newPOS == 'U':
                return list("next")
        return newdata



class DesignConfig():
    def __init__(self, **kwargs):
        keys = kwargs.keys()
        if 'font' in kwargs:
            self.font = kwargs.get('font')
        else:
            self.font = 'starwars'
        if 'message' in keys:
            self.message = kwargs.get('message')
        else:
            self.message = 'Permanent Overdrive'

class CursesController():
    def __init__(self, level):
        self.level = level
        self.data = list(
        "IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII\n" +
        "I                               I\n" +
        "I      Permanent Overdrive      I\n" +
        "I                               I\n" +
        "I                               I\n" +
        "I                               I\n" +
        "I                               I\n" +
        "I                               I\n" +
        "IIIIIIIIIII           IIIIIIIIIII\n" +
        "I                               I\n" +
        "I                               I\n" +
        "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU\n"
        )

    def initCurses(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.stdscr.nodelay(1)
        self.stdscr.keypad(1)
        rows = "".join(self.data).split("\n")
        i=0
        for row in rows:
            self.stdscr.addstr(0+i,0+X,row)
            i+=1

        self.stdscr.addstr(3, 50+X, "Score: " + str(self.level))
        self.stdscr.addstr(6, 50+X, "Go to bottom to advance!")
        self.stdscr.addstr(7, 50+X, "Movement speed is random for each key press")
        self.stdscr.addstr(8, 50+X, "You die if you touch walls! ('I')")
        self.stdscr.addstr(9, 50+X, "Press arrow to move in that direction")
        self.stdscr.addstr(10, 50+X, "Move to start game")
        self.stdscr.addstr(12, 50+X, "\"q\" to quit!")

    def write(self):
        self.stdscr.clear()
        rows = "".join(self.data).split("\n")
        i=0
        for row in rows:
            self.stdscr.addstr(0+i,0+X,row)
            i+=1
        self.stdscr.addstr(3, 50+X, "Score: " + str(self.level))
        self.stdscr.addstr(6, 50+X, "Go to bottom to advance!")
        self.stdscr.addstr(7, 50+X, "Movement speed is random for each key press")
        self.stdscr.addstr(8, 50+X, "You die if you touch walls! ('I')")
        self.stdscr.addstr(9, 50+X, "Press arrow to move in that direction")
        self.stdscr.addstr(10, 50+X, "Move to start game")
        self.stdscr.addstr(12, 50+X, "\"q\" to quit!")

    def closeCurses(self):
        curses.nocbreak()
        self.stdscr.keypad(0)
        curses.echo()
        curses.endwin()

def cutBeginning(curses_controller, o):
    data = curses_controller.data
    lines_to_cut = 1
    i = 0
    while i < lines_to_cut:
        curses_controller.data = data[34:]
        i+=1
    x, y = o.location
    o.location = (x,(y-lines_to_cut))
    refresh(curses_controller, o)


def game(curses_controller):
    o = O()
    while 1:
        key = curses_controller.stdscr.getch()

        if curses_controller.data != "Dead! Press \"r\" for restart":
            if key == curses.KEY_LEFT:
                cutBeginning(curses_controller, o)
                random_move(curses_controller, o, "left")
                #cutBeginning(curses_controller, o)

            if key == curses.KEY_RIGHT:
                cutBeginning(curses_controller, o)
                random_move(curses_controller, o, "right")
                #cutBeginning(curses_controller, o)

            if key == curses.KEY_UP:
                cutBeginning(curses_controller, o)
                random_move(curses_controller, o, "up")
                #cutBeginning(curses_controller, o)

            if key == curses.KEY_DOWN:
                cutBeginning(curses_controller, o)
                random_move(curses_controller, o, "down")
                #cutBeginning(curses_controller, o)

            if key == ord('q'):
                curses_controller.closeCurses()
                exit()
        else:
            if key == ord('q'):
                curses_controller.closeCurses()
                exit()

            if key == ord('r'):
                curses_controller.closeCurses()
                main()



def random_move(curses_controller, o, direction):
    displacement = randint(1, 5)
    if o.level < 5:
        if direction == "left" or direction == "right":
            displacement += 3
    i = 0
    while i < displacement:
        i += 1
        status = o.move(direction, curses_controller.data)
        if "".join(status) == "dead":
            curses_controller.data = "Dead! Press \"r\" for restart"
            refresh(curses_controller, o)
            break;
        elif "".join(status) == "next":
            o.level +=1
            curses_controller.level=o.level
            if o.level < 5:
                random_wall = list("IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII\n")
                hole = randint(3, 29)
                random_wall[hole] = ' '
                random_wall[hole + 1] = ' '
                random_wall[hole + 2] = ' '
                random_wall[hole - 1] = ' '
                random_wall[hole - 2] = ' '
                animate_open_doors(curses_controller, o)
                curses_controller.data += list(
                "I                               I\n" +
                "I                               I\n" +
                "I                               I\n" +
                "I                               I\n" +
                "I                               I\n" +
                "I                               I\n" +
                "I                               I\n" +
                "I                               I\n" +
                "".join(random_wall) +
                "I                               I\n" +
                "I                               I\n" +
                "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU\n"
                )
                refresh(curses_controller, o)
                break;
            elif o.level == 5:
                animate_open_doors(curses_controller, o)
                curses_controller.data += list(
                "I                               I\n" +
                "I                               I\n" +
                "I                               I\n" +
                "I                               I\n" +
                "I                               I\n" +
                "II                             II\n" +
                "IIII                         IIII\n" +
                "IIIIII                     IIIIII\n" +
                "IIIIIIII                 IIIIIIII\n" +
                "IIIIIIIIII             IIIIIIIIII\n" +
                "IIIIIIIIII             IIIIIIIIII\n" +
                "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU\n"
                )
                refresh(curses_controller, o)
                break;
            elif o.level > 5:
                animate_open_doors(curses_controller, o)
                random_wall = list("IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII\n")
                hole = randint(10, 22)
                random_wall[hole] = ' '
                animate_open_doors(curses_controller, o)
                curses_controller.data += list(
                "IIIIIIIIII             IIIIIIIIII\n" +
                "IIIIIIIIII             IIIIIIIIII\n" +
                "IIIIIIIIII             IIIIIIIIII\n" +
                "IIIIIIIIII             IIIIIIIIII\n" +
                "IIIIIIIIII             IIIIIIIIII\n" +
                "IIIIIIIIII             IIIIIIIIII\n" +
                "IIIIIIIIII             IIIIIIIIII\n" +
                "".join(random_wall) +
                "IIIIIIIIII             IIIIIIIIII\n" +
                "IIIIIIIIII             IIIIIIIIII\n" +
                "IIIIIIIIII             IIIIIIIIII\n" +
                "UUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUUU\n"
                )
                refresh(curses_controller, o)
                break;
        else:
            curses_controller.data = status
            refresh(curses_controller, o)
    

def refresh(curses_controller, o):
    overflow = len(curses_controller.data) - (34 * Y)
    if overflow > 0:
        curses_controller.data = curses_controller.data[overflow:]
        x, y = o.location
        o.location = (x,(y-(overflow//34)))
    curses_controller.write()
    curses_controller.stdscr.refresh()
    time.sleep(.030)

def animate_open_doors(curses_controller, o):
    length = len(curses_controller.data)
    curses_controller.data[length-18]=' '
    refresh(curses_controller, o)
    i = 1
    width=2
    if o.level > 5:
        width=11
    while i<17:
        curses_controller.data[length-18+i]=' '
        curses_controller.data[length-18-i]=' '
        if i>17-width:
           curses_controller.data[length-18+i]='I'
           curses_controller.data[length-18-i]='I'
        i+=1
        refresh(curses_controller, o)
    curses_controller.data[length-1]='\n'
    refresh(curses_controller, o)


if __name__ == '__main__':
    main()
