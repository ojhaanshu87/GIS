''' 
There Were three kind of Distrotion while capturing the Image :

Roll : Flight turn left or right movement
Pitch : Head up and down movement
Yaw : Head left and right movement

In this script the calculation of off-nadir or nadir angle based on YPR data.

LIMITATIONS : 

since, this script is missing parameters like satellite tilt angle (t), 
scan angle (n), and height (H), so calculation may vary, in next commit, will recover it.
'''

import csv
import math
import numpy as np

class Solution (object):

	def __init__(self, roll, pitch, yaw):
		self.roll = roll
		self.pitch = pitch
		self.yaw = yaw

	def calculation (self):
	    #Base case, if roll and pitch both 0 then nadir
	    if self.roll==0.0 and self.pitch==0.0:
	        return 0
	    #otherwise not at nadir
	    else:
			#standred roll matrix
			roll_matrix = np.matrix([
				[1, 0, 0],
				[0, math.cos(self.roll), -math.sin(self.roll)],
				[0, math.sin(self.roll), math.cos(self.roll)]
				])

			#standred yaw matrix
			yaw_matrix = np.matrix([
				[math.cos(self.yaw), -math.sin(self.yaw), 0],
				[math.sin(self.yaw), math.cos(self.yaw), 0],
				[0, 0, 1]
				])

			#standred pitch matrix
			pitch_matrix = np.matrix([
				[math.cos(self.pitch), 0, math.sin(self.pitch)],
				[0, 1, 0],
				[-math.sin(self.pitch), 0, math.cos(self.pitch)]
				])
	        #general reversal law of Transpose matrix
			multiplication_factor = roll_matrix * yaw_matrix * pitch_matrix 

		    #new nadir angle
			theta = math.acos(((multiplication_factor[0, 0] + multiplication_factor[1, 1] + multiplication_factor[2, 2]) - 1) / 2)
			#azimuthal angle 
			multi = 1 / (2 * math.sin(theta))

			rx = multi * (multiplication_factor[2, 1] - multiplication_factor[1, 2]) * theta
			ry = multi * (multiplication_factor[0, 2] - multiplication_factor[2, 0]) * theta
			rz = multi * (multiplication_factor[1, 0] - multiplication_factor[0, 1]) * theta

			return theta

with open("/path/to/csv/file/*.csv", 'rb') as csv_file:

	file_reader = csv.reader(csv_file, delimiter=',', quotechar='|')
	#skip the headers
	next(file_reader, None)
	#Ignore above line if you have directly roll, pitch and yaw in Order without header.
	for row in file_reader:
		solution = Solution(float(row[0]), float(row[1]), float(row[2]))
		print solution.calculation()