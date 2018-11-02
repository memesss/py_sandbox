__author__ = 'Administrator'
import json
#####################################################
class circle():
	def __init__(self,plist):
		self.X 		= plist[0]
		self.Y 		= plist[1]
		self.radius		= plist[2]
		self.corearea	= plist[3]
#####################################################
def build_circle_list():
	file_in = open("circles_merge.txt", 'r')
	datain = file_in.read()
	circles = json.loads(datain)
	file_in.close()
	circle_list = []
	for entry in circles:
		circle_list.append(circle (entry))
	return circle_list

if (__name__ == "__main__") :
	circle_list = build_circle_list()

	print ("found " + str(len(circle_list)) + "circles")

	circle_group0=[]
	circle_group1=[]
	circle_group2=[]
	circle_group3=[]
	circle_group4=[]
	circle_group5=[]

	for circle in circle_list:
		if ( circle.X > 0 and circle.X < 1701):
			circle_group0.append(circle.radius)
		if ( circle.X > 1701 and circle.X < 3376):
			circle_group1.append(circle.radius)
		if ( circle.X > 3376 and circle.X < 5077):
			circle_group2.append(circle.radius)
		if ( circle.X > 5077 and circle.X < 6779):
			circle_group3.append(circle.radius)
		if ( circle.X > 6779 and circle.X < 8480):
			circle_group4.append(circle.radius)
		if ( circle.X > 8480):
			circle_group5.append(circle.radius)

	group0_radius_avg = 0

	for radius in circle_group0:
		group0_radius_avg = group0_radius_avg + radius

	group0_radius_avg = group0_radius_avg / len(circle_group0)
	print ("group0 radius avg = " + str(group0_radius_avg) )

	group1_radius_avg = 0

	for radius in circle_group1:
		group1_radius_avg = group1_radius_avg + radius

	group1_radius_avg = group1_radius_avg / len(circle_group1)
	print ("group1 radius avg = " + str(group1_radius_avg) )

	group2_radius_avg = 0

	for radius in circle_group2:
		group2_radius_avg = group2_radius_avg + radius

	group2_radius_avg = group2_radius_avg / len(circle_group2)
	print ("group2 radius avg = " + str(group2_radius_avg) )

	group3_radius_avg = 0

	for radius in circle_group3:
		group3_radius_avg = group3_radius_avg + radius

	group3_radius_avg = group3_radius_avg / len(circle_group3)
	print ("group3 radius avg = " + str(group3_radius_avg) )

	group4_radius_avg = 0

	for radius in circle_group4:
		group4_radius_avg = group4_radius_avg + radius

	group4_radius_avg = group4_radius_avg / len(circle_group4)
	print ("group4 radius avg = " + str(group4_radius_avg) )

	group5_radius_avg = 0

	for radius in circle_group5:
		group5_radius_avg = group5_radius_avg + radius

	group5_radius_avg = group5_radius_avg / len(circle_group5)
	print ("group5 radius avg = " + str(group5_radius_avg) )