import re, sys, time
import httplib, urllib
from threading import Thread
from gui import *

class Auther:
    def __init__(self, username='', password=''):
        self.username = username
        self.password = password
        self.host = ''

    def authenticate(self):
        "Attempts to authenticates, indicates success."
        try:
            params  = urllib.urlencode(dict(fname="wba_login",
                                            username=self.username,
                                            key=self.password))
            conn = httplib.HTTPSConnection(self.host)
            conn.request("POST", "/aaa/kmutt3.html", params,
                         {'Accept': 'text/html',
                          'Host': self.host,
                          'Content-Type': 'application/x-www-form-urlencoded'})
            return "Now connecting" in conn.getresponse().read()
        except:
            return False

    def watchdog(self, host='www.kmutt.ac.th'):
        "Checks if Internet requires authentication, returns host if needed."
        try:
            conn = httplib.HTTPConnection(host)
            conn.request("GET", "/", None,
                         {'Accept': 'text/html',
                          'Host': host})
            response = conn.getresponse()
            if response.status == 302: # authentication required
                match = re.search(r"wx[A-Za-z0-9]+\.kmutt.ac.th",
                                  dict(response.getheaders())['location'])
                if match:
                    self.host = match.group(0)
                    return self.host
                else: # normal operation
                    return True
            else: # normal operation
                return True
        except: # connection failure
            return False

class Monitor(Thread):
    def __init__(self, *args, **kwargs):
        Thread.__init__(self, *args, **kwargs)
        self.daemon = True
        self.start()

    def run(self):
        while True:
            win.update_status("Checking...")
            status = auth.watchdog()
            if status == False:
                win.update_status("Not Connected", 'off')
                time.sleep(15)
            elif status == True:
                win.update_status("Connected", 'on')
                time.sleep(60)
            else:
                win.popup("Logging on to KMUTT WiFi...", "Please wait while you are being authenticated.")
                win.update_status("Logging on...", 'off')
                while not auth.authenticate():
                    time.sleep(3)
                win.popup("You are now logged on", "You can start browsing the Internet normally.")
                win.update_status("Connected", 'on')
                time.sleep(30)

auth = Auther()
win = Window(auth)
mon = Monitor()
sys.exit(app.exec_())
