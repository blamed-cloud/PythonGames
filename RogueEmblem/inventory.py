#!/user/bin/env python3
#inventory.py

class Inventory(object):

	maxItems = 8

	def __init__(self, items, equipped = True):
		assert len(items) <= Inventory.maxItems
		self.items = items
		self.equipped = True

	def __len__(self):
		return len(self.items)

	def __getitem__(self, i):
		return self.items[i]

	def swap(self, i, j):
		temp = self.items[i]
		self.items[i] = self.items[j]
		self.items[j] = temp

	def replace(self, i, item):
		temp = self.items[i]
		self.items[i] = item
		return temp

	def trade(self, i, other, j):
		assert isinstance(other, Inventory)
		thisItem = self.items[i]
		self.items[i] = other.replace(j, thisItem)

	def toggleEquipped(self):
		self.equipped = not self.equipped

	def isEquipped(self):
		return self.equipped

	def getEquippedItem(self):
		return self.items[0]


