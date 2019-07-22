# coding=gbk

class Settings():
	def __init__(self):
		#屏幕设置
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (230,230,230)
		
		#飞船设置
		self.ship_limit = 3
		
		#子弹设置
		self.bullet_width = 8
		self.bullet_height = 15
		self.bullet_color = (60, 60, 60)
		self.bullet_allowed = 300
		
		#外星人设置
		self.fleet_drop_speed = 20
		#fleet_direction为1表示向右，-1表示向左
		self.fleet_direction = 1
		
		#以什么样的速度加快游戏节奏
		self.speed_scale = 1.1
		self.score_scale = 1.5
		
		self.initialize_dynamic_settings()
		
	def initialize_dynamic_settings(self):
		self.ship_speed_factor = 1
		self.bullet_speed_factor = 3
		self.alien_speed_factor = 2
		self.fleet_direction = 1
		self.alien_points = 50
		
	def increase_speed(self):
		self.ship_speed_factor *= self.speed_scale
		self.bullet_speed_factor *= self.speed_scale
		self.alien_speed_factor *= self.speed_scale
		self.alien_points *= self.score_scale
