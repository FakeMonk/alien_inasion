# coding=gbk

import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_events(ship, ai_settings, bullets, screen, stats, play_button, aliens, sb):
	"""响应按键和鼠标事件"""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(stats, play_button, mouse_x, mouse_y, ai_settings, screen, aliens, ship, bullets, sb)
		elif event.type == pygame.KEYDOWN:
			check_down_events(event, ship, bullets, screen, ai_settings)
		elif event.type == pygame.KEYUP:
			check_up_events(event, ship)

def check_play_button(stats, play_button, mouse_x, mouse_y, ai_settings, screen, aliens, ship, bullets,sb):
	"""在玩家单机play按钮时开始游戏"""
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		pygame.mouse.set_visible(False)
		#重置游戏统计信息
		stats.reset_stats()
		stats.game_active = True
		#重置游戏设置
		ai_settings.initialize_dynamic_settings()
		#重置级分图像
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		sb.prep_ship()
		
		#清空外星人列表和子弹
		aliens.empty()
		bullets.empty()
		
		#创建一群新的外星人，并让飞船剧中
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
def check_down_events(event, ship, bullets, screen, ai_settings):
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_q:
		sys.exit()
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		fire_bullet(bullets, ai_settings, ship, screen)
	elif event.key ==pygame.K_UP:
		ship.moving_up = True
	elif event.key ==pygame.K_DOWN:
		ship.moving_down = True

def check_up_events(event, ship):
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key ==pygame.K_LEFT:
		ship.moving_left = False
	elif event.key ==pygame.K_UP:
		ship.moving_up = False
	elif event.key ==pygame.K_DOWN:
		ship.moving_down = False
		
def fire_bullet(bullets, ai_settings, ship, screen):
	if len(bullets) < ai_settings.bullet_allowed:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)
			
def update_screen(ai_settings, ship, screen, bullets, aliens, play_botton, stats, sb):
	"""更新屏幕上的图像，平切换到新屏幕"""
	#每次循环时都重绘屏幕
	screen.fill(ai_settings.bg_color)
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	ship.blitme()
	aliens.draw(screen)
	sb.show_score()
	if not stats.game_active:
		play_botton.draw_button()
	
	#让最近绘制的屏幕可见
	pygame.display.flip()
	
def update_bullets(bullets, aliens, ai_settings, screen, ship, sb, stats):
	"""更新屏幕上的子弹"""
	bullets.update()
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	check_bullet_alien_collisions(bullets, aliens, ai_settings, screen, ship, sb, stats)
		
def check_bullet_alien_collisions(bullets, aliens, ai_settings, screen, ship, sb, stats):
	#检查子弹是否集中外星人，
	#如果集中，就将相应的外星人和子弹删除
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	
	if collisions:
		for aliens1 in collisions.values():
			stats.score += ai_settings.alien_points *len(aliens1)
			sb.prep_score()
		check_high_score(stats, sb)
	if len(aliens) == 0:
		#删除现有子弹，并新建一群外星人
		bullets.empty()
		ai_settings.increase_speed()
		#提高等级
		stats.level += 1
		sb.prep_level()
		create_fleet(ai_settings, screen, ship, aliens)
			
def get_number_aliens_x(ai_settings, alien_width):
	"""计算每行可容纳多少个外星人"""
	avaliable_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(avaliable_space_x / (2 * alien_width))
	return number_aliens_x
	
def get_number_rows(ai_settings, ship_height, alien_height):
	"""计算屏幕能容纳多少行外星人"""
	avaliable_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
	number_rows = int(avaliable_space_y / (2 * alien_height))
	return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	"""创建一个外星人并放入当前行"""
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height *row_number
	aliens.add(alien)
def create_fleet(ai_settings, screen, ship, aliens):
	"""创建外星人群"""
	#创建一个外星人并计算一行能容纳多少外星人和整个屏幕能容纳多少行外星人
	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
	#创建第一行外星人
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings, screen, aliens, alien_number, row_number)
			
def check_fleet_edges(ai_settings, aliens):
	"""有外星人到达边缘时采取措施"""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break

def change_fleet_direction(ai_settings, aliens):
	"""将正群外星人下移，并改变他们的方向"""
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1
	
def ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb):
	"""响应被外星人撞到的飞船"""
	if stats.ships_left > 0:
		
		#将ships_left减1
		stats.ships_left -= 1
		sb.prep_ship()
	
		#清空外星人列表和子弹列表
		aliens.empty()
		bullets.empty()
	
		#创建一群新的外星人，并让飞船居中
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
	
		#暂停
		sleep(0.5)
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)
	
def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets ,sb):
	"""检查外星人是否触碰底线"""
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)
			break
	
def update_aliens(ai_settings, aliens, stats, screen, ship, bullets, sb):
	"""检查是否有外星人位于屏幕边缘，并更新正群外星人的位置"""
	check_fleet_edges(ai_settings, aliens)
	aliens.update()
	
	#检测外星人和飞船碰撞
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)
	#检查是否到达底部
	check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb)
	
def check_high_score(stats, sb):
	"""检查是否诞生新分数"""
	if stats.high_score < stats.score:
		stats.high_score = stats.score
		sb.prep_high_score()
