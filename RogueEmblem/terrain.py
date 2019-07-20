#!/user/bin/env python3
#classstat.py


class Terrain(object):

	def __init__(self, avoidBonus, defBonus, resBonus, healing):
		self.avoidBonus = avoidBonus
		self.defBonus = defBonus
		self.resBonus = resBonus
		self.healing = healing

	def getAvoidBonus(self):
		return self.avoidBonus

	def getDefBonus(self):
		return self.defBonus

	def getResBonus(self):
		return self.resBonus

	def getHealing(self):
		return self.healing


