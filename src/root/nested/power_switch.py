import logging
import time
import requests
from requests.auth import HTTPDigestAuth
import subprocess


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
    logging.info("ADDER: Login Check")
    ret = subprocess.popen("ruby aim_login.rb")
    if ret == 0:
        pass
    else:
        logging.info("ADDER: Problem with Aim Login")
    
def aim_shutdown():
    logging.info("ADDER: Shutdown Aim")
    ret = subprocess.popen("ruby aim_shutdown.rb")
    if ret == 0:
        pass
    else:
        logging.info("ADDER: Problem with Aim Shutdown")  

def aim_restart():
    logging.info("ADDER: Restart Aim")
    ret = subprocess.popen("ruby aim_restart.rb")
    if ret == 0:
        pass
    else:
        logging.info("ADDER: Problem with Aim Restart")
    
def aim_reset():
    logging.info("ADDER: Reset Aim")
    ret = subprocess.popen("ruby aim_reset.rb")
    if ret == 0:
        pass
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
            passes += 1
            logging.info("ADDER: Exes: %d Passes: %d Fails: %d" %(execution, passes, fails))
        except Exception as e:
            fails += 1
            logging.info("ADDER: Exes: %d Passes: %d Fails: %d" %(execution, passes, fails))
        except KeyboardInterrupt:
            logging_stop()