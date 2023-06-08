from pygame import *

#клас-батько для інших спрайтів
class GameSprite(sprite.Sprite):
    #конструктор класу
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        # Викликаємо конструктор класу (Sprite):
        sprite.Sprite.__init__(self)
    
        #кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(image.load(player_image), (size_x, size_y))

        #кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
    #метод, що малює героя на вікні
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

#клас головного гравця
class Player(GameSprite):
    #метод, у якому реалізовано управління спрайтом за кнопками стрілочкам клавіатури
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed,player_y_speed):
        # Викликаємо конструктор класу (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)

        self.x_speed = player_x_speed
        self.y_speed = player_y_speed
    ''' переміщає персонажа, застосовуючи поточну горизонтальну та вертикальну швидкість'''
    def update(self):  
        # Спершу рух по горизонталі
        if packman.rect.x <= win_width-80 and packman.x_speed > 0 or packman.rect.x >= 0 and packman.x_speed < 0:
            self.rect.x += self.x_speed
        # якщо зайшли за стінку, то встанемо впритул до стіни
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.x_speed > 0: # йдемо праворуч, правий край персонажа - впритул до лівого краю стіни
            for p in platforms_touched:
                self.rect.right = min(self.rect.right, p.rect.left) # якщо торкнулися відразу кількох, то правий край - мінімальний із можливих
        elif self.x_speed < 0: # йдемо ліворуч, ставимо лівий край персонажа впритул до правого краю стіни
            for p in platforms_touched:
                self.rect.left = max(self.rect.left, p.rect.right) # якщо торкнулися кількох стін, то лівий край - максимальний
        if packman.rect.y <= win_height-80 and packman.y_speed > 0 or packman.rect.y >= 0 and packman.y_speed < 0:
            self.rect.y += self.y_speed
        # якщо зайшли за стінку, то встанемо впритул до стіни
        platforms_touched = sprite.spritecollide(self, barriers, False)
        if self.y_speed > 0: # йдемо вниз
            for p in platforms_touched:
                # Перевіряємо, яка з платформ знизу найвища, вирівнюємося по ній, запам'ятовуємо її як свою опору:
                if p.rect.top < self.rect.bottom:
                    self.rect.bottom = p.rect.top
        elif self.y_speed < 0: # йдемо вгору
            for p in platforms_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom) # вирівнюємо верхній край по нижніх краях стінок, на які наїхали
    # метод "постріл" (використовуємо місце гравця, щоб створити там кулю)
    def fire(self):
        bullet = Bullet('ammo.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)

#клас спрайту-ворога
class Enemy_H(GameSprite):
    side = "left"
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, x1, x2):
        # Викликаємо конструктор класу (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
        self.x1 = x1
        self.x2 = x2
   #рух ворога
    def update(self):
        if self.rect.x <= self.x1: #w1.wall_x + w1.wall_width
            self.side = "right"
        if self.rect.x >= self.x2:
            self.side = "left"
        if self.side == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Enemy_V(GameSprite):
    side = "up"
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, y1, y2):
        # Викликаємо конструктор класу (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
        self.y1 = y1
        self.y2 = y2
   #рух ворога
    def update(self):
        if self.rect.y <= self.y1: #w1.wall_x + w1.wall_width
            self.side = "down"
        if self.rect.y >= self.y2:
            self.side = "up"
        if self.side == "up":
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed





# клас спрайту-кулі
class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # Викликаємо конструктор класу (Sprite):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
    #рух ворога
    def update(self):
        self.rect.x += self.speed
        # зникає, якщо дійде до краю екрана
        if self.rect.x > win_width+10:
            self.kill()

#Створюємо віконце
win_width = 1200
win_height = 800
display.set_caption("Лабіринт")
window = display.set_mode((win_width, win_height))
back = transform.scale(image.load('background.jpg'), (win_width,win_height))
#Створюємо групу для стін
barriers = sprite.Group()

#створюємо групу для куль
bullets = sprite.Group()

#Створюємо групу для монстрів
monsters = sprite.Group()

#Створюємо стіни картинки
w1 = GameSprite('Untitled2.jpg', 640, 140, 25, 690)
w2 = GameSprite('Untitled3.jpg', 10, 270, 500, 25)
w3 = GameSprite('Untitled3.jpg', 10, 540, 500, 25)
w4 = GameSprite('Untitled2.jpg', 10, 270, 20, 290)
w5 = GameSprite('Untitled3.jpg', 140, 400, 500, 25)
w6 = GameSprite('Untitled2.jpg', 500, 540, 20, 155)
w7 = GameSprite('Untitled3.jpg', 10, 670, 500, 25)
w8 = GameSprite('Untitled3.jpg', 150, 140, 500, 25)
w9 = GameSprite('Untitled2.jpg', 800, 0, 25, 240)
w10 = GameSprite('Untitled3.jpg', 640, 350, 400, 25)
w11 = GameSprite('Untitled2.jpg', 1020, 175, 25, 200)
w12 = GameSprite('Untitled3.jpg', 800, 480, 500, 25)
w13 = GameSprite('Untitled3.jpg', 650, 630, 410, 25)

barriers = sprite.Group()
bullets = sprite.Group()
barriers.add(w1)
barriers.add(w2)
barriers.add(w3)
barriers.add((w4))
barriers.add(w5)
barriers.add(w6)
barriers.add(w7)
barriers.add(w8)
barriers.add(w9)
barriers.add(w10)
barriers.add(w11)
barriers.add(w12)
barriers.add(w13)


#додаємо монети
font.init()
font1 = font.SysFont('arial', 25)

coins_amount_1 = 0

coin1 = GameSprite('coin.png', 570, 460, 20, 20)
coin2 = GameSprite('coin.png', 500, 50, 20, 20)
coin3 = GameSprite('coin.png', 265, 360, 20, 20)
coin4 = GameSprite('coin.png', 900, 300, 20, 20)
coin5 = GameSprite('coin.png', 1050, 570, 20, 20)
coins = sprite.Group()
coins.add(coin1)
coins.add(coin2)
coins.add(coin3)
coins.add(coin4)
coins.add(coin5)




#створюємо спрайти
packman = Player('PEOPLE.png', 5, win_height - 80, 80, 80, 0, 0)
monster1 = Enemy_V('anemy1.png', 550, 255, 80, 80, 5,150,310)
monster2 = Enemy_V('ANEMY2.png', 540, 550, 80, 80, 5,450,740)
monster3 = Enemy_H('ANEMY3.png', 200, 320, 80, 80, 5, 35,180)
monster4 = Enemy_H('ANEMY4.png', 330,60,80,80,5,360,550)
monster5 = Enemy_H('ANEMY3.png', 640, 260, 80, 80, 5, 660,920)
monster6 = Enemy_V('ANEMY2.png', 880, 10, 80, 80, 5,20,250)
monster7 = Enemy_V('ANEMY4.png', 1090, 20, 80, 80, 5,40,320)
monster8 = Enemy_V('anemy1.png', 1090, 700, 80, 80, 5,520,710)
monster9 = Enemy_H('ANEMY2.png', 670,550,80,80,5,670,900)
final_sprite = GameSprite('FINAL SPRITE.png', 690, 710, 80, 80)

#додаємо монстра до групи
monsters.add(monster1)
monsters.add(monster2)
monsters.add(monster3)
monsters.add(monster4)
monsters.add(monster5)
monsters.add(monster6)
monsters.add(monster7)
monsters.add(monster8)
monsters.add(monster9)
#змінна, що відповідає за те, як закінчилася гра
finish = False
#

   
#ігровий цикл
run = True
while run:
    #цикл спрацьовує кожну 0.05 секунд
    time.delay(50)
        #перебираємо всі події, які могли статися
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                packman.x_speed = -5
            elif e.key == K_RIGHT:
                packman.x_speed = 5
            elif e.key == K_UP:
                packman.y_speed = -5
            elif e.key == K_DOWN:
                packman.y_speed = 5
            elif e.key == K_SPACE:
                packman.fire()


        elif e.type == KEYUP:
            if e.key == K_LEFT:
                packman.x_speed = 0
            elif e.key == K_RIGHT:
                packman.x_speed = 0 
            elif e.key == K_UP:
                packman.y_speed = 0
            elif e.key == K_DOWN:
                packman.y_speed = 0

#перевірка, що гра ще не завершена
    if not finish:
        #оновлюємо фон кожну ітерацію
        window.blit(back, (0,0))#зафарбовуємо вікно кольором
        
        #запускаємо рухи спрайтів
        packman.update()
        bullets.update()

        #оновлюємо їх у новому місці при кожній ітерації циклу
        packman.reset()
        #рисуємо стіни 2
        
        bullets.draw(window)
        barriers.draw(window)
        final_sprite.reset()
    
        sprite.groupcollide(monsters, bullets, True, True)
        monsters.update()
        monsters.draw(window)
        sprite.groupcollide(bullets, barriers, True, False)

       
        sprite.spritecollide(packman, coins, True,)
        coins.update()
        coins.draw(window)
        #
        if sprite.spritecollide(packman, coins, True):
            coins_amount_1 += 1
        coin = font1.render(f'Монеток : {coins_amount_1}/5', True, (0, 0, 0))
        window.blit(coin, (545, 10))

        #Перевірка зіткнення героя з ворогом та стінами
        if sprite.spritecollide(packman, monsters, False):
            finish = True
            # обчислюємо ставлення
            img = image.load('fail3.png')
            d = img.get_width() // img.get_height()
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_height * d, win_height)), (90, 0))

        if sprite.collide_rect(packman, final_sprite) and coins_amount_1 == 5:
            finish = True
            img = image.load('win.png')
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (win_width, win_height)), (0, 0))

        

    display.update()