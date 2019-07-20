#!/user/bin/env python3
#weapon.py
from enums import *

def defaultEffectiveDamage(wType):
	if wType is WeaponType.BOW:
		return {ClassType.PEGASUS, ClassType.WYVERN, ClassType.BIRD}
	elif wType is WeaponType.FIRE:
		return {ClassType.BEAST, ClassType.HORSE}
	elif wType is WeaponType.THUNDER:
		return {ClassType.WYVERN, ClassType.DRAGON}
	elif wType is WeaponType.WIND:
		return {ClassType.PEGASUS, ClassType.BIRD}
	return set()

class WeaponRange(object):

	def __init__(self, minRange, maxRange):
		self.minRange = minRange
		self.maxRange = maxRange

	def getMinRange(self):
		return self.minRange

	# a maxRange of -1 means magic/2
	def getMaxRange(self):
		return self.maxRange


class WeaponStats(object):

	def __init__(self, wRank, might, hit, crit, weight, wRange):
		self.wRank = wRank
		self.might = might
		self.hit = hit
		self.crit = crit
		self.weight = weight
		self.wRange = wRange

	def getRank(self):
		return self.wRank

	def getMight(self):
		return self.might

	def getHit(self):
		return self.hit

	def getCrit(self):
		return self.crit

	def getWeight(self):
		return self.weight

	def getRange(self):
		return self.wRange


class Weapon(object):

	def __init__(self, name, wType, wStats, maxUses, usesLeft, isMagic, extraEffDmg = None, bonusStats = None, characterOnly = None):
		self.name = name
		self.wType = wType
		self.wStats = wStats
		self.maxUses = maxUses
		self.usesLeft = usesLeft
		self.isMagic = isMagic
		self.extraEffDmg = extraEffDmg
		self.bonusStats = bonusStats
		self.characterOnly = characterOnly

	def getName(self):
		return self.name

	def getWeaponType(self):
		return self.wType

	def getWeaponStats(self):
		return self.wStats

	def getMaxUses(self):
		return self.maxUses

	def getUsesLeft(self):
		return self.usesLeft

	def isMagic(self):
		return self.isMagic

	def hasExtraEffectiveDamage(self):
		return self.extraEffDmg is not None

	def getExtraEffectiveDamage(self):
		return self.extraEffDmg

	def getAllEffectiveDamage(self):
		if self.hasExtraEffectiveDamage():
			return self.getExtraEffectiveDamage().union(defaultEffectiveDamage(self.getWeaponType()))
		else:
			return defaultEffectiveDamage(self.getWeaponType())

	def hasBonusStats(self):
		return self.bonusStats is not None

	def getBonusStats(self):
		return self.bonusStats

	def isUniqueWeapon(self):
		return self.characterOnly is not None

	def getUniqueCharacter(self):
		return self.characterOnly


