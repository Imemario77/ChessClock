from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.uix.button import ButtonBehavior
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from kivy.clock import Clock
import pygame

pygame.mixer.init()


class TimeBox(Screen):
	start_player_1 = ObjectProperty()
	player1 = ObjectProperty()
	start_player_2 = ObjectProperty()
	player2 = ObjectProperty()
	player1_moves = ObjectProperty()
	player2_moves = ObjectProperty()
	pause_game = ObjectProperty()
	add_more_time =  ObjectProperty()
	
class PlayerTime(ButtonBehavior, MDBoxLayout):
    pass

	
	
      	
class CenterMenu(MDBoxLayout):
	pass

class MainApp(MDApp):
	player_1TimeLeft = 60
	player_2TimeLeft = 60
	player_1_moves_count = 0
	player_2_moves_count = 0
	player_1status = False
	player_2status = False
	start_game = False
	mins, secs = divmod(player_1TimeLeft , 60)
	Game_Time = '{:02d}:{:02d}'.format(mins, secs)
	
	def __init__(self, **kwargs):
		super(MainApp, self).__init__(**kwargs)

	def build(self):
		self.theme_cls.primary_palette ='Gray'
		self.clock = Clock.schedule_interval(self.update_count,1)
		return TimeBox()
	def play_sound(self,file_path):
	   pygame.mixer.music.load(file_path)
	   pygame.mixer.music.play()
	   if self.player_1TimeLeft <= 0 or self.player_2TimeLeft <= 0:
	   	pygame.mixer.music.stop()
	   return pygame.mixer.music
	   
	   
	def update_count(self, obj):
		if self.player_1status:
			mins, secs = divmod(self.player_1TimeLeft , 60)
			timer = '{:02d}:{:02d}'.format(mins, secs)
			self.player_1TimeLeft  -= 1
			self.root.ids.player1.text = timer
			if mins <= 0 and secs <= 0:
				self.time_out()
				self.root.ids.start_player_1.md_bg_color = (1,0,0,1)
			if mins == 0 and secs <= 4:
				self.play_sound('5sec.wav')
			elif mins == 0 and secs <= 30:
				self.play_sound('beep.wav')
			
			
	
		if self.player_2status:
			mins, secs = divmod(self.player_2TimeLeft , 60)
			timer = '{:02d}:{:02d}'.format(mins, secs)
			self.player_2TimeLeft  -= 1
			self.root.ids.player2.text = timer
			if mins <= 0 and secs <= 0:
				self.time_out()
				self.root.ids.start_player_2.md_bg_color =  (1,0,0,1)
			if mins == 0 and secs <= 4:
				self.play_sound('5sec.wav')
			elif mins == 0 and secs <= 30:
				self.play_sound('beep.wav')
			
	def add_time(self):
		self.player_1TimeLeft += 60
		mins, secs = divmod(self.player_1TimeLeft , 60)
		timer = '{:02d}:{:02d}'.format(mins, secs)
		self.root.ids.player1.text = timer 
		self.player_2TimeLeft += 60
		mins, secs = divmod(self.player_2TimeLeft , 60)
		timer = '{:02d}:{:02d}'.format(mins, secs)
		self.root.ids.player2.text = timer 
   
	def start_count(self, player):
		self.play_sound('beep.wav')
		if player == 'player_1_start':
			if not self.start_game:
				self.player_2status = True
				self.start_game = True
				self.root.ids.start_player_2.md_bg_color = '#ffa05c'
				self.root.ids.start_player_1.disabled = True
				self.root.ids.pause_game.opacity = 1
				self.root.ids.pause_game.disabled = False
			else:
				if self.player_1status:
					self.player_1status = not self.player_1status
					self.player_2status = True
					self.root.ids.start_player_2.md_bg_color = '#ffa05c'
					self.root.ids.start_player_1.md_bg_color = '#524e44'
					self.root.ids.start_player_2.disabled = False
					self.root.ids.start_player_1.disabled = True
					self.player_1_moves_count += 1
					self.root.ids.player1_moves.text = 'Moves:  ' + str(self.player_1_moves_count)
					
			
		if player == 'player_2_start':
			if not self.start_game:
				self.player_1status = True
				self.start_game = True
				self.root.ids.start_player_2.disabled = True
				self.root.ids.start_player_1.md_bg_color = '#ffa05c'
				self.root.ids.pause_game.opacity = 1
				self.root.ids.pause_game.disabled = False
			else:
				if self.player_2status:
					self.player_2status = not self.player_2status
					self.player_1status = True
					self.root.ids.start_player_1.md_bg_color = '#ffa05c'
					self.root.ids.start_player_2.md_bg_color = '#524e44'
					self.root.ids.start_player_1.disabled = False
					self.root.ids.start_player_2.disabled = True
					self.player_2_moves_count += 1
					self.root.ids.player2_moves.text = 'Moves:  ' + str(self.player_2_moves_count)
						
	def restart_time(self):
		close_btn = MDFlatButton(text='No', on_release= self.stop_reset)
		reset_btn =   MDFlatButton(text='Yes', on_release= self.confirm_reset) 
		self.popup = MDDialog(title="Reset the clock", size_hint=(0.8, 0.15),pos_hint= {"center_x": 0.5},
								buttons=[close_btn, reset_btn])
		self.popup.open()
		
	def stop_reset(self,obj):
		self.popup.dismiss()
		
	def confirm_reset(self,obj):
		self.pause_time()
		self.popup.dismiss()
		self.player_1TimeLeft = 60
		self.player_2TimeLeft = 60
		self.root.ids.player1_moves.text = 'Moves:  0'
		self.root.ids.player2_moves.text = 'Moves:  0'
		self.root.ids.player1.text = self.Game_Time
		self.root.ids.player2.text = self.Game_Time
		self.root.ids.pause_game.opacity = 0
		self.root.ids.pause_game.disabled = True
		self.root.ids.add_more_time.disabled = False
		self.clock.cancel()
		self.clock = Clock.schedule_interval(self.update_count,1)
	
	def time_out(self):
		self.clock.cancel()
		stop = self.play_sound('beep.wav')
		stop.stop()
		self.player_1status = False
		self.player_2status = False
		self.root.ids.start_player_1.disabled = True
		self.root.ids.start_player_2.disabled = True
		self.root.ids.pause_game.opacity = 0
		self.root.ids.pause_game.disabled = True
		self.root.ids.add_more_time.disabled  = True
	
	def pause_time(self):
		stop = self.play_sound('beep.wav')
		stop.stop()
		self.player_1status = False
		self.player_2status = False
		self.start_game = False
		self.root.ids.start_player_1.disabled = False
		self.root.ids.start_player_2.disabled = False
		self.root.ids.start_player_1.md_bg_color = '#524e44'
		self.root.ids.start_player_2.md_bg_color = '#524e44'
		self.root.ids.pause_game.opacity = 0
		self.root.ids.pause_game.disabled = True
MainApp().run()