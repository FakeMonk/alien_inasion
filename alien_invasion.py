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
	#初始化并创建游戏对象
	pygame.init()
	ai_settings = Settings()
	screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
	pygame.display.set_caption("Alien Invasion")
	
	#创建一艘飞船
	ship = Ship(ai_settings, screen)
	
	#创建一个用于存储子弹的编组
	bullets = Group()
	
	#创建一个外星人群
	aliens = Group()
	gf.create_fleet(ai_settings, screen, ship, aliens)
	
	#创建用于存储游戏统计的实例
	stats = GameStats(ai_settings)
	sb = Scoreboard(ai_settings, screen, stats)
	
	#创建play按钮
	play_button = Button(ai_settings, screen, "Play")
	
	
	
	#开始游戏循环
	while True:
		gf.check_events(ship, ai_settings, bullets, screen, stats, play_button, aliens, sb)
		if stats.game_active:
			ship.update()
			gf.update_bullets(bullets, aliens, ai_settings , screen, ship, sb, stats)
			gf.update_aliens(ai_settings, aliens, stats, screen, ship, bullets, sb)
		gf.update_screen(ai_settings, ship, screen, bullets, aliens, play_button, stats, sb)
		
run_game()
