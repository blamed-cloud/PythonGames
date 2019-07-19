#!/user/bin/env python3
#weaponranks.py
from enums import *

class WeaponRanks(object):

	def __init__(self, weaponTypes, weaponRanks, weaponExp):
		assert len(weaponTypes) == len(weaponRanks)
		assert len(weaponTypes) == len(weaponExp)
		self.ranks = {}
		self.weaponExperience = {}
		for i, wType in enumerate(weaponTypes):
			assert wType in WeaponType
			wRank = weaponRanks[i]
			assert wRank in WeaponRank
			self.ranks[wType] = wRank
			self.weaponExperience = weaponExp[i]

	def getRank(self, wType):
		assert wType in WeaponType
		if wType in self.ranks:
			return self.ranks[wType]
		else:
			return WeaponRank.UNUSABLE

	def getExperience(self, wType):
		assert wType in WeaponType
		if wType in self.weaponExperience:
			return self.weaponExperience[wType]
		else:
			return 0

	def addExperience(self, wType, exp):
		assert wType in WeaponType
		assert wType in self.weaponExperience
		self.weaponExperience[wType] += abs(exp)

	def setRank(self, wType, wRank):
		assert wType in WeaponType
		assert wRank in WeaponRank
		self.ranks[wType] = wRank


