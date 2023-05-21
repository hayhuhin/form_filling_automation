from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains as ac
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from usernames import password_list
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

    self.stage = "first"
    self.passwords = [i for i in password_list]

    self.end = ""



  def credential_validation(self):#method to check username and password validation
    login_error_list = [("id","usernameError"),("id","passwordError")]

    for by,value in login_error_list:
      sleep(5)
      try:
        sleep(5)
        error = self.driver.find_element(by,value).is_displayed()
        if error:
          report = ReportToCsv(self.username,self.status["0"],value,True)
          report.reporting()
          return False
        return False
        break
      
      except NoSuchElementException:
        return True
        

  def password_all(self):
    i = 0
    while True:
      try:
        #sending keyboard password
        # find = self.driver.find_element(By.NAME,"passwd")
        typing_pass = ac(self.driver)
        typing_pass.send_keys(password_list[i])
        typing_pass.perform()

      #click next after filling the password
        find = self.driver.find_element("id","idSIButton9")  
        find.click()

        #indexing through the list
        i += 1
      

        #checking if there is error message and breaks if there isnt one
        check_for_errors = self.credential_validation()
        if check_for_errors == False:
          #ADD clearing input area from the previous password
          print("no error in the pass")
          break

        #breaking if there is no error message
        else:
          print("error in the pass")
          continue
    
      
      #this except skips if there is no passwrd name tag at all
      except:
        print("there is no pass at all")
        break
    
    report = ReportToCsv(self.username,self.status["0"],"password is wrong",True)
    report.reporting()
   
    




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
    print(check)
    sleep(5)

    #filling all passwords if found continue else:report to csv
    self.password_all()

    sleep(5)


  
  #method to check if secority defaults are enabled window appear  
  def security_defaults_windows(self):#fill the security window(reports to csv if cant proceed)
    self.stage = "third"
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
        else:
          report = ReportToCsv(self.username
          ,self.status["0"],value,True)
        break

      except NoSuchElementException:
        pass
      
      #if not security window so click on No and continue 
    # except:
    #   find = self.driver.find_element("id","idBtn_Back")
    #   if find.is_displayed():
    #     find.click()


  def check_auth_partnership(self):#last form fill
    """ method that uses global class attributes to fill the partner relationship 
        action:waits 45sec,two/one checkboxes every time pressing confirm button,request btn and a popup with "Yes"
        button.
    """
   
    time = sleep(55)
  
    all_checkboxes = self.driver.find_elements(By.CLASS_NAME,"ms-Checkbox-checkmark")


                  #IMPORTANT here its twice because the checkbox and the click must be completed one after another
    
    try:
      #IMPORTANT          #TODO the two checkboxes having the same attributes so i have to find a way to check both of them but not
      #                         in the same time #REMEBER the driver iterates over the website every 500 ml seconds
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



  def activate(self):#method that runs everything togheter(main method)
    """ main method that will run the whole code """

    #destination path that can gets the path from settings.py
    self.driver.get(self.destination_path)
    

    #method that fill the credentials and checking for errors(wrong username or password and if error exists it will return a report to csv file)
    self.credentials_fill(self.username)



    #checking if there is security window is enabled(checking if can i go to the next step or not)
    self.security_defaults_windows()

    sleep(5)

    #STAY signed in?window
    try:
      find = self.driver.find_element("id","idBtn_Back")
      find.click()
    except:
      pass


    #filling the partnership form
    self.check_auth_partnership()


    return self.end 




# form = AutomatedFormFill(DESTINATION_URL,"012ps@targum4biz.onmicrosoft.com")
# form.activate()

username_data = ["012ps@tar4biz.onmicrosoft.com","012ps@targum4biz.onmicrosoft.com"]

for i in username_data:
  form = AutomatedFormFill(DESTINATION_URL,i)
  form.activate()