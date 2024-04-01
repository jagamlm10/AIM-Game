import pygame
import math
import random
import time

# Initialising Pygame 
pygame.init()

# Setting Width and Height of our Window object 
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AIM Trainer")  # Setting Captions

TARGET_INCREMENT = 400
TARGET_EVENT = pygame.USEREVENT  # Created a custom event using USEREVENT
TARGET_PADDING = 30

BG_COLOR = (0, 25, 40)
LIVES = 30
TOP_BAR_HEIGHT = 50

clock = pygame.time.Clock()

# Creating font objects from pygame module 

LABEL_FONT = pygame.font.SysFont("comicsans", 24)
HEAD_FONT = pygame.font.SysFont("comicsans", 32)


class Target:
    MAX_SIZE = 20  # Maximum size of our targets
    GROWTH_RATE = 0.2  # Rate at which they will increase/decrease
    COLOR = "red"
    SECOND_COLOR = "white"

    def __init__(self, x, y) -> None:
        # Setting coordinates for the centre of the circle( i.e Target)
        self.x = x
        self.y = y
        self.size = 0  # Radius of the circle
        self.grow = True

    # A method to monitor the growth of target object
    def update(self):
        # If the circle has already reached its maximum size
        #  then it is time to start shrinking it
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.grow = False

        if self.grow:
            self.size += self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE

    # A method to draw the target circle with ring like patterns 
    def draw(self, win):
        # The smaller circles get drawn over the larger circle 
        # since they are drawn after the larger ones
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size)
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.8)
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size * 0.6)
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.4)

    def collide(self, x, y):
        # Using the distance formaula of cordinate geometry we find the dist of our click from centre of target 
        # If our distance is less than the radius of the target then our target was pressed else not pressed
        dis = math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)
        return self.size >= dis


# A function to add sound_effects to the game 
def play_sound(address):
    pygame.mixer.init()
    pygame.mixer.music.load(address)
    pygame.mixer.music.set_volume(0.8)
    pygame.mixer.music.play()


# A function to fill the screen with BG_COLOR and draw all the targets in the targets list for each and every new frame
def draw(win, targets):
    win.fill(BG_COLOR)
    for target in targets:
        target.draw(win)


# A function to give a neat representation of time
def format_time(secs):
    milli = math.floor((secs * 1000 % 1000) / 100)
    seconds = int(round(secs % 60, 1))
    minutes = int(secs // 60)

    return f"{minutes:02d}:{seconds:02d}.{milli}"


# This function creates the top-bar for every new frame
def draw_top_bar(win, elapsed_time, targets_pressed, misses):
    pygame.draw.rect(win, "grey", (0, 0, WIDTH, TOP_BAR_HEIGHT))

    # Rendering instances of the font object inside the rectangle then we drew
    time_label = LABEL_FONT.render(f"Time : {format_time(elapsed_time)}", True, "black")
    if elapsed_time == 0:
        speed = 0
    else:
        speed = round(targets_pressed / elapsed_time, 1)

    speed_label = LABEL_FONT.render(f"Speed : {speed} t/s", True, "black")
    hit_label = LABEL_FONT.render(f"Hits : {targets_pressed}", True, "black")
    lives_label = LABEL_FONT.render(f"Lives : {LIVES - misses}", True, "black")

    win.blit(time_label, (10, 5))
    win.blit(speed_label, (200, 5))
    win.blit(hit_label, (450, 5))
    win.blit(lives_label, (650, 5))


# This functions renders the ending screen, when the game is over
def end_screen(win, elapsed_time, targets_pressed, clicks):
    win.fill(BG_COLOR)

    # Rendering instances of the font object onto the ending screen to show statistics
    head_label = HEAD_FONT.render("GAME OVER!!!", True, "white")
    time_label = LABEL_FONT.render(f"Time : {format_time(elapsed_time)}", True, "white")
    if elapsed_time == 0:
        speed = 0
    else:
        speed = round(targets_pressed / elapsed_time, 1)

    speed_label = LABEL_FONT.render(f"Speed : {speed} t/s", True, "white")
    hit_label = LABEL_FONT.render(f"Targets Hit : {targets_pressed}", True, "white")
    if clicks == 0:
        accuracy = 0
    else:
        accuracy = round(targets_pressed / clicks, 1)
    acc_label = LABEL_FONT.render(f"Accuracy : {accuracy}", True, "white")

    win.blit(head_label, (get_middle(head_label), 50))
    win.blit(time_label, (get_middle(time_label), 150))
    win.blit(speed_label, (get_middle(speed_label), 250))
    win.blit(hit_label, (get_middle(hit_label), 350))
    win.blit(acc_label, (get_middle(acc_label), 450))

    pygame.display.update()
    play_sound("./sound_effects/smb_gameover.wav")
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                quit()


def get_middle(surface):
    return WIDTH / 2 - surface.get_width() / 2


def main():
    run = True
    targets = []

    clicks = 0
    missess = 0
    targets_pressed = 0
    start_time = time.time()

    # This triggers the USEREVENT every TARGET_INCREMENT seconds
    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)

    while run:

        click = False
        mouse_pos = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time

        # Setting framerate to 60fps
        clock.tick(60)

        # Checking for events, mainly mouse_clicks, quit or a custom-event
        for event in pygame.event.get():

            # When the triggered event is quit event 
            if event.type == pygame.QUIT:
                run = False
                break

            # In case when USEREVENT gets triggered we create a new Target object and add it to he targets list 
            if event.type == pygame.USEREVENT:
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                y = random.randint(TARGET_PADDING + TOP_BAR_HEIGHT, HEIGHT - TARGET_PADDING)

                target = Target(x, y)
                targets.append(target)

            # When mouse_click is detected 
            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1

        for target in targets:
            target.update()

            if target.size <= 0:
                targets.remove(target)
                missess += 1

            if click and target.collide(*mouse_pos):
                targets.remove(target)
                targets_pressed += 1
                play_sound("./sound_effects/smb_coin.wav")

        if missess >= LIVES:
            end_screen(WIN, elapsed_time, targets_pressed, clicks)

        # The new frames for BG_COLOR + targets gets created along with the updated top-bar 
        # This frame is then rendered onto the screen with .update() method of .display() object 
        draw(WIN, targets)
        draw_top_bar(WIN, elapsed_time, targets_pressed, missess)
        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
