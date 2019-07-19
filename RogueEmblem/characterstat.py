#!/user/bin/env python3
#characterstat.py
from enum import Enum


class PrimaryStats(object):

	def __init__(self, hp, strength, magic, skill, speed, luck, defense, resistance):
		self.stats = {}
		self.stats[PrimaryStatNames.HP] = hp
		self.stats[PrimaryStatNames.STRENGTH] = strength
		self.stats[PrimaryStatNames.MAGIC] = magic
		self.stats[PrimaryStatNames.SKILL] = skill
		self.stats[PrimaryStatNames.SPEED] = speed
		self.stats[PrimaryStatNames.LUCK] = luck
		self.stats[PrimaryStatNames.DEFENSE] = defense
		self.stats[PrimaryStatNames.RESISTANCE] = resistance

	def getStatByName(self, name):
		assert name in PrimaryStatNames
		return self.stats[name]


class CharacterStat(object):

	def __init__(self, name, amount, personalGrowth):
		self.name = name
		self.amount = amount
		self.personalGrowth = personalGrowth
		self.modifier = 0
		self.multiplier = 1
		self.bonus = 0

	def getName(self):
		return self.name

	def getBaseAmount(self):
		return self.amount

	# additive modifiers are added before multipliers
	# and bonuses are added after multipliers
	def getAmount(self):
		return int((self.amount + self.modifier) * self.multiplier + self.bonus)

	def setPersonalGrowth(self, pGr):
		self.personalGrowth = pGr

	def getPersonalGrowth(self):
		return self.personalGrowth

	def increase(self, amount = 1, cap = None):
		if cap is not None:
			if self.amount < cap:
				self.amount += abs(amount)
				if self.amount > cap:
					self.amount = cap
		else:
			self.amount += abs(amount)

	def setModifier(self, amount):
		self.modifier = amount

	def clearModifier(self):
		self.modifier = 0

	# multipliers cannot be negative
	def setMultiplier(self, amount):
		self.multiplier = abs(amount)

	def clearMultiplier(self):
		self.multiplier = 1

	def setBonus(self, bonus):
		self.bonus = bonus

	def clearBonus(self):
		self.bonus = 0

	def clearChanges(self):
		self.clearModifier()
		self.clearMultiplier()
		self.clearBonus()


