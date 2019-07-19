#!/user/bin/env python3
#characterstat.py
from enum import Enum


class PrimaryStats(object):

	def __init__(self, hp, strength, magic, skill, speed, luck, defense, resistance):
		self.stats = {}
		self.stats[PrimaryStatNames.HP] = hpGr
		self.stats[PrimaryStatNames.STRENGTH] = strGr
		self.stats[PrimaryStatNames.MAGIC] = magGr
		self.stats[PrimaryStatNames.SKILL] = sklGr
		self.stats[PrimaryStatNames.SPEED] = spdGr
		self.stats[PrimaryStatNames.LUCK] = lckGr
		self.stats[PrimaryStatNames.DEFENSE] = defGr
		self.stats[PrimaryStatNames.RESISTANCE] = resGr

	def getStatByName(self, name):
		assert name in PrimaryStatNames
		return self.stats[name]


class CharacterStat(object):

	def __init__(self, name, amount, cap, personalGrowth, classGrowth):
		self.name = name
		self.amount = amount
		self.cap = cap
		self.personalGrowth = personalGrowth
		self.classGrowth = classGrowth
		self.growthRate = self.personalGrowth + self.classGrowth
		self.modifier = 0
		self.multiplier = 1

	def getName(self):
		return self.name

	def getBaseAmount(self):
		return self.amount

	# additive modifiers are added before multipliers
	def getAmount(self):
		return int((self.amount + self.modifier) * self.multiplier)

	def hasCap(self):
		return self.cap is not None

	def getCap(self):
		return self.cap

	def setPersonalGrowth(self, pGr):
		self.personalGrowth = pGr
		self._updateGrowthRate()

	def setClassGrowth(self, cGr):
		self.classGrowth = cGr
		self._updateGrowthRate()

	def _updateGrowthRate(self):
		self.growthRate = self.personalGrowth + self.classGrowth

	def getGrowthRate(self):
		return self.growthRate

	def increase(self, amount = 1):
		if self.hasCap():
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

	def clearChanges(self):
		self.clearModifier()
		self.clearMultiplier()


