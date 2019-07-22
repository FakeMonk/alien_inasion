# coding=gbk

class Settings():
	def __init__(self):
		#��Ļ����
		self.screen_width = 1200
		self.screen_height = 800
		self.bg_color = (230,230,230)
		
		#�ɴ�����
		self.ship_limit = 3
		
		#�ӵ�����
		self.bullet_width = 8
		self.bullet_height = 15
		self.bullet_color = (60, 60, 60)
		self.bullet_allowed = 300
		
		#����������
		self.fleet_drop_speed = 20
		#fleet_directionΪ1��ʾ���ң�-1��ʾ����
		self.fleet_direction = 1
		
		#��ʲô�����ٶȼӿ���Ϸ����
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
