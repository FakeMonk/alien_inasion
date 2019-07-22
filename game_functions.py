# coding=gbk

import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_events(ship, ai_settings, bullets, screen, stats, play_button, aliens, sb):
	"""��Ӧ����������¼�"""
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
	"""����ҵ���play��ťʱ��ʼ��Ϸ"""
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		pygame.mouse.set_visible(False)
		#������Ϸͳ����Ϣ
		stats.reset_stats()
		stats.game_active = True
		#������Ϸ����
		ai_settings.initialize_dynamic_settings()
		#���ü���ͼ��
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		sb.prep_ship()
		
		#����������б���ӵ�
		aliens.empty()
		bullets.empty()
		
		#����һȺ�µ������ˣ����÷ɴ�����
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
	"""������Ļ�ϵ�ͼ��ƽ�л�������Ļ"""
	#ÿ��ѭ��ʱ���ػ���Ļ
	screen.fill(ai_settings.bg_color)
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	ship.blitme()
	aliens.draw(screen)
	sb.show_score()
	if not stats.game_active:
		play_botton.draw_button()
	
	#��������Ƶ���Ļ�ɼ�
	pygame.display.flip()
	
def update_bullets(bullets, aliens, ai_settings, screen, ship, sb, stats):
	"""������Ļ�ϵ��ӵ�"""
	bullets.update()
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	check_bullet_alien_collisions(bullets, aliens, ai_settings, screen, ship, sb, stats)
		
def check_bullet_alien_collisions(bullets, aliens, ai_settings, screen, ship, sb, stats):
	#����ӵ��Ƿ��������ˣ�
	#������У��ͽ���Ӧ�������˺��ӵ�ɾ��
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
	
	if collisions:
		for aliens1 in collisions.values():
			stats.score += ai_settings.alien_points *len(aliens1)
			sb.prep_score()
		check_high_score(stats, sb)
	if len(aliens) == 0:
		#ɾ�������ӵ������½�һȺ������
		bullets.empty()
		ai_settings.increase_speed()
		#��ߵȼ�
		stats.level += 1
		sb.prep_level()
		create_fleet(ai_settings, screen, ship, aliens)
			
def get_number_aliens_x(ai_settings, alien_width):
	"""����ÿ�п����ɶ��ٸ�������"""
	avaliable_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(avaliable_space_x / (2 * alien_width))
	return number_aliens_x
	
def get_number_rows(ai_settings, ship_height, alien_height):
	"""������Ļ�����ɶ�����������"""
	avaliable_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
	number_rows = int(avaliable_space_y / (2 * alien_height))
	return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
	"""����һ�������˲����뵱ǰ��"""
	alien = Alien(ai_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height *row_number
	aliens.add(alien)
def create_fleet(ai_settings, screen, ship, aliens):
	"""����������Ⱥ"""
	#����һ�������˲�����һ�������ɶ��������˺�������Ļ�����ɶ�����������
	alien = Alien(ai_settings, screen)
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
	#������һ��������
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(ai_settings, screen, aliens, alien_number, row_number)
			
def check_fleet_edges(ai_settings, aliens):
	"""�������˵����Եʱ��ȡ��ʩ"""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break

def change_fleet_direction(ai_settings, aliens):
	"""����Ⱥ���������ƣ����ı����ǵķ���"""
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1
	
def ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb):
	"""��Ӧ��������ײ���ķɴ�"""
	if stats.ships_left > 0:
		
		#��ships_left��1
		stats.ships_left -= 1
		sb.prep_ship()
	
		#����������б���ӵ��б�
		aliens.empty()
		bullets.empty()
	
		#����һȺ�µ������ˣ����÷ɴ�����
		create_fleet(ai_settings, screen, ship, aliens)
		ship.center_ship()
	
		#��ͣ
		sleep(0.5)
	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)
	
def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets ,sb):
	"""����������Ƿ�������"""
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)
			break
	
def update_aliens(ai_settings, aliens, stats, screen, ship, bullets, sb):
	"""����Ƿ���������λ����Ļ��Ե����������Ⱥ�����˵�λ��"""
	check_fleet_edges(ai_settings, aliens)
	aliens.update()
	
	#��������˺ͷɴ���ײ
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, stats, screen, ship, aliens, bullets, sb)
	#����Ƿ񵽴�ײ�
	check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets, sb)
	
def check_high_score(stats, sb):
	"""����Ƿ����·���"""
	if stats.high_score < stats.score:
		stats.high_score = stats.score
		sb.prep_high_score()
