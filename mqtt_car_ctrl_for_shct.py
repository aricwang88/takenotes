import pygame
import os,sys,time,math
from socket import *
from pygame.locals import *
import _thread
import paho.mqtt.client as mqtt
import struct

CAR_CTRL_SERVER = "139.196.113.149" #"192.168.1.88"
CAR_CTRL_PORT = 1883


gUSV_speed = 0.0
gUSV_angle = 0


old_dat = ""

gForward = False
gBack = False
gLeft = False
gRight = False

sock = True

###############################################################
#Send Network Packets to Control Boat
# |<--- 4 bytes --->|<---4 bytes --->|<-1 bytes ->|
#  speed:(0.1 ~ 1.0)  angle(-90~90)   MagicWord:20 (0x14)
#
def fmt_dat(speed, angle):
    ret = None
    ret = struct.pack("!ffB", speed, angle, 20)
    return ret
    
###############################################################
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    
mqttc = mqtt.Client("python_pub")
mqttc.connect(CAR_CTRL_SERVER, CAR_CTRL_PORT)
mqttc.on_connect = on_connect

time.sleep(5.0)

def mqtt_send(cmd):
    ctl_data = "%s" % cmd
    (r,v) = mqttc.publish("/minicar/cmd", ctl_data)
    if r == 0:
        print("SENT OK")
    else:
        print("ERROR VAL:", v)
    
    mqttc.loop(2)
        
        
###############################################################


def send_data(sock, dat):
    global old_dat
    if sock and old_dat != dat:
        mqtt_send(dat.encode())
        #print("SEND CTL:", dat)
        old_dat = dat
    pass
    
old_dat_f = ""
def send_dataF(sock, dat):
    global old_dat_f
    if sock and old_dat_f != dat:
        mqtt_send(dat.encode())
        #print("SEND CTL:", dat)
        old_dat_f = dat
    pass
    
old_dat_b = ""
def send_dataB(sock, dat):
    global old_dat_b
    if sock and old_dat_b != dat:
        mqtt_send(dat.encode())
        #print("SEND CTL:", dat)
        old_dat_b = dat
    pass
    
old_dat_l = ""
def send_dataL(sock, dat):
    global old_dat_l
    if sock and old_dat_l != dat:
        mqtt_send(dat.encode())
        #print("SEND CTL:", dat)
        old_dat_l = dat
    pass
    
old_dat_r = ""
def send_dataR(sock, dat):
    global old_dat_r
    if sock and old_dat_r != dat:
        mqtt_send(dat.encode())
        #print("SEND CTL:", dat)
        old_dat_r = dat
    pass
    
def task_proc():
    global  gUSV_angle, gUSV_speed, mqttc
    
    while True:
        print("gUSV_angle=", gUSV_angle,"\tgUSV_speed=", gUSV_speed)
        
        deltaAngle = math.fabs(gUSV_angle)
        deltaSpeed = math.fabs(gUSV_speed)
        if gUSV_speed > 0.8:
            gUSV_speed = 1.0
        if gUSV_speed < -0.8:
            gUSV_speed = -1.0
        if gUSV_angle > 0.8:
            gUSV_angle = 1.0
        if gUSV_angle < -0.8:
            gUSV_angle = -1.0
        
        if deltaAngle > 0.1 or deltaSpeed > 0.1:
            ctl_data = fmt_dat(gUSV_speed, gUSV_angle)
            (r,v) = mqttc.publish("/ctrl", ctl_data)
            if r == 0:
                print("SENT OK")
            else:
                print("ERROR VAL:", v)
                mqttc.connect(CAR_CTRL_SERVER, CAR_CTRL_PORT)
                
            mqttc.loop(2)
        
        time.sleep(0.3)
    pass
    
    
class App:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Joystick 5G Mini Car Controller")

        # Set up the joystick
        pygame.joystick.init()

        self.my_joystick = None
        self.joystick_names = []

        # Enumerate joysticks
        for i in range(0, pygame.joystick.get_count()):
            self.joystick_names.append(pygame.joystick.Joystick(i).get_name())

        print(self.joystick_names)

        # By default, load the first available joystick.
        if (len(self.joystick_names) > 0):
            self.my_joystick = pygame.joystick.Joystick(0)
            self.my_joystick.init()
        else:
            print("No joystick!")
            sys.exit(0)
            
        max_joy = max(self.my_joystick.get_numaxes(), 
                      self.my_joystick.get_numbuttons(), 
                      self.my_joystick.get_numhats())

        self.screen = pygame.display.set_mode( (max_joy * 40 + 10, 170) )

        self.font = pygame.font.SysFont("Courier", 20)

    # A couple of joystick functions...
    def check_axis(self, p_axis):
        if (self.my_joystick):
            if (p_axis < self.my_joystick.get_numaxes()):
                return self.my_joystick.get_axis(p_axis)

        return 0

    def check_button(self, p_button):
        if (self.my_joystick):
            if (p_button < self.my_joystick.get_numbuttons()):
                return self.my_joystick.get_button(p_button)

        return False

    def check_hat(self, p_hat):
        if (self.my_joystick):
            if (p_hat < self.my_joystick.get_numhats()):
                return self.my_joystick.get_hat(p_hat)

        return (0, 0)

    def draw_text(self, text, x, y, color, align_right=False):
        surface = self.font.render(text, True, color, (0, 0, 0))
        surface.set_colorkey( (0, 0, 0) )

        self.screen.blit(surface, (x, y))

    def center_text(self, text, x, y, color):
        surface = self.font.render(text, True, color, (0, 0, 0))
        surface.set_colorkey( (0, 0, 0) )

        self.screen.blit(surface, (x - surface.get_width() / 2, 
                                   y - surface.get_height() / 2))

    def main(self):
        global gForward, gBack, gLeft, gRight
        global gUSV_angle, gUSV_speed
        
        while (True):
            self.g_keys = pygame.event.get()

            self.screen.fill(0)

            for event in self.g_keys:
                if (event.type == KEYDOWN and event.key == K_ESCAPE):
                    self.quit()
                    return

                elif (event.type == QUIT):
                    self.quit()
                    return

            self.draw_text("Joystick Name:  %s" % self.joystick_names[0], 
                           5, 5, (0, 255, 0))

            self.draw_text("Axes (%d)" % self.my_joystick.get_numaxes(), 
                           5, 25, (255, 255, 255))
            axis0=axis1=axis2=axis3=0
            for i in range(0, self.my_joystick.get_numaxes()):
                #print("AXIS:%d VALUE:%f" % (i, self.my_joystick.get_axis(i)))
                if i== 0:
                    #print("AXIS:%d VALUE:%f" % (i, self.my_joystick.get_axis(i)))
                    axis0 = self.my_joystick.get_axis(i)
                    gUSV_angle = axis0
                if i== 1:
                    #print("AXIS:%d VALUE:%f" % (i, self.my_joystick.get_axis(i)))
                    
                    axis1 = self.my_joystick.get_axis(i)
                    gUSV_speed = axis1
                        
                if i== 2:
                    axis2 = self.my_joystick.get_axis(i)
                        
                #print("AXIS 0: %f  1: %f, 2: %f 3: %f" % (axis0,axis1,axis2,axis3))
                
                    
                if (self.my_joystick.get_axis(i)):
                    pygame.draw.circle(self.screen, (0, 0, 200), 
                                       (20 + (i * 30), 50), 10, 0)
                else:
                    pygame.draw.circle(self.screen, (255, 0, 0), 
                                       (20 + (i * 30), 50), 10, 0)

                self.center_text("%d" % i, 20 + (i * 30), 50, (255, 255, 255))

            self.draw_text("Buttons (%d)" % self.my_joystick.get_numbuttons(), 
                           5, 75, (255, 255, 255))

            for i in range(0, self.my_joystick.get_numbuttons()):
                if (self.my_joystick.get_button(i)):
                    pygame.draw.circle(self.screen, (0, 0, 200), 
                                       (20 + (i * 30), 100), 10, 0)
                    if i == 7:
                        #send_data(sock,"FORWARD")
                        gForward = True
                    elif i== 6:
                        #send_data(sock,"BACK")
                        gBack = True
                    else:
                        pass
                else:
                    if i== 7:
                        #send_data(sock,"STOPF")
                        gForward = False
                    elif i == 6:
                        #send_data(sock,"STOPB")
                        gBack = False
                    else:
                        pass
                        
                    pygame.draw.circle(self.screen, (255, 0, 0), 
                                       (20 + (i * 30), 100), 10, 0)

                self.center_text("%d" % i, 20 + (i * 30), 100, (255, 255, 255))

            self.draw_text("POV Hats (%d)" % self.my_joystick.get_numhats(), 
                           5, 125, (255, 255, 255))

            for i in range(0, self.my_joystick.get_numhats()):
                if (self.my_joystick.get_hat(i) != (0, 0)):
                    pygame.draw.circle(self.screen, (0, 0, 200), 
                                       (20 + (i * 30), 150), 10, 0)
                else:
                    pygame.draw.circle(self.screen, (255, 0, 0), 
                                       (20 + (i * 30), 150), 10, 0)

                self.center_text("%d" % i, 20 + (i * 30), 100, (255, 255, 255))
            time.sleep(0.05)
            pygame.display.flip()

    def quit(self):
        pygame.display.quit()

_thread.start_new_thread(task_proc,(()))
app = App()
app.main()