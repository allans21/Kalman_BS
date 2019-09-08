import pandas 
import plotly.graph_objects as graph
import numpy as np
import math


DF = pandas.read_csv('SKYPILOT_BODY_2019.csv', encoding = 'ISO-8859-1')
for i in list(DF):
	pandas.to_numeric(DF[i])


#if you wanna see that shit
#fig = graph.Figure(data = graph.Scatter(x = DF['Time (ms)'], y = DF['Our - Altitude (m)'], mode = 'markers'))
#fig.show()

#use a linear approximation to get the new angle 
def calculate_angle(angular_velocity_new, angular_velocity_old, delta_time, angle):
	angular_velocity_old = math.radians(angular_velocity_old)
	angular_velocity_new = math.radians(angular_velocity_new)
	slope = (angular_velocity_new - angular_velocity_old)/(delta_time/1000)
	angle_integration = (slope*angular_velocity_new**2 - slope*angular_velocity_old**2)/2
	#if abs(angular_velocity_old) > 12 and abs(angular_velocity_new) > 12:
	return angle + angle_integration
	#else: 
	#	return angle


ROLL = 0 #x
PITCH = 0 #y
YAW = 0 #z



#lists for graph 
alt = list()
time_stamp = list()
accel_z = list()


for i, rows in DF.iterrows():
	#calculate new angles
	if i > 0:
		delta_time = DF.at[i, 'Time (ms)'] - DF.at[i-1, 'Time (ms)']

		#get new angles in radians
		ROLL = calculate_angle(DF.at[i, 'Gyro X'], DF.at[i-1, 'Gyro X'], delta_time, ROLL)
		PITCH = calculate_angle(DF.at[i, 'Gyro Y'], DF.at[i-1, 'Gyro Y'], delta_time, PITCH)
		YAW = calculate_angle(DF.at[i, 'Gyro Z'], DF.at[i-1, 'Gyro Z'], delta_time, YAW)

		#Creating Rotation matrices 
		# YAW rotation
		# cosYAW, -sinYAW, 0 
		# sinYAW, cosYAW, 0
		# 0, 0, 1
		RZ = np.array([[math.cos(YAW), math.sin(YAW), 0], [math.sin(YAW), math.cos(YAW), 0], [0, 0, 1]])

		#Pitch rotation 
		# cosPitch, 0, sinPitch
		# 0, 1, 0
		# -sinPitch, 0, cosPitch 
		RY = np.array([[math.cos(PITCH), 0, math.sin(PITCH)], [0, 1, 0], [-math.sin(PITCH), 0, math.cos(PITCH)]])

		#Roll Rotation
		# 1, 0, 0
		# 0, cosRoll, -sinRoll
		# 0, sinRoll, cosRoll
		RX = np.array([[1, 0, 0], [0, math.cos(ROLL), -math.sin(ROLL)], [0, math.sin(ROLL), math.cos(ROLL)]])

		A = np.array([DF.at[i, 'Accel X'], DF.at[i, 'Accel Y'], DF.at[i, 'Accel Z']])
		#A_orient is oriented in the standard coordinate plane 
		# A_orient =  RZ RY RX A
		#R = RZ RY RX  
		#A_orient = R A
		R = np.dot(RZ, RY)
		R = np.dot(R, RX)
		A_orient = np.dot(R, A)
		if DF.at[i, 'State'] == 2 or DF.at[i, 'State'] == 3:
			time_stamp.append(DF.at[i, 'Time (ms)'])
			alt.append(DF.at[i, 'Accel Z'])
			accel_z.append(A_orient[2])
			#print(str(math.degrees(ROLL)) + '			' + str(math.degrees(PITCH)) + '		' + str(math.degrees(YAW)))
		#print(str(A_orient[2]) + '			' + str(DF.at[i, 'State']) + '			' +str(DF.at[i, 'Time (ms)']))







#graph accel y comprisons
fig = graph.Figure()
fig.add_trace(graph.Scatter(x = time_stamp, y = alt, mode = 'markers', name = 'Z accel'))
fig.add_trace(graph.Scatter(x = time_stamp, y = accel_z, mode = 'lines+markers', name = 'calculated Z accel'))

fig.show()
