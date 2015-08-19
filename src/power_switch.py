import logging
import time
import requests
from requests.auth import HTTPDigestAuth
import os
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

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

def start_driver():
    driver = webdriver.Firefox()
    wait = WebDriverWait(driver, 30)
    return driver, wait

def aim_login():
    global LOGIN_FLAG
    LOGIN_FLAG = False
    logging.info("ADDER: Login Aim")
    try:
        driver, wait = start_driver()
        driver.navigate.to("http://10.10.10.10/")
        wait.until(EC.presense_of_element_located((By.CSS_SELECTOR, "#username"))).send_keys("admin")
        wait.until(EC.presense_of_element_located((By.CSS_SELECTOR, "#password"))).send_keys("password")
        wait.until(EC.presense_of_element_located((By.CSS_SELECTOR, "#login"))).click()
        LOGIN_FLAG = wait.until(EC.presense_of_element_located((By.LINK_TEXT, "DASHBOARD"))).is_displayed()
    except Exception as e:
        logging.info("ADDER: Problem with Aim Login - Stacktrace: %s" %e)
    finally:
        driver.quit()
    # ret = os.system("ruby aim_login.rb")
    # if ret == 0:
    #     LOGIN_FLAG = True
    # else:
    #     logging.info("ADDER: Problem with Aim Login")
    
def aim_shutdown():
    global SHUTDOWN_FLAG
    SHUTDOWN_FLAG = False
    logging.info("ADDER: Login and Shutdown Aim")
    try:
        driver, wait = start_driver()
        driver.navigate.to("http://10.10.10.10/")
        wait.until(EC.presense_of_element_located((By.CSS_SELECTOR, "#username"))).send_keys("admin")
        wait.until(EC.presense_of_element_located((By.CSS_SELECTOR, "#password"))).send_keys("password")
        wait.until(EC.presense_of_element_located((By.CSS_SELECTOR, "#login"))).click()
        wait.until(EC.presense_of_element_located((By.LINK_TEXT, "DASHBOARD"))).is_displayed()
        driver.navigate.to("http://10.10.10.10/admin/process_power.php?mode=shutdown")
        time.sleep(5)
        driver.refresh()
        found = driver.find_elements((By.LINK_TEXT, "DASHBOARD"))
        if len(found) == 0:
            SHUTDOWN_FLAG = True
    except Exception as e:
        logging.info("ADDER: Problem with Aim Shutdown - Stacktrace: %s" %e)
    finally:
        driver.quit()
    # ret = os.system("ruby aim_shutdown.rb")
    # if ret == 0:
    #     SHUTDOWN_FLAG = True
    # else:
    #     logging.info("ADDER: Problem with Aim Shutdown")  

def aim_restart():
    global RESTART_FLAG
    RESTART_FLAG = False
    logging.info("ADDER: Login and Restart Aim")
    try:
        driver, wait = start_driver()
        driver.navigate.to("http://10.10.10.10/")
        wait.until(EC.presense_of_element_located((By.CSS_SELECTOR, "#username"))).send_keys("admin")
        wait.until(EC.presense_of_element_located((By.CSS_SELECTOR, "#password"))).send_keys("password")
        wait.until(EC.presense_of_element_located((By.CSS_SELECTOR, "#login"))).click()
        wait.until(EC.presense_of_element_located((By.LINK_TEXT, "DASHBOARD"))).is_displayed()
        driver.navigate.to("http://10.10.10.10/admin/process_power.php?mode=restart")
        time.sleep(20)
        driver.refresh()
        RESTART_FLAG = wait.until(EC.presense_of_element_located((By.LINK_TEXT, "DASHBOARD"))).is_displayed()
    except Exception as e:
        logging.info("ADDER: Problem with Aim Restart - Stacktrace: %s" %e)
    finally:
        driver.quit()
    # ret = os.system("ruby aim_restart.rb")
    # if ret == 0:
    #     RESTART_FLAG = True
    # else:
    #     logging.info("ADDER: Problem with Aim Restart")
    
def aim_reset():
    global RESET_FLAG
    RESET_FLAG = False
    logging.info("ADDER: Login and Reset Aim")
    try:
        driver, wait = start_driver()
        driver.navigate.to("http://10.10.10.10/")
        wait.until(EC.presense_of_element_located((By.CSS_SELECTOR, "#username"))).send_keys("admin")
        wait.until(EC.presense_of_element_located((By.CSS_SELECTOR, "#password"))).send_keys("password")
        wait.until(EC.presense_of_element_located((By.CSS_SELECTOR, "#login"))).click()
        wait.until(EC.presense_of_element_located((By.LINK_TEXT, "DASHBOARD"))).is_displayed()
        wait.until(EC.presense_of_element_located((By.LINK_TEXT, "UPDATES"))).click()
        wait.until(EC.presense_of_element_located((By.LINK_TEXT, "Reset AIM Configuration"))).click()
        wait.until(EC.presense_of_element_located((By.CSS_SELECTOR, "#confirm_reset_link"))).click()
        time.sleep(120)        
        RESET_FLAG = wait.until(EC.presense_of_element_located((By.LINK_TEXT, "DASHBOARD"))).is_displayed()
    except Exception as e:
        logging.info("ADDER: Problem with Aim Reset - Stacktrace: %s" %e)
    finally:
        driver.quit()
    # ret = os.system("ruby aim_reset.rb")
    # if ret == 0:
    #     RESET_FLAG = True
    # else:
    #     logging.info("ADDER: Problem with Aim Reset")

if __name__ == "__main__":
    logging_start()
    execution = 0
    passes = 0
    fails = 0
    while True:
        try:
            execution += 1
            send_power_on()
            time.sleep(60)
            
            aim_login()
            time.sleep(60)
            
            send_power_off()
            time.sleep(60)
            
            send_power_on()
            time.sleep(60)
            
            aim_login()
            time.sleep(60)
            
            send_power_restart()
            time.sleep(60)
            
            aim_shutdown()
            time.sleep(60)
            
            send_power_restart()
            time.sleep(60)
            
            aim_restart()
            time.sleep(60)
            
            aim_reset()
            time.sleep(60)
            
            aim_login()
            time.sleep(60)
            
            send_power_off()
            time.sleep(60)
            
            if LOGIN_FLAG and SHUTDOWN_FLAG and RESET_FLAG and RESTART_FLAG:
                passes += 1
            else:
                fails += 1
            logging.info("ADDER: Exes: %d Passes: %d Fails: %d" %(execution, passes, fails))
        except KeyboardInterrupt:
            logging_stop()
            break
