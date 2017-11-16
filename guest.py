# -*-coding: utf-8-*-
import pygame as pg
import threading
from tv import Television
import inputbox
import time
from random import randint

pg.init()

SCREEN_SIZE = (700, 700) #Comprimento definido
BACKGROUND_COLOR = (255, 255, 255)
CAPTION = "The guests and a TV"
stop = pg.image.load('stop.jpg')
watching = pg.image.load('watching.jpg')
blocked = pg.image.load('blocked.jpg')
resting = pg.image.load('resting.jpg')
tvsprite = pg.image.load("cinema.jpg")
update = pg.image.load("update.jpg")
update2 = pg.image.load("update2.jpg")
controle = pg.image.load("controle.png")

font = pg.font.SysFont('ubuntu', 16)
big = pg.font.SysFont('ubuntu', 30)
extrabig = pg.font.SysFont('ubuntu', 70)

class Guest(threading.Thread):

    global tv
    tv = Television()

    def __init__(self, favorite, watch_time, rest_time, name, pos_y):
        threading.Thread.__init__(self)
        self.fps = 60.0
        self.clock = pg.time.Clock()
        self.done = True

        self.favorite = favorite
        self.watch_time = watch_time
        self.rest_time = rest_time
        self.name = name
        self.pos_y = pos_y

    def animation_loop(self):
        pg.event.get()
        screen.blit(blocked, (30, self.pos_y))     #Desenha sprite blocked
        pg.display.update()

        tv.s.acquire()

        screen.blit(update2, (130, self.pos_y + 40))
        pg.display.update()

        if tv.channel != self.favorite:

            if tv.w > 0:
                tv.mutex2.acquire()
                tv.up = tv.up + 1
                tv.mutex2.release()

                tv.s.release()

                screen.blit(font.render("Blocked", True, (255, 0, 0)), (130, self.pos_y + 40))
                print "{} está bloqueado".format(self.name)
                pg.display.update()

                tv.c.acquire()

                screen.blit(update2, (130, self.pos_y + 40))
                pg.display.update()

                tv.mutex2.acquire()
                tv.up = tv.up - 1
                tv.mutex2.release()

                if tv.channel == self.favorite:
                    tv.mutex1.acquire()
                    tv.w = tv.w + 1

                    screen.blit(update2, (400, 220))
                    screen.blit(font.render("Watching amount: {} ".format(str(tv.w)), True, (0, 0, 0)), (400, 220))
                    pg.display.update()
                    tv.mutex1.release()

            else:
                tv.mutex1.acquire()
                tv.w = tv.w + 1

                screen.blit(update2, (400, 220))
                screen.blit(font.render("Watching amount: {} ".format(str(tv.w)), True, (0, 0, 0)), (400, 220))
                pg.display.update()
                screen.blit(update2, (400, 240))

                screen.blit(controle, (340, self.pos_y))

                screen.blit(font.render("{} grabbed the remote".format(str(self.name)), True, (255, 0, 0)), (400, 240))
                print "{} pegou o controle".format(self.name)
                pg.display.update()

                tv.channel = self.favorite

                #######################################MudouDeCanal################################
                screen.blit(tvsprite, (400, 20))
                screen.blit(extrabig.render(str(tv.channel), True, (0, 0, 0)), (510, 45))
                pg.display.update()
                ###################################################################################

                tv.mutex1.release()
                tv.s.release()

        else:
            tv.mutex1.acquire()
            tv.w = tv.w + 1

            screen.blit(update2, (400, 220))
            screen.blit(font.render("Watching amount: {} ".format(str(tv.w)), True, (0, 0, 0)), (400, 220))
            pg.display.update()
            tv.mutex1.release()
            tv.s.release()

        if tv.channel == self.favorite:

            ###################################Assiste#############################################
            screen.blit(font.render("Watching...", True, (35, 142, 35)), (130, self.pos_y + 40))
            print "{} está assistindo".format(self.name)
            pg.display.update()
            for i in range(self.watch_time, 0, -1):
                screen.blit(big.render(str(i), True, (35, 142, 35)), (85, self.pos_y + 10))
                pg.display.update()

                screen.blit(stop, (30, self.pos_y))
                pg.display.update()
                time.sleep(0.25)

                screen.blit(watching, (30, self.pos_y))
                pg.display.update()
                time.sleep(0.25)

                screen.blit(stop, (30, self.pos_y))
                pg.display.update()
                time.sleep(0.25)

                screen.blit(watching, (30, self.pos_y))
                pg.display.update()
                time.sleep(0.25)

                screen.blit(update, (85, self.pos_y + 10))
                pg.display.update()

            screen.blit(update2, (130, self.pos_y + 40))
            screen.blit(update, (340, self.pos_y))
            pg.display.update()
            #######################################################################################

            tv.mutex1.acquire()
            tv.w = tv.w - 1

            if tv.w == 0:
                for i in range(tv.up):
                    tv.c.release()

            screen.blit(update2, (400, 220))
            screen.blit(font.render("Watching amount: {} ".format(str(tv.w)), True, (0, 0, 0)), (400, 220))
            pg.display.update()

            tv.mutex1.release()

            ########################################Descansa#############################################
            screen.blit(resting, (30, self.pos_y))
            screen.blit(update, (85, self.pos_y + 10))
            screen.blit(font.render("Resting...", True, (0, 0, 156)), (130, self.pos_y + 40))
            print "{} está descansando".format(self.name)
            pg.display.update()
            for i in range(self.rest_time, 0, -1):
                screen.blit(update, (85, self.pos_y + 10))
                screen.blit(big.render(str(i), True, (0, 0, 156)), (85, self.pos_y + 10))
                pg.display.update()

                time.sleep(1)
            screen.blit(update, (85, self.pos_y + 10))
            screen.blit(update2, (130, self.pos_y + 40))
            pg.display.update()
            #############################################################################################

    def run(self):

        screen.blit(font.render("identity: {}".format(str(self.name)), True, (0, 0, 0)), (130, self.pos_y)) #id da thread
        screen.blit(font.render("Favorite: {}".format(str(self.favorite)), True, (153, 50, 205)), (130, self.pos_y + 20)) #canal favorito
        screen.blit(font.render("Watch Time: {}".format(str(self.watch_time)), True, (0, 0, 0)), (215, self.pos_y)) #tempo que asssiste
        screen.blit(font.render("Rest Time: {}".format(str(self.rest_time)), True, (0, 0, 0)), (215, self.pos_y + 20)) #tempo que descansa

        while True:
            self.animation_loop()
            self.clock.tick(self.fps)

def main():

    screen2 = pg.display.set_mode((280, 250))
    screen2.fill((255, 255, 255))
    pg.display.set_caption(CAPTION)

    num_guests = int(inputbox.ask(screen2, 20, 10, 220, 30, "Quantidade de hospedes"))
    num_channel = int(inputbox.ask(screen2, 20, 50, 220, 30, "Quantidade de canais"))
    min_watch_time = int(inputbox.ask(screen2, 20, 90, 220, 30, "Tempo minimo assistindo"))
    max_watch_time = int(inputbox.ask(screen2, 20, 130, 220, 30, "Tempo maximo assistindo"))
    min_rest_time = int(inputbox.ask(screen2, 20, 170, 220, 30, "Tempo minimo descansando"))
    max_rest_time = int(inputbox.ask(screen2, 20, 210, 220, 30, "Tempo maximo descansando"))

    pg.display.quit()

    global screen
    screen = pg.display.set_mode(SCREEN_SIZE)
    screen.fill(BACKGROUND_COLOR)
    pg.display.set_caption(CAPTION)

    y = 20
    for i in range(num_guests):
        t = Guest(randint(1, num_channel), randint(min_watch_time, max_watch_time), randint(min_rest_time, max_rest_time), i, 0)
        t.pos_y = y
        t.start()
        y = y + 71

if __name__ == "__main__":
    main()
