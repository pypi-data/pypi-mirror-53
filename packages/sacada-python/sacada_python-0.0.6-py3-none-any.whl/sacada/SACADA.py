from serial import Serial
from thermocouples_reference import thermocouples

class InvalidChannel(Exception):
    pass

class InvalidOption(Exception):
    pass

class SACADA(object):

    """SACADA boards Python interface
       Right now it just implements support for SACADA Mini using SCPI
       over USB-CDC. The plan is to provide a generic base class for use
       with all SACADA boards.
    """

    IN_CHANNELS = ["A0", "A1", "A2", "A3", "A4", "INSTR", "TC"]
    OUT_CHANNELS = ["CH1", "CH2"]

    def __init__(self, location):
        self.open(location)
        self._zero = 0

    def open(self, location):
        self._serial = Serial(location, timeout=1) # We use USB-CDC so baud rate doesn't matter

    def close(self):
        self._serial.close()

    def identify(self):
        return self.sendSCPICommand("*IDN?")

    def sendSCPICommand(self, command):
        self._write(command + "\r\n") # SACADA Mini requires \r\n at the end of commands
        return self._read()

    def readVoltage(self, channel):
        if channel not in self.IN_CHANNELS:
            raise InvalidChannel("{} is not a valid input channel".format(channel))

        return float(self.sendSCPICommand("MEAS:VOLT:DC? {}".format(channel)))

    def setVoltage(self, channel, voltage):
        if channel not in self.OUT_CHANNELS:
            raise InvalidChannel("{} is not a valid output channel".format(channel))

        return float(self.sendSCPICommand("SET:VOLT:DC {} {}".format(channel, voltage)))

    def readTemperature(self, tref, _type='R'):
        voltage = self.readVoltage("TC")
        return thermocouples[_type].inverse_CmV((voltage - self._zero)*1000, Tref=tref)

    def zero(self, samples=5):
        # Take the average of a few measurements
        average = 0
        for i in range(samples): # Arbitrary
            average += self.readVoltage("TC")
        self._zero = average/samples
        return self._zero

    def _write(self, m):
        self._serial.write(bytes(m, "utf-8"))

    def _read(self):
        return self._serial.readline().strip()
