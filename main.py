from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains as ac
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from usernames import USERNAME,PASSWORD,PASSWORD2
from settings import CHROME_DRIVER_PATH,DESTINATION_PATH
from report_csv import ReportToCsv




class AutomatedFormFill:

  def __init__(self,destination_path):
    options = webdriver.ChromeOptions()
    # options.binary_location = "./Applications/Google Chrome.app/Contents/MacOS/Google Chrome/bin"
    self.driver = webdriver.Chrome(CHROME_DRIVER_PATH)
    self.destination_path = destination_path

    self.status = ""






    

  def completed(self,status):
    pass


  def check_username(self):
    #username is wrong or not existing
    try:
      username_error = self.driver.find_element("id","usernameError")
      report = ReportToCsv(USERNAME,"Null","username is incorect")
      report.reporting()
    
    except:
      pass


  def check_password(self):
      password_error = self.driver.find_element("id","passwordError")
      if password_error:
        report = ReportToCsv(USERNAME,"Null","password is incorect",True)
        report.reporting()
      else:
        return 0
        



  def wait_5_sec(self):
    sleep(5)


  def credentials_check(self,username,password):

    #first step to check the username
    typing = ac(self.driver)
    typing.send_keys(username)
    typing.perform()
    
    #clicking the Next button
    find = self.driver.find_element("id","idSIButton9")  
    find.click()

    #check if this username is exists
    self.check_username()
    self.wait_5_sec()

    #second step is to check if the password is right
    typing_pass = ac(self.driver)
    typing_pass.send_keys(password)
    typing_pass.perform()

    find = self.driver.find_element("id","idSIButton9")  
    find.click()

    self.check_password()


  def security_defaults_windows(self):
    self.wait_5_sec()
    #method to check if secority defaults are enabled window appear
    try:
      #checking if there is security windows
      find = self.driver.find_element("id","idSubmit_ProofUp_Redirect")
      with open("report.txt","w") as report:
        report.write(f"{USERNAME} is having error:security 2FA")
      
      #if not security window so click on No and continue 
    except:
      find = self.driver.find_element("id","idBtn_Back")
      find.click()


  def check_auth_partnership(self):
    sleep(15)
    try:
      #TODO dont forget that you can access all class names by BY class method
      find = self.driver.find_element(By.CLASS_NAME,"ms-Checkbox-checkmark")
      find.click()
      print(find.text)
      print("its found the class")

    except:
      print("its didnt find the element")
      pass

  def activate(self):

    self.driver.get(self.destination_path)
    
    #waiting 5 second before continue
    sleep(5)


    #method that checking the credentials 
    self.credentials_check(USERNAME,PASSWORD)

    self.security_defaults_windows()

    self.check_auth_partnership()
    
    # try:
    #   find = self.driver.find_element("id","idBtn_Back")
    #   find.click()
    # except:
    #   pass
    # try:
    #   find_window = self.driver.find_element("h2","Microsoft Authenticator")
    #   print("window exists")
    # except:
    #   print("test")
    # click_next = self.driver.find_element("value","Next").click()
    # click_next.send_keys(Keys.RETURN)

    # find = self.driver.find_element("id","idSIButton9")  
    # find.click()

    
    
    

    # search_bar = driver.find_element("").send_keys("012ps@investigatio.onmicrosoft.com")
    # # # find = driver.find_element()
    # # # find.clear()
    # # # find = driver.send_keys("012ps@investigatio.onmicrosoft.com")
    # # # find.send_keys(Keys.RETURN)
    # search_bar.clear()
    # search_bar.send_keys("012ps@investigatio.onmicrosoft.com")
    # search_bar.send_keys(Keys.RETURN)
    
    #example of waiting for a certain element to show up and then click
    # try:
    # element = WebDriverWait(driver, 5).until(
    # EC.presence_of_element_located((By.ID, "id-of-new-element"))
    # )
    # finally:
    # driver.quit()



    #method that will return which username us succeded in the form filling and which is not succeded
    self.completed(self.status)


    #while loop only for testing so the windows is not automaticly close
    while True:
      pass


    












form = AutomatedFormFill(DESTINATION_PATH)
form.activate()