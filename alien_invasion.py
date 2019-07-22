# coding=gbk

import pygame
from pygame.sprite import Group

import game_functions as gf
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():
	#��ʼ����������Ϸ����
	pygame.init()
	ai_settings = Settings()
	screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
	pygame.display.set_caption("Alien Invasion")
	
	#����һ�ҷɴ�
	ship = Ship(ai_settings, screen)
	
	#����һ�����ڴ洢�ӵ��ı���
	bullets = Group()
	
	#����һ��������Ⱥ
	aliens = Group()
	gf.create_fleet(ai_settings, screen, ship, aliens)
	
	#�������ڴ洢��Ϸͳ�Ƶ�ʵ��
	stats = GameStats(ai_settings)
	sb = Scoreboard(ai_settings, screen, stats)
	
	#����play��ť
	play_button = Button(ai_settings, screen, "Play")
	
	
	
	#��ʼ��Ϸѭ��
	while True:
		gf.check_events(ship, ai_settings, bullets, screen, stats, play_button, aliens, sb)
		if stats.game_active:
			ship.update()
			gf.update_bullets(bullets, aliens, ai_settings , screen, ship, sb, stats)
			gf.update_aliens(ai_settings, aliens, stats, screen, ship, bullets, sb)
		gf.update_screen(ai_settings, ship, screen, bullets, aliens, play_button, stats, sb)
		
run_game()
