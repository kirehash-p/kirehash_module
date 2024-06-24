import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

def init_audio():
    """音声再生の初期化"""
    pygame.mixer.init()
    return True

def play_audio(file_path, strength=1.0):
    """音声ファイルを再生する"""
    sound = pygame.mixer.Sound(file_path)
    sound.set_volume(strength)
    sound.play()
    return sound

def play_audio_loop(file_path, strength=1.0):
    """音声ファイルをループ再生する"""
    sound = pygame.mixer.Sound(file_path)
    sound.set_volume(strength)
    sound.play(-1)
    return sound

def quit_audio():
    """音声再生の終了"""
    pygame.mixer.quit()
    return True