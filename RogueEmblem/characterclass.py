#!/user/bin/env python3
#characterclass.py
from enums import *


def CharacterClass(object):

	def __init__(self, className, classTier, classType, moveType, classStats, maxWeaponRanks): # TODO: skills
		self.className = className
		self.classTier = classTier
		self.classType = classType
		self.moveType = moveType
		self.classStats = classStats
		self.maxRanks = maxWeaponRanks

	def getClassName(self):
		return self.className

	def getClassTier(self):
		return self.classTier

	def getClassType(self):
		return self.classType

	def getMoveType(self):
		return self.moveType

	def getStat(self, stat):
		return self.classStats.getStatByName(stat)

	def getMaxRank(self, wType):
		return self.maxRanks.getRank(wType)


