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


def UnitClass(object):

	def __init__(self, classType, moveType, classGrowths): # TODO: skills, weaponRanks
		self.classType = classType
		self.moveType = moveType
		self.growths = classGrowths

	def getClassType(self):
		return self.classType

	def getMoveType(self):
		return self.moveType

	def getGrowth(self, stat):
		return self.ClassGrowths.getGrowth(stat)


