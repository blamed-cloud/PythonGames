#!/user/bin/env python3
#character.py

class Character(object):

	# TODO: skills, secondaryStats, affinity, race, condition, support, associations, biorhythm, level
	def __init__(self, name, charClass, primaryStats, inventory, weaponRanks):
		self.name = name
		self.characterClass = charClass
		self.primaryStats = primaryStats
		self.inventory = inventory
		self.weaponRanks = weaponRanks

	def getName(self):
		return self.name

	def getClass(self):
		return self.characterClass

	def getPrimaryStats(self):
		return self.primaryStats

	def getStat(name):
		return self.primaryStats.getStatByName(name)

	def getInventory(self):
		return self.inventory

	def getWeaponRanks(self):
		return self.weaponRanks

