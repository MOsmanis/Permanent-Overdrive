import subprocess
import curses
import time
import random
from random import randint
import socket
import pickle
import threading
import sys

SERVER = "127.0.0.1"
PORT = 8080
NAME = "player"
SCORE = 0
STATUS = "alive"
GAME_BOARD = "Loading..."
ENEMY_NAME = "Not connected"
ENEMY_SCORE = "Not connected"
ENEMY_MAX_SCORE = 0
ENEMY_STATUS = "Not connected"
ENEMY_X = 120
ENEMY_GAME_BOARD = "Not Connected"
WAITING_FOR_ENEMY = True
X = 20


def main():
    if len(sys.argv)>1:
        global NAME
        NAME = sys.argv[1]
    clientThread = ClientThread()
    clientThread.start()
    if(WAITING_FOR_ENEMY):
        print("Waiting for second player...")
    while(WAITING_FOR_ENEMY):
      continue
    try:
        while(WAITING_FOR_ENEMY):
            continue
        curses_controller = CursesController(0)
        curses_controller.initCurses()
        game(curses_controller)
    except KeyboardInterrupt:
        curses_controller.closeCurses()
        exit()

class ClientThread(threading.Thread):
    def __init__(self): 
        threading.Thread.__init__(self)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def run(self):
        global ENEMY_NAME
        global ENEMY_SCORE
        global ENEMY_STATUS
        global WAITING_FOR_ENEMY
        global ENEMY_GAME_BOARD
        self.client.connect((SERVER, PORT))
        playerData = PlayerData(NAME, SCORE, SCORE, STATUS, GAME_BOARD)
        data_string = pickle.dumps(playerData)
        self.client.send(data_string)
        enemyData = self.client.recv(8192)
        enemy = pickle.loads(enemyData)
        ENEMY_NAME = enemy.name
        ENEMY_SCORE = enemy.score
        ENEMY_MAX_SCORE = enemy.max_score
        ENEMY_STATUS = enemy.status
        ENEMY_GAME_BOARD = enemy.game_board
        WAITING_FOR_ENEMY = False
        while True:
            playerData = PlayerData(NAME, SCORE, SCORE, STATUS, GAME_BOARD)
            data_string = pickle.dumps(playerData)
            self.client.send(data_string)
            enemyData = self.client.recv(8192)
            enemy = pickle.loads(enemyData)
            ENEMY_NAME = enemy.name
            ENEMY_SCORE = enemy.score
            ENEMY_MAX_SCORE = enemy.max_score
            ENEMY_STATUS = enemy.status
            ENEMY_GAME_BOARD = enemy.game_board

class PlayerData():
    def  __init__(self, name, score, max_score, status, game_board):
        self.name = name
        self.score = score
        self.max_score = max_score
        self.status = status
        self.game_board = game_board
  

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
        global GAME_BOARD
        GAME_BOARD = self.data

    def initCurses(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        self.stdscr.nodelay(1)
        self.stdscr.keypad(1)
        max_rows, max_cols = self.stdscr.getmaxyx()
        rows = "".join(self.data).split("\n")
        enemy_rows = "".join(ENEMY_GAME_BOARD).split("\n")
        i=0
        for row in rows:
            if i>=max_rows:
                break
            overflow = X+len(row) - max_cols
            if overflow<len(row):
                if overflow>=0:
                    row_length = len(row)
                    self.stdscr.addstr(i,X,row[0:row_length-overflow])
                else:
                    self.stdscr.addstr(i,X,row)
            i+=1
        i=0
        for enemy_row in enemy_rows:
            if i>=max_rows:
                break
            overflow = ENEMY_X+len(enemy_row) - max_cols
            if overflow<len(enemy_row):
                if overflow>=0:
                    row_length = len(enemy_row)
                    self.stdscr.addstr(i,ENEMY_X,enemy_row[0:row_length-overflow])
                else:
                    self.stdscr.addstr(i,ENEMY_X,enemy_row)
            i+=1
        instruction_rows = ["Score: " + str(self.level)+ "     Enemy Screen:",
        "Go to bottom to advance!",
        "Movement speed is random for each key press",
        "You die if you touch walls! ('I')",
        "Press arrow to move in that direction",
        "Move down to start game",
        "\"q\" to quit!",
        "Enemy name: " + ENEMY_NAME,
        "Enemy score: " + str(ENEMY_SCORE),
        "Enemy status: " + ENEMY_STATUS]
        i=3
        for instruction_row in instruction_rows:
            i+=1
            overflow = 50+X+len(instruction_row) - max_cols
            if overflow<len(instruction_row):
                if overflow>=0:
                    row_length = len(instruction_row)
                    self.stdscr.addstr(i,50+X, instruction_row[0:row_length-overflow])
                else:
                    self.stdscr.addstr(i,50+X, instruction_row)
        curses.curs_set(0)
    def write(self):
        self.stdscr.clear()
        rows = "".join(self.data).split("\n")
        enemy_rows = "".join(ENEMY_GAME_BOARD).split("\n")
        max_rows, max_cols = self.stdscr.getmaxyx()
        i=0
        for row in rows:
            if i>=max_rows:
                break
            overflow = X+len(row) - max_cols
            if overflow<len(row):
                if overflow>=0:
                    row_length = len(row)
                    self.stdscr.addstr(i,X,row[:row_length-overflow])
                else:
                    self.stdscr.addstr(i,X,row)
            i+=1
        i=0
        for enemy_row in enemy_rows:
            if i>=max_rows:
                break
            overflow = ENEMY_X+len(enemy_row) - max_cols
            if overflow<len(enemy_row):
                if overflow>=0:
                    row_length = len(enemy_row)
                    self.stdscr.addstr(i,ENEMY_X,enemy_row[:row_length-overflow])
                else:
                    self.stdscr.addstr(i,ENEMY_X,enemy_row)
            i+=1
        instruction_rows = ["Score: " + str(self.level)+ "     Enemy Screen:",
        "Go to bottom to advance!",
        "Movement speed is random for each key press",
        "You die if you touch walls! ('I')",
        "Press arrow to move in that direction",
        "Move down to start game",
        "\"q\" to quit!",
        "Enemy name: " + ENEMY_NAME,
        "Enemy score: " + str(ENEMY_SCORE),
        "Enemy status: " + ENEMY_STATUS]
        i=3
        for instruction_row in instruction_rows:
            overflow = 50+X+len(instruction_row) - max_cols
            i+=1
            if overflow<len(instruction_row):
                if overflow>=0:
                    row_length = len(instruction_row)
                    self.stdscr.addstr(i,50+X, instruction_row[0:row_length-overflow])
                else:
                    self.stdscr.addstr(i,50+X, instruction_row)
        
        curses.curs_set(0)

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
        global SCORE
        global STATUS
        global GAME_BOARD
        GAME_BOARD = curses_controller.data
        SCORE = o.level
        
        if curses_controller.data != "Dead! Press \"r\" for restart":
            STATUS = "alive"
            if key == curses.KEY_LEFT:
                cutBeginning(curses_controller, o)
                random_move(curses_controller, o, "left")

            if key == curses.KEY_RIGHT:
                cutBeginning(curses_controller, o)
                random_move(curses_controller, o, "right")

            if key == curses.KEY_UP:
                cutBeginning(curses_controller, o)
                random_move(curses_controller, o, "up")

            if key == curses.KEY_DOWN:
                cutBeginning(curses_controller, o)
                random_move(curses_controller, o, "down")

            if key == -1:
              refresh(curses_controller, o)

            if key == ord('q'):
                curses_controller.closeCurses()
                exit()
        else:
            STATUS = "dead"
            if key == ord('q'):
                curses_controller.closeCurses()
                exit()

            if key == ord('r'):
                curses_controller.closeCurses()
                main()

            if key == -1:
              refresh(curses_controller, o)



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
            break
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
                break
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
                break
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
                break
        else:
            curses_controller.data = status
            refresh(curses_controller, o)
    

def refresh(curses_controller, o):
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
