#!/user/bin/env python3
#unitclass.py
from enums import *

class ClassGrowths(object):

	def __init__(self, hpGr, strGr, magGr, sklGr, spdGr, lckGr, defGr, resGr):
		self.growths = {}
		self.growths[PrimaryStatNames.HP] = hpGr
		self.growths[PrimaryStatNames.STRENGTH] = strGr
		self.growths[PrimaryStatNames.MAGIC] = magGr
		self.growths[PrimaryStatNames.SKILL] = sklGr
		self.growths[PrimaryStatNames.SPEED] = spdGr
		self.growths[PrimaryStatNames.LUCK] = lckGr
		self.growths[PrimaryStatNames.DEFENSE] = defGr
		self.growths[PrimaryStatNames.RESISTANCE] = resGr

	def getGrowth(self, stat):
		assert stat in PrimaryStatNames
		return self.growths[stat]


class WeaponRanksDict(object):

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


def UnitClass(object):

	def __init__(self, classType, moveType, classGrowths, maxWeaponRanks): # TODO: skills, promotiongains
		self.classType = classType
		self.moveType = moveType
		self.growths = classGrowths
		self.maxRanks = maxWeaponRanks

	def getClassType(self):
		return self.classType

	def getMoveType(self):
		return self.moveType

	def getGrowth(self, stat):
		return self.ClassGrowths.getGrowth(stat)

	def getMaxRank(self, wType):
		return self.maxRanks.getMaxRank(wType)


