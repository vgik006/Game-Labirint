from pygame import*


class GameSprite(sprite.Sprite):
    def __init__(self,picture,x,y,w,h):
        sprite.Sprite.__init__(self)
        self.image= transform.scale(image.load(picture),(w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))


class Player(GameSprite):
    def __init__(self,picture,x,y,w,h,speed_x,speed_y):
        GameSprite.__init__(self,picture,x,y,w,h)
        self.speed_x = speed_x
        self.speed_y = speed_y
    def update(self):#метод
        if player.rect.x <= win_w-80 and player.speed_x > 0 or player.rect.x >=0 and player.speed_x < 0:
            self.rect.x += self.speed_x
        platform_touchad = sprite.spritecollide(self,barriers, False)
        if self.speed_x >0:
            for  p in platform_touchad:
                self.rect.right = min(self.rect.right,p.rect.left)
        elif self.speed_x <0:
            for p in platform_touchad:
                self.rect.right = max(self.rect.right,p.rect.left)
        if player.rect.y <= win_h-80 and player.speed_y > 0 or player.rect.y >=0 and player.speed_y <0:
            self.rect.y += self.speed_y
        platform_touchad = sprite.spritecollide(self,barriers, False)
        if self.speed_y >0:
            for p in platform_touchad:
                self.rect.bottom = min(self.rect.bottom,p.rect.top)
        elif self.speed_y <0:
            for p in platform_touchad:
                self.rect.top = max(self.rect.top,p.rect.bottom)
    def fire(self):
        bullet = Bullets('Bullet.png',self.rect.right ,self.rect.centery,20,26,30)
        bullets.add(bullet)

class Enemy(GameSprite):
    direction = 'down'
    def __init__(self,picture,x,y,w,h,speed):
        GameSprite.__init__(self,picture,x,y,w,h)
        self.speed = speed
    def update2(self):
        if self.rect.y >= 440:
            self.direction = 'up'
        if self.rect.y <= win_h - 470:
            self.direction = 'down'
        if self.direction == 'up':
           self.rect.y -= self.speed
        else:
            self.rect.y += self.speed
    def update(self):
        if self.rect.y >= 170:
            self.direction = 'up'
        if self.rect.y <= win_h -470:
            self.direction = 'down'
        if self.direction == 'up':
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed

class Bullets(GameSprite):
    def __init__(self,picture,x,y,w,h,speed):
        GameSprite.__init__(self,picture,x,y,w,h)
        self.speed = speed 
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > win_w + 10:
            self.kill()
        

                



back = (250,250,250)
win_w = 740
win_h = 500
window = display.set_mode((win_w,win_h))
display.set_caption('Моя первая игра')
w1 = GameSprite('wall.png',270,200,60,350)
w2 = GameSprite('wall.png',win_w/2-win_w/3,win_h/2,350,50)
w3 = GameSprite('wall.png',450,250,60,170)
w4 = GameSprite('wall.png',450,100,60,170)
w5 = GameSprite('wall.png',490,130,120,20)
w6 = GameSprite('wall.png',490,310,120,20)
player = Player('tank.png',5,320,110,40,0,0)
enemy = Enemy('Enemy.png',340,10,100,70,5)
enemy2 = Enemy('Enemy.png',620,30,100,70,4)
final = GameSprite('final.png',343,290,120,120)
win = transform.scale(image.load('win.jpg'),(win_w,win_h))
lose = transform.scale(image.load('lose.jpg'),(win_w,win_h))
barriers = sprite.Group()
barriers.add(w1)
barriers.add(w2)
barriers.add(w3)
barriers.add(w4)
barriers.add(w5)
barriers.add(w6)
bullets = sprite.Group()
enemys = sprite.Group()
enemys.add(enemy)
enemys2 = sprite.Group()
enemys2.add(enemy2)
start = True
finish = False
while start:
    time.delay(50)
    for e in event.get():
        if e.type == QUIT:
            start = False 
        if e.type == KEYDOWN:
            if e.key == K_w:
                player.speed_y = -5
            elif e.key == K_a:
                player.speed_x = -5
            elif e.key == K_s:
                player.speed_y = 5
            elif e.key == K_d:
                player.speed_x = 5
            elif e.key == K_SPACE:
                player.fire()
        if e.type == KEYUP:
            if e.key == K_w:
                player.speed_y = 0
            elif e.key == K_a:
                player.speed_x = 0               
            elif e.key == K_s:
                player.speed_y = 0                
            elif e.key == K_d:
                player.speed_x = 0
        
            
    if not finish:
        window.fill(back)
        player.reset()
        player.update()
        enemys.update()
        enemys.draw(window)
        enemys2.update()
        enemys2.draw(window)
        final.reset()
        bullets.update()
        bullets.draw(window)
        barriers.draw(window)

        if sprite.collide_rect(player,final):
            finish = True
            window.blit(win,(0,0))
        if sprite.spritecollide(player,enemys,False) or sprite.spritecollide(player,enemys2,False):
            finish  = True
            window.blit(lose,(0,0))
        sprite.groupcollide(bullets,barriers, True, False)
        sprite.groupcollide(bullets,enemys,True,True)
        sprite.groupcollide(bullets,enemys2,True,True)
    


    display.update()

        


