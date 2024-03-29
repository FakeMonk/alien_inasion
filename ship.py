# coding=gbk

import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
	
	def __init__(self ,ai_settings, screen):
		"""初始化飞船的位置"""
		super().__init__()
		self.screen = screen
		self.ai_settings = ai_settings
		
		#加载飞船并获取其外接矩形
		self.image = pygame.image.load('images/ship1.png')
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()
		
		#将每艘飞船放在屏幕底部中央
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom
		self.center = float(self.rect.centerx)
		
		#设置移动标志
		self.moving_right = False
		self.moving_left = False
		self.moving_up = False
		self.moving_down = False
		
	def blitme(self):
		"""在指定位置绘制飞船"""
		self.screen.blit(self.image,self.rect)
		
	def update(self):
		"""根据移动标志调整飞船位置"""
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.center += self.ai_settings.ship_speed_factor
		if self.moving_left and self.rect.left > self.screen_rect.left:
			self.center -= self.ai_settings.ship_speed_factor
		
		self.rect.centerx = self.center
		if self.moving_up:
			self.rect.centery -= self.ai_settings.ship_speed_factor
		if self.moving_down:
			self.rect.centery += self.ai_settings.ship_speed_factor
	
	def center_ship(self):
		"""让飞船在屏幕上剧中"""
		self.center = self.screen_rect.centerx
		
