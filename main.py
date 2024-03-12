# ////////////////////////////////////////////////////////////////
# //                     IMPORT STATEMENTS                      //
# ////////////////////////////////////////////////////////////////
import math
import sys
import time
import threading

from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import *
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.slider import Slider
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock
from kivy.animation import Animation
from functools import partial
from kivy.config import Config
from kivy.core.window import Window
from pidev.kivy import DPEAButton
from pidev.kivy import PauseScreen
from time import sleep
from dpeaDPi.DPiComputer import *
from dpeaDPi.DPiStepper import *

# ////////////////////////////////////////////////////////////////
# //                     HARDWARE SETUP                         //
# ////////////////////////////////////////////////////////////////
"""Stepper Motor goes into MOTOR 0 )
    Limit Switch associated with Stepper Motor goes into HOME 0
    One Sensor goes into IN 0
    Another Sensor goes into IN 1
    Servo Motor associated with the Gate goes into SERVO 1
    Motor Controller for DC Motor associated with the Stairs goes into SERVO 0"""


# ////////////////////////////////////////////////////////////////
# //                      GLOBAL VARIABLES                      //
# //                         CONSTANTS                          //
# ////////////////////////////////////////////////////////////////
ON = False
OFF = True
HOME = True
TOP = False
OPEN = False
CLOSE = True
PINK = 1, 0.3, 0.5, 1
BLUE = 0, 0, 1, 1
DEBOUNCE = 0.1
INIT_RAMP_SPEED = 2
RAMP_LENGTH = 725


# ////////////////////////////////////////////////////////////////
# //            DECLARE APP CLASS AND SCREENMANAGER             //
# //                     LOAD KIVY FILE                         //
# ////////////////////////////////////////////////////////////////
class MyApp(App):
    def build(self):
        self.title = "Perpetual Motion"
        return sm

Builder.load_file('main.kv')
Window.clearcolor = (.1, .1,.1, 1) # (WHITE)



# ////////////////////////////////////////////////////////////////
# //                    SLUSH/HARDWARE SETUP                    //
# ////////////////////////////////////////////////////////////////
sm = ScreenManager()

# SERVO
dpiComputer = DPiComputer()
dpiComputer.initialize()


# ////////////////////////////////////////////////////////////////
# //                       MAIN FUNCTIONS                       //
# //             SHOULD INTERACT DIRECTLY WITH HARDWARE         //
# ////////////////////////////////////////////////////////////////

# ////////////////////////////////////////////////////////////////
# //        DEFINE MAINSCREEN CLASS THAT KIVY RECOGNIZES        //
# //                                                            //
# //   KIVY UI CAN INTERACT DIRECTLY W/ THE FUNCTIONS DEFINED   //
# //     CORRESPONDS TO BUTTON/SLIDER/WIDGET "on_release"       //
# //                                                            //
# //   SHOULD REFERENCE MAIN FUNCTIONS WITHIN THESE FUNCTIONS   //
# //      SHOULD NOT INTERACT DIRECTLY WITH THE HARDWARE        //
# ////////////////////////////////////////////////////////////////
class MainScreen(Screen):

    staircaseSpeedText = '0'
    rampSpeed = INIT_RAMP_SPEED
    staircaseSpeed = 40


    # USE THREADING
    # THREAD THREAD THREAD

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.initialize()

    def toggleGate(self):
        print("Open and Close gate here")
        self.openGate()
        self.closeGate()


    def toggleStaircase(self):
        print("Turn on and off staircase here")
        
    def toggleRamp(self):
        print("Move ramp up and down here")
        
    def auto(self):
        print("Run through one cycle of the perpetual motion machine")
        
    def setRampSpeed(self, speed):
        print("Set the ramp speed and update slider text")
        
    def setStaircaseSpeed(self, speed):
        print("Set the staircase speed and update slider text")
        
    def initialize(self):
        print("Close gate, stop staircase and home ramp here")

    def resetColors(self):
        self.ids.gate.color = PINK
        self.ids.staircase.color = PINK
        self.ids.ramp.color = PINK
        self.ids.auto.color = BLUE

    def openGate(self):
        i = 1
        servo_number = 1
        for i in range(100, 0, -1):
            dpiComputer.writeServo(servo_number, i)
            sleep(.05)
    def closeGate(self):
        i = 1
        servo_number = 1
        for i in range(100, 0, -1):
            dpiComputer.writeServo(servo_number, i)
            sleep(.05)


    
    def quit(self):
        print("Exit")
        MyApp().stop()

sm.add_widget(MainScreen(name = 'main'))

# ////////////////////////////////////////////////////////////////
# //                          RUN APP                           //
# ////////////////////////////////////////////////////////////////

MyApp().run()
