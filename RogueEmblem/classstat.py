#!/user/bin/env python3
#classstat.py
from enum import Enum


class ClassStat(object):

	def __init__(self, name, cap, promotionBonus, classGrowth):
		self.name = name
		self.cap = cap
		self.promotionBonus = promotionBonus
		self.classGrowth = classGrowth

	def getName(self):
		return self.name

	def getCap(self):
		return self.cap

	def setCap(self, newCap):
		self.cap = newCap

	def increaseCap(self, amount = 1):
		self.cap += abs(amount)

	def setClassGrowth(self, cGr):
		self.classGrowth = cGr

	def getClassGrowth(self):
		return self.classGrowth

	def getPromotionBonus(self):
		return self.promotionBonus

	def setPromotionBonus(self, bonus):
		self.promotionBonus = bonus
