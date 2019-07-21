#!/user/bin/env python3
#combat.py
from enums import *
from calculations import *

class Combat(object):

	def __init__(self, attacker, atkTerrain, defender, defTerrain, distance, highGround):
		# input values
		self.attacker = attacker
		self.atkTerrain = atkTerrain
		self.defender = defender
		self.defTerrain = defTerrain
		self.distance = distance
		self.highGround = highGround
		# class checking
		self.attackerClassType = self.attacker.getClass().getClassType()
		self.defenderClassType = self.defender.getClass().getClassType()
		# weapon checking
		if not self.attacker.getInventory().isEquipped():
			# the attacker must be equipped at the start of the combat (but not for the whole thing due to skills)
			raise ValueError
		self.attackerEquipped = True
		self.attackerDamageType = self.attacker().getInventory().getEquippedItem().getDamageType()
		self.attackerWType = self.attacker.getInventory().getEquippedItem().getWeaponType()

		self.defenderEquipped = self.defender.getInventory().isEquipped()
		if self.defenderEquipped:
			defWeapon = self.defender().getInventory().getEquippedItem()
			self.defenderDamageType = defWeapon.getDamageType()
			self.defenderWType = defWeapon.getWeaponType()
		else:
			self.defenderDamageType = DamageType.NONE
			self.defenderWType = None

		# calculated values for preview purposes (actual values may change when fighting)
		self.attackerDamage = None
		self.attackerDefense = None
		self.defenderDamage = None
		self.defenderDefense = None
		self._calcAtkDef()
		self.attackerPreviewDamage = calcDamage(self.attackerDamage, self.defenderDefense, isCrit = False)
		if self.defenderEquipped:
			self.defenderPreviewDamage = calcDamage(self.defenderDamage, self.attackerDefense, isCrit = False)
		else:
			self.defenderPreviewDamage = None

		self.attackerAccuracy = None
		self.attackerAvoid = None
		self.defenderAccuracy = None
		self.defenderAvoid = None
		self._calcAccAvo()
		self.attackerPreviewHitChance = calcHitChance(self.attackerAccuracy, self.defenderAvoid)
		if self.defenderEquipped:
			self.defenderPreviewHitChance = calcHitChance(self.defenderAccuracy, self.attackerAvoid)
		else:
			self.defenderPreviewHitChance = None

		self.attackerCritRate = None
		self.attackerDodge = None
		self.defenderCritRate = None
		self.defenderDodge = None
		self._calcCritDodge()
		self.attackerPreviewCritChance = calcCritChance(self.attackerCritRate, self.defenderDodge)
		if self.defenderEquipped:
			self.defenderPreviewCritChance = calcCritChance(self.defenderCritRate, self.attackerDodge)
		else:
			self.defenderPreviewCritChance = None

		self.previewDoubler = calcDoubler(self.attacker, self.defender)
		self.previewNone = '---'
		self.attackerPreviewHP = getCharacterStat(self.attacker, PrimaryStatNames.HP)
		self.defenderPreviewHP = getCharacterStat(self.defender, PrimaryStatNames.HP)



	def _calcCritDodge(self):
		if self.attackerEquipped:
			self.attackerCritRate = calcCritRate(self.attacker)
			self.defenderDodge = calcDodge(self.defender)
		else:
			self.attackerCritRate = None
			self.defenderDodge = None

		if self.defenderEquipped:
			self.defenderCritRate = calcCritRate(self.defender)
			self.attackerDodge = calcDodge(self.attacker)
		else:
			self.defenderCritRate = None
			self.attackerDodge = None

	def _calcAccAvo(self):
		atkHighGround = self.highGround is Combatant.ATTACKER
		defHighGround = self.highGround is Combatant.DEFENDER
		if self.attackerEquipped:
			self.attackerAccuracy = calcAccuracy(self.attacker, self.defenderWType, atkHighGround, defHighGround, self.distance)
			self.defenderAvoid = calcAvoid(self.defender, self.defTerrain)
		else:
			self.attackerAccuracy = None
			self.defenderAvoid = None

		if self.defenderEquipped:
			self.defenderAccuracy = calcAccuracy(self.defender, self.attackerWType, defHighGround, atkHighGround, self.distance)
			self.attackerAvoid = calcAvoid(self.attacker, self.atkTerrain)
		else:
			self.defenderAccuracy = None
			self.attackerAvoid = None

	def _calcAtkDef(self):
		if self.attackerDamageType is DamageType.PHYSICAL:
			hasHighGround = self.highGround is Combatant.ATTACKER
			self.attackerDamage = calcPhysicalDmg(self.attacker, self.defenderClassType, self.defenderWType, hasHighGround)
			self.defenderDefense = calcPhysicalDef(self.defender, self.defTerrain)
		elif self.attackerDamageType is DamageType.MAGICAL:
			hasHighGround = self.highGround is Combatant.ATTACKER
			self.attackerDamage = calcMagicDmg(self.attacker, self.defenderClassType, self.defenderWType, hasHighGround)
			self.defenderDefense = calcMagicDef(self.defender, self.defTerrain)
		else:
			self.attackerDamage = None
			self.defenderDefense = None

		if self.defenderDamageType is DamageType.PHYSICAL:
			hasHighGround = self.highGround is Combatant.DEFENDER
			self.defenderDamage = calcPhysicalDmg(self.defender, self.attackerClassType, self.attackerWType, hasHighGround)
			self.attackerDefense = calcPhysicalDef(self.attacker, self.atkTerrain)
		elif self.defenderDamageType is DamageType.MAGICAL:
			hasHighGround = self.highGround is Combatant.DEFENDER
			self.defenderDamage = calcMagicDmg(self.defender, self.attackerClassType, self.attackerWType, hasHighGround)
			self.attackerDefense = calcMagicDef(self.attacker, self.atkTerrain)
		else:
			self.defenderDamage = None
			self.attackerDefense = None

