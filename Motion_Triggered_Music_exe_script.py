import RPi.GPIO as GPIO
import os,random
import time
from time import sleep
from random import randrange
import shutil

GPIO.setmode(GPIO.BCM)
GPIO_PIR = 7
#Set pin as input
GPIO.setup(GPIO_PIR,GPIO.IN)

Current_State = 0
Previous_State = 0
music_src = "/media/pi/GL_Drive/music/"
music_dst = "/media/pi/GL_Drive/played/"
        
def ransong():
#Pick randomly and play a song from /media/pi/GL_Drive/music/
    a = os.listdir(music_src)
    random_index = randrange(0,len(a))
    a = a[random_index]
    print "Now playing: " + a
    os.system('omxplayer -o local '+ music_src + str(a))
    return a

def changefolder(song):
#Move the previously played song to folder "played"
    src = music_src + str(song)
    dst = music_dst
    shutil.move(src,dst)

def renamefiles(pth):
#There are some characters that "confuse" the str() built in method.
#This method renames all the .mp3 files removing those characters.    
        lista = os.listdir(pth)
        for name in lista:
                newname = name.translate(None," ';()&")
                os.rename(pth+name,pth+newname)
                #print newname
        return "done"

    

try:
    print("Waiting for PIR to settle...")
    

    #Loop unitl PIR output is 0
    while GPIO.input(GPIO_PIR)==1:
        Current_State = 0

    renamefiles(music_src)
    	
    print(" Ready")

    #Loop until user quits with CTRL-C
    while True:

        #Read PIR State
        Current_State = GPIO.input(GPIO_PIR)
	#print Current_State


        if Current_State==True and Previous_State==False:
            print(" Motion detected!")
            Previous_State=True
            if os.listdir(music_src)==[]:
                print "Refreshing the song pool"
                os.rename(music_src,"/media/pi/GL_Drive/tmp/")
                os.rename(music_dst,music_src)
                os.rename("/media/pi/GL_Drive/tmp/",music_dst)
                print "Refresh completed"
            else:
                a = ransong()
                changefolder(a)
        elif Current_State==False and Previous_State==True:
            print("\n---------- Waiting for motion ----------\n")
            Previous_State=False
	    time.sleep(0.2)
	    
except KeyboardInterrupt:
    print(" Quit")
    #Reset GPIO settings





