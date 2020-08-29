import socket, threading
import pickle

PLAYER_COUNT = 0
PLAYER_NAMES = {}
PLAYER_SCORES = {}
PLAYER_MAX_SCORES = {}
PLAYER_STATUS = {}
PLAYER_GAME_BOARDS = {}
MAX_PLAYERS = 2
LOCALHOST = "127.0.0.1"
PORT = 8080

class PlayerData():
    def  __init__(self, name, score, max_score, status, game_board):
        self.name = name
        self.score = score
        self.max_score = max_score
        self.status = status
        self.game_board = game_board

class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket, clientId):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.id = clientId
        print ("New connection added: ", clientAddress)
    def run(self):
        print ("Connection from : ", clientAddress)
        playerData = self.csocket.recv(8192)
        player = pickle.loads(playerData)
        PLAYER_NAMES[self.id] = player.name
        PLAYER_SCORES[self.id] = player.score
        PLAYER_STATUS[self.id] = player.status
        PLAYER_MAX_SCORES[self.id] = int(player.max_score)
        PLAYER_GAME_BOARDS[self.id] = player.game_board
        if(self.id==0):
            print("Waiting for other player")
        while( (len(PLAYER_NAMES) < MAX_PLAYERS) or (len(PLAYER_SCORES) < MAX_PLAYERS) or (len(PLAYER_STATUS) < MAX_PLAYERS) ):
            continue
        enemyId = (self.id + 1) % MAX_PLAYERS
        enemyData = PlayerData(PLAYER_NAMES[enemyId], PLAYER_SCORES[enemyId], int(PLAYER_MAX_SCORES[enemyId]), PLAYER_STATUS[enemyId], PLAYER_GAME_BOARDS[enemyId])
        print(enemyData.name)
        data_string = pickle.dumps(enemyData)
        self.csocket.send(data_string)

        while True:
            playerData = self.csocket.recv(8192)
            player = pickle.loads(playerData)
            PLAYER_NAMES[self.id] = player.name
            PLAYER_SCORES[self.id] = player.score
            if int(PLAYER_MAX_SCORES[self.id]) < int(player.max_score):
                PLAYER_MAX_SCORES[self.id] = player.max_score
            PLAYER_STATUS[self.id] = player.status
            PLAYER_GAME_BOARDS[self.id] = player.game_board

            enemyData = PlayerData(PLAYER_NAMES[enemyId], PLAYER_SCORES[enemyId], int(PLAYER_MAX_SCORES[enemyId]), PLAYER_STATUS[enemyId], PLAYER_GAME_BOARDS[enemyId])
            data_string = pickle.dumps(enemyData)
            self.csocket.send(data_string)
        print ("Client at ", clientAddress , " disconnected...")
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("Server started")
print("Waiting for client request..")
while True:
    server.listen(1)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock, PLAYER_COUNT)
    newthread.start()
    PLAYER_COUNT+=1
    if(PLAYER_COUNT==MAX_PLAYERS):
        break