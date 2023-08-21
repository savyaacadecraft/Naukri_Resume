from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException

import traceback
from inputimeout import inputimeout, TimeoutOccurred

from os import mkdir, path, system
from time import sleep


def getGmailPin(engine):
    OTP = None
    
    main_handle = engine.current_window_handle
    engine.switch_to.new_window()
    sleep(5)
    
    engine.get('https://mail.google.com')
    
    searchBox = WebDriverWait(engine, 10).until(EC.element_to_be_clickable((By.XPATH, '//input[contains(@placeholder, "Search in mail")]')))
    searchBox.click()
    sleep(1)
    searchBox.send_keys("Authorization code for suspicious high Resdex usage")
    sleep(2)
    searchBox.send_keys(Keys.RETURN)

    sleep(5)
    try:
        WebDriverWait(engine, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[7]/div[3]/div/div[2]/div[5]/div/div/div/div/div[2]/div/div[1]/div/div[3]/div[5]/div[1]/div/table/tbody/tr"))).click()
    except Exception as E:
        print("Exception While Loading....")    
        engine.get('https://mail.google.com')
    
        searchBox = WebDriverWait(engine, 10).until(EC.element_to_be_clickable((By.XPATH, '//input[contains(@placeholder, "Search in mail")]')))
        searchBox.click()
        sleep(1)
        searchBox.send_keys("Authorization code for suspicious high Resdex usage")
        sleep(2)
        searchBox.send_keys(Keys.RETURN)

    sleep(5)
    otp_elements = engine.find_elements(By.XPATH, "//td[contains(@style, 'font-family:Tahoma,Geneva,sans-serif;font-size:16px;font-weight:bold;color:#47739f;text-decoration:none;line-height:30px;text-align:center')]")
    for i in otp_elements:
        OTP = i.text
    sleep(2)

    engine.close()
    engine.switch_to.window(main_handle)

    print("OTP is ", OTP)
    sleep(3)

    engine.find_element(By.XPATH, "//input[contains(@class, '__input')]").send_keys(OTP)
    print("OTP inserted...")
    sleep(3)

    engine.find_element(By.XPATH, "//button[contains(text(), 'Verify')]").click()
    sleep(1)
    
def captchaByPass(engine):
    iframe_element = engine.find_element(By.XPATH, "//iframe[contains(@title, 'reCAPTCHA')]")
    engine.switch_to.frame(iframe_element)
    sleep(2)

    engine.find_element(By.ID, "recaptcha-anchor").click()
    print("Captcha Button is Clicked...")

    sleep(3)
    try:
        WebDriverWait(engine, 1).until(EC.visibility_of_element_located((By.CLASS_NAME, "captcha")))
        input("Enter Captcha: ")
    except TimeoutOccurred:
        print("Captcha Pass")
    engine.switch_to.default_content()

    sleep(4)

def resumeDownload(engine):
    try:
        try:
            # Searching for Attached CV Clickable Text
            WebDriverWait(engine, 1).until(EC.element_to_be_clickable((By.XPATH, "//div[contains( text(), 'Attached CV')]"))).click()

        except Exception:

            # Searching for CV & Video Profile Clickable Text
            WebDriverWait(engine, 1).until(EC.element_to_be_clickable((By.XPATH, "//div[contains( text(), 'CV & video profile')]"))).click()
        try:
            # Clicking on Download Resume Button
            WebDriverWait(engine, 1).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/div[1]/div/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div[1]/div[2]/a"))).click()
        except Exception as E:
            pass

    except Exception as E:
        resumeDownload(engine)
    
def getProfiles(engine, Profile_list, URL):

    engine.get(URL)
    sleep(4)

    LIMIT = False
    LIMITING_VALUE = 0
   
    last_page = engine.find_element(By.CLASS_NAME, "page-value").text
    last_page = int(last_page.split(" ")[3])
    
    for j in range(last_page):
        
        try:
            WebDriverWait(engine, 0.5).until(EC.visibility_of_element_located((By.XPATH, "//div[contains( text(), 'Authorization for CV Download/Movement')]")))
            print("OTP validation happened during data collection")
            sleep(1)
            getGmailPin(engine)
        except TimeoutException as T:
            pass

        except Exception as E:
            traceback.print_exc()
            print("Exception - OTP DC: ", E)

            pass

        try:
            WebDriverWait(engine, 0.5).until(EC.visibility_of_element_located((By.CLASS_NAME, "captcha")))
            engine.get(i)
            print("Captcha Found")
            sleep(1)
            captchaByPass(engine)
            print("Test Passed")
        except TimeoutException as T:
            pass

        except Exception as E:
            # print("Captcha Exception: ", E)
            pass
        

        for i in engine.find_elements(By.CLASS_NAME, "tuple-card "):
            try:

                if i.find_element(By.CLASS_NAME, "arrow-icon"):
                    continue
            except Exception as E:
                if len(Profile_list) < LIMITING_VALUE:
                    Profile_list.add(i.find_element(By.CLASS_NAME, "candidate-name").get_attribute("href"))
                else:
                    LIMIT = True
                    break
        
        if LIMIT: break

        try:
            WebDriverWait(engine, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div/div[1]/div/div[3]/div/div[2]/div/div[1]/div[2]/div[2]/button[3]"))).click()
            sleep(0.3)

        except TimeoutException as T:
            pass

        except StaleElementReferenceException as STE:
            try:
                WebDriverWait(engine, 10).until(EC.element_to_be_clickable((By.XPATH, "//Button[contains(@data-testid, 'next-page')]"))).click()
                sleep(0.3)
                pass
            except Exception as E:
                traceback.print_exc()
                pass

        except Exception as E:
            traceback.print_exc()
            print("****")
            print(E)
            pass

    
    Profile_list = list(Profile_list)
    print("Count of Profile: ", len(Profile_list))

    file = open("X_Remaining_Profile.txt", "w")
    file.write("\n".join(Profile_list))
    
    

    while len(Profile_list):
        try:
            i = Profile_list.pop()
            engine.get(i)

            try:
                WebDriverWait(engine, 1).until(EC.visibility_of_element_located((By.XPATH, "//div[contains( text(), 'Authorization for CV Download/Movement')]")))
                print("OTP validation happened during resume downloading")
                sleep(1)
                getGmailPin(engine)

            except TimeoutException as T:
                pass

            except Exception as E:
                print("Exception - OTP RD: ", E)
                traceback.print_exc()
                pass


            try:
                WebDriverWait(engine, 0.5).until(EC.visibility_of_element_located((By.CLASS_NAME, "captcha")))
                engine.get(i)
                print("Captcha Found")
                sleep(1)
                captchaByPass(engine)
                print("Test Passed")

            except TimeoutException as T:
                pass

            except Exception as E:
                traceback.print_exc()
                print("Captcha Exception: ", E)
                pass

            resumeDownload(engine)

        except KeyboardInterrupt as KE:
            file.write("\n".join(Profile_list))
            file.close()

        except Exception as E:
            traceback.print_exc()
            file.write("\n".join(Profile_list))
            file.close()
            

def downloadFromFile(engine, i):
        engine.get(i)

        try:
            WebDriverWait(engine, 1).until(EC.visibility_of_element_located((By.XPATH, "//div[contains( text(), 'Authorization for CV Download/Movement')]")))
            print("OTP validation happened during resume downloading")
            sleep(1)
            getGmailPin(engine)

        except TimeoutException as T:
            pass
        except Exception as E:
            print("Exception - OTP RD: ", E)
            pass
        
        try:
            WebDriverWait(engine, 1).until(EC.visibility_of_element_located((By.CLASS_NAME, "captcha")))
            engine.get(i)
            print("Captcha Found")
            sleep(1)
            captchaByPass(engine)
            print("Test Passed")

        except TimeoutException as T:
            pass

        except Exception as E:
            pass

        resumeDownload(engine)


if __name__ == "__main__":

    PROFILE_URL = ""
    
    Profile_list = set()

    profile = "Paid Marketing Manager"
    
    options = webdriver.ChromeOptions()
    options.add_experimental_option("debuggerAddress", "localhost:9999")

    service = Service(ChromeDriverManager().install())

    engine = webdriver.Chrome(service=service, options=options)
    engine.maximize_window()
    print("Operation Started--------")
    
    try:
        getProfiles(engine, Profile_list, PROFILE_URL)
    except Exception as E:
        traceback.print_exc()
        print("Main Function: ", E)
        
            
        if not path.isdir(i.replace(" ", "_")):
            mkdir(i.replace(" ", "_"))
    
        system(f"mv ~/Downloads/Naukri_* ~/Desktop/ACADECRAFT/Naukari_Data/{profile.replace(' ', '_')}/")

    engine.quit()
