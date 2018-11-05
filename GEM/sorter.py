__author__ = 'Administrator'
import json
#####################################################
class circle():
	def __init__(self,plist,um_per_pxX,um_per_pxY):
		self.X 		= abs(plist[0] * um_per_pxX)
		self.Y 		= abs(plist[1] * um_per_pxY)
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
		
#####################################################
um_per_pxX = 218.0 / 1510.0
um_per_pxY = 212.0 / 1446.0
path = 'Y:/GEM0/'
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
	
	ybin_width_um = 100 
	ymax_um		  = 15000
	
	circle_list = build_circle_list()

	print ("found " + str(len(circle_list)) + " circles")
	#############################################################################
	XBinsBounds = range (0, xmax_um, xbin_width_um)
	Xbins=[]
	for bin in range (0, len(XBinsBounds), 1):
		Xbins.append ([])

	YBinsBounds = range (0, ymax_um, ybin_width_um)
	Ybins=[]
	for bin in range (0, len(YBinsBounds), 1):
		Ybins.append ([])
	#############################################################################
	for circle in circle_list:
		
		for i in range (0, len(XBinsBounds) - 1, 1):
			if (circle.X > XBinsBounds [i] and circle.X < XBinsBounds [i + 1] and circle.Y > YBinsBounds [0] and circle.Y < YBinsBounds [1]):
				Xbins[i].append(circle.radius)
				break
			i = i + 1
	
	file_out = open (path + "circles_radius_avg_scanX.rep", "w")
	#############################################################################
	for Xbin in Xbins[:-1]: 
		group_radius_avg = 0

		for radius in Xbin:
			group_radius_avg = group_radius_avg + radius

		group_radius_avg = group_radius_avg / len(Xbin)
		
		print ("Xgroup radius avg = " + str(group_radius_avg) )
		file_out.write("group radius avg = %.5f\n" %(group_radius_avg))
		
	file_out.close()
	#############################################################################
	
	
	#############################################################################


	for circle in circle_list:
		
		for i in range (0, len(YBinsBounds) - 1, 1):
			if (circle.Y > YBinsBounds [i] and circle.Y < YBinsBounds [i + 1] and circle.Y > YBinsBounds [0] and circle.Y < YBinsBounds [1]):
				Ybins[i].append(circle.radius)
				break
			i = i + 1
	
	file_out = open (path + "circles_radius_avg_scanY.rep", "w")
	#############################################################################
	for Ybin in Ybins[:-1]: 
		group_radius_avg = 0

		for radius in Ybin:
			group_radius_avg = group_radius_avg + radius

		group_radius_avg = group_radius_avg / len(Ybin)
		
		print ("Ygroup radius avg = " + str(group_radius_avg) )
		file_out.write("group radius avg = %.5f\n" %(group_radius_avg))
		
	file_out.close()
	#############################################################################