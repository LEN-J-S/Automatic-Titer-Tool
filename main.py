import serial
import time

# Configuration
SERIAL_PORT = 'COM5'  
BAUD_RATE = 115200    

# Defined positions These values are the x and y coordinates for the replacement tips.
X_P = 136.30 # Location of 4th replacement tip
Y_P = 215.4
# Defined positions These values are the x and y coordinates for the well plate.
X_W = 136.30 # Location of 4th well plate
Y_W = 123.00 #


# Function starts sending commands to printer
def send_gcode_command(ser, command):
    ser.write(f"{command}\n".encode())
    print(f"Sent command: {command}")
    time.sleep(3)  # Delay to prevent crashes

# Dispense base solution into well plate (has liquid already in the pump)
def well_plate(ser, x, y):
    send_gcode_command(ser, "G0 Z67.00") # Move up before traveling
    send_gcode_command(ser, f"G0 X{x} Y{y} F5000") # Move to well plate
    send_gcode_command(ser, "G0 Z51.00") # Lower pipette
    send_gcode_command(ser, "G1 E40.00 F1000") # Dispense liquid
    send_gcode_command(ser, "G0 Z67.00") # Move up after dispensing

# Funtion to move pump to replacement tips and pick them up
def pit_refill(ser, x, y):
    send_gcode_command(ser, "G0 Z67.00")  # Moves pump up to prevent crashing
    send_gcode_command(ser, f"G0 X{x} Y{y} F5000") # Moves to specified row of new pipett tips
    send_gcode_command(ser, "G0 Z04.00") # Moves down to pick up tip
    #send_gcode_command(ser, "G0 Z15.00") # Moves up a bit
    #send_gcode_command(ser, "G0 Z05.00") # Moves down to pick up tip

    send_gcode_command(ser, f"G0 X{x+1} Y{y} F5000") # Moves to specified row of new pipett tips
    send_gcode_command(ser, f"G0 X{x-2} Y{y} F5000") # Moves to specified row of new pipett tips
    send_gcode_command(ser, f"G0 X{x} Y{y} F5000") # Moves to specified row of new pipett tips

    send_gcode_command(ser, f"G0 X{x} Y{y+1} F5000") # Moves to specified row of new pipett tips
    send_gcode_command(ser, f"G0 X{x} Y{y-2} F5000") # Moves to specified row of new pipett tips
    send_gcode_command(ser, f"G0 X{x} Y{y} F5000") # Moves to specified row of new pipett tips

    #send_gcode_command(ser, "G0 Z10.00") # Moves up a bit
    #send_gcode_command(ser, "G0 Z05.00") # Moves down to pick up tip
    send_gcode_command(ser, "G0 Z83.00") # Moves up to standard height
    # send_gcode_command(ser, "G0 X37.00 Y212.00 F5000")# Goes to Pit Remover to level each tip
    # send_gcode_command(ser, "G0 Z32.00 F5000") # levels each tip
    # send_gcode_command(ser, "G0 Z83.00") # Moves back up

# Funtion to move pump to tip remover area
def pit_removal(ser):
    send_gcode_command(ser, "G0 Z67.00") # Goes to standard height
    send_gcode_command(ser, "G0 X-5.00 F5000") # Moves all the way to the left
    send_gcode_command(ser, "G0 Y212.00 F5000") # Moves all the way upt to the tip remover corner
    send_gcode_command(ser, "G0 Z18.70 F5000") # Positions itself at the appropriate height of the tip remover
    send_gcode_command(ser, "G0 X33.00") # Slides right into tip remove
    send_gcode_command(ser, "G0 Z39.00") # Pulls up, letting the tips fall out
    #send_gcode_command(ser, "G0 Z67.00") # Return to standard height

# Function to pipett the final sample into the petri dish
def petri_dish(ser):
    send_gcode_command(ser, "G0 Z67.00") # Return to standard height
    send_gcode_command(ser, "G1 E-30.00 F1000") # Move pump up for buffer area
    send_gcode_command(ser, "G0 Z41.00") # Moves pipett tip down to well plate
    send_gcode_command(ser, "G1 E-34.00 F1000") # Pipett 10% sample
    send_gcode_command(ser, "G0 Z67.00") # Return to standard height
    send_gcode_command(ser, "G0 X60 Y102.00") # Goes to petridish area
    send_gcode_command(ser, "G0 Z10.00") # Lowers pump closer to petri dish
    send_gcode_command(ser, "G1 E50.00 F1000") # Pumps sample into dish
    #send_gcode_command(ser, "G0 Z67.00") # Return to standard height

# Extract base solution from container
def solution(ser):
    send_gcode_command(ser, "G0 Z83.00") # Return to standard height
    send_gcode_command(ser, "G0 X69.30 Y159.00 F5000") # goes to the location of the base
    send_gcode_command(ser, "G1 E-55.00 F1000") # lift pump to create buffer area to keep extruder motor from crashing while pumping
    send_gcode_command(ser, "G0 Z20.00") # Lowers pipett tip into container
    send_gcode_command(ser, "G1 E-25.00 F1000") # pump out little extra air
    send_gcode_command(ser, "G1 E-65.00 F1000") # extracts buffer from container
    send_gcode_command(ser, "G0 Z52.00") # Return to standard height
    send_gcode_command(ser, "G1 E-67.00 F1000") # sucks in little more to prevent liquid from dripping out

def mixing(ser, x, y):
    send_gcode_command(ser, "G0 Z70.00") # Return to standard height
    send_gcode_command(ser, f"G0 X{x} Y{y} F5000") # Move to designated rown and column of well plate
    send_gcode_command(ser, "G1 E-30.00 F1000") # Move pump up to create buffer area
    send_gcode_command(ser, "G0 Z41.50") # Move pipett tip down to well height
    send_gcode_command(ser, "G1 E-34.00 F1000") # Proceeds to extract and pump 3 times, mixing the solution
    send_gcode_command(ser, "G1 E-28.00 F1000")
    send_gcode_command(ser, "G1 E-32.00 F1000")
    send_gcode_command(ser, "G1 E-25.00 F1000")
    send_gcode_command(ser, "G1 E-32.00 F1000")
    send_gcode_command(ser, "G1 E0.00 F1000") # Dispense back all the solution into well plate


#transfers solution from previous row to next row
def transfer(ser,x,a,b):
    send_gcode_command(ser, "G0 Z53.00") # goes slightly above the well plate
    send_gcode_command(ser, f"G0 X{x} Y{a} F5000") # goes to the specified well plate location
    send_gcode_command(ser, "G1 E-30.00 F1000") # pumps down to create buffer
    send_gcode_command(ser, "G0 Z41.50") # goes to same well plate level
    send_gcode_command(ser, "G1 E-40.00 F1000") # pipette liquid slowly
    send_gcode_command(ser, "G0 Z55.00") # goes up
    send_gcode_command(ser, f"G0 X{x} Y{b} F1000") # goes to the next well plate row
    #send_gcode_command(ser, "G0 Z40.50") # lowers down to the well plate
    send_gcode_command(ser, "G1 E50.00 F1000") # pipettes liquid out slowly
    send_gcode_command(ser, "G0 Z67.00")



def main():
    try: # Trying to establish connection to printer. If it doesnt work, prints out error message.
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            print("Connected to printer")

            send_gcode_command(ser, "M302 S0") # Enables cold extrusion. Allows us to use extruder motor for the pump.
            send_gcode_command(ser, "M500") # Save settings to printer.
            print("Heat bed is OFF")
            print("Printer is homing")
            send_gcode_command(ser, "G28") # Homes all axes of printer.
           
           
            print("Homing extruder")
            send_gcode_command(ser, "G1 E-220.00 F5000")  # Move extruder up by 270 mm
            send_gcode_command(ser, "G1 E.210 F5000")  # Move extruder down by 270 mm
            time.sleep(15)

            print("Printer is now ready for tasking")
           
            iterations = int(input("Enter number of iterations: ")) #how many rows do we want to dilute?
            parallels = int(input("Enter number of parallel samples: ")) #how many samples do we want to dilute?
           
            # G1 X136.9
            # G1 X127.9
            # G1 X118.9
            # G1 X109.9

            x_p = 109.9 # x location of first pipette tip
            x_w = 109.9 # x location of first well plate

            X_P = x_p + 9 * (parallels - 1) # Location of 4th replacement tip
            # Defined positions These values are the x and y coordinates for the well plate.
            X_W = x_w + 9 * (parallels - 1) # Location of 4th well plate

           
            pit_refill(ser, X_P, Y_P) # goes to get the first set of tips

            # Fills the wells with buffer. Starts at the last row and ends at the first row
            for i in range(iterations, 0, -1): # starts at #ofiterations, ends at 0, incroments by -1
                print(f"Iteration {i}") # prints the current row it is on
                y_well_plate = Y_W-((i-1)*9) # increases the Y-distance, which moves up by one row. i is the current row we are on
                solution(ser) # uses function to extract buffer from container
                well_plate(ser, X_W, y_well_plate) # uses fuction to dispense buffer into well plate.              
           
            # after well plates are filled with buffer, it's going to mix and transfer the solution to next row (repeats)
            for j in range(iterations, 0, -1): # starts at #ofiterations, ends at 0, incroments by -1

               
                y_well_plate = Y_W-(abs(j-iterations)*9) # decreases the Y-distance, which moves down by one row. i is the current row we are on
                mixing(ser, X_W, y_well_plate) # Uses mixing function to mix the solution in the current well

                #y_well_plate = Y_P-(((iterations+1)-j)*9) # calculates the next row to move to
               
               
               
                # If we still haven't finished serial dilution yet
                if j!=1:
                    y_c = Y_W-(abs((j-1)-iterations)*9) #calculating the next row
                    transfer(ser,X_W,y_well_plate,y_c) # Function that transfers sample from previous row to next row
                    pit_removal(ser) # Moves pump tip remover and remove tips      
                    y_tip_refill = Y_P-(((iterations+1)-j)*9)    
                    pit_refill(ser, X_P, y_tip_refill) # Goes to the next set of fresh tips.
                   
                # If we are on the last row of the well plate
                if j==1:
                    petri_dish(ser) # at the last row, pipetts sample into petri dish.
                    pit_removal(ser) # removes contaminated tips.

            send_gcode_command(ser,"G0 X-5.00 Y199.00 Z60.00") # pushes bed to front to access petri dish

            print("Program Complete")

    except serial.SerialException as e:
        print(f"SerialException: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
