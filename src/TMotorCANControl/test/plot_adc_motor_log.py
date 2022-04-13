from cProfile import label
from matplotlib import pyplot as plt
import csv
import numpy as np
from scipy.signal import butter, lfilter, freqz

def butter_lowpass(cutoff, fs, order=5):
    return butter(order, cutoff, fs=fs, btype='low', analog=False)

def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y

time = []
torque_command = []
torque_adc = []
torque_motor = []
current_motor = []
speed_motor = []

test_dir= "saved_logs/"
<<<<<<< HEAD
log_dir="torque_performance_max_curr/"
name="log_adc_and_motor_no_comp"
# log_dir="torque_lower_baud_rate/"
# name="log_adc_and_motor_recalibrated"
=======
log_dir="no_torque_tests/"
name="no_torque_training_data"
>>>>>>> 88cc3d9a3222ec80c76bf6794eeaf61376b116de

with open(test_dir + log_dir + name + ".csv",'r') as fd:
    reader = csv.reader(fd)
    i = 0
    for row in reader:
        if i > 1:
            time.append(float(row[0]))
            torque_command.append(float(row[1]))
            torque_adc.append(float(row[2]))
            torque_motor.append(float(row[3]))
            current_motor.append(float(row[4]))
            speed_motor.append(float(row[5]))
        i += 1

torque_motor = np.array(torque_motor)
current_motor = np.array(current_motor)
torque_adc = np.array(torque_adc)

kt_Tmotor = 0.091
kt_actual = 0.11
kt_dephy = 0.142
gr = 9

current_qaxis = (current_motor)*(1/np.sqrt(2))

torque_adc_adjusted = -1*torque_adc

current_adc = torque_adc_adjusted/(kt_actual*gr)
current_factor = 1.2 # current_motor/current_adc
print(np.average(current_factor))
current_qaxis = current_qaxis/current_factor
og_torque = current_qaxis*kt_actual*gr

order = 6
fs = 1/0.01       # sample rate, Hz
cutoff = 10.0  # desired cutoff frequency of the filter, Hz

torque_adc_filtered = butter_lowpass_filter(torque_adc_adjusted, cutoff, fs, order).reshape(-1,)

# torque_adc_filtered = np.array(torque_adc_filtered)


print("Average τ_adc: " + str(np.average(torque_adc_filtered)))
print("Std Dev τ_adc: " + str(np.std(torque_adc_filtered)))
print("Max τ_adc: " + str(torque_adc_filtered.max()))

print("Average τ_motor: " + str(np.average(torque_motor)))
print("Std Dev τ_motor: " + str(np.std(torque_motor)))
print("Max τ_motor: " + str(torque_motor.max()))

# current_motor = current_motor/1.56

print("Average i_motor: " + str(np.average(current_motor)))
print("Std Dev i_motor: " + str(np.std(current_motor)))
print("Max i_motor: " + str(current_motor.max()))



# plt.subplot(2, 1, 1)
# plt.plot(np.array(time),torque_adc_adjusted.flatten(),label="τ_adc_raw (max: " + str(round(torque_adc_adjusted.max(),2)) + "Nm)")
plt.plot(time,og_torque,label="τ_motor (max: "+ str(round(og_torque.max(),2)) + "Nm)")
# plt.plot(time,og_torque,label="τ_unadjusted (max: "+ str(round(og_torque.max(),2)) + "Nm)" )
# plt.plot(np.array(time),speed_motor,label="v")
plt.plot(np.array(time),current_qaxis,label="i_q (max: " + str(round(current_qaxis.max(),2)) + "A)")
plt.plot(np.array(time),torque_adc_filtered,label="τ_adc (max: " + str(round(torque_adc_filtered.max(),2)) + "Nm)")
plt.plot(np.array(time),current_adc,label="i_q (max: " + str(round(current_adc.max(),2)) + "A)")
plt.title('Torque vs Time')
plt.ylabel('Torque [Nm]')
plt.xlabel('Time [s]')
plt.grid(True)
plt.legend()

plt.show()

plt.savefig(test_dir + log_dir + name + "1" + ".png")
# plt.clf()

Kt = 0.146*9
time = np.array(time)
# current_motor = current_motor[time < 12]
# torque_adc_filtered = torque_adc_filtered[time < 12]
# print(np.mean(current_motor - torque_adc_filtered))


