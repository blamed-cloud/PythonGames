#!/user/bin/env python3
#calculations.py

def getCharacterStat(character, statName):
	if statName in PrimaryStatNames:
		return character.getPrimaryStats().getStatByName(statName)
	elif statName in SecondaryStatNames
		return character.getSecondaryStats().getStatByName(statName)
	else:
		raise ValueError

def calcAttackSpeed(character):
	speed = getCharacterStat(character, PrimaryStatNames.SPEED)
	strength = getCharacterStat(character, PrimaryStatNames.STRENGTH)
	if character.getInventory().isEquipped():
		weapon = character.getInventory().getEquippedItem()
		wWeight = weapon.getWeaponStats().getWeight()
	else:
		wWeight = 0
	if (strength < wWeight):
		penalty = wWeight - strength
	else:
		penalty = 0
	if speed <= penalty:
		return 0
	else:
		return speed - penalty

def calcAvoid(character, )

