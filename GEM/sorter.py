__author__ = 'Administrator'
import json
#####################################################
class circle():
	def __init__(self,plist,um_per_pxX,um_per_pxY):
		self.X 		= (plist[0] + 100500) * um_per_pxX
		self.Y 		= 	plist[1] * um_per_pxY
		self.radius		= plist[2] * um_per_pxY
		self.corearea	= plist[3]
		
	def getX (self):
		return self.X
	def getY (self):
		return self.Y
	def getradius (self):
		return self.radius
	def getcorearea (self):
		return self.corearea
	def getdistance(self,othercircle):
		return (sqrt ( (self.X - othercircle.X)^2 + (self.Y - othercircle.Y)^2) )
	def getXdistance(self,othercircle):
		return abs(self.X - othercircle.X)
	def getYdistance(self,othercircle):
		return abs(self.Y - othercircle.Y)
		
#####################################################
um_per_pxX = 218.0 / 1510.0
um_per_pxY = 212.0 / 1446.0
closeby_pixel_search_xdist_um_max = 55.0
closeby_pixel_search_xdist_um_min = 30.0 

path = 'V:/GEM_FM2_422/'
#####################################################
def build_circle_list():
	file_in = open(path + "circles.mrg", 'r')
	datain = file_in.read()
	circles = json.loads(datain)
	file_in.close()
	circle_list = []
	for entry in circles:
		circle_list.append(circle (entry,um_per_pxX,um_per_pxY))
	return circle_list
	
if (__name__ == "__main__") :
	
	xbin_width_um = 100 
	xmax_um		  = 15000
	
	ybin_width_um = 45 
	ymax_um		  = 15000
	
	circle_list = build_circle_list()

	print ("found " + str(len(circle_list)) + " circles")
	
	
	#############################################################################
	XBinsBounds = range (0, xmax_um, xbin_width_um)
	radiusXbins=[]
	for bin in range (0, len(XBinsBounds), 1):
		radiusXbins.append ([])
	
	YBinsBounds = range (0, ymax_um, ybin_width_um)
	radiusYbins=[]
	for bin in range (0, len(YBinsBounds), 1):
		radiusYbins.append ([])
		

	circles_slice = []
	for circle in circle_list:
		if(circle.Y > YBinsBounds [10] and circle.Y < YBinsBounds [11]):
			circles_slice.append(circle)
	print("X Slicing found %d circles:" %(len (circles_slice)))
	#############################################################################
	for circle in circles_slice:
		
		for i in range (0, len(XBinsBounds) - 1, 1):
			if (circle.X > XBinsBounds [i] and circle.X < XBinsBounds [i + 1]):
				radiusXbins[i].append(circle.radius)
				break
			i = i + 1
	
	file_out = open (path + "circles_radius_avg_scanX.rep", "w")
	#############################################################################
	for Xbin in radiusXbins[:-1]: 
		group_radius_avg = 0

		for radius in Xbin:
			group_radius_avg = group_radius_avg + radius

		if (len(Xbin) > 0 ):
			group_radius_avg = group_radius_avg / len(Xbin)
		
		print ("Xgroup radius avg = " + str(group_radius_avg) )
		file_out.write("group radius avg = %.5f\n" %(group_radius_avg))
		
	file_out.close()
	#############################################################################
	pitchXbins = []
	for bin in range (0, len(XBinsBounds), 1):
		pitchXbins.append( [] )
	#############################################################################
			
	print("X Pitch Analysis:")
	for i in range (0, len(XBinsBounds) - 1, 1):
		
		for pivot_circle in circles_slice:
			for closeby_pixel in circles_slice:
				tempxdist = closeby_pixel.getXdistance(pivot_circle)
				if( tempxdist<= closeby_pixel_search_xdist_um_max and tempxdist > closeby_pixel_search_xdist_um_min and pivot_circle.X > XBinsBounds [i] and pivot_circle.X < XBinsBounds [i + 1]):
					pitchXbins[i].append(tempxdist)
		print("Bin[%d] (%d,%d) found %d pitches" %(i,XBinsBounds[i],XBinsBounds[i + 1], len(pitchXbins[i])) )
	
	file_out = open (path + "circles_pitch_avg_scanX.rep", "w")
	
	for pitchXbin in pitchXbins:
		pitch_avg = 0
		for pitch in pitchXbin:
			pitch_avg = pitch_avg + pitch
		if (len(pitchXbin) > 0 ):
			pitch_avg = pitch_avg / len(pitchXbin)
		print ("Xgroup pitch avg = " + str(pitch) )
		file_out.write("group pitch avg = %.5f\n" %(pitch))
		
	file_out.close()
	
	#############################################################################
	print("Y Slicing:")
	circles_slice = []
	for circle in circle_list:
		if(circle.Y > XBinsBounds [2] and circle.Y < XBinsBounds [3]):
			circles_slice.append(circle)
	#############################################################################
	for circle in circles_slice:
		
		for i in range (0, len(YBinsBounds) - 1, 1):
			if (circle.Y > YBinsBounds [i] and circle.Y < YBinsBounds [i + 1]):
				radiusYbins[i].append(circle.radius)
				break
			i = i + 1
	
	file_out = open (path + "circles_radius_avg_scanY.rep", "w")
	#############################################################################
	for Ybin in radiusYbins[:-1]: 
		group_radius_avg = 0

		for radius in Ybin:
			group_radius_avg = group_radius_avg + radius

		if (len(Ybin) > 0 ):
			group_radius_avg = group_radius_avg / len(Ybin)
		
		print ("Ygroup radius avg = " + str(group_radius_avg) )
		file_out.write("group radius avg = %.5f\n" %(group_radius_avg))
		
	file_out.close()
	#############################################################################