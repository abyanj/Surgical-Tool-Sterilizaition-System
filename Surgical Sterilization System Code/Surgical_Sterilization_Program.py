## ----------------------------------------------------------------------------------------------------------
## TEMPLATE
## Please DO NOT change the naming convention within this template. Some changes may
## lead to your program not functioning as intended.

import sys
import random
sys.path.append('../')

from Common_Libraries.p2_lib import *

import os
from Common_Libraries.repeating_timer_lib import repeating_timer

def update_sim ():
    try:
        arm.ping()
    except Exception as error_update_sim:
        print (error_update_sim)

arm = qarm()

update_thread = repeating_timer(2, update_sim)


## STUDENT CODE BEGINS
## ----------------------------------------------------------------------------------------------------------
## Project 2 - Robtic Arm Controller
## This program controls the movement of a robtic arm via muscle sensor input
## Davis Lenover
## lenoverd
## Abyan Jaigirdar
## jaigia1
## 12-06-2020

## Define Variables and lists
has_pickedup_item = False
waiting_on_user = True
containner_status = 0
gripper_status = 0
cage_id = 0

## Each cage id will correspond to a index slot in the list below (n-1)
## If the boolean inside is true, that means the cage has spawned before and has been put inside an autoclave container
inventory = [False, False, False, False, False, False]

## move_end_effector controls the arm given muscle inputs from the muscle sensor
## Originally written by Abyan Jaigirdar - Modified by Davis Lenover
def move_end_effector(left,right):
    global has_pickedup_item
    global containner_status
    ## First, check if both muscle sensors are between 0.05 and 0.1 and are equal to eachother
    if ((left >= 0.05 and right >= 0.05) and (left < 0.1 and right < 0.1) and (right == left)):
        # Move the arm to the pickp location
        arm.move_arm(0.4578, 0.0, 0.0424)
        has_pickedup_item = True
        
    ## Series of if statments checking muscles sensor values
    ## These values indicate where to move the arm to drop the container
    elif ((left >= 0.9 and right >= 0.9) and (right == left)): ## Large blue autoclave - 6
        ## Get the drop-off (target) location as a list for the autoclave by calling the function with the specific cage_id value (in this case 6)
        autoclave_location = get_autoclave_bin_location(6)
        ## Check if the boolean is set to True
        ## This will move the arm back to the home position without opening it's gripper (because it has the item)
        if (has_pickedup_item):
            arm.move_arm(0.4064,0,0.4826)
            time.sleep(1)
            ## Reset boolean
            has_pickedup_item = False
        ## Move the arm to the corresponding drop_off location
        arm.move_arm(autoclave_location[0], autoclave_location[1], autoclave_location[2])
        ## Set containner status variable to keep track of what process the containner is in
        ## 1 means a large containner is hovering over the target location
        containner_status = 1
        
    elif ((left >= 0.8 and right >= 0.8) and (left < 0.9 and right < 0.9) and (right == left)): ## Small red autoclave - 1
        autoclave_location = get_autoclave_bin_location(1)
        if (has_pickedup_item):
            arm.move_arm(0.4064,0,0.4826)
            time.sleep(1)
            has_pickedup_item = False
        arm.move_arm(autoclave_location[0], autoclave_location[1], autoclave_location[2])
        ## 2 means a small containner is hovering over the target location
        containner_status = 2

    elif ((left >= 0.7 and right >= 0.7) and (left < 0.8 and right < 0.8) and (right == left)): ## Large red autoclave - 4
        autoclave_location = get_autoclave_bin_location(4)
        if (has_pickedup_item):
            arm.move_arm(0.4064,0,0.4826)
            time.sleep(1)
            has_pickedup_item = False
        arm.move_arm(autoclave_location[0], autoclave_location[1], autoclave_location[2])
        containner_status = 1

    elif ((left >= 0.6 and right >= 0.6) and (left < 0.7 and right < 0.7) and (right == left)): ## Small blue autoclave - 3
        autoclave_location = get_autoclave_bin_location(3)
        if (has_pickedup_item):
            arm.move_arm(0.4064,0,0.4826)
            time.sleep(1)
            has_pickedup_item = False
        arm.move_arm(autoclave_location[0], autoclave_location[1], autoclave_location[2])
        containner_status = 2

    elif ((left >= 0.5 and right >= 0.5) and (left < 0.6 and right < 0.6) and (right == left)): ## Small green autoclave - 2
        autoclave_location = get_autoclave_bin_location(2)
        if (has_pickedup_item):
            arm.move_arm(0.4064,0,0.4826)
            time.sleep(1)
            has_pickedup_item = False
        arm.move_arm(autoclave_location[0], autoclave_location[1], autoclave_location[2])
        containner_status = 2

    elif ((left >= 0.4 and right >= 0.4) and (left < 0.5 and right < 0.5) and (right == left)): ## Large green autoclave - 5
        autoclave_location = get_autoclave_bin_location(5)
        if (has_pickedup_item):
            arm.move_arm(0.4064,0,0.4826)
            time.sleep(1)
            has_pickedup_item = False
        arm.move_arm(autoclave_location[0], autoclave_location[1], autoclave_location[2])
        containner_status = 1
        
## control_gripper controls the gripper of the arm based on muscle sensor data
## Control gripper function - Written by Abyan Jaigirdar - Modified by Davis Lenover
def control_gripper(left, right):
    ## Define both variables needed outside the function
    global containner_status
    global gripper_status
    
    ## Check the status of the gripper via an external (global variable)
    ## Checking the status avoids unwanted calls to close or open the gripper continuously
    ## Close gripper
    if (gripper_status == 0):
        if ((left < 0.5 and left >= 0.1) and (right == 0)):
            arm.control_gripper(45)
            gripper_status = 1
    if (gripper_status == 1):
        ## Open gripper
        if (left > 0.5 and right == 0):
            arm.control_gripper(-45)
            gripper_status = 0
            ## Check if the status of the containner is 2, this means that a small containner has been placed in its autoclave
            if (containner_status == 2):
                ## Set status so that the while loop knows the containner has been placed
                containner_status = 3
                
## open_autoclave_bin_controller controls the opening and closing of a specific autoclave given muscle sensor data
## Open autoclave controller function - Written by Davis Lenover and Edited by Abyan Jaigirdar      
def open_autoclave_bin_controller(left, right):
    global containner_status
    ## Check right muscle sensor to determine if the corresponding autoclave should be opened or closed
    ## Check left muscle sensor to determine if the autoclave bin should have the ability to be interacted with (i.e. it should be zero)
    ## Open Autoclave
    if (left == 0):
        ## Check specific cage_id to open correct autoclave bin
        if (right >= 0.1 and right < 0.2):
            arm.open_green_autoclave(True)
        elif (right >= 0.2 and right < 0.3):
            arm.open_red_autoclave(True)
        elif (right >= 0.4 and right < 0.5):
            arm.open_blue_autoclave(True)
    ## Close Autoclave
        elif (right >= 0.6 and right < 0.7):
            arm.open_green_autoclave(False)
            ## If the containner status was 1 and the autoclave is being closed, this means the containner is in the autoclave
            if (containner_status == 1):
            ## Change containner status to tell the while loop that the containner is in the autoclave
                containner_status = 3
        elif (right >= 0.8 and right < 0.9):
            arm.open_red_autoclave(False)
            if (containner_status == 1):
                containner_status = 3
        elif (right >= 0.9):
            arm.open_blue_autoclave(False)
            if (containner_status == 1):
                containner_status = 3
    
## Change inventory function - Written By Davis Lenover
## Change inventory changes the inventory status of the given containner in the list to true
## The inventory list allows us to keep track of which containners have been placed in bins and therefore, we do not want them to spawn again
def change_inventory(cage_id):
    inventory[cage_id-1] = True

## Get dropoff function - Written By Davis Lenover
## Function containning autoclave cords and will return them given the object (cage_id)
## Cords were found by trial and error
def get_autoclave_bin_location(cage_id):
    if (cage_id == 1): ## Red - Small
        return (-0.5516, 0.2184, 0.3932)
    elif (cage_id == 2): ## Green - Small
        return (0.0, -0.5933, 0.3932)
    elif (cage_id == 3): ## Blue - Small
        return (0.0, 0.5933, 0.3932)
    elif (cage_id == 4): ## Red - Large
        return (-0.3327, 0.1344, 0.2917)
    elif (cage_id == 5): ## Green - Large
        return (0.0, -0.3588, 0.2917)
    elif (cage_id == 6): ## Blue - Large
        return (0.0, 0.3588, 0.2917)
    else: ## Error
        print("Error, invalid dropoff location! Returning to home!")
        return (0.4064, 0.0, 0.4826)

## Get inventory function - Written by Davis Lenover and Edited by Abyan Jaigirdar     
# Function to check the inventory of each cage
def get_inventory(cage_id):
    ## Check if the inventory boolean value is true or false and return true or false based on that
    if inventory[cage_id-1] != True:
        return False
    else:
        return True

## For loop to run six times (for six different types of containers)
for i in range(6):
    ## Generate a random number (integer) between 1 and 6
    print("Generating container...")
    cage_id = random.randint(1,6)
    ## Check if the cage_id in the inventory corresponding to a index in the inventory list is equal to true
    ## This tells us that the specific container is already in it's own autoclave
    while (get_inventory(cage_id) == True):
        ## Therefore, keep re-generating a number until it's corresponding container has not been used yet
        cage_id = random.randint(1,6)
    ## Move the arm to the home position
    print("Moving home...")
    arm.home()
    time.sleep(1)
    ## Spawn the corresponding container
    arm.spawn_cage(cage_id)
    print("Container spawned, ready for pickup!")
    ## While loop to allow user input from the muslce sensors to move the arm and move the container into the correct autoclave
    while (get_inventory(cage_id) == False):
        ## If statment in place to check if the user has both muscles set to their "default position"
        ## This prevents any unwanted functions from being called while the arm is either just starting or restting
        if (waiting_on_user):
            if (arm.emg_left() < 0.05 and arm.emg_right() < 0.05):
                waiting_on_user = False
                print("Muscles are set to 0! User may now continue.")
            else:
                print("Waiting for user to reset muscles...")
        ## If the waiting on user boolean is false, then continuously call the functions to control the arm and to allow placement of the containner
        else:
            time.sleep(2)
            move_end_effector(arm.emg_left(), arm.emg_right())
            time.sleep(1)
            control_gripper(arm.emg_left(), arm.emg_right())
            time.sleep(1)
            open_autoclave_bin_controller(arm.emg_left(), arm.emg_right())
            time.sleep(1)
            ## Check if the containner was placed via a status variable
            if (containner_status == 3):
                ## Call function to change inventory status of specific cage_id (containner)
                change_inventory(cage_id)
                ## Reset containner status
                containner_status = 0
                ## Set waiting_on_user to True to avoid, again, unwanted function calls
                waiting_on_user = True
            
## Once the cage_id has returned True from the get_inventory function, this means that the container has been placed in or on the autoclave and a new container can be spawned
arm.home()
print("All containers have been placed! The program will now exit.")
exit()
