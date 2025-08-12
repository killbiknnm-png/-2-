from pygame import*
from random import randint
from time import time as timer
font.init()
font2 =  font.Font(None, 40)
























clock = time.Clock()




















mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
mixer.music.set_volume(0.1)




















fire_sound = mixer.Sound('fire.ogg')
fire_sound.set_volume(0.5)
















 
window_windth = 1800
window_height = 1000
window = display.set_mode((window_windth, window_height))
display.set_caption('Space Shooter')
img_back = 'galaxy.jpg'
background = transform.scale(image.load(img_back), (window_windth, window_height))
run = True
finish = False
font.init()
font1 = font.Font(None, 80)
lose = font1.render('ТЫ ПРОИГРАЛ', True,(180, 0, 0))
win = font1.render('ПОБЕДА', True,(50, 205, 50))




















class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_width, player_height, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (player_width, player_height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def draw(self):
        window.blit(self. image, (self.rect.x, self.rect.y))
   




















class Player(GameSprite):
    def move (self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x>5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < window_windth - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
























lost = 0
score = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > window_height:
            self.rect.y = 0
            self.rect.x = randint(80, window_height-80)
            lost += 1


class Enemy2(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > window_height:
            self.rect.y = 0
            self.rect.x = randint(80, window_height-80)
           
       
class Bullet(GameSprite):








    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
 
bullets = sprite.Group()


monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy("ufo.png", randint(80, window_windth-80),-40, 80, 50, randint(1, 3))
    monsters.add(monster)
text_lose = font2.render("Пропущено: " + str(lost), 10, (255, 255, 255))


asteroids = sprite.Group()
for i in range(2):
    monster = Enemy2("asteroid.png", randint(80, window_windth-80),-40, 80, 50, randint(1, 3))
    asteroids.add(monster)


ship = Player('rocket.png', 5, window_height - 100, 80, 100, 10)




lives = 5
colors_lives = [
    (107, 0, 0),
    (107, 0, 0),
    (173, 86, 9),
    (250, 217, 0),
    (157, 181, 2),
    (0, 199, 43),
]



 
rel_time = False
num_fire = 0
while run:




    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == MOUSEBUTTONDOWN:
            if num_fire < 8 and rel_time == False:
                num_fire = num_fire + 1
                ship.fire()
                fire_sound.play()



            if num_fire >= 8 and rel_time == False:
                last_time = timer()
                rel_time = True            
    if not finish:
        if lost >=100:
            text2 = font2.render('ты проиграл!', 1, (255, 0, 0))
            window.blit(text2, (250, 250))
       
        window.blit(background, (0, 0))
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        text2 = font2.render('счет:'+str(score), 1, (255, 0, 0))
        window.blit(text2, (10, 30))
        ship.move()


        if sprite.spritecollide(ship, monsters, True):
            lives -= 1
            monster = Enemy('ufo.png', randint(80, window_windth - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)




        if sprite.spritecollide(ship, asteroids, True):
            lives -= 1
            monster = Enemy('asteroid.png', randint(80, window_windth - 80), -40, 80, 50, randint(1, 5))
            asteroids.add(monster)




        text_lives = font1.render(str(lives), 1, colors_lives[lives])
        window.blit(text_lives, (650, 10))  




        if rel_time == True:
            now_time = timer()
         
            if now_time - last_time < 3:
                reload = font2.render('Оружее заклинело....Ждите', 1, (250, 250, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False




        monsters.update()
        asteroids.update()
        monsters.draw(window)
        asteroids.draw(window)
        ship.draw()
        bullets.update()
        bullets.draw(window)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for i in collides:
            score += 1
            monster = Enemy("ufo.png", randint(80, window_windth - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        if lives <=0 or lost >= 11:
            finish = True
            window.blit(lose, (160, 150))
        if score >=11:
            finish = True
            window.blit(win, (150, 150))
           


    display.update()
    clock.tick(60)
