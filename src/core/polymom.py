class Polymom(object):
	MIN_SIZE = 20
	MAX_SIZE = 50

	def __init__(self, canvas, vertices_count):
		self.growing = True
		self.canvas = canvas
		self.vertices_count = vertices_count
		self.counter = self.MIN_SIZE

	def live(self):
		if self.counter == self.MAX_SIZE and self.growing:
			self.growing = False

		elif self.counter == self.MIN_SIZE and not self.growing:
			self.growing = True

		self.counter += 1 if self.growing else -1

	def get_coordinates(self):
		cw = round(200 / 2)
		ch = round(200 / 2)
		self.live()
		d = round(self.counter / 2)
		return [cw - d, ch - d, cw + d, ch + d]

	def draw(self):
		self.canvas.delete('all')
		self.canvas.create_oval(self.get_coordinates(), fill='black')

	def draw_poly(self):
		self.canvas.delete('all')
		coords = self.get_coordinates()
		points = [
			coords[0], coords[1],
			coords[2], coords[1],
			coords[2], coords[3],
			coords[0], coords[3],
			coords[0], coords[1]
		]
		self.canvas.create_polygon(points, fill='black', smooth=True, outline='', splinesteps=self.counter * 12)
