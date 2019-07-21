#!/user/bin/env python3
#calculations.py
from enums import *

### Damage & accuracy constants ###
CRIT_MULITPLIER = 3
EFFECTIVE_MULTIPLIER = 3

HIGH_GROUND_DAMAGE_BONUS = 2
HIGH_GROUND_ACCURACY_BONUS = 50
BOW_STANDARD_DISTANCE = 2
BOW_RANGE_PENALTY = 30

### weapon triangle constants ###
PHYSICAL_TRIANGLE = [WeaponType.SWORD, WeaponType.AXE, WeaponType.LANCE]
MAGIC_TRIANGLE_A = [WeaponType.FIRE, WeaponType.WIND, WeaponType.THUNDER]

MAGIC_TYPE_ANIMA = MAGIC_TRIANGLE_A

MAGIC_TRIANGLE_B = ["anima", WeaponType.LIGHT, WeaponType.DARK]

TRIANGLE_ADVANTAGE = 1
TRIANGLE_DISADVANTAGE = -1

WEAPON_TRIANGLE_DAMAGE_BONUS = 1
WEAPON_TRIANGLE_HIT_BONUS = 10

def truncateToPercent(num):
	if num < 0:
		return 0
	elif num > 100:
		return 100
	else:
		return num

def getTriangleDirection(thisWeapon, otherWeapon, triangle):
	thisIndex = triangle.index(thisWeapon)
	otherIndex = triangle.index(otherWeapon)
	if abs(thisIndex - otherIndex) == 2:
		if thisIndex < otherIndex:
			return TRIANGLE_DISADVANTAGE
		else:
			return TRIANGLE_ADVANTAGE
	else:
		if thisIndex < otherIndex:
			return TRIANGLE_ADVANTAGE
		else:
			return TRIANGLE_DISADVANTAGE

def getWeaponTriangleDirection(wType1, wType2):
	if wType1 is wType2:
		return 0
	direction = 0
	if wType1 in PHYSICAL_TRIANGLE:
		if wType2 in PHYSICAL_TRIANGLE:
			direction = getTriangleDirection(wType1, wType2, PHYSICAL_TRIANGLE)
	elif wType1 in MAGIC_TYPE_ANIMA:
		if wType2 in MAGIC_TYPE_ANIMA:
			direction = getTriangleDirection(wType1, wType2, MAGIC_TRIANGLE_A)
		elif wType2 in MAGIC_TRIANGLE_B:
			direction = getTriangleDirection("anima", wType2, MAGIC_TRIANGLE_B)
	elif wType1 in MAGIC_TRIANGLE_B:
		if wType2 in MAGIC_TYPE_ANIMA:
			direction = getTriangleDirection(wType1, "anima", MAGIC_TRIANGLE_B)
		elif wType2 in MAGIC_TRIANGLE_B:
			direction = getTriangleDirection(wType1, wType2, MAGIC_TRIANGLE_B)
	return direction

def getCharacterStat(character, statName):
	if statName in PrimaryStatNames:
		return character.getPrimaryStats().getStatByName(statName).getAmount()
	elif statName in SecondaryStatNames
		return character.getSecondaryStats().getStatByName(statName).getAmount()
	else:
		raise ValueError

def calcAttackSpeed(character):
	speed = getCharacterStat(character, PrimaryStatNames.SPEED)
	strength = getCharacterStat(character, PrimaryStatNames.STRENGTH)
	wWeight = 0
	penalty = 0
	if character.getInventory().isEquipped():
		weapon = character.getInventory().getEquippedItem()
		wWeight = weapon.getWeaponStats().getWeight()
	if (strength < wWeight):
		penalty = wWeight - strength
	if speed <= penalty:
		return 0
	else:
		return speed - penalty

# TODO: support bonus
def calcPhysicalDmg(character, enemyClassType, enemyWType, hasHighGround):
	wMight = 0
	isEffectiveDamage = False
	triangleDirection = 0
	if character.getInventory().isEquipped():
		weapon = character.getInventory().getEquippedItem()
		if weapon.isMagic():
			return 0
		else:
			wMight = weapon.getWeaponStats().getMight()
		# TODO: check skills as well!
		effectiveDamageSet = weapon.getAllEffectiveDamage()
		if enemyClassType in effectiveDamageSet:
			isEffectiveDamage = True
		triangleDirection = getWeaponTriangleDirection(weapon.getWeaponType(), enemyWType)

	weaponDamage = wMight + triangleDirection*WEAPON_TRIANGLE_DAMAGE_BONUS
	if isEffectiveDamage:
		weaponDamage *= EFFECTIVE_MULTIPLIER

	strength = getCharacterStat(character, PrimaryStatNames.STRENGTH)

	damage = strength + weaponDamage
	if hasHighGround:
		damage += HIGH_GROUND_DAMAGE_BONUS

	return damage

# TODO: support bonus
def calcPhysicalDef(character, terrain):
	defense = getCharacterStat(character, PrimaryStatNames.DEFENSE)
	return defense + terrain.getDefBonus()


def calcMagicDmg(character, enemyClassType, enemyWType, hasHighGround):
	wMight = 0
	isEffectiveDamage = False
	triangleDirection = 0
	if character.getInventory().isEquipped():
		weapon = character.getInventory().getEquippedItem()
		if not weapon.isMagic():
			return 0
		else:
			wMight = weapon.getWeaponStats().getMight()
		# TODO: check skills as well!
		effectiveDamageSet = weapon.getAllEffectiveDamage()
		if enemyClassType in effectiveDamageSet:
			isEffectiveDamage = True
		triangleDirection = getWeaponTriangleDirection(weapon.getWeaponType(), enemyWType)

	weaponDamage = wMight + triangleDirection*WEAPON_TRIANGLE_DAMAGE_BONUS
	if isEffectiveDamage:
		weaponDamage *= EFFECTIVE_MULTIPLIER

	magic = getCharacterStat(character, PrimaryStatNames.MAGIC)

	damage = magic + weaponDamage
	if hasHighGround:
		damage += HIGH_GROUND_DAMAGE_BONUS

	return damage

# TODO: support bonus
def calcMagicDef(character, terrain):
	resistance = getCharacterStat(character, PrimaryStatNames.RESISTANCE)
	return resistance + terrain.getResBonus()

def calcDamage(totalDamage, enemyDefence, isCrit):
	if (totalDamage < enemyDefence):
		return 0
	else:
		damage = (totalDamage - enemyDefence)
		if isCrit:
			damage *= CRIT_MULITPLIER
		return damage

# TODO: biorhythm, support, leadership?, affinity?
def calcAccuracy(character, enemyWType, hasHighGround, hasLowGround, distance):
	if not character.getInventory.isEquipped():
		return 0
	weapon = character.getInventory().getEquippedItem()
	wHit = weapon.getWeaponStats().getHit()
	skill = getCharacterStat(character, PrimaryStatNames.SKILL)
	luck = getCharacterStat(character, PrimaryStatNames.LUCK)
	triangleDirection = getWeaponTriangleDirection(weapon.getWeaponType(), enemyWType)
	distancePenalty = 0
	heightBonus = 0
	if weapon.getWeaponType() is WeaponType.BOW and distance != BOW_STANDARD_DISTANCE:
		distancePenalty = BOW_RANGE_PENALTY
	if hasHighGround:
		heightBonus = HIGH_GROUND_ACCURACY_BONUS
	elif hasLowGround:
		heightBonus = -1 * HIGH_GROUND_ACCURACY_BONUS
	accuracy = wHit + (skill * 2) + luck + (triangleDirection * WEAPON_TRIANGLE_HIT_BONUS) + heightBonus - distancePenalty
	if accuracy > 0:
		return accuracy
	else:
		return 0

# TODO: biorhythm, support, leadership?, affinity?
def calcAvoid(character, terrain):
	attackSpeed = calcAttackSpeed(character)
	luck = getCharacterStat(character, PrimaryStatNames.LUCK)
	avoid = (attackSpeed * 2) + luck + terrain.getAvoidBonus()
	return avoid

def calcHitChance(accuracy, avoid):
	hitChance = accuracy - avoid
	return truncateToPercent(hitChance)

# TODO: staff accuracy

# TODO: glare accuracy

# TODO: skill crit bonus, bond bonus?
def calcCritRate(character):
	if not character.getInventory.isEquipped():
		return 0
	weapon = character.getInventory().getEquippedItem()
	wCrit = weapon.getWeaponStats().getCrit()
	skill = getCharacterStat(character, PrimaryStatNames.SKILL)
	critRate = wCrit + int(skill / 2)
	if critRate < 0:
		return 0
	else:
		return critRate

# TODO: bond bonus?
def calcDodge(character):
	return getCharacterStat(character, PrimaryStatNames.LUCK)

def calcCritChance(crit, dodge):
	critChance = crit - dodge
	return truncateToPercent(critChance)

### MISC ###

def calcDoubler(attacker, defender):
	attackerAS = calcAttackSpeed(attacker)
	defenderAS = calcAttackSpeed(defender)
	if attackerAS - defenderAS >= 4:
		return Combatant.ATTACKER
	elif defenderAS - attackerAS >= 4:
		return Combatant.DEFENDER
	else:
		return Combatant.NONE

