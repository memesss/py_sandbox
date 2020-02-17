import threading
import queue
import serial
import time


txqueueLock = threading.Lock()
rxqueueLock = threading.Lock()

txQueue = queue.Queue(10)
rxQueue = queue.Queue(10)
serial = serial.Serial(port = "COM7", baudrate=9600, timeout = 1)
EndTaskString = "QUIT"
##################################################################
##################################################################
class RXThread (threading.Thread):
  
  def __init__(self, name):
    threading.Thread.__init__(self)
    self.name = name  
  def run(self):
    print (serial)
    print ("Starting " + self.name)
    while True:
        if not rxQueue.empty():
          rxqueueLock.acquire()
          msg = rxQueue.get()
          rxqueueLock.release()
          if EndTaskString in msg:
            break
        else:
          data = serial.readline()
          print (str(data))
    serial.close()
    print ("Exiting " + self.name)
##################################################################
class TXThread (threading.Thread):
  
  def __init__(self, name):
    threading.Thread.__init__(self)
    self.name = name
    self.stop = False
  def run(self):
    print ("Starting " + self.name)
    
    while not self.stop:
      txqueueLock.acquire()
      
      while not txQueue.empty():
          item_to_send = txQueue.get()
          if EndTaskString not in item_to_send:
            serial.write(item_to_send)
          else:
             self.stop = True
      txqueueLock.release()
    
    print ("Exiting " + self.name)
##################################################################
class keyboard_Thread (threading.Thread):
  def __init__(self, name):
    threading.Thread.__init__(self)
    self.name = name
    self.stop = False       
  def run(self):
    print ("Starting " + self.name)
    while not self.stop:
   
      outdata = input("Type ")
      print ("You Typed %s" %outdata)
      
      if EndTaskString in outdata:
        self.stop = True
        print ("Exiting " + self.name)
        
        #signal the RX thread the EndTaskString
        rxqueueLock.acquire()
        rxQueue.put(outdata)
        rxqueueLock.release()
      ###queue EndTaskString anyway 
      txqueueLock.acquire()
      txQueue.put(outdata) 
      txqueueLock.release()
        



# Create new threads
RX = RXThread("RX-Thread")
TX = TXThread("TX-Thread")
Keyboard = keyboard_Thread("Keyboard-Thread")

# Start new Threads

TX.start()
RX.start()
Keyboard.start()

Keyboard.join()
