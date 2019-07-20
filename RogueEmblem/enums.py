#!/user/bin/env python3
#enums.py
from enum import Enum

class OrderedEnum(Enum):

	def __ge__(self, other):
		if self.__class__ is other.__class__:
			return self.value >= other.value
		return NotImplemented

	def __gt__(self, other):
		if self.__class__ is other.__class__:
			return self.value > other.value
		return NotImplemented

	def __le__(self, other):
		if self.__class__ is other.__class__:
			return self.value <= other.value
		return NotImplemented

	def __lt__(self, other):
		if self.__class__ is other.__class__:
			return self.value < other.value
		return NotImplemented



class PrimaryStatNames(Enum):
	HP = 0
	STRENGTH = 1
	MAGIC = 2
	SKILL = 3
	SPEED = 4
	LUCK = 5
	DEFENSE = 6
	RESISTANCE = 7


class SecondaryStatNames(Enum):
	CON = 1
	WEIGHT = 2
	MOVE = 3


class ClassTiers(OrderedEnum):
	FIRST = 1
	SECOND = 2
	THIRD = 3


class ClassType(Enum):
	INFANTRY = 0
	MAGE = 1
	ARMOR = 2
	HORSE = 3
	PEGASUS = 4
	WYVERN = 5
	BEAST = 6
	DRAGON = 7
	BIRD = 8


class MoveType(Enum):
	FOOT = 0
	HORSE = 1
	FLYING = 2


class WeaponType(Enum):
	SWORD = 0
	LANCE = 1
	AXE = 2
	BOW = 3
	KNIFE = 4
	STRIKE = 5
	FIRE = 6
	THUNDER = 7
	WIND = 8
	LIGHT = 9
	DARK = 10
	STAFF = 11


class WeaponRank(OrderedEnum):
	UNUSABLE = 0
	E = 1
	D = 2
	C = 2
	B = 3
	A = 4
	S = 5
	SS = 6


