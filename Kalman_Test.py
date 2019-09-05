import pandas 
import plotly.graph_objects as graph
import numpy as np


DF = pandas.read_csv('SKYPILOT_BODY_2019.csv', encoding = 'ISO-8859-1')
for i in list(DF):
	pandas.to_numeric(DF[i])


#if you wanna see that shit
#fig = graph.Figure(data = graph.Scatter(x = DF['Time (ms)'], y = DF['Our - Altitude (m)'], mode = 'markers'))
#fig.show()
def calcuate_angle(angular_velocity, time, angle):
	return angular_velocity*time + angle

#helper list, change these based off titles 
A = ['Accel X', 'Accel Y', 'Accel Z']
G = ['Gyro X', 'Gyro Y', 'Gyro Z']


#for logging calculated alttitude for comparison, currently just doing accelration 
Alt_raw= list()
Alt_kal = list()
time_stamp = list()

Accel_x = np.zeros(len(DF.index))

#Values run through the kalman filter, x,y,z
Accel_n = np.zeros(3)
Gyro_n = np.zeros(3)


#Kalman gain, x,y,z respectively
K_Accel = np.zeros(3)
K_Gyro = np.zeros(3)

#Covariance, x,y,z, idfk with the initializations
P_Accel = np.full(3, 10)
P_Gyro = np.full(3, 10)


r_Accel = 4
r_Gyro = 1

#initialize kalman gain
for i in range(0,2):
	K_Accel[i] = P_Accel[i]/(P_Accel[i]+r_Accel) 
	K_Gyro[i] = P_Gyro[i]/(P_Gyro[i]+r_Gyro)
#initial values 
Accel_n[0] = DF.at[0, 'Accel X']
Accel_n[1] = DF.at[0, 'Accel Y']
Accel_n[2] = DF.at[0, 'Accel Z']

Gyro_n[0] = DF.at[0, 'Gyro X']
Gyro_n[1] = DF.at[0, 'Gyro Y']
Gyro_n[2] = DF.at[0, 'Gyro Z']


for i, rows in DF.iterrows():
	if int(DF.at[i, 'State']) > 1 and int(DF.at[i, 'State']) <4:
		for j in range(0,2):
			#fuck with the process noise
			P_Accel[j] = P_Accel[j] + 1.5
			K_Accel[j] = P_Accel[j]/(P_Accel[j] + r_Accel)
			Accel_n[j] = Accel_n[j] + K_Accel[j]*(DF.at[i, A[j]] - Accel_n[j])
			P_Accel[j] = (1-K_Accel[j])*P_Accel[j]
		time_stamp.append(DF.at[i, 'Time (ms)'])
		Alt_raw.append(DF.at[i, 'Accel Y'])
		Alt_kal.append(Accel_n[1])



#graph accel y comprisons
fig = graph.Figure()
fig.add_trace(graph.Scatter(x = time_stamp, y = Alt_raw, mode = 'markers', name = 'RAW'))
fig.add_trace(graph.Scatter(x = time_stamp, y = Alt_kal, mode = 'lines+markers', name = 'Kalman'))

fig.show()
