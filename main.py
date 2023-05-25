from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains as ac
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from usernames import password_list,username_list
from settings import CHROME_DRIVER_PATH,DESTINATION_URL
from report_csv import ReportToCsv
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as ec





class AutomatedFormFill:

  def __init__(self,destination_path,username):
    self.driver = webdriver.Chrome(CHROME_DRIVER_PATH)
    self.destination_path = destination_path
    self.username = username

    self.status = {"1":"Added","0":"Not Added"}

    self.passwords = [i for i in password_list]



  def credential_validation(self):#method to check username and password validation


    login_error_list = [("id","usernameError"),("id","passwordError")]

    for by,value in login_error_list:
      try:
        sleep(5)
        error = self.driver.find_element(by,value).is_displayed()
        if value == "usernameError":
          return "usernameError"

        elif value == "passwordError":
          return "passwordError"

      
      except :
        pass
      

  def password_all(self,pas):

        #sending keyboard password
      typing_pass = ac(self.driver)
      typing_pass.send_keys(pas)
      typing_pass.perform()

    #click next after filling the password
      try:
        find = self.driver.find_element("id","idSIButton9")  
        find.click()
      except:
        pass
      check = self.credential_validation()
      return check

    
  def credentials_fill(self,username):#filling the credentials and check for errors

    """ fillind the credentials and checking for errors"""
  
    sleep(5)  

    #first step to check the username
    typing = ac(self.driver)
    typing.send_keys(username)
    typing.perform()
    
    #clicking the Next button
    sleep(3)
    find = self.driver.find_element("id","idSIButton9")  
    find.click()

    #check if this username is exists
    check = self.credential_validation()
    if check == "usernameError":
      report = ReportToCsv(self.username,self.status["0"],check,True)
      report.reporting()
      self.driver.close()
      self.driver.quit()
      sleep(5)
    else:
      pass

    #filling all passwords if it exceede all passwords then it will close the report to csv

    counter = 0
    for i in self.passwords:
      checking = self.password_all(i)
      counter += 1
      if counter == 4 and checking == "passwordError":
        pass_report = ReportToCsv(self.username,self.status["0"],checking,True)
        pass_report.reporting()
        self.driver.close()
        self.driver.quit()
        pass
      # elif 
      
    sleep(5)
  
  #method to check if security defaults are enabled and the window appear  
  def security_defaults_windows(self):#fill the security window(reports to csv if it cant proceed)
    sleep(5)
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
        pass

      except NoSuchElementException:
        report = ReportToCsv(self.username,self.status["0"],f"needed 2FA to procceed error: {value}",True)
        report.reporting()
        pass
      

  def check_auth_partnership(self):#last form fill
    """ method that uses global class attributes to fill the partner relationship 
        action:waits 45sec,two/one checkboxes every time pressing confirm button,request btn and a popup with "Yes"
        button.
    """
   
    time = sleep(45)
  
    all_checkboxes = self.driver.find_elements(By.CLASS_NAME,"ms-Checkbox-checkmark")


                   #IMPORTANT here its twice because the checkbox and the click must be completed one after another
    
    
    try

      find = self.driver.find_element(By.CLASS_NAME,"ms-Checkbox-checkmark")
      print(find)
      find.click()
      print(find.is_selected())
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
        
    for i in all_checkboxes[1:]:
        try:
            all_checkboxes[1].click()
            

        except:
              print("its didnt find the element")
              pass
      
    try:
        
      find = self.driver.find_element(By.CLASS_NAME,"ms-Button--primary")
      find.click()
    except:
      pass

    sleep(4)

    try:
      find = self.driver.find_element(By.CLASS_NAME,"ms-Button--primary")
      find.click()
    except:
      pass

    sleep(3)


    el = self.driver.find_element(By.CLASS_NAME,"ms-Dialog-action")
    action = webdriver.common.action_chains.ActionChains(self.driver)
    action.move_to_element_with_offset(el, 5, 5)
    action.click()
    action.perform()

    sleep(10)
    #sending report of successfuly added
    report = ReportToCsv(self.username
    ,self.status["1"],"account added successfuly",True)
    report.reporting()
    self.end = "done"


  def activate(self):#method that runs all methods in a certain order (main method)
    """ main method that run all methods in a certain order
        on every step it will pass(continue ot execute) or break(report will be sent to csv file with detailes)
        the class is callable even if the code will break(to disable it for troubleshooting reasons remove "try/except" in the activate method
    """

    try:

      #destination path that get the path from settings.py
      self.driver.get(self.destination_path)
      

      #method that fill the credentials and checking for errors(wrong username or password and if error exists it will return a report to csv file)
      self.credentials_fill(self.username)



      #checking if there is security window enabled(checking if possible to proceed or not)
      self.security_defaults_windows()

      sleep(5)

      #clicking the: (STAY signed in?:YES/NO)
      try:
        find = self.driver.find_element("id","idBtn_Back")
        find.click()
      except:
        pass


      #filling the partnership form
      self.check_auth_partnership()
    except Exception:
      pass






if "__main__" == __name__:
  
  #loop over all usernames and then creating instance of a class and start the proccess of filling the form
  #the usernames need to be stored as list of strings  EXAMPLE: username_list = ["usarname@gmail.com","username2@gmail.com"]
  
  
  
  for username in username_list:
    form = AutomatedFormFill(DESTINATION_URL,username)
    form.activate()
