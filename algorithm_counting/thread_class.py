from threading import Thread
import dect_fire
import threading 
import os

class worker(Thread):
    
    def __init__(self, room_num):
        Thread.__init__(self)   
        self.room_num = room_num       
    
    def run(self):           
        th = dect_fire.process(self.room_num)       
          
status = True 
room_list = ["hall", "room512", "room529"]

while True:
    try:
        if status == True:
            for i in room_list:
                w = worker(i)
                p = w.start() 
            
            #check the list of thread  
            for thread in threading.enumerate():
                print("**************", thread.name)  
                
            status = False

    except KeyboardInterrupt:
        os.kill(os.getpid(),2)