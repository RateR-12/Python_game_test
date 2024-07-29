import arcade
import os
import random
import time
from PIL import Image

'''
Скачал пак ассетов, а там анимации в виде GIF
Пришлось добавить с помощью Pillow разобрать его на кадры.
Код не стал убирать, дабы получить отзыв и по нему.
'''


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

SCREEN_TITLE = ''
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 500

GRAVITY = 2
PLAYER_MOVEMENT_SPEED = 8
PLAYER_JUMP_SPEED = 20

RIGHT_FACING = 0
LEFT_FACING = 1

DEFAULT_LINE_HEIGHT = 45
DEFAULT_FONT_SIZE = 16

class Player(arcade.Sprite):
	def __init__(self):
		super().__init__()
		self.center_x = 50
		self.center_y = 100
		self.person_face_direction = RIGHT_FACING
		self.cur_texture = 0
		self.scale = 3
		self.idle = True

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
		
		self.player = None
		self.physics_engine = None
		self.camera = None

		self.soundtrack = arcade.load_sound('sounds/Valve_-_Jungle_Drums_(Zvyki.com).mp3')
		self.soundtrack_play = arcade.play_sound(self.soundtrack, volume=0.1, looping=True)
		self.nature_sound = arcade.load_sound('sounds/Y2mate.mx - Sounds of the Jungle (320 kbps).mp3')
		self.nature_sound_play = arcade.play_sound(self.nature_sound, volume=0.1, looping=True)
		
		self.run_sound = arcade.load_sound('sounds/run_sound.wav')
		self.walk_sound = arcade.load_sound('sounds/walk_sound.wav')
		self.rip_fall = arcade.load_sound('sounds/rip-fall.mp3')

		self.fall_sound_played = False
		self.game_over = False
		self.was_on_ground = False
		self.last_pressed_key = None

	def setup(self):
		self.camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
		self.ground_list = arcade.SpriteList()
		self.phys_ground_list = arcade.SpriteList()
		self.light_bush_list = arcade.SpriteList()
		self.flying_cubic_bush_list = arcade.SpriteList()

		for j in range(0, SCREEN_WIDTH + 1000, 490):
			ground = arcade.Sprite('sprites/jungle tileset/dirt.png', 3.1)
			ground.center_x = j
			ground.center_y = 5
			self.ground_list.append(ground)

		for j in range(0, SCREEN_WIDTH + 1000, 160):
			ground = arcade.Sprite('sprites/jungle tileset/phys_dirt.png', 2.5)
			ground.center_x = j
			ground.center_y = 5
			self.phys_ground_list.append(ground)

		for j in range(0, SCREEN_WIDTH + 2000, 450):
			ground = arcade.Sprite('sprites/jungle tileset/light_bush.png', 2.5)
			ground.center_x = j + random.randint(200, 400)
			ground.center_y = 60
			self.light_bush_list.append(ground)

		for j in range(0, 2600, 150):
			flying_cubic_bush = arcade.Sprite('sprites/jungle tileset/flying_cubic_bush.png', 1.5)
			flying_cubic_bush.center_x = j + 100
			flying_cubic_bush.center_y = 30 + (j/2)
			self.flying_cubic_bush_list.append(flying_cubic_bush)


		self.player = Player()

		self.ground_list.center_y = 2
		self.physics_engine = arcade.PhysicsEnginePlatformer(
			self.player, gravity_constant=GRAVITY, walls=[self.phys_ground_list, self.light_bush_list, self.flying_cubic_bush_list]
		)

	def on_draw(self):
		self.clear()

		for i in range(0, 1601, 800):
			arcade.draw_lrwh_rectangle_textured(i, 0, 800, SCREEN_HEIGHT, self.bg_layer_1)
			arcade.draw_lrwh_rectangle_textured(i, 0, 800, SCREEN_HEIGHT, self.bg_layer_2)
			arcade.draw_lrwh_rectangle_textured(i, 0, 800, SCREEN_HEIGHT, self.bg_layer_3)
			arcade.draw_lrwh_rectangle_textured(i, 0, 800, SCREEN_HEIGHT, self.bg_layer_4)
			arcade.draw_lrwh_rectangle_textured(i, 0, 800, SCREEN_HEIGHT, self.bg_layer_5)

		self.player.draw()
		self.light_bush_list.draw()
		self.ground_list.draw()
		self.flying_cubic_bush_list.draw()

		if self.player.bottom < 0:
			camera_center_x = self.camera.position.x + self.camera.viewport_width / 2
			camera_center_y = self.camera.position.y + self.camera.viewport_height / 2

			arcade.draw_rectangle_filled(camera_center_x, camera_center_y, SCREEN_WIDTH, SCREEN_HEIGHT, (0, 0, 0, 200))

			arcade.draw_rectangle_filled(camera_center_x, camera_center_y + 20, 700, 100, arcade.color.RED)
			arcade.draw_text("ПОТРАЧЕНО", camera_center_x, camera_center_y, arcade.color.WHITE, 40, anchor_x="center")
			arcade.draw_text("Нажми 'ПРОБЕЛ' чтобы начать заново.", camera_center_x, camera_center_y - 70, arcade.color.WHITE, DEFAULT_FONT_SIZE, anchor_x="center")
			arcade.draw_text("Нажми 'Я' чтобы выйти.", camera_center_x, camera_center_y - 100, arcade.color.WHITE, DEFAULT_FONT_SIZE, anchor_x="center")
			self.game_over = True
			
		self.camera.use()

	def on_key_press(self, key, modifiers):
		if self.game_over == False:
			if key == arcade.key.SPACE:
				if self.physics_engine.can_jump():
					self.player.change_y = PLAYER_JUMP_SPEED

			elif key == arcade.key.LEFT or key == arcade.key.A:
				self.player.change_x = -PLAYER_MOVEMENT_SPEED
				self.player.idle = False
				self.last_pressed_key = key
				if self.physics_engine.can_jump() and self.player.change_x != 0:
					self.run_sound_play = arcade.play_sound(self.run_sound, volume=0.2, looping=False)
				'''else:
					arcade.stop_sound(self.run_sound_play)'''

			elif key == arcade.key.RIGHT or key == arcade.key.D:
				self.player.change_x = PLAYER_MOVEMENT_SPEED
				self.player.idle = False
				self.last_pressed_key = key
				if self.physics_engine.can_jump() and self.player.change_x != 0:
					self.run_sound_play = arcade.play_sound(self.run_sound, volume=0.2, looping=False)
				'''else:
					arcade.stop_sound(self.run_sound_play)'''

		if self.game_over and key == arcade.key.SPACE:
			self.game_over = False
			self.player.center_x = 50
			self.player.center_y = 100
			self.fall_sound_played = False
			arcade.stop_sound(self.rip_fall_play)
			arcade.stop_sound(self.soundtrack_play)
			arcade.stop_sound(self.nature_sound_play)
			self.soundtrack_play = arcade.play_sound(self.soundtrack, volume=0.1, looping=True)
			self.nature_sound_play = arcade.play_sound(self.nature_sound, volume=0.1, looping=True)
			self.player.change_x = 0
			self.player.change_y = 0
			self.player.idle = True
			self.last_pressed_key = None
			if self.walk_sound_play:
				arcade.stop_sound(self.walk_sound_play)
				self.walk_sound_play = None


	def on_key_release(self, key, modifiers):
		if key == arcade.key.SPACE:
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

		player_centered  = screen_center_x, screen_center_y
		self.camera.move_to(player_centered)

	def on_update(self, delta_time):
		self.physics_engine.update()
		self.player.update_animation()
		self.center_camera_to_player()

		if self.player.left < 0:
			self.player.left = 0
		if self.player.right > 2400:
			self.player.right = 2400

		if self.player.top < 0 and self.fall_sound_played == False:
			self.rip_fall_play = arcade.play_sound(self.rip_fall, volume=0.3, looping=False)
			self.fall_sound_played = True


def main():
	game = Game()
	game.setup()
	arcade.run()

if __name__ == '__main__':
	main()
