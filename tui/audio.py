import pygame


pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()


def play(filepath, sound_cache={}):
    if filepath not in sound_cache:
        sound_cache[filepath] = pygame.mixer.Sound(filepath.encode())

    # pygame.mixer.Channel(0).play(sound_cache[filepath])
    sound_cache[filepath].play()
