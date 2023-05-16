from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains as ac
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from usernames import USERNAME,PASSWORD
from settings import CHROME_DRIVER_PATH,DESTINATION_PATH
from report_csv import ReportToCsv
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as ec





class AutomatedFormFill:

  def __init__(self,destination_path):
    self.driver = webdriver.Chrome(CHROME_DRIVER_PATH)
    self.destination_path = destination_path

    self.status = ""



  def completed(self,status):
    pass


  def credential_validation(self):
    login_error_list = [("id","usernameError"),("id","passwordError")]

    for by,value in login_error_list:
      try:
        error = self.driver.find_element(by,value).is_displayed()
        if error:
          report = ReportToCsv(USERNAME,"Null",value,True)
          report.reporting()
        break
        
      except NoSuchElementException:
        pass


  def credentials_fill(self,username,password):

    #first step to check the username
    typing = ac(self.driver)
    typing.send_keys(username)
    typing.perform()
    
    #clicking the Next button
    find = self.driver.find_element("id","idSIButton9")  
    find.click()

    #check if this username is exists
    self.credential_validation()
    sleep(5)

    #sending keys to the webpage with the password
    typing_pass = ac(self.driver)
    typing_pass.send_keys(password)
    typing_pass.perform()

    #click next after filling the password
    find = self.driver.find_element("id","idSIButton9")  
    find.click()

    # checking if password exists
    self.credential_validation()
    sleep(5)

  def security_defaults_windows(self):
    sleep(5)
    #method to check if secority defaults are enabled window appear
    windows = [("id","idSubmit_ProofUp_Redirect"),("id","idBtn_Back")]
    for by,value in windows:
      try:
        #checking if there is security windows
        find = self.driver.find_element(by,value)
        if value == "idSubmit_ProofUp_Redirect":
          find = self.driver.find_element("id","btnAskLater")
          find.click()
        elif value == "idBtn_Back":
          find = self.driver.find_element("id","idBtn_Back")
          find.click()
        else:
          report = ReportToCsv(USERNAME,"none",value,True)
        break

      except NoSuchElementException:
        pass
      
      #if not security window so click on No and continue 
    # except:
    #   find = self.driver.find_element("id","idBtn_Back")
    #   if find.is_displayed():
    #     find.click()





  def check_auth_partnership(self):
    sleep(35)
    # wait = WebDriverWait(self.driver,35)
    # element = wait.until(ec.element_to_be_clickable((By.CLASS_NAME, 'ms-Checkbox-checkmark')))
    # element.click()

    # check_boxes = [(By.CLASS_NAME,"ms-Checkbox-checkmark"),(By.CLASS_NAME,"ms-Checkbox-checkmark")]
    # try:
    #   #TODO dont forget that you can access all class names by BY class method
    #   find = self.driver.find_elements(By.CLASS_NAME,"ms-Checkbox-checkmark")
    #   for i in find:
    #     print(i)
    #   # find.click()
    #   # print(find.text)
    #   print("its found the class")

    # except:
    #   print("its didnt find the element")
    #   pass
    # try:
    #   find = self.driver.find_element(By.CLASS_NAME,"ms-Button")
    #   find.click()
    # except:
    #   pass


                  #IMPORTANT here its twice because the checkbox and the click must be completed one after another
    
    try:
      #IMPORTANT          #TODO the two checkboxes having the same attributes so i have to find a way to check both of them but not
      #                         in the same time #REMEBER the driver iterates over the website every 500 ml seconds
      find = self.driver.find_element(By.CLASS_NAME,"ms-Checkbox-checkmark")
      find.click()
      print(find.text)
      print("its found the class")

    except:
      print("its didnt find the element")
      pass
    sleep(5)
    try:
      find = self.driver.find_element(By.CLASS_NAME,"ms-Button--primary")
      find.click()
    except:
      pass
    sleep(5)
        
    try:
        find = self.driver.find_element(By.CLASS_NAME,"ms-Checkbox-checkmark")
        find.click()
        print(find.text)
        print("second_checkbox")

    except:
          print("its didnt find the element")
          pass



  def activate(self):

    self.driver.get(self.destination_path)
    
    #waiting 5 second before continue
    # sleep(5)


    #method that checking the credentials 
    self.credentials_fill(USERNAME,PASSWORD)

    self.security_defaults_windows()

    try:
      find = self.driver.find_element("id","idBtn_Back")
      find.click()
    except:
      pass


    #here its inside the RRR and starting to fill the form 
    self.check_auth_partnership()

    #method that will return which username us succeded in the form filling and which is not succeded
    self.completed(self.status)


    #while loop only for testing so the windows is not automaticly close
    while True:
      pass


    












form = AutomatedFormFill(DESTINATION_PATH)
form.activate()