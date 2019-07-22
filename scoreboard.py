# coding=gbk

import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard():
	"""显示得分信息类"""
	
	def __init__(self, ai_settings, screen, stats):
		"""初始化显示得分涉及的属性"""
		self.screen = screen
		self.screen_rect = screen.get_rect()
		self.ai_settings = ai_settings
		self.stats = stats
		
		#显示得分信息时使用的字体设置
		self.text_color = (30, 30, 30)
		self.font = pygame.font.SysFont(None, 48)
		
		#准备初始得分图像
		self.prep_score()
		self.prep_high_score()
		self.prep_level()
		self.prep_ship()
		
	def prep_score(self):
		"""将得分渲染成图像"""
		rounded_score = int(round(self.stats.score, -1))
		score_str = "{:,}".format(rounded_score)
		self.score_image = self.font.render(score_str, True, self.text_color, self.ai_settings.bg_color)
		
		#将得分图像放在屏幕右上角
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20
		self.score_rect.top = 20
		
	def prep_high_score(self):
		"""将最高分渲染成图像"""
		rounded_high_score = int(round(self.stats.high_score, -1))
		high_score_str = "{:,}".format(rounded_high_score)
		self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.ai_settings.bg_color)
		
		#将最高分图片放在屏幕中间上部
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.top = 20
		self.high_score_rect.centerx = self.screen_rect.centerx
		
	def prep_level(self):
		"""将等级渲染成图像"""
		self.level_image = self.font.render(str(self.stats.level), True, self.text_color, self.ai_settings.bg_color)
		
		#将等级显示在得分下方
		self.level_image_rect = self.level_image.get_rect()
		self.level_image_rect.top = self.score_rect.bottom + 10
		self.level_image_rect.right = self.screen_rect.right - 20
		
	def prep_ship(self):
		"""显示还余下多少艘飞船"""
		self.ships = Group()
		for ship_number in range(self.stats.ships_left):
			ship =Ship(self.ai_settings, self.screen)
			ship.rect.x = 10 + ship_number * ship.rect.width
			ship.rect.y = 10
			self.ships.add(ship)
				
	def show_score(self):
		"""在屏幕上显示得分"""
		self.screen.blit(self.score_image, self.score_rect)
		self.screen.blit(self.high_score_image, self.high_score_rect)
		self.screen.blit(self.level_image, self.level_image_rect)
		#绘制飞船
		self.ships.draw(self.screen)
