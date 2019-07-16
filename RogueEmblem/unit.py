#!/user/bin/env python3
#unit.py

class Unit(object):

	# TODO: weaponRank, skills, secondaryStats, affinity, race, condition, support, associations, biorhythm
	def __init__(self, name, unitClass, primaryStats, inventory):
		self.name = name
		self.unitClass = unitClass
		self.primaryStats = primaryStats
		self.inventory = inventory

	def getName(self):
		return self.name

	def getClass(self):
		return self.unitClass

	def getPrimaryStats(self):
		return self.primaryStats

	def getStat(name):
		return self.primaryStats.getStatByName(name)
