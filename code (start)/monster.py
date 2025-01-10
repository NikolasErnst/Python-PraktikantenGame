from game_data import MONSTER_DATA, attack_DATA

class Monster:
	def __init__(self, name, level):
		self.name, self.level = name, level
		self.paused = False

		# stats 
		self.element = MONSTER_DATA[name]['stats']['element']
		self.base_stats = MONSTER_DATA[name]['stats']
		self.health = self.base_stats['max_health'] * self.level
		self.energy = self.base_stats['max_energy'] * self.level
		self.initiative = 0
		self.abilities = MONSTER_DATA[name]['abilities']
		self.defending = False

		# experience
		self.xp = 0
		self.level_up = self.level * 150
		self.evolution = MONSTER_DATA[self.name]['evolve']