from databasegp import InventoryDB
import pygame
import ctypes
import random
import sqlite3

db = InventoryDB()
conn = sqlite3.connect("inventory.db")
cursor = conn.cursor()

app_id = 'Pythongame.app'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id) # Fixes an issue with the taskbar icon not displaying correctly.

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((900, 600))
pygame.display.set_icon(pygame.image.load("images/icon.png"))
pygame.display.set_caption("Python Game")
screen.fill((0, 0, 0))

# Different font sizes
font = pygame.font.Font("fonts/papyrus.ttf", 30)
smallfont = pygame.font.Font("fonts/papyrus.ttf", 20)
bigfont = pygame.font.Font("fonts/papyrus.ttf", 50)

# Unchangeable text
text_surface_0 = font.render("You have 3 heros to choose from: Number 1, 2 and 3.", False, "White")
text_surface_1 = font.render("To continue, press any key.", False, "White")
text_choice = font.render("Press 1, 2, or 3 to change character only once", False, "White")
text_hero_choice = font.render("Press A to attack or press H to heal", False, "White")

# Changeable text
text_monster_action = font.render("", False, "White")
text_heal_action = font.render("", False, "White")

bg = pygame.image.load("images/bg.jpg")
bg = pygame.transform.scale(bg, (900, 600))

redslime = pygame.image.load("spritesheet/redslime.png").convert_alpha()
greenslime = pygame.image.load("spritesheet/greenslime.png").convert_alpha()
idle_1 = [
	pygame.image.load("spritesheet/Woodcutter_idle1.png"),
	pygame.image.load("spritesheet/Woodcutter_idle2.png"),
	pygame.image.load("spritesheet/Woodcutter_idle3.png"),
	pygame.image.load("spritesheet/Woodcutter_idle4.png"),
]
idle_2 = [
	pygame.image.load("spritesheet/SteamMan_idle1.png"),
	pygame.image.load("spritesheet/SteamMan_idle2.png"),
	pygame.image.load("spritesheet/SteamMan_idle3.png"),
	pygame.image.load("spritesheet/SteamMan_idle4.png"),
]
idle_3 = [
	pygame.image.load("spritesheet/GraveRobber_idle1.png"),
	pygame.image.load("spritesheet/GraveRobber_idle2.png"),
	pygame.image.load("spritesheet/GraveRobber_idle3.png"),
	pygame.image.load("spritesheet/GraveRobber_idle4.png"),
]

anim_count = 0

# monster
monster_variation = random.randint(1,2)
hp_m = random.randint(10,20)
attack_m = 3
regeneration_m = 2
m_count = 0

# Heros
hp_hero = 0
attack = 0
idle = idle_1


hp_h_1 =  10
hp_h_2 =  12
hp_h_3 =  7
attack_h_1 = 5
attack_h_2 = 4
attack_h_3 = 6
heal_potion = 2
hero_count = 0

# Wins
score = 0

running = True
while running:
	items = db.get_all_items()
	screen.blit(bg, (0, 0))
	screen.blit(text_surface_0, (150, 100))
	screen.blit(text_surface_1, (150, 200))
	screen.blit(font.render("1", False, "White"), (360, 500))
	screen.blit(font.render("2", False, "White"), (435, 500))
	screen.blit(font.render("3", False, "White"), (510, 500))
	screen.blit(font.render(f"Wins: {score}", False, "White"), (750, 550))
	cursor.execute("SELECT 1 FROM inventory LIMIT 1")
	if score > 0 or cursor.fetchone():
		for index, item in enumerate(items):
			text_str = f"Inventory: {item[1]}({item[2]})"
			text_inventory = font.render(text_str, False, (255, 255, 255))
			screen.blit(text_inventory, (50, 550 + index * 30))

	screen.blit(font.render(f"Healing potins: {heal_potion}", False, "White"), (50, 500))
	screen.blit(idle_1[anim_count], (350, 400))
	screen.blit(idle_2[anim_count], (425, 400))
	screen.blit(idle_3[anim_count], (500, 400))

	# Animation
	if anim_count == 3:
		anim_count = 0
	else:
		anim_count += 1

	pygame.display.update()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
			pygame.quit()
		elif event.type == pygame.KEYDOWN:
			while running:
				text_heal_amount = font.render(f"Healing potions remaining: {heal_potion}", False, "White")
				hp_mtext = font.render(f"Health: {hp_m}", True, (255, 255, 255))
				hp_htext = font.render(f"Health: {hp_hero}", True, (255, 255, 255))
				attack_mtext = font.render(f"Attack: {attack_m}", True, (255, 255, 255))
				attack_htext = font.render(f"Attack: {attack}", True, (255, 255, 255))
				screen.blit(bg, (0, 0))
				if hero_count == 0:
					screen.blit(font.render("1", False, "White"), (60, 500))
					screen.blit(font.render("2", False, "White"), (185, 500))
					screen.blit(font.render("3", False, "White"), (310, 500))
					screen.blit(idle_1[anim_count], (50, 400))
					screen.blit(idle_2[anim_count], (175, 400))
					screen.blit(idle_3[anim_count], (300, 400))
					screen.blit(smallfont.render(f"Health: {hp_h_1}", True, (255, 255, 255)), (50, 350))
					screen.blit(smallfont.render(f"Health: {hp_h_2}", True, (255, 255, 255)), (175, 350))
					screen.blit(smallfont.render(f"Health: {hp_h_3}", True, (255, 255, 255)), (280, 350))
					screen.blit(smallfont.render(f"Attack: {attack_h_1}", True, (255, 255, 255)), (50, 370))
					screen.blit(smallfont.render(f"Attack: {attack_h_2}", True, (255, 255, 255)), (175, 370))
					screen.blit(smallfont.render(f"Attack: {attack_h_3}", True, (255, 255, 255)), (280, 370))
					screen.blit(text_choice, (100, 150))
				else:
					screen.blit(idle[anim_count], (350, 400))
					screen.blit(hp_htext, (300, 340))
					screen.blit(attack_htext, (300, 370))
					screen.blit(text_heal_amount, (100, 200))
					screen.blit(text_hero_choice, (100, 150))
					screen.blit(text_heal_action, (150, 550))
					screen.blit(text_monster_action, (500, 550))
				screen.blit(hp_mtext, (500, 370))
				screen.blit(attack_mtext, (500, 400))
				if anim_count == 3:
					anim_count = 0
				else:
					anim_count += 1

				if monster_variation == 1:
					screen.blit(redslime, (500, 370))
				else:
					screen.blit(greenslime, (500, 370))

				if hp_m <= 0:
					db.add_item("Slime", 1)
					hp_m = random.randint(10, 20)
					monster_variation = random.randint(1,2)
					hero_count = 0
					m_count = 0
					heal_potion = 2
					score += 1
					break

				pygame.display.update()
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						running = False
						pygame.quit()
					elif event.type == pygame.KEYDOWN:
						if hero_count == 1:
							if event.key == pygame.K_a:
								hp_m = hp_m - attack
								if  m_count == 1 or m_count == 3 or m_count == 5:
									hp_hero = hp_hero - attack_m
									text_monster_action = font.render("He dealt 3 damage to you!", False, "White")
								else:
									hp_m = hp_m + regeneration_m
									text_monster_action = font.render("He regenerated 2 HP!", False, "White")
								m_count += 1
							elif event.key == pygame.K_h and heal_potion > 0:
								hp_hero = hp_hero + 5
								text_heal_action = font.render("You healed 5 HP!", False, "White")
								if  m_count == 1 or m_count == 3 or m_count == 5:
									hp_hero = hp_hero - attack_m
									text_monster_action = font.render("He dealt 3 damage to you!", False, "White")
								else:
									hp_m = hp_m + regeneration_m
									text_monster_action = font.render("He regenerated 2 HP!", False, "White")
								m_count += 1
								heal_potion = heal_potion - 1
						elif hero_count == 0:
							if event.key == pygame.K_1:
								idle = idle_1
								attack = attack_h_1
								hp_hero = hp_h_1
								hero_count += 1
							elif event.key == pygame.K_2:
								idle = idle_2
								attack = attack_h_2
								hp_hero = hp_h_2
								hero_count += 1
							elif event.key == pygame.K_3:
								idle = idle_3
								attack = attack_h_3
								hp_hero = hp_h_3
								hero_count += 1
				clock.tick(5)
			
	clock.tick(5)