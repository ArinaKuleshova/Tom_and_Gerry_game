from pygame import *
from random import *
from time import time as timer

lost = 0
score = 0
reload_time = False
count_bullet = 0
start_reload = 0
life_score = 5

class Sprite(sprite.Sprite):
    def __init__(self, image_sprite, x_sprite, y_sprite, speed_sprite, weight, height):
        super().__init__()
        self.image = transform.scale(image.load(image_sprite), (weight, height))
        self.speed = speed_sprite
        self.rect = self.image.get_rect()
        self.rect.x = x_sprite
        self.rect.y = y_sprite
        self.weight = weight
        self.height = height

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(Sprite):
    def update(self):
        keys = key.get_pressed()
        global count_bullet, reload_time, start_reload
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_w - self.weight:
            self.rect.x += self.speed
        if keys[K_SPACE]:
            if count_bullet < 5 and reload_time is False:
                count_bullet += 1
                self.fire()
            elif count_bullet >= 5 and  reload_time is False:
                reload_time = True
                start_reload = timer()


    def fire(self):
        bullets.add(Bullet('cheese.png', self.rect.centerx, self.rect.y, 15, 20, 20) )


class Enemy(Sprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_h:
            self.rect.x = randint(0, win_w - 80)
            self.rect.y = 0 
            lost += 1 


class Bullet(Sprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()



win_w = 700
win_h = 500
window = display.set_mode((win_w,win_h))
display.set_caption('Лабиринт')
background = transform.scale(image.load('back.jpg'), (win_w,win_h))
clock = time.Clock()
mixer.init()
mixer.music.load('space.ogg')
font.init()
font_one = font.SysFont('Arial', 36)
win = font_one.render('ПОБЕДА', True, (255, 255, 255))
lose = font_one.render('ПОРАЖЕНИЕ', True, (255, 255, 255))
wait = font_one.render('Перезарядка', True, (255, 0, 0))


finish = False

player = Player('tom.png', 5, 400, 10, 100, 100)

bullets = sprite.Group()

enemys = sprite.Group()

bad_enemys = sprite.Group()


for i in range(5):
    enemys.add(Enemy('mouse.png', randint(0, win_w - 80), -40, randint(1,3), 50, 50))
for i in range(3):
    bad_enemys.add(Enemy('dog.png', randint(0, win_w - 80), -40, randint(1,3), 70, 70))

end = True
while end:
    for e in event.get():
        if e.type == QUIT:
            end = False
    if not finish:
        text_lost = font_one.render('Пропущено ' + str(lost), True, (255, 255, 255))
        text_score = font_one.render('Уничтожено ' + str(score), True, (255, 255, 255))
        life = font_one.render(str(life_score), True, (255, 255, 255))
        window.blit(background, (0,0))
        bullets.draw(window)
        bullets.update()
        player.reset()
        player.update()
        enemys.draw(window)
        enemys.update()
        bad_enemys.draw(window)
        bad_enemys.update()
        window.blit(life, (650, 10))

        collides = sprite.groupcollide(bullets, enemys, True, True)
        for collide in collides:
            score += 1
            enemys.add(Enemy('mouse.png', randint(0, win_w - 80), -40, randint(1,3), 50, 50))
        if sprite.spritecollide(player, enemys, True) or lost > 3 or sprite.spritecollide(player, bad_enemys, True):
            life_score -= 1
            
        if score == 10:
            finish = True
            window.blit(win, (300, 250))

        if reload_time is True:
            now_time = timer()
            if now_time - start_reload < 3:
                window.blit(wait, (250, 450))
            else:
                count_bullet = 0
                reload_time = False
        
        if life_score <= 0:
            finish = True
            window.blit(lose, (300, 250))

        window.blit(text_lost, (10, 50))
        window.blit(text_score, (10, 100))

        clock.tick(60)
        display.update()
