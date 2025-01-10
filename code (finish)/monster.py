from game_data import MONSTER_DATA, attack_DATA
from random import randint

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

	def __repr__(self):
		return f'monster: {self.name}, lvl: {self.level}'

	def get_stat(self, stat):
		return self.base_stats[stat] * self.level

	def get_stats(self):
		return {
			'health': self.get_stat('max_health'),
			'energy': self.get_stat('max_energy'),
			'Kommunikation': self.get_stat('Kommunikation'),
			'Softwarekenntnisse': self.get_stat('Softwarekenntnisse'),
			'speed': self.get_stat('speed'),
			'Hardwarekenntnisse': self.get_stat('Hardwarekenntnisse'),
		}

	def get_abilities(self, all  = True):
		if all:
			return [ability for lvl, ability in self.abilities.items() if self.level >= lvl]
		else:
			return [ability for lvl, ability in self.abilities.items() if self.level >= lvl and attack_DATA[ability]['cost'] < self.energy]

	def get_info(self):
		return (
			(self.health, self.get_stat('max_health')),
			(self.energy, self.get_stat('max_energy')),
			(self.initiative, 100)
			)

	def reduce_energy(self, Kommunikation):
		self.energy -= attack_DATA[Kommunikation]['cost']

	def get_base_damage(self, Kommunikation):
		return self.get_stat('Kommunikation') * attack_DATA[Kommunikation]['amount']

	def update_xp(self, amount):
		if self.level_up - self.xp > amount:
			self.xp += amount
		else:
			self.level += 1
			self.xp = amount - (self.level_up - self.xp)
			self.level_up = self.level * 150

	def stat_limiter(self):
		self.health = max(0, min(self.health, self.get_stat('max_health')))
		self.energy = max(0, min(self.energy, self.get_stat('max_energy')))

	def update(self, dt):
		self.stat_limiter()
		if not self.paused:
			self.initiative += self.get_stat('speed') * dt