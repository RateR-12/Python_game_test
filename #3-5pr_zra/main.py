import arcade
import os
import random
import time
from PIL import Image
from arcade.experimental.lights import Light, LightLayer


def splits_gif_into_frames(path_to_file, saving_path):
	with Image.open(path_to_file) as image:
		if os.path.isdir(saving_path) == False:
			os.makedirs(saving_path)
		for i in range(image.n_frames):
			image.seek(i)
			image.save(f'{saving_path}''/{}.png'.format(i))


idle_path = 'Jungle Asset Pack/Character/sprites/idle.gif'
idle_saving_path = 'sprites/idle'
run_path = 'Jungle Asset Pack/Character/sprites/run.gif'
run_saving_path = 'sprites/run'

splits_gif_into_frames(idle_path, idle_saving_path)
splits_gif_into_frames(run_path, run_saving_path)

SCREEN_TITLE = 'ИНДИАНА ДЖОНС: Сокровища орангутанга.'
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500

GRAVITY = 2
PLAYER_MOVEMENT_SPEED = 7
PLAYER_JUMP_SPEED = 23
CHEST_OPEN_DELAY = 1.5

RIGHT_FACING = 0
LEFT_FACING = 1

DEFAULT_LINE_HEIGHT = 45
DEFAULT_FONT_SIZE = 16

MUSIC_VOLUME = 0.1
SOUND_VOLUME = 0.3


class Player(arcade.Sprite):
	def __init__(self):
		super().__init__()
		self.center_x = 50
		self.center_y = 100
		self.person_face_direction = RIGHT_FACING
		self.cur_texture = 0
		self.scale = 3
		self.idle = True
		self.hit_box_algorithm = "Detailed"
		self.hit_points = 3

		self.idle_textures = []
		for i in range(0, 12):
			texture = arcade.load_texture_pair(f'sprites/idle/{i}.png')
			self.idle_textures.append(texture)

		self.run_textures = []
		for i in range(0, 8):
			texture = arcade.load_texture_pair(f'sprites/run/{i}.png')
			self.run_textures.append(texture)
		self.texture = self.idle_textures[0][0]

	def update_animation(self, delta_time: float = 1 / 30):
		if self.change_x < 0 and self.person_face_direction == RIGHT_FACING:
			self.person_face_direction = LEFT_FACING
		elif self.change_x > 0 and self.person_face_direction == LEFT_FACING:
			self.person_face_direction = RIGHT_FACING

		if self.change_x == 0:
			self.cur_texture += 0.15
			if self.cur_texture % 2 == 0:
				self.texture = self.idle_textures[0][self.person_face_direction]
			if self.cur_texture >= 5:
				self.cur_texture = 0
			self.texture = self.idle_textures[int(self.cur_texture)][
				self.person_face_direction
		]
		if not self.idle:
			self.cur_texture = (self.cur_texture + 0.25) % len(self.run_textures)  # изменено здесь
			self.texture = self.run_textures[int(self.cur_texture)][
				self.person_face_direction
			]


class Agatic(arcade.Sprite):
	def __init__(self, x, y, left_border, right_border):
		super().__init__()
		self.center_x = x
		self.center_y = y
		self.change_x = 2
		self.person_face_direction = RIGHT_FACING
		self.cur_texture = 0
		self.scale = 2
		self.set_hit_box([[-10, -10], [10, -10], [10, 10], [-10, 10]])

		self.left_border = left_border
		self.right_border = right_border
		self.idle_textures = []

		texture = arcade.load_texture_pair(f'sprites/agaric/agaric_idle.png')
		self.idle_textures.append(texture)
		texture = arcade.load_texture_pair(f'sprites/agaric/agaric_idle_down.png')
		self.idle_textures.append(texture)


	def update_animation(self, delta_time: float = 1 / 30):
		self.cur_texture += 0.03
		if self.cur_texture % 2 == 0:
			self.texture = self.idle_textures[0][self.person_face_direction]
		if self.cur_texture >= 2:
			self.cur_texture = 0
		self.texture = self.idle_textures[int(self.cur_texture)][
			self.person_face_direction
		]



class GreenAgatic(arcade.Sprite):
	def __init__(self, x, y, left_border, right_border):
		super().__init__()
		self.center_x = x
		self.center_y = y
		self.change_x = 2
		self.person_face_direction = RIGHT_FACING
		self.cur_texture = 0
		self.scale = 2
		self.set_hit_box([[-10, -10], [10, -10], [10, 10], [-10, 10]])

		self.left_border = left_border
		self.right_border = right_border
		self.idle_textures = []

		texture = arcade.load_texture_pair(f'sprites/agaric/green_agaric_idle.png')
		self.idle_textures.append(texture)
		texture = arcade.load_texture_pair(f'sprites/agaric/green_agaric_idle_down.png')
		self.idle_textures.append(texture)


	def update_animation(self, delta_time: float = 1 / 30):
		self.cur_texture += 0.03
		if self.cur_texture % 2 == 0:
			self.texture = self.idle_textures[0][self.person_face_direction]
		if self.cur_texture >= 2:
			self.cur_texture = 0
		self.texture = self.idle_textures[int(self.cur_texture)][
			self.person_face_direction
		]


class Chest(arcade.Sprite):
	def __init__(self):
		super().__init__()
		self.closed_texture = arcade.load_texture("sprites/chest/close_chest.png")
		self.open_texture = arcade.load_texture("sprites/chest/open_chest.png")
		self.texture = self.closed_texture
		self.center_x = 2300
		self.center_y = 130
		self.scale = 0.5
		self.is_open = False
		self.open_time = None

	def open(self):
		self.texture = self.open_texture
		self.is_open = True


class Firefly:
	def __init__(self, center_x, center_y, radius, color):
		self.center_x = center_x
		self.center_y = center_y
		self.radius = radius
		self.color = color
		self.change_x = random.uniform(-1, 1)
		self.change_y = random.uniform(-1, 1)


class Game(arcade.Window):
	def __init__(self):
		super().__init__(
			width=SCREEN_WIDTH,
			height=SCREEN_HEIGHT,
			title=SCREEN_TITLE,
			update_rate=1 / 60
			)
		self.bg_layer_1 = arcade.load_texture('Jungle Asset Pack/parallax background/plx-1.png')
		self.bg_layer_2 = arcade.load_texture('Jungle Asset Pack/parallax background/plx-2.png')
		self.bg_layer_3 = arcade.load_texture('Jungle Asset Pack/parallax background/plx-3.png')
		self.bg_layer_4 = arcade.load_texture('Jungle Asset Pack/parallax background/plx-4.png')
		self.bg_layer_5 = arcade.load_texture('Jungle Asset Pack/parallax background/plx-5.png')

		self.zero_hit_points = arcade.load_texture('sprites/hit_points/0_hit_points.png')
		self.one_hit_points = arcade.load_texture('sprites/hit_points/1_hit_points.png')
		self.two_hit_points = arcade.load_texture('sprites/hit_points/2_hit_points.png')
		self.tree_hit_points = arcade.load_texture('sprites/hit_points/3_hit_points.png')

		self.player = None
		self.agatic = None
		self.agatic_2 = None
		self.chest = None
		self.physics_engine = None
		self.agatic_physics_engine = None
		self.agatic_physics_engine_2 = None
		self.camera = None

		self.light_layer = LightLayer(SCREEN_WIDTH, SCREEN_HEIGHT)
		self.player_light = Light(0, 0, 200, arcade.color.WHITE, "soft")

		self.soundtrack = arcade.load_sound('sounds/Valve_-_Jungle_Drums__Zvyki.com_.wav')
		self.soundtrack_play = arcade.play_sound(self.soundtrack, volume=MUSIC_VOLUME, looping=True)
		self.nature_sound = arcade.load_sound('sounds/Y2mate.mx-Sounds-of-the-Jungle-_320-kbps_.wav')
		self.nature_sound_play = arcade.play_sound(self.nature_sound, volume=MUSIC_VOLUME, looping=True)
		
		self.cj_replica_sound = arcade.load_sound('sounds/CJ_-_oh_shit_here_we_go_again_66148716.wav')
		self.run_sound = arcade.load_sound('sounds/run_sound.wav')
		self.walk_sound = arcade.load_sound('sounds/walk_sound.wav')

		self.rip_fall = arcade.load_sound('sounds/rip-fall.wav')
		self.death_mario = arcade.load_sound('sounds/death_mario.wav')
		self.death_sounds = [self.rip_fall, self.death_mario]

		self.open_chest = arcade.load_sound('sounds/open_chest.wav')
		self.use_key = arcade.load_sound('sounds/use_key.wav')
		self.yeahboy_sound = arcade.load_sound('sounds/yeahboy.wav')
		self.o_my_god_sound = arcade.load_sound('sounds/o_my_god.wav')
		self.dange_sound = [self.yeahboy_sound, self.o_my_god_sound]

		self.last_pressed_key = None
		self.fall_sound_played = False
		self.was_on_ground = False
		self.game_over = False
		self.win = False

		self.time_of_complete_game = 0
		self.end_time = 0
		self.start_time = 0
		

	def setup(self):
		self.camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
		self.agatic_list = arcade.SpriteList()
		self.chest_list = arcade.SpriteList()
		self.dirt_list = arcade.SpriteList()
		self.phys_dirt_list = arcade.SpriteList()
		self.light_bush_list = arcade.SpriteList()
		self.flying_cubic_bush_list = arcade.SpriteList()
		self.phys_light_bush_list = arcade.SpriteList()

		self.firefly_list = []
		for _ in range(40):
			center_x = random.uniform(0, 2000)
			center_y = random.uniform(0, SCREEN_HEIGHT)
			radius = random.uniform(1, 5)
			color = arcade.color.YELLOW
			firefly = Firefly(center_x, center_y, radius, color)
			self.firefly_list.append(firefly)
			light = Light(center_x, center_y, radius * 2.5, color, "soft")
			self.light_layer.add(light)
			firefly.light = light

		for j in range(0, 400, 490):
			dirt = arcade.Sprite('sprites/jungle tileset/dirt.png', 3.1)
			dirt.center_x = j
			dirt.center_y = 5
			self.dirt_list.append(dirt)

			phys_dirt = arcade.Sprite('sprites/jungle tileset/phys_dirt.png', 3.1)
			phys_dirt.center_x = dirt.center_x
			phys_dirt.center_y = dirt.center_y - 10
			self.phys_dirt_list.append(phys_dirt)

		for j in range(1950, 2400, 400):
			dirt = arcade.Sprite('sprites/jungle tileset/dirt.png', 3.1)
			dirt.center_x = j
			dirt.center_y = 60
			self.dirt_list.append(dirt)

			phys_dirt = arcade.Sprite('sprites/jungle tileset/phys_dirt.png', 3.1)
			phys_dirt.center_x = dirt.center_x
			phys_dirt.center_y = dirt.center_y - 10
			self.phys_dirt_list.append(phys_dirt)

		for j in range(400, 800, 200):
			light_bush = arcade.Sprite('sprites/jungle tileset/light_bush.png', 2.5)
			light_bush.center_x = j #+ random.randint(200, 400)
			light_bush.center_y = 60 + random.randint(0, 50)
			self.light_bush_list.append(light_bush)

			phys_light_bush = arcade.Sprite('sprites/jungle tileset/phys_light_bush.png', 2.5)
			phys_light_bush.center_x = light_bush.center_x
			phys_light_bush.center_y = light_bush.center_y
			self.phys_light_bush_list.append(phys_light_bush)

		for j in range(100, 280, 30):
			light_bush = arcade.Sprite('sprites/jungle tileset/light_bush.png', 2.5)
			light_bush.center_x = 1260 + random.randint(0, 15)
			light_bush.center_y = j
			self.light_bush_list.append(light_bush)

			phys_light_bush = arcade.Sprite('sprites/jungle tileset/phys_light_bush.png', 2.5)
			phys_light_bush.center_x = light_bush.center_x
			phys_light_bush.center_y = light_bush.center_y
			self.phys_light_bush_list.append(phys_light_bush)
		
		def draw_dirt(x, y, scale):
			dirt = arcade.Sprite('sprites/jungle tileset/dirt.png', scale)
			dirt.center_x = x
			dirt.center_y = y
			self.dirt_list.append(dirt)

			phys_dirt = arcade.Sprite('sprites/jungle tileset/phys_dirt.png', scale)
			phys_dirt.center_x = dirt.center_x
			phys_dirt.center_y = dirt.center_y - 10
			self.phys_dirt_list.append(phys_dirt)

		draw_dirt(1050, 60, 3.1)

		def draw_light_bush(x, y, scale):
			light_bush = arcade.Sprite('sprites/jungle tileset/light_bush.png', 2.5)
			light_bush.center_x = x
			light_bush.center_y = y
			self.light_bush_list.append(light_bush)

			phys_light_bush = arcade.Sprite('sprites/jungle tileset/phys_light_bush.png', 2.5)
			phys_light_bush.center_x = light_bush.center_x
			phys_light_bush.center_y = light_bush.center_y
			self.phys_light_bush_list.append(phys_light_bush)

		draw_light_bush(1160, 100, 2.5)
		draw_light_bush(1500, 100, 2.5)

		def draw_flying_cubic_bush(x, y, scale):
			flying_cubic_bush = arcade.Sprite('sprites/jungle tileset/flying_cubic_bush.png', scale)
			flying_cubic_bush.center_x = x
			flying_cubic_bush.center_y = y
			self.flying_cubic_bush_list.append(flying_cubic_bush)

		draw_flying_cubic_bush(1030, 150, 1.7)
		draw_flying_cubic_bush(1050, 175, 1.7)
		draw_flying_cubic_bush(1270, 290, 1.7)
		draw_flying_cubic_bush(1280, 350, 1.7)

		self.player = Player()
		self.agatic = GreenAgatic(850, 200, 800, 955)
		self.chest = Chest()

		self.chest_list.append(self.chest)

		self.light_layer.add(self.player_light)

		self.agatic_physics_engine = arcade.PhysicsEnginePlatformer(
			self.agatic, 
			gravity_constant=GRAVITY, 
			walls=[self.phys_dirt_list, self.phys_light_bush_list, self.flying_cubic_bush_list,  self.chest_list]
		)

		self.agatic_list.append(self.agatic)

		self.agatic_2 = Agatic(1990, 200, 1750, 2200)
		self.agatic_physics_engine_2 = arcade.PhysicsEnginePlatformer(
			self.agatic_2, 
			gravity_constant=GRAVITY, 
			walls=[self.phys_dirt_list, self.phys_light_bush_list, self.flying_cubic_bush_list,  self.chest_list]
		)

		self.agatic_list.append(self.agatic_2)

		self.physics_engine = arcade.PhysicsEnginePlatformer(
			self.player, 
			gravity_constant=GRAVITY, 
			walls=[self.phys_dirt_list, self.phys_light_bush_list, self.flying_cubic_bush_list,  self.chest_list, self.agatic_list]
		)

		self.start_time = time.time()

	def on_draw(self):
		self.clear()

		with self.light_layer:
			for i in range(0, 1601, 800):
				arcade.draw_lrwh_rectangle_textured(i, 0, 800, SCREEN_HEIGHT, self.bg_layer_1)
				arcade.draw_lrwh_rectangle_textured(i, 0, 800, SCREEN_HEIGHT, self.bg_layer_2)
				arcade.draw_lrwh_rectangle_textured(i, 0, 800, SCREEN_HEIGHT, self.bg_layer_3)
				arcade.draw_lrwh_rectangle_textured(i, 0, 800, SCREEN_HEIGHT, self.bg_layer_4)
				arcade.draw_lrwh_rectangle_textured(i, 0, 800, SCREEN_HEIGHT, self.bg_layer_5)

			self.player.draw()
			self.agatic.draw()
			self.agatic_2.draw()
			self.chest.draw()
			self.light_bush_list.draw()
			self.phys_light_bush_list.draw()
			self.flying_cubic_bush_list.draw()
			self.dirt_list.draw()
		
		self.light_layer.draw(ambient_color=(20, 20, 20))

		if self.player.hit_points == 0:
			arcade.draw_lrwh_rectangle_textured(self.camera.position.x + 10, self.camera.position.y + 440, 50, 50, self.zero_hit_points)
		if self.player.hit_points == 1:
			arcade.draw_lrwh_rectangle_textured(self.camera.position.x + 10, self.camera.position.y + 440, 50, 50, self.one_hit_points)
		if self.player.hit_points == 2:
			arcade.draw_lrwh_rectangle_textured(self.camera.position.x + 10, self.camera.position.y + 440, 50, 50, self.two_hit_points)
		if self.player.hit_points == 3:
			arcade.draw_lrwh_rectangle_textured(self.camera.position.x + 10, self.camera.position.y + 440, 50, 50, self.tree_hit_points)

		for firefly in self.firefly_list:
			arcade.draw_circle_filled(firefly.center_x, firefly.center_y, firefly.radius, firefly.color)

		if (self.player.bottom < 0 and self.player.hit_points > 0) or arcade.check_for_collision(self.player, self.agatic_2):
			camera_center_x = self.camera.position.x + self.camera.viewport_width / 2
			camera_center_y = self.camera.position.y + self.camera.viewport_height / 2

			arcade.draw_rectangle_filled(camera_center_x, camera_center_y, SCREEN_WIDTH, SCREEN_HEIGHT, (0, 0, 0, 200))

			arcade.draw_rectangle_filled(camera_center_x, camera_center_y + 20, 700, 100, arcade.color.RED)
			arcade.draw_text("ПОТРАЧЕНО", camera_center_x, camera_center_y, arcade.color.WHITE, 40, anchor_x="center")
			arcade.draw_text("Нажми 'ESCAPE' чтобы начать заново.", camera_center_x, camera_center_y - 70, arcade.color.APPLE_GREEN, DEFAULT_FONT_SIZE, anchor_x="center")
			arcade.draw_text("Нажми 'Я' ('Z') чтобы выйти.", camera_center_x, camera_center_y - 100, arcade.color.REDWOOD, DEFAULT_FONT_SIZE, anchor_x="center")
			self.game_over = True

		elif self.player.bottom < 0 and self.player.hit_points == 0:
			camera_center_x = self.camera.position.x + self.camera.viewport_width / 2
			camera_center_y = self.camera.position.y + self.camera.viewport_height / 2

			arcade.draw_rectangle_filled(camera_center_x, camera_center_y, SCREEN_WIDTH, SCREEN_HEIGHT, (0, 0, 0, 200))

			arcade.draw_rectangle_filled(camera_center_x, camera_center_y + 20, 700, 100, arcade.color.RED)
			arcade.draw_text("ПОМЕР", camera_center_x, camera_center_y, arcade.color.WHITE, 40, anchor_x="center")
			arcade.draw_text("Ты потратил все жизни, игра окончена.", camera_center_x, camera_center_y - 70, arcade.color.RED, DEFAULT_FONT_SIZE, anchor_x="center")
			arcade.draw_text("Нажми 'Я' ('Z') чтобы выйти.", camera_center_x, camera_center_y - 100, arcade.color.REDWOOD, DEFAULT_FONT_SIZE, anchor_x="center")
			self.game_over = True

		elif self.win:
			camera_center_x = self.camera.position.x + self.camera.viewport_width / 2
			camera_center_y = self.camera.position.y + self.camera.viewport_height / 2

			arcade.draw_rectangle_filled(camera_center_x, camera_center_y, SCREEN_WIDTH, SCREEN_HEIGHT, (0, 0, 0, 200))
			arcade.draw_rectangle_filled(camera_center_x, camera_center_y + 20, 700, 100, (0, 81, 0))
			
			arcade.draw_text(f"Время прохождения игры: {round(self.time_of_complete_game, 2)}", camera_center_x, camera_center_y - 200, arcade.color.WHITE, DEFAULT_FONT_SIZE, anchor_x="center")
			arcade.draw_text("Здесь... золото, сапфиры, изумруды и самое ценное - PyPI!", camera_center_x, camera_center_y + 10, arcade.color.WHITE, DEFAULT_FONT_SIZE, anchor_x="center")			
			arcade.draw_text("Ты нашёл сокровища! Игра пройдена!", camera_center_x, camera_center_y - 70, arcade.color.ELECTRIC_GREEN, DEFAULT_FONT_SIZE, anchor_x="center")
			arcade.draw_text("Нажми 'Я' ('Z') чтобы выйти.", camera_center_x, camera_center_y - 100, arcade.color.REDWOOD, DEFAULT_FONT_SIZE, anchor_x="center")

		self.camera.use()

	def on_key_press(self, key, modifiers):
		if self.game_over == False and self.win == False:
			if key == arcade.key.SPACE  or key == arcade.key.W:
				if self.physics_engine.can_jump():
					self.player.change_y = PLAYER_JUMP_SPEED
				if key == arcade.key.LEFT or key == arcade.key.A or key == arcade.key.RIGHT or key == arcade.key.D:
					if self.physics_engine.can_jump():
						self.run_sound_play = arcade.play_sound()

			elif key == arcade.key.LEFT or key == arcade.key.A:
				self.player.change_x = -PLAYER_MOVEMENT_SPEED
				self.player.idle = False
				self.last_pressed_key = key
				if self.physics_engine.can_jump() and self.player.change_x != 0:
					self.run_sound_play = arcade.play_sound(self.run_sound, volume=SOUND_VOLUME, looping=False)

			elif key == arcade.key.RIGHT or key == arcade.key.D:
				self.player.change_x = PLAYER_MOVEMENT_SPEED
				self.player.idle = False
				self.last_pressed_key = key
				if self.physics_engine.can_jump() and self.player.change_x != 0:
					self.run_sound_play = arcade.play_sound(self.run_sound, volume=SOUND_VOLUME, looping=False)

			elif key == arcade.key.E:
				distance = arcade.get_distance_between_sprites(self.player, self.chest)
				if distance < 70 and not self.chest.is_open:
					self.use_key_play  = arcade.play_sound(self.use_key, volume=SOUND_VOLUME + 0.2, looping=False)
					self.chest.open_time = time.time()

		if self.game_over and self.player.hit_points > 0 and key == arcade.key.ESCAPE:
			self.game_over = False
			self.player.center_x = 50
			self.player.center_y = 100
			self.player.change_x = 0
			self.player.change_y = 0
			self.player.idle = True
			self.player.hit_points -= 1

			arcade.stop_sound(self.rip_fall_play)
			arcade.stop_sound(self.soundtrack_play)
			arcade.stop_sound(self.nature_sound_play)
			self.soundtrack_play = arcade.play_sound(self.soundtrack, volume=MUSIC_VOLUME, looping=True)
			self.nature_sound_play = arcade.play_sound(self.nature_sound, volume=MUSIC_VOLUME, looping=True)
			self.cj_replica_sound_play = arcade.play_sound(self.cj_replica_sound, volume=MUSIC_VOLUME, looping=False)

			self.fall_sound_played = False
			self.last_pressed_key = None
			

		if (self.game_over or self.win) and key == arcade.key.Z:
			arcade.close_window()

	def on_key_release(self, key, modifiers):
		if key == arcade.key.SPACE or key == arcade.key.W:
			self.player.change_y = 0
		elif (key == arcade.key.LEFT or key == arcade.key.A) and self.last_pressed_key == key:
			self.player.change_x = 0
			self.player.idle = True
			arcade.stop_sound(self.run_sound_play)
		elif (key == arcade.key.RIGHT or key == arcade.key.D) and self.last_pressed_key == key:
			self.player.change_x = 0
			self.player.idle = True
			arcade.stop_sound(self.run_sound_play)

	def center_camera_to_player(self):
		screen_center_x = self.player.center_x - (self.camera.viewport_width / 2)
		screen_center_y = self.player.center_y - (self.camera.viewport_height / 2)

		if screen_center_x < 0:
			screen_center_x = 0
		if screen_center_y < 0 or screen_center_y > 0:
			screen_center_y = 0
		if screen_center_x > 1700:
			screen_center_x = 1700

		self.player_light.position = self.player.position

		player_centered  = screen_center_x, screen_center_y
		self.camera.move_to(player_centered)

		for firefly in self.firefly_list:
			firefly.light.position = firefly.center_x, firefly.center_y

	def on_update(self, delta_time):
		self.physics_engine.update()
		self.agatic_physics_engine.update()
		self.agatic_physics_engine_2.update()
		self.player.update_animation()
		self.agatic.update_animation()
		self.agatic.update()
		self.agatic_2.update_animation()
		self.agatic_2.update()
		self.center_camera_to_player()

		for firefly in self.firefly_list:
			firefly.center_x += firefly.change_x
			firefly.center_y += firefly.change_y
			if firefly.center_x < 0 or firefly.center_x > 2300:
				firefly.change_x *= -1
			if firefly.center_y < 0 or firefly.center_y > SCREEN_HEIGHT:
				firefly.change_y *= -1
			firefly.light.position = firefly.center_x, firefly.center_y

		for chest in self.chest_list:
			if chest.open_time is not None:
				elapsed_time = time.time() - chest.open_time
				if elapsed_time >= CHEST_OPEN_DELAY:
					self.chest.open()
					self.open_chest_play  = arcade.play_sound(self.open_chest, volume=SOUND_VOLUME + 0.2, looping=False)
					self.dange_sound_play  = arcade.play_sound(random.choice(self.dange_sound), volume=SOUND_VOLUME + 0.2, looping=False)
					self.win = True
					chest.open_time = None

					self.end_time = time.time()
					self.time_of_complete_game =  (self.end_time - self.start_time)

		if self.player.left < 0:
			self.player.left = 0
		if self.player.right > 2400:
			self.player.right = 2400

		if self.player.top < 0 and self.fall_sound_played == False:
			self.rip_fall_play = arcade.play_sound(random.choice(self.death_sounds), volume=SOUND_VOLUME, looping=False)
			self.fall_sound_played = True

		if self.agatic.center_x >= self.agatic.right_border:
			self.agatic.change_x = -1
		elif self.agatic.left == self.agatic.left_border:
			self.agatic.change_x = 1

		if self.agatic_2.center_x >= self.agatic_2.right_border:
			self.agatic_2.change_x = -1
		elif self.agatic_2.left == self.agatic_2.left_border:
			self.agatic_2.change_x = 1

		if arcade.check_for_collision(self.player, self.agatic_2):
			self.player.center_x = 50
			self.player.center_y = 100
			self.player.change_x = 0
			self.player.change_y = 0
			self.player.idle = True
			self.player.hit_points -= 1

			arcade.stop_sound(self.soundtrack_play)
			arcade.stop_sound(self.nature_sound_play)
			self.soundtrack_play = arcade.play_sound(self.soundtrack, volume=MUSIC_VOLUME, looping=True)
			self.nature_sound_play = arcade.play_sound(self.nature_sound, volume=MUSIC_VOLUME, looping=True)
			self.cj_replica_sound_play = arcade.play_sound(self.cj_replica_sound, volume=MUSIC_VOLUME, looping=False)

			self.fall_sound_played = False
			self.last_pressed_key = None

		if self.game_over == False and self.player.hit_points < 0:
			arcade.close_window()			


def main():
	game = Game()
	game.setup()
	arcade.run()

if __name__ == '__main__':
	main()