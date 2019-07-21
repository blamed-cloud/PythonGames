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


class Combatant(Enum):
	NONE = 0
	ATTACKER = 1
	DEFENDER = 2


class DamageType(Enum):
	NONE = 0
	PHYSICAL = 1
	MAGICAL = 2


class CalculatedStats(Enum):
	ACCURACY = 0
	AVOID = 1
	CRIT = 2
	DODGE = 3
	DAMAGE = 4


class StatChangeTypes(Enum):
	MODIFIER = 0
	MULTIPLIER = 1
	BONUS = 2


class SkillActivation(Enum):
	ALWAYS = 0
	IN_COMBAT = 1
	COMMAND = 2
	HP_THRESHOLD = 3
	CHANCE = 4
	TURN_START = 5
	ATTACKS_SECOND = 6
	ATTACKED_INDIRECTLY = 7


class SkillTags(Enum):
	STAT_CHANGE = 0
	CANCEL_COUNTERATTACK = 1
	NEGATE_CRIT = 2
	ADEPT_ATTACK = 3
	HEALING = 4
	EXP_MULTIPLIER = 5
	PASS = 6
	EFFECTIVE_DAMAGE = 7
	ATTACK_FIRST = 8
	IGNORE_TERRAIN = 9
	DEAL_DAMAGE = 10
	UNEQUIP = 11
	CORRODE = 12
	NEGATE_EFFECTIVE_DAMAGE = 13
	MASTERY_ATTACK = 14
	WEXP_MULTIPLIER = 15
	FATAL_DAMAGE = 16


class SkillTarget(Enum):
	SELF = 0
	ADJACENT_ALLY = 1
	ADJACENT_ENEMY = 2
	ADJACENT_ANY = 3
	COMBAT_ENEMY = 4


# sacrifice?
# wildheart?
# glare?
class SkillActions(Enum):
	SHOVE = 0
	CANTO = 1
	STEAL = 2
	SMITE = 3
	FORMSHIFT = 4
	GALDRAR = 5


