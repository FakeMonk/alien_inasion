# coding=gbk

import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard():
	"""��ʾ�÷���Ϣ��"""
	
	def __init__(self, ai_settings, screen, stats):
		"""��ʼ����ʾ�÷��漰������"""
		self.screen = screen
		self.screen_rect = screen.get_rect()
		self.ai_settings = ai_settings
		self.stats = stats
		
		#��ʾ�÷���Ϣʱʹ�õ���������
		self.text_color = (30, 30, 30)
		self.font = pygame.font.SysFont(None, 48)
		
		#׼����ʼ�÷�ͼ��
		self.prep_score()
		self.prep_high_score()
		self.prep_level()
		self.prep_ship()
		
	def prep_score(self):
		"""���÷���Ⱦ��ͼ��"""
		rounded_score = int(round(self.stats.score, -1))
		score_str = "{:,}".format(rounded_score)
		self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)
		
		#���÷�ͼ�������Ļ���Ͻ�
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20
		self.score_rect.top = 20
		
	def prep_high_score(self):
		"""����߷���Ⱦ��ͼ��"""
		rounded_high_score = int(round(self.stats.high_score, -1))
		high_score_str = "{:,}".format(rounded_high_score)
		self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.ai_settings.bg_color)
		
		#����߷�ͼƬ������Ļ�м��ϲ�
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.top = 20
		self.high_score_rect.centerx = self.screen_rect.centerx
		
	def prep_level(self):
		"""���ȼ���Ⱦ��ͼ��"""
		self.level_image = self.font.render(str(self.stats.level), True, self.text_color, self.ai_settings.bg_color)
		
		#���ȼ���ʾ�ڵ÷��·�
		self.level_image_rect = self.level_image.get_rect()
		self.level_image_rect.top = self.score_rect.bottom + 10
		self.level_image_rect.right = self.screen_rect.right - 20
		
	def prep_ship(self):
		"""��ʾ�����¶����ҷɴ�"""
		self.ships = Group()
		for ship_number in range(self.stats.ships_left):
			ship =Ship(self.ai_settings, self.screen)
			ship.rect.x = 10 + ship_number * ship.rect.width
			ship.rect.y = 10
			self.ships.add(ship)
				
	def show_score(self):
		"""����Ļ����ʾ�÷�"""
		self.screen.blit(self.score_image, self.score_rect)
		self.screen.blit(self.high_score_image, self.high_score_rect)
		self.screen.blit(self.level_image, self.level_image_rect)
		#���Ʒɴ�
		self.ships.draw(self.screen)
