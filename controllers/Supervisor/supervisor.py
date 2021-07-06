import sys
sys.path.append('../')

import random
from controller import Supervisor
from const import parameter

def calc_elaspsed_time(step, timestep):
    elapsed_time = ((step/1000)*timestep)/60
    return elapsed_time

supervisor = Supervisor()
parameter = parameter()

log_mode = parameter.data_log_mode
random_mode = parameter.random_disturbance_mode

fluid_node = supervisor.getFromDef("STILL_WATER") # type Node
stream_vel = fluid_node.getField("streamVelocity") # type Field

step = 0
min_duration = parameter.duration # duration time[minutes]
total_step = parameter.total_step
timestep = parameter.TIME_STEP
display_mode = parameter.state_display_mode

x_strength = [0.1, 0.2, 0.3, 0.4, 0.5, -0.1, -0.2, -0.3, -0.4, -0.5]
z_strength = [0.1, 0.2, 0.3, 0.4, 0.5, -0.1, -0.2, -0.3, -0.4, -0.5]

count = 0
play_count = 0

""""
if log_mode == True:
    import csv
    import datetime
    now = datetime.datetime.now()
    str_date = now.strftime("%Y%m%d%H%M")
    filename = "./disturbance/" + str_date  + "disturbance.csv"
    f = open(filename, 'a', newline='')
    csvWriter = csv.writer(f)
    csvWriter.writerow(['step', 'x', 'z'])
"""
while supervisor.step(timestep) != 1:
    if step % (total_step/10) == 0:
        if random_mode == True:
            x = round(random.uniform(-0.5, 0.5), 2)
            z = round(random.uniform(-0.5, 0.5), 2)
        elif random_mode == False:
            x = x_strength[count]
            z = z_strength[count]
            count = count + 1
        if count == len(x_strength):
            count = 0
            play_count = play_count + 1
            if play_count == 6:
                break
        """"
        if log_mode==True:
            csvWriter.writerow([step, x, z])
            print("Complete disturbance log")
            f.close()
        if count == len(x_strength):
            break
        """
        st_vel = [x, 0.0, z]
        stream_vel.setSFVec3f(st_vel)

    if step == total_step-1:
        # pause the smulation
        # supervisor.simulationSetMode(-1)
        pass

    if display_mode:
        step_label = "STEP: " + str(step+1) + "/" + str(total_step)
        elapsed_time = round(calc_elaspsed_time(step, timestep), 2)
        time_label = "Elapsed time: " + str('{:.2f}'.format(elapsed_time)) + "/" + str(min_duration) + "[min]"
        supervisor.setLabel(1, step_label, 0.5, 0.1, 0.1, 0x00FF00, 0, "Arial")
        supervisor.setLabel(2, time_label, 0.5, 0.2, 0.1, 0x00FF00, 0, "Arial")

        disturbance_label = "Disturbance[X, Z]: " + str(x) + ", " + str(z)
        supervisor.setLabel(3, disturbance_label, 0.5, 0.3, 0.1, 0x00FF00, 0, "Arial")
    
    step += 1
