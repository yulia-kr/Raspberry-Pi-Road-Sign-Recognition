from PipeWriter import PipeWriter
import threading
import time
import wiringpi
import cv2


# CONSTANTS
PIPE_PATH = "/tmp/mech_daemon_pipe"
SONIC_ECHO_GPIO = 24
SONIC_TRIG_GPIO = 23


class CarApi:
    def __init__(self):
        self.__initGPIO()
        self.pipeWriter = PipeWriter(PIPE_PATH)
        self.distMeasOn = False
        self.lastDistance = 0


    def __del__(self):
        self.pipeWriter.close()


    def setMotorPower(self, perc):
        """ Set motor to the given percentage <-100, 100> of its maximum power.
        Positive percentage is forward, negative is backwards, zero is power off. """
        self.pipeWriter.write("MS{0}".format(round(perc)))


    def setSteeringAngle(self, perc):
        """ Set servo to the given percentage <-100, 100> of its maximum angle.
        Positive percentage is right steering, negative is left steering, zero is center. """
        self.pipeWriter.write("SS{0}".format(round(perc)))


    def startContDistMeas(self):
        """ Start continuous distance measurement (in a separate thread).
        The measured value is accessible by calling getLastDistance(). """
        self.distMeasOn = True
        thread = threading.Thread(target=self.__distMeasWorker, daemon=True)
        thread.start()


    def stopContDistMeas(self):
        """ Stop continuous distance measurement. Its dedicated thread will stop ASAP. """
        self.distMeasOn = False


    def getLastDistance(self):
        """ Get the last value acquired by continuous distance measurement.
        It is refreshed each <0.1, 1.1> seconds. Initial value is zero (until the first measurement). """
        return self.lastDistance


    def __distMeasWorker(self):
        while self.distMeasOn:
            wiringpi.digitalWrite(SONIC_TRIG_GPIO, 1)
            time.sleep(0.00001)
            wiringpi.digitalWrite(SONIC_TRIG_GPIO, 0)
            triggered = time.time()

            while wiringpi.digitalRead(SONIC_ECHO_GPIO) == 0 and time.time() - triggered < 0.5:
                pass
            pulse_start = time.time()

            while wiringpi.digitalRead(SONIC_ECHO_GPIO) == 1 and time.time() - triggered < 1:
                pass
            pulse_end = time.time()

            pulse_duration = pulse_end - pulse_start
            self.lastDistance = pulse_duration * 17150

            time.sleep(0.1)


    def __initGPIO(self):
        # Initialize wiringpi GPIO itself
        wiringpi.wiringPiSetupGpio()

        # Setup ultrasonic pins
        wiringpi.pinMode(SONIC_ECHO_GPIO, wiringpi.GPIO.INPUT)
        wiringpi.pinMode(SONIC_TRIG_GPIO, wiringpi.GPIO.OUTPUT)
        