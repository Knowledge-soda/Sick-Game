import random

import pygame


class Presser:
    def __init__(self, table):
        self.w_table = table
        self.r_table = dict.fromkeys(table.values(), 0)

    def __call__(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.r_table[self.w_table.get(event.key)] = 1
            if event.type == pygame.KEYUP:
                self.r_table[self.w_table.get(event.key)] = 0

    def get(self, key):
        return self.r_table.get(key)


class Printer:
    def __init__(self, screen, x, y, newline):
        self.screen = screen
        self.x = x
        self.y = y
        self.nl = newline
        self.font = pygame.font.SysFont("Arial", 42)
        self.color = (244, 122, 18)
        self.lines = ["You are infected with:"]
        self.update()

    def update(self):
        self.images = [self.font.render(line, True, self.color)
                       for line in self.lines]

    def blit(self):
        for i, image in enumerate(self.images):
            self.screen.blit(image, (self.x, self.y + self.nl * i))

    def add(self, text):
        self.lines.append(text)
        self.update()


class Guy:
    def __init__(self, screen, diseases, image):
        self.screen = screen
        self.diseases = diseases
        self.dead = True
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.bottom = 700

    def init(self, right, speed):
        self.disease = random.choice(self.diseases)[:-1]
        if right:
            self.rect.x = 1280
            self.speed = -speed
        else:
            self.rect.right = 0
            self.speed = speed
        self.dead = False

    def be(self):
        if self.dead:
            return
        
        self.rect.x += self.speed
        if self.rect.x > 1280 or self.rect.right < 0:
            self.dead = True

    def blit(self):
        self.screen.blit(self.image, self.rect)

    def is_dead(self):
        return self.dead

    def get_disease(self):
        return self.disease


class Player:
    def __init__(self, screen, x, image):
        self.screen = screen
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.bottom = 700
        self.rect.x = x
        self.fy = 0
        self.antijump = False

    def be(self):
        self.rect.y += self.fy
        self.fy += 0.1
        if self.rect.bottom > 700:
            self.rect.bottom = 700
            self.fy = 0
            self.antijump = False

    def blit(self):
        self.screen.blit(self.image, self.rect)

    def move(self, x):
        self.rect.x += x
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.right > 1280:
            self.rect.right = 1280

    def jump(self):
        if self.rect.bottom >= 700 and not self.antijump:
            self.fy -= 5
            self.antijump = True

    def collide(self, other):
        return self.rect.colliderect(other.rect)


def get_guy(guys, screen, diseases, image):
    for guy in guys:
        if guy.is_dead():
            return guy
    ret = Guy(screen, diseases, image)
    guys.append(ret)
    return ret


def init_guy(guy):
    guy.init(random.randrange(2), random.randrange(4) + 1)


def main():
    with open("diseases.list") as some_file:
        all_diseases = some_file.readlines()
    r_screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    rs_size = r_screen.get_size()
    screen = pygame.Surface((1280, 800))

    pygame.init()

    keyboard = Presser({
        pygame.K_ESCAPE: "quit",
        pygame.K_RIGHT: "right",
        pygame.K_LEFT: "left",
        pygame.K_UP: "jump",
    })

    player_image = pygame.image.load("red.png")
    sick_image = pygame.image.load("green.png")

    ground = pygame.Rect(0, 700, 1280, 100)
    pl = Player(screen, 500, player_image)
    guys = []
    random_rate = 200
    next_rate = random.randint(1000, 2000)
    printer = Printer(screen, 20, 20, 50)
    my_diseases = set()
    print(next_rate)

    states = ["Healthy", "Neglibly sick", "A bit sick", "Sick",
              "Sicker", "Quite sick", "Sick, dude", "Sick AF",
              "Rad sick", "You'll survive"]
    s_font = pygame.font.SysFont("Arial", 42)
    state = "Health state: " + states[0]
    s_image = s_font.render(state, True, (23, 231, 88))

    end = False
    e_font = pygame.font.SysFont("Arial", 70)
    e_image = e_font.render("You are dead now!", True, (0, 0, 0))


    clock = pygame.time.Clock()

    run = True
    while run:
        keyboard()

        if keyboard.get("quit"):
            run = False

        if keyboard.get("right"):
            pl.move(2)
        if keyboard.get("left"):
            pl.move(-2)
        if keyboard.get("jump"):
            pl.jump()

        next_rate -= 1
        if not next_rate:
            random_rate = int(random_rate * 0.75)
            next_rate = random.randint(1500, 2000)
            if random_rate < 30:
                random_rate = 30
            print(random_rate, next_rate)
        if not random.randrange(random_rate):
            init_guy(get_guy(guys, screen, all_diseases, sick_image))

        pl.be()
        for guy in guys:
            guy.be()
            if pl.collide(guy):
                dis = guy.get_disease()
                if dis not in my_diseases:
                    printer.add(dis)
                    my_diseases.add(dis)
                if len(my_diseases) == 10:
                    end = True
                if len(my_diseases) < 10:
                    state = "Health state: " + states[len(my_diseases)]
                    s_image = s_font.render(state, True, (23, 231, 88))

        screen.fill((20, 20, 20))

        if end:
            screen.blit(e_image, (300, 300))
        else:
            printer.blit()
            screen.blit(s_image, (750, 20))

            for guy in guys:
                guy.blit()
            pl.blit()

            screen.fill((40, 60, 220), ground)

        pygame.transform.scale(screen, rs_size, r_screen)

        pygame.display.flip()

        clock.tick(120)
    print(len(guys))


if __name__ == "__main__":
    main()
