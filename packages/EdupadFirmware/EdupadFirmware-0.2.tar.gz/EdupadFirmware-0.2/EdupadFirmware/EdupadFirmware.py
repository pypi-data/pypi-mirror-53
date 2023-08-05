# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 17:08:27 2019

@author: Skills Cafe
"""




from threading import Timer
import serial
import requests
import time
import pyttsx3
import speech_recognition as sr

import vlc
# import EmailTest

#variable for SMS function
global response
global Auth_Key1

#for VideoOnPointer
vid_count=0
defaultPath="Videos/"
prev_media=vlc.MediaPlayer()
prev_pointer=0
media_flag="not"
prev_card=0

media=vlc.MediaPlayer()

#for VideoOnCard
media_card=vlc.MediaPlayer()
vid_count_card=0
prev_media_card=vlc.MediaPlayer()
prev_card=0
media_flag_card="not"

media_jump=vlc.MediaPlayer()
prevVideoName="none"
#def serialInit(PortName):


SendData = list("&[$000000000000000000000000000000000000000000000000000^")
InitializeData=list("&[>000000000000000000000000000000000000000000000000000^")
global receivedData
global data1
global data
global ser
receivedData =      ['&', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
                          '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
                          '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
                          '0', '0','0','0','0','0','0','0','0','0','0', '0',
                          '0', '0','0','0','0','0','0','0','0','0','0', '0',
                          '0', '0','0','0','0','0','0','0','0','0','0', '0',
                          '^']
receivedDataReset ='&000000000000000000000000000000000000000000000000000000000000^'
global timer
startState=0
debug1='a'

timeoutCounter=0

def init(PortName,debug='a'):
    global debug1
    global ser
    global timer
    ser = serial.Serial(timeout=1)
    ser.baudrate=9600
    ser.port=PortName
    ser.open()
    time.sleep(0.1)
    timer=RepeatTimer(0.1,Show)
    timer.start()
    debug1=debug
    return debug1


class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)

i=0
def Show():
    global SendData1
    global i
    global receivedData
    global data
    global data1
    global debug1
    global timeoutCounter


    if startState==1:
        
        str1 = ''.join(SendData)
        ser.write((str1).encode())
       # print(str1)
        ser.flush()
       # time.sleep(0.01)
        try:
            
            
           # print('in try')
            data=str((ser.read(62)))#Received Data in String
            ser.flush()
            data1=str(data)
            #print('out try')
            
            
        except:
            data1=receivedDataReset
        #data1=data
        #print (data)
        
        if('&' in data1):
            receivedData=list(data1) #Converted Data to List(Array)
            #print(receivedData)
            if(debug1=='p'):
                print(data1)
        return receivedData



def SendSMS(Channel,Number,Message):

    global response
    global Auth_Key1

    if Channel == 1:
        Auth_Key1 = "86AmSeoipQBCKcPz2l5ZU1j3XJRsabgMhYLdvDywNuqT9fGr7kJPYjaOrS50UomfLQGtd4IMgHp69R81"

    url = "https://www.fast2sms.com/dev/bulk"

    payload = "sender_id=FSTSMS&message="+":: SkillsCafe IoT :: "+ Message +"&language=english&route=p&numbers="+str(Number)

    headers = {

    'authorization': Auth_Key1,

    'Content-Type': "application/x-www-form-urlencoded",

    'Cache-Control': "no-cache"

    }
    response = requests.request("POST", url, data=payload, headers=headers)

    return response


def setPort(portNum,function):
    if function=='dRead':
        InitializeData[portNum-2]='a'
    if function=='dWrite':
        InitializeData[portNum-2]='b'
    if function=='aRead':
        InitializeData[portNum-2]='c'
    if function=='servo':
        InitializeData[portNum+4]='e'
    if function=='LED':
        InitializeData[portNum-2]='b'
        InitializeData[portNum+4]='b'


def startIO():
    global startState
    InitStr = ''.join(InitializeData)
    print(InitStr)
    ser.write((InitStr).encode())
    time.sleep(1)
    startState=1
    return startState

def ConvertSpeed(Speed,MotorNum):

    Temp1 = list(str(Speed))
    if(Speed >=100):
        if(MotorNum==1):
            SendData[42]=Temp1[0]
            SendData[43]=Temp1[1]
            SendData[44]=Temp1[2]

        if(MotorNum==2):
            SendData[45]=Temp1[0]
            SendData[46]=Temp1[1]
            SendData[47]=Temp1[2]

        if(MotorNum==3):
            SendData[48]=Temp1[0]
            SendData[49]=Temp1[1]
            SendData[50]=Temp1[2]

        if(MotorNum==4):
            SendData[51]=Temp1[0]
            SendData[52]=Temp1[1]
            SendData[53]=Temp1[2]

    if(Speed <100) and (Speed >=10) :
        if(MotorNum==1):
            SendData[42]='0'
            SendData[43]=Temp1[0]
            SendData[44]=Temp1[1]

        if(MotorNum==2):
            SendData[45]='0'
            SendData[46]=Temp1[0]
            SendData[47]=Temp1[1]

        if(MotorNum==3):
            SendData[48]='0'
            SendData[49]=Temp1[0]
            SendData[50]=Temp1[1]

        if(MotorNum==4):
            SendData[51]='0'
            SendData[52]=Temp1[0]
            SendData[53]=Temp1[1]

    if(Speed <10)  :
        if(MotorNum==1):
            SendData[42]='0'
            SendData[43]='0'
            SendData[44]=Temp1[0]

        if(MotorNum==2):
            SendData[45]='0'
            SendData[46]='0'
            SendData[47]=Temp1[0]

        if(MotorNum==3):
            SendData[48]='0'
            SendData[49]='0'
            SendData[50]=Temp1[0]

        if(MotorNum==4):
            SendData[51]='0'
            SendData[52]='0'
            SendData[53]=Temp1[0]


   # print(Temp1)



def ConvertAngle(ServoNum,Angle):

    Temp1 = list(str(Angle))
    if(Angle >=100):
        if(ServoNum==5):
            SendData[24]=Temp1[0]
            SendData[25]=Temp1[1]
            SendData[26]=Temp1[2]

        if(ServoNum==6):
            SendData[27]=Temp1[0]
            SendData[28]=Temp1[1]
            SendData[29]=Temp1[2]

        if(ServoNum==7):
            SendData[30]=Temp1[0]
            SendData[31]=Temp1[1]
            SendData[32]=Temp1[2]

        if(ServoNum==8):
            SendData[33]=Temp1[0]
            SendData[34]=Temp1[1]
            SendData[35]=Temp1[2]

        if(ServoNum==9):
            SendData[36]=Temp1[0]
            SendData[37]=Temp1[1]
            SendData[38]=Temp1[2]

        if(ServoNum==10):
            SendData[39]=Temp1[0]
            SendData[40]=Temp1[1]
            SendData[41]=Temp1[2]

    if(Angle <100) and (Angle >=10) :
        if(ServoNum==5):
            SendData[24]='0'
            SendData[25]=Temp1[0]
            SendData[26]=Temp1[1]

        if(ServoNum==6):
            SendData[27]='0'
            SendData[28]=Temp1[0]
            SendData[29]=Temp1[1]

        if(ServoNum==7):
            SendData[30]='0'
            SendData[31]=Temp1[0]
            SendData[32]=Temp1[1]

        if(ServoNum==8):
            SendData[33]='0'
            SendData[34]=Temp1[0]
            SendData[35]=Temp1[1]

        if(ServoNum==9):
            SendData[36]='0'
            SendData[37]=Temp1[0]
            SendData[38]=Temp1[1]

        if(ServoNum==10):
            SendData[39]='0'
            SendData[40]=Temp1[0]
            SendData[41]=Temp1[1]

    if(Angle <10)  :
        if(ServoNum==5):
            SendData[24]='0'
            SendData[25]='0'
            SendData[26]=Temp1[0]

        if(ServoNum==6):
            SendData[27]='0'
            SendData[28]='0'
            SendData[29]=Temp1[0]

        if(ServoNum==7):
            SendData[30]='0'
            SendData[31]='0'
            SendData[32]=Temp1[0]

        if(ServoNum==8):
            SendData[33]='0'
            SendData[34]='0'
            SendData[35]=Temp1[0]

        if(ServoNum==9):
            SendData[36]='0'
            SendData[37]='0'
            SendData[38]=Temp1[0]

        if(ServoNum==10):
            SendData[39]='0'
            SendData[40]='0'
            SendData[41]=Temp1[0]

def MotorControl(motorNum,direction,Speed):

        if(motorNum == 1 ):
            #print(str(Speed))
            if(direction=="cw") or (direction=="CW") :
               SendData[16]='0'
               SendData[17]='1'
            if(direction=="ccw") or (direction=="CCW"):

                SendData[16]='1'
                SendData[17]='0'

            if(direction=="stp") or (direction=="STP")or (direction=="STOP"):

                SendData[16]='0'
                SendData[17]='0'

            ConvertSpeed(Speed,1)

        if(motorNum == 2 ):
            #print(str(Speed))
            if(direction=="cw") or (direction=="CW") :
               SendData[18]='0'
               SendData[19]='1'
            if(direction=="ccw") or (direction=="CCW"):

                SendData[18]='1'
                SendData[19]='0'

            if(direction=="stp") or (direction=="STP")or (direction=="STOP"):

                SendData[18]='0'
                SendData[19]='0'

            ConvertSpeed(Speed,2)


        if(motorNum == 3 ):

            if(direction=="cw") or (direction=="CW") :

                 SendData[20]='0'
                 SendData[21]='1'

            if(direction=="ccw") or (direction=="CCW"):

                SendData[20]='1'
                SendData[21]='0'

            if(direction=="stp") or (direction=="STP")or (direction=="STOP"):

                SendData[20]='0'
                SendData[21]='0'

            ConvertSpeed(Speed,3)

        if(motorNum == 4 ):

                if(direction=="cw") or (direction=="CW") :

                     SendData[22]='0'
                     SendData[23]='1'

                if(direction=="ccw") or (direction=="CCW"):

                    SendData[22]='1'
                    SendData[23]='0'

                if(direction=="stp") or (direction=="STP")or (direction=="STOP"):

                    SendData[22]='0'
                    SendData[23]='0'

                ConvertSpeed(Speed,4)

def MoveServo(ServoNum,Angle):

    if(Angle>180):
        Angle=180
    if(Angle<0):
        Angle=0

    ConvertAngle(ServoNum,Angle)

def dWrite(PinNum,Val):
    if(Val==1):
            SendData[PinNum-2]='1'
    else:
            SendData[PinNum-2]='0'

def ControlLED(port,LEDNum,State):

    if(LEDNum==1):
        if(State=='ON' or State=='1' or State=='on'):
            SendData[port-2]='1' #for location 3 to 8
        if(State=='OFF' or State=='0' or State=='off'):
            SendData[port-2]='0'
    if(LEDNum==2):
        if(State=='ON' or State=='1' or State=='on'):
            SendData[port+4]='1' #for location 9 to 14
        if(State=='OFF' or State=='0' or State=='off'):
            SendData[port+4]='0'
    # if(PinNum==1):
    #     if(Val==1):
    #         SendData[3]='1'
    #     else:
    #         SendData[3]='0'
    #
    # if(PinNum==2):
    #     if(Val==1):
    #         SendData[4]='1'
    #     else:
    #         SendData[4]='0'
    #
    # if(PinNum==3):
    #     if(Val==1):
    #         SendData[5]='1'
    #     else:
    #         SendData[5]='0'
    #
    # if(PinNum==4):
    #     if(Val==1):
    #         SendData[6]='1'
    #     else:
    #         SendData[6]='0'



def RGB(Red,Green,Blue):
   Temp1 = list(str(Red))
   Temp2 = list(str(Green))
   Temp3 = list(str(Blue))
   SendData[17]='1'
   SendData[19]='1'
   SendData[21]='1'
   if(Red >=100):

            SendData[42]=Temp1[0]
            SendData[43]=Temp1[1]
            SendData[44]=Temp1[2]
   if(Green >=100):

            SendData[45]=Temp2[0]
            SendData[46]=Temp2[1]
            SendData[47]=Temp2[2]
   if(Blue >=100):

            SendData[48]=Temp3[0]
            SendData[49]=Temp3[1]
            SendData[50]=Temp3[2]

   if(Red <100) and (Red >=10) :
            SendData[42]='0'
            SendData[43]=Temp1[0]
            SendData[44]=Temp1[1]

   if(Green <100) and (Green >=10) :
            SendData[45]='0'
            SendData[46]=Temp2[0]
            SendData[47]=Temp2[1]

   if(Blue <100) and (Blue >=10) :
            SendData[48]='0'
            SendData[49]=Temp3[0]
            SendData[50]=Temp3[1]

   if(Red <10)  :
            SendData[42]='0'
            SendData[43]='0'
            SendData[44]=Temp1[0]

   if(Green <10)  :
            SendData[45]='0'
            SendData[46]='0'
            SendData[47]=Temp2[0]

   if(Blue <10)  :
            SendData[48]='0'
            SendData[49]='0'
            SendData[50]=Temp3[0]

def ReadMap():
    mapData=''.join(receivedData)
    mapID=mapData[55:63]

    if 'TINK' in mapID:
        mapID1=int(mapData[59:63])
    elif 'bbbbbbbb' in mapID:
        mapID1=int('00000000')
    else :
        mapID1=0
    
    #mapID=int(mapIDstr)
    return mapID1

def ReadCard():
    cardData=''.join(receivedData)
    cardID=cardData[47:55]

    if 'TINK' in cardID:
        cardID1=int(cardData[51:55])
       # print(cardID1)
        #cardID=int(cardIDstr)
    elif 'aaaaaaaa' in cardID:
        cardID1=int('00000000')
        #cardID=int(cardIDstr)
        
    else: 
        cardID1=0
        
    return cardID1

def ReadPointer():
    switchData=''.join(receivedData)
    switchIDstr=switchData[39:41]
    
    try:
        switchID=int(switchIDstr)
    except:
        switchID=0
    
        
    return switchID

def aRead(PinNum):
    AData=''.join(receivedData)
    if(PinNum==5):
        A1Val=int(AData[15:19])
        return A1Val
    if(PinNum==6):
        A2Val=int(AData[19:23])
        return A2Val
    if(PinNum==7):
        A3Val=int(AData[23:27])
        return A3Val
    if(PinNum==8):
        A4Val=int(AData[27:31])
        return A4Val

    if(PinNum==9):
        A5Val=int(AData[31:35])
        return A5Val

    if(PinNum==10):
        A6Val=int(AData[35:39])
        return A6Val


def dRead(PinNum):

     if(receivedData[PinNum-2]=='1'):

            return 1
     else:
            return 0
            #print(data)
def initiateVideo(VideoName):
    global defaultPath
    global media_jump
    
    media_jump=vlc.MediaPlayer(defaultPath+VideoName)
    return media_jump
            
def playVideo(VideoName):
   
    global media_jump
    global prevVideoName
    
    
    if(VideoName != prevVideoName):
        #media_jump=vlc.MediaPlayer(defaultPath+VideoName)
        media_jump.play()
        prevVideoName=VideoName
    return media_jump
    
def jumpInVideo(media,timeInSec):
    
    media.set_time(timeInSec*1000)
            
def mediaFolder(VideoPath):
    global defaultPath
    
    defaultPath=defaultPath+VideoPath
    
    return defaultPath

def videoOnPointer(VideoName,pointer=0):
            global media
            global vid_count
            global prev_media
            global prev_pointer
            global media_flag
            global media_flag_card
            global media_card
            
           # vid_count=vid_count+1
           # print(vid_count)
            
            media = vlc.MediaPlayer(defaultPath+VideoName) 
            
            if(ReadPointer()==pointer):
                
                if media_flag=='not' and prev_pointer != pointer:
                    vid_count=vid_count+1
                    if(vid_count>1):
                        prev_media.stop()
                        
#                    if media_card.is_playing():
#                        media_card.stop()
#                        print('in')
                    
                    media.play()
                    prev_pointer=pointer
                    media_flag='playing'
                    prev_media= media
                    
                    if(vid_count>100):
                        vid_count=0
            else:
                media_flag='not'
                    
#                while(ReadPointer()==0):
#                    pass
#                media.play() 
#                vid_count=vid_count+1
#                
#               
#                if(vid_count>1):
#                    prev_media.stop()
#                    
#                
#                
#                
#                prev_media= media
#               # prev_pointer=pointer
#                #vid_count=0
#                if(vid_count>100):
#                    vid_count=0
            return media,pointer
  

def videoOnCard(VideoName,card=0):
            global media_card
            global vid_count_card
            global prev_media_card
            global prev_card
            global media_flag_card
            global media
            global media_flag
            
           # vid_count=vid_count+1
           # print(vid_count)
           
            media_card = vlc.MediaPlayer(defaultPath+VideoName) 
            cardData=ReadCard()
            #print(card)
            if(cardData==card):
                #print("card matched")
                if media_flag_card=='not' and prev_card != card:
                    
                    vid_count_card=vid_count_card+1
                    if(vid_count_card>1):
                        prev_media_card.stop()
                        
#                    if media.is_playing():
#                        media.stop()
                        
                    media_card.play()
                    prev_card=card
                    media_flag_card='playing'
                    prev_media_card= media_card
                    
                    if(vid_count_card>100):
                        vid_count_card=0
            else:
                media_flag_card='not'   
                
            return media_card,card
          
def MediaClose():
    global media
    global prev_media
    media.stop()
    prev_media.stop()
    
def videoPosition(media,sec):
    position=media.get_time()
    positioninSec=int(position/1000)
    #print(positioninSec)
    if(positioninSec==sec):
        return True
    else:
        return False
        
    
def pauseVideo(media)    :
    media.pause()
      
def resumeVideo(media)    :
    media.pause()
    
def initVoiceOutput(voiceType):
    global engine
    
    engine = pyttsx3.init() # object creation

    """ RATE"""
    rate = engine.getProperty('rate')   # getting details of current speaking rate
    print (rate)                        #printing current voice rate
    engine.setProperty('rate', 125)     # setting up new voice rate
    
    
    """VOLUME"""
    volume = engine.getProperty('volume')   #getting to know current volume level (min=0 and max=1)
    print (volume)                          #printing current volume level
    engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1
    
    """VOICE"""
    voices = engine.getProperty('voices')       #getting details of current voice
    
    if voiceType=="M":
    #engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male
        engine.setProperty('voice', voices[0].id)   #changing index, changes voices. 1 for female
    if voiceType=="F":
         engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female
         
    return engine

def VoiceOutput(Text)    :
    global engine
    engine.say(Text)
    engine.runAndWait()
    return engine

def VoiceInput(vInput):
    try:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Speak:")
            audio = r.listen(source)
    
        command=r.recognize_google(audio)
        print("You said " + command )
        
        if vInput in command:
            return True
        else:
            return False
        
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
    

def close():
    global ser
    global timer
    global media
    global prev_media
    global media_card
    global prev_media_card
    global media_jump
    global engine
    
    timer.cancel()
    media.stop()
    prev_media.stop()
    media_card.stop()
    prev_media_card.stop()
    media_jump.stop()
    engine.stop()
    ser.close()

 # print(aRead(2))

#    if( dRead(3) == 1):
#        print ('Sensed')
#        dWrite(1,1)
#    else:
#         print ('Clear')
#         dWrite(1,0)

##MotorControl(2,"CW",255)
##MotorControl(1,"CCW",9)
#MoveServo(3,0)
#dWrite(1,1)
#dWrite(2,0)
#dWrite(3,1)
#dWrite(4,0)
#
#RGB(0,0,255)
