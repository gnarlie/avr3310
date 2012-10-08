import socket
import string
from time import sleep
import re

LIMIT=135

class Avr3310:
    def __init__(self, addr, port = 23):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((addr, port))
        self.buf=[]

    def command(self, message):
        self.sock.send(message + '\r')

    def response(self):
        if len(self.buf) < 2:
            data=self.sock.recv(LIMIT)
            n = string.split(data, '\r')
            if len(self.buf) == 1:
                n[0] = self.buf[0] + n[0]
            self.buf = n

        return self.buf.pop(0).strip()

    def close(self):
        self.sock.close()

    # *** volume & mute *********
    def vol_up(self):
        self.command("MVUP")

    def vol_down(self):
        self.command("MVDOWN")

    def vol_query(self):
        self.command("MV?")
        return self.response()

    def mute(self):
        self.command("MUON");

    def unmute(self):
        self.command("MUOFF");

    def is_muted(self):
        self.command("MU?")
        return self.response() != "MUOFF"

    # *** input *** 
    def select_dvr(self):
        self.command("SIDVR")

    def select_rhapsody(self):
        self.command("SIRHAPSODY")

    def select_hdp(self):
        self.command("SIHDP")

    def select_server(self):
        self.command("SIHDP")

    def source(self):
        self.command("SI?")
        return self.response()

    # *** net screen ***
    def onscreen_display(self):
        self.command("NSE")
        ret = []
        for line in range(9):
            n = self.response()
            n = n[4:-1]
            if line != 0 and line != 8:
                # tag = n[0]
                n = n[1:-1]
            ret.append( n )
        return string.join(ret, '\n')


x = Avr3310("192.168.1.85")

#x.select_rhapsody()
#print x.source() 
print x.onscreen_display()

sleep(2)

#x.select_hdp()

x.close()
    
