# coding=gbk

import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
	
	def __init__(self ,ai_settings, screen):
		"""��ʼ���ɴ���λ��"""
		super().__init__()
		self.screen = screen
		self.ai_settings = ai_settings
		
		#���طɴ�����ȡ����Ӿ���
		self.image = pygame.image.load('images/ship1.png')
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()
		
		#��ÿ�ҷɴ�������Ļ�ײ�����
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom
		self.center = float(self.rect.centerx)
		
		#�����ƶ���־
		self.moving_right = False
		self.moving_left = False
		self.moving_up = False
		self.moving_down = False
		
	def blitme(self):
		"""��ָ��λ�û��Ʒɴ�"""
		self.screen.blit(self.image,self.rect)
		
	def update(self):
		"""�����ƶ���־�����ɴ�λ��"""
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
		"""�÷ɴ�����Ļ�Ͼ���"""
		self.center = self.screen_rect.centerx
		
