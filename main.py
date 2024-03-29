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
INIT_RAMP_SPEED = 10
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
# Stepper
dpiStepper = DPiStepper()
microstepping = 8
dpiStepper.setMicrostepping(microstepping)

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
    staircaseSpeed = 40
    rampSpeed = INIT_RAMP_SPEED

    # USE THREADING
    # THREAD THREAD THREAD

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.initialize()

    def toggleGate(self):
        print("Open and Close gate here")
        threading.Thread(target=self.toggleGateThread).start()

    def toggleStaircase(self):
        print("Turn on and off staircase here")
        threading.Thread(target=self.toggleStaircaseThread).start()

    def toggleRamp(self):
        print("Move ramp up and down here")
        threading.Thread(target=self.toggleRampThread).start()

    def auto(self):
        print("Run through one cycle of the perpetual motion machine")
        self.initialize()
        sleep(.01)
        self.runSensors()
    def setRampSpeed(self, speed):
        print("Set the ramp speed and update slider text")
        
    def setStaircaseSpeed(self, speed):
        print("Set the staircase speed and update slider text")
        
    def initialize(self):
        print("Close gate, stop staircase and home ramp here")
        self.closeGate()
        self.stopStairs()
        self.rampDown()

    def resetColors(self):
        self.ids.gate.color = PINK
        self.ids.staircase.color = PINK
        self.ids.ramp.color = PINK
        self.ids.auto.color = BLUE

# ////////////////////////////////////////////////////////////////
# //                       MAIN FUNCTIONS                       //
# //             SHOULD INTERACT DIRECTLY WITH HARDWARE         //
# ////////////////////////////////////////////////////////////////
# ///////////// gate things //////////////
    def openGate(self):
        i = 0
        servo_number = 1
        for i in range(100):
            dpiComputer.writeServo(servo_number, i)
            sleep(.03)
    def closeGate(self):
        i = 0
        servo_number = 1
        for i in range(100, 0, -1):
            dpiComputer.writeServo(servo_number, i)
            sleep(.02)
    def toggleGateThread(self):
        global OPEN
        if OPEN == False:
            OPEN = True
            print("a")
            self.ids.gate.text = 'Close Gate'
            self.openGate()
        else:
            OPEN = False
            self.ids.gate.text = 'Open Gate'
            self.closeGate()
            print("b")
# ///////////// stair shtuff //////////////
    def toggleStaircaseThread(self):
        global ON
        if ON == False:
            ON = True
            print("moving stairs")
            self.ids.staircase.text = 'Staircase Off'
            self.moveStairs()
        else:
            ON = False
            self.ids.staircase.text = 'Staircase On'
            self.stopStairs()
            print("stopped stairs")
    def moveStairs(self):
        i = 0
        servo_number = 0
        for i in range(100, 0, -1):
            dpiComputer.writeServo(servo_number, i)
            sleep(.1)
    def stopStairs(self):
        servo_number = 0
        dpiComputer.writeServo(servo_number, 90)
        sleep(.2)
# ///////////// ramp ///////////////
    def toggleRampThread(self):
        print("ramp threading fn")
        global HOME
        if HOME == True:
            HOME = False
            print("moving stairs")
            self.rampUp()
            self.ids.ramp.text = 'move down'
        else:
            HOME = True
            self.rampDown()
            self.ids.ramp.text = 'go up'
    def rampUp(self):
        stepper_num = 0
        dpiStepper.enableMotors(True)
        dpiStepper.setBoardNumber(0)
        # set stepper number & enable motors
        gear_ratio = 1
        motorStepPerRevolution = 1600 * gear_ratio
        dpiStepper.setStepsPerRevolution(stepper_num, motorStepPerRevolution)
        # set steps per rev
        dpiStepper.setCurrentPositionInRevolutions(stepper_num, 0)

        speed_in_revolutions_per_sec = int(self.ids.rampSpeed.value)
        dpiStepper.setSpeedInRevolutionsPerSecond(stepper_num, speed_in_revolutions_per_sec)
        accel_in_revolutions_per_sec_per_sec = 2.0
        dpiStepper.setAccelerationInRevolutionsPerSecondPerSecond(stepper_num, accel_in_revolutions_per_sec_per_sec)
        # set position and speed and accel
        dpiStepper.moveToAbsolutePositionInRevolutions(0, -28.7, waitToFinishFlg=True)
        dpiStepper.enableMotors(False)
        print("up")
    def rampDown(self):
        dpiStepper.enableMotors(True)
        speed_in_steps_per_sec = 5500 #self.ids.rampSpeed.value
        MaxDistanceToMoveInSteps = 46000
        dpiStepper.moveToHomeInSteps(0, 1, speed_in_steps_per_sec, MaxDistanceToMoveInSteps)
        dpiStepper.enableMotors(False)
        print("moved down")

    # def rampSpeed
    #     speed_in_steps_per_sec = int(self.ids.rampSpeed.value)
# ///////////////// auto fn & sensors ///////////
    def runSensors(self):
        self.bottomSensor()
        # self.topSensor()
    def bottomSensor(self):
        value = dpiComputer.readDigitalIn(dpiComputer.IN_CONNECTOR__IN_0)
        dpiComputer.writeDigitalOut(dpiComputer.OUT_CONNECTOR__OUT_2, value)
        blah = 0
        while blah < 3:
            blah + 1
            if (dpiComputer.readDigitalIn(dpiComputer.IN_CONNECTOR__IN_0)):
                sleep(8)
                if (dpiComputer.readDigitalIn(dpiComputer.IN_CONNECTOR__IN_0)):  # a little debounce logic
                    print("Input 0 is HIGH")
            else:
                print("Input 0 is LOW")
                self.rampUp()
                self.moveStairs()
                self.rampDown()
                self.stopStairs()
                self.openGate()
                self.closeGate()
        if blah == 3:
            print("no ball found. put one in and try again")
    def topSensor(self):
        value = dpiComputer.readDigitalIn(dpiComputer.IN_CONNECTOR__IN_1)
        dpiComputer.writeDigitalOut(dpiComputer.OUT_CONNECTOR__OUT_2, value)
        while True:
            if (dpiComputer.readDigitalIn(dpiComputer.IN_CONNECTOR__IN_1)):
                sleep(.5)
                if (dpiComputer.readDigitalIn(dpiComputer.IN_CONNECTOR__IN_1)):  # a little debounce logic
                    print("Input 1 is HIGH")
            else:
                print("Input 1 is LOW")
                threading.Thread(target=self.moveStairs).start()


    def quit(self):
        print("Exit")
        MyApp().stop()

sm.add_widget(MainScreen(name = 'main'))

# ////////////////////////////////////////////////////////////////
# //                          RUN APP                           //
# ////////////////////////////////////////////////////////////////

MyApp().run()
