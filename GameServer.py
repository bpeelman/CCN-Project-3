import threading
import pygame
import socket
import sys
import random

name = "test"
posx = 300
posy = 200
playerSpeed = 15
dropperSpeed = 0.2
collected = 0
gameover = False
dropped = []
circleColor1 = (255, 0, 204)

clientConnected = False


def GameThread():
    pygame.init()
    global clientConnected

    global circleColor1
    background = (135, 206, 235)
    playerColor = (120, 120, 120)
    
    fps = pygame.time.Clock()

    screen_size = screen_width, screen_height = 600, 400
    screen = pygame.display.set_mode(screen_size)

    pygame.display.set_caption('Welcome to the CCN Bucket Game.')

    global collected
    global gameover


    global posx 
    global posy 

    player = pygame.Rect(0, 0, 40, 40)
    global playerSpeed
    
    dropperCenter = (0, 0)
    dropperCenter = list(dropperCenter)
    dropperRadius = 10
    global dropperSpeed

    global dropped

    def numToDrop():
        num = random.randint(1, 3)
        return num
    
    font = pygame.font.SysFont(None, 30)  # Font for displaying the score

    
    """ def check_collision(center, radius, player):
        x = max(player.left, min(center[0], player.right))
        y = max(player.top, min(center[1], player.bottom))
        distance = math.sqrt((center[0] - x) ** 2 + (center[1] - y) ** 2)

        if (distance < radius):
            return True
        else:
            return False """

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(background)

        if gameover == False and clientConnected == True:


            if ((pygame.time.get_ticks() // 1000) % 6 == 0) and (len(dropped) < 5):
                for i in range(numToDrop()):
                    x_coord_dropped = random.randint(dropperRadius, screen_width-dropperRadius)
                    dropperCenter = [x_coord_dropped, 0]
                    dropped.append(dropperCenter)
            
            for dropperCenter in dropped:
                if (player.collidepoint(dropperCenter)):
                    if ((collected+1) % 11 == 0):
                        dropperSpeed += 0.1
                        playerSpeed += 5
                    collected += 1
                    dropped.remove(dropperCenter)
                else:
                    dropperCenter[1] += dropperSpeed
                if (dropperCenter[1] + dropperRadius) > screen_height:
                    gameover = True
            
            
                
        
        player.center = (posx, posy)

        for dropperCenter in dropped:
            if (collected > 50):
                circleColor1 = (255, 255, 255)
            elif (collected > 40):
                circleColor1 = (0, 255, 0)
            elif (collected > 30):
                circleColor1 = (255, 255, 0)
            elif (collected > 20):
                circleColor1 = (255, 165, 0)
            elif (collected > 10):
                circleColor1 = (255, 0, 0)

            pygame.draw.circle(screen, circleColor1, dropperCenter, dropperRadius)
        
        pygame.draw.rect(screen, playerColor, player)
        pygame.draw.rect(screen, (230, 230, 230), (0, 0, screen_width, 30), border_radius=15)

        score_text = font.render(f"Collected: {collected}", True, (0, 0, 0))
        screen.blit(score_text, (0, screen_height-20))
        

        pygame.display.update()
        fps.tick(60)

    
        if gameover:
            gameoverText = font.render("Game Over!", True, (0, 0, 0))
            screen.blit(gameoverText, (screen_width // 2 - 60, screen_height // 2 - 20))
            pygame.display.update()
            pygame.time.wait(5000)


    pygame.quit()


def restart():
    global collected
    global gameover
    global dropped
    global playerSpeed
    global dropperSpeed
    global circleColor1
    collected = 0
    gameover = False
    dropped = []
    dropperSpeed = 0.1
    playerSpeed = 10
    circleColor1 = (255, 0, 204)




def ServerThread():
    global posy
    global posx
    global playerSpeed
    global gameover
    global clientConnected
    # get the hostname
    host = socket.gethostbyname(socket.gethostname())
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    host = s.getsockname()[0]
    s.close()
    print(host)
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together
    print("Server enabled...")
    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))    
    while True:        
        clientConnected = True
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        
        print("from connected user: " + str(data))
        if(data == 'w'):
            posy -= playerSpeed
        if(data == 's'):
            posy += playerSpeed
        if(data == 'a'):
            posx -= playerSpeed
        if(data == 'd'):
            posx += playerSpeed
        if(gameover == True and data == 'r'):
            restart()
    conn.close()  # close the connection


t1 = threading.Thread(target=GameThread, args=[])
t2 = threading.Thread(target=ServerThread, args=[])
t1.start()
t2.start()