import logging
import time
import requests
from requests.auth import HTTPDigestAuth
import os


LOGIN_FLAG = False
SHUTDOWN_FLAG = False
RESTART_FLAG = False
RESET_FLAG = False

def logging_start():
    logging.basicConfig(filename="/var/log/aim-power/result.log",
                        format="%(asctime)s:%(levelname)s:%(message)s",
                        level=logging.INFO)
    logging.info("ADDER: ==== Started Logging ====")


def logging_stop():
    logging.info("ADDER: ==== Stopped Logging ====")
    time.sleep(1)
    logging.shutdown()


def send_power_on():
    logging.info("ADDER: Power On")
    r = requests.get("http://10.10.10.254/hidden.htm?M0:O1=On", auth=HTTPDigestAuth("api", "api"))
    assert(r.status_code == 200)


def send_power_off():
    logging.info("ADDER: Power Off")
    r = requests.get("http://10.10.10.254/hidden.htm?M0:O1=Off", auth=HTTPDigestAuth("api", "api"))
    assert(r.status_code == 200)
    
def send_power_restart():
    logging.info("ADDER: Power Restart")
    r = requests.get("http://10.10.10.254/hidden.htm?M0:O1=Restart", auth=HTTPDigestAuth("api", "api"))
    assert(r.status_code == 200)

def aim_login():
    time.sleep(20)
    LOGIN_FLAG = False
    logging.info("ADDER: Login Check")
    ret = os.system("ruby aim_login.rb")
    if ret == 0:
        LOGIN_FLAG = True
    else:
        logging.info("ADDER: Problem with Aim Login")
    
def aim_shutdown():
    time.sleep(20)
    SHUTDOWN_FLAG = False
    logging.info("ADDER: Shutdown Aim")
    ret = os.system("ruby aim_shutdown.rb")
    if ret == 0:
        SHUTDOWN_FLAG = True
    else:
        logging.info("ADDER: Problem with Aim Shutdown")  

def aim_restart():
    time.sleep(20)
    RESTART_FLAG = False
    logging.info("ADDER: Restart Aim")
    ret = os.system("ruby aim_restart.rb")
    if ret == 0:
        RESTART_FLAG = True
    else:
        logging.info("ADDER: Problem with Aim Restart")
    
def aim_reset():
    time.sleep(20)
    RESET_FLAG = False
    logging.info("ADDER: Reset Aim")
    ret = os.system("ruby aim_reset.rb")
    if ret == 0:
        RESET_FLAG = True
    else:
        logging.info("ADDER: Problem with Aim Reset")

if __name__ == "__main__":
    logging_start()
    execution = 0
    passes = 0
    fails = 0
    while True:
        try:
            execution += 1
            send_power_on()
            aim_login()
            send_power_off()
            time.sleep(60)
            send_power_on()
            aim_login()
            send_power_restart()
            aim_login()
            aim_shutdown()
            time.sleep(60)
            send_power_restart()
            aim_login()
            aim_restart()
            aim_reset()
            if LOGIN_FLAG and SHUTDOWN_FLAG and RESET_FLAG and RESTART_FLAG:
                passes += 1
            else:
                fails += 1
            logging.info("ADDER: Exes: %d Passes: %d Fails: %d" %(execution, passes, fails))
        except KeyboardInterrupt:
            logging_stop()