import sys
import tkinter as tk
import time

import maestro

"""
position_neutral = 7080
position_TIA = 6532 TIA2 = 6400
position_Gatan = 8000
"""
    
class ScanSelector(tk.Frame):
    def __init__(self, master):
        super().__init__(master, com_port='COM10')
        self.pack()

        self.com_port = com_port # COM4 for TEAM0.5_support; COM10 for OneView computer 
        
        self.button_TIA = tk.Button(text="TIA", width=25, height=5, bg="yellow",fg="black",command=self.set_TIA2)
        self.button_TIA.pack()
        
        self.button_Gatan = tk.Button(text="Gatan", width=25, height=5, bg="gray",fg="black",command=self.set_Gatan)
        self.button_Gatan.pack()
        
        self.set_TIA2()
        
    def set_TIA(self,):
        with maestro.Controller(ttyStr=self.com_port) as servo:
            position = 6532
            # 10 is a good speed
            servo.setSpeed(1, 10)

            x = servo.getPosition(1) #get the current position of servo 1
            print('Starting position = {}'.format(x))
        
            servo.setTarget(1, position)
            time.sleep(3)
            y = servo.getPosition(1) #get the current position of servo 1
            print('new position = {}'.format(y))
            
        self.button_TIA['background'] = 'yellow'
        self.button_Gatan['background'] = 'gray'
            
    def set_TIA2(self,):
        with maestro.Controller(ttyStr=self.com_port) as servo:
            position = 6400
            # 10 is a good speed
            servo.setSpeed(1, 10)

            x = servo.getPosition(1) #get the current position of servo 1
            print('Starting position = {}'.format(x))
        
            servo.setTarget(1, position)
            time.sleep(3)
            y = servo.getPosition(1) #get the current position of servo 1
            print('new position = {}'.format(y))
            
        self.button_TIA['background'] = 'yellow'
        self.button_Gatan['background'] = 'gray'
            
            
    def set_Gatan(self,):
        with maestro.Controller(ttyStr=self.com_port) as servo:
            position = 8000

            # 10 is a good speed
            servo.setSpeed(1, 10)

            x = servo.getPosition(1) #get the current position of servo 1
            print('Starting position = {}'.format(x))
        
            servo.setTarget(1, position)
            time.sleep(3)
            y = servo.getPosition(1) #get the current position of servo 1
            print('new position = {}'.format(y))
        
        self.button_Gatan['background'] = 'yellow'
        self.button_TIA['background'] = 'gray'
            
    def set_neutral(self,):
        with maestro.Controller(ttyStr=self.com_port) as servo:
            position = 7080

            # 10 is a good speed
            servo.setSpeed(1, 10)

            x = servo.getPosition(1) #get the current position of servo 1
            print('Starting position = {}'.format(x))
        
            servo.setTarget(1, position)
            
            time.sleep(3)
            
            y = servo.getPosition(1) #get the current position of servo 1
            print('new position = {}'.format(y))
            
    def set_value(self,val):
        with maestro.Controller(ttyStr=self.com_port) as servo:
            position = val

            # 10 is a good speed
            servo.setSpeed(1, 10)

            x = servo.getPosition(1) #get the current position of servo 1
            print('Starting position = {}'.format(x))
        
            servo.setTarget(1, position)
            
            time.sleep(3)
            
            y = servo.getPosition(1) #get the current position of servo 1
            print('new position = {}'.format(y))
    
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Scan selector")
    myapp = ScanSelector(root, com_port="COM10") # COM10 is for the Gatan PC
    root.iconbitmap('TIA-Gatan.ico')
    myapp.mainloop()
