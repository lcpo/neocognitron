

class Location(object):

	def __init__(self, plane, x, y):
		self.plane = plane
		self.x = x
		self.y = y

	def getPlane(self):
		return self.plane

	def getPoint(self):
		return (self.x, self.y)

	def setPoint(self, x, y):
		self.x = x
		self.y = y

	def getX(self):
		return self.x

	def getY(self):
		return self.y