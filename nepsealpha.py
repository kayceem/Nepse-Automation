from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class NepseAlpha:

    def __init__(self, browser ,info):
        self.browser = browser
        self.info = info

    def login(self,ID):
        try:
            username = self.browser.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div/div/div[2]/form/div[1]/input")
            username.clear()
            username.send_keys("kaycx")
            passwd = self.browser.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div/div/div[2]/form/div[2]/input")
            passwd.send_keys("kaycee@nepsealpha30")
            self.browser.find_element(By.ID, "loginClick").click()
            sleep(5)
            # select 49967
            option = Select(self.browser.find_element(By.ID, 'shareHolderOpt'))
            option.select_by_value(f'{ID}')
            return True
        except:
            return False
    
    def add_stocks(self):
        logs = []
        total = len(self.info)
        
        
        for index, data in enumerate(self.info):
            isBonus = False
            check = False

            name,type,amount,cost,date = data
            
            while True:
                option = Select(self.browser.find_element(By.ID, 'trans_typeOpt'))
                if type == "Sell":
                    option.select_by_value('sell')
                    
                if type == "Buy":
                    option.select_by_value('buy')
                    
                option = Select(self.browser.find_element(By.ID, 'purchaseType'))
                if type == "Bonus":
                    isBonus = True
                    check = True
                    option.select_by_value('bonus')
                    
                if type == "Right":
                    check = True
                    option.select_by_value('right')
                    
                # click selection
                # add ticker
                option = Select(self.browser.find_element(By.ID, 'portfolioSymbols'))
                option.select_by_value(f'{name}')


                # add quantity
                quantity = self.browser.find_element(By.XPATH, "/html/body/div/div/div/div/div[2]/div[1]/div[3]/div/div[1]/div/form/div/div[3]/div/input")
                quantity.clear()
                quantity.send_keys(amount)
                
                # add date
                trade_date = self.browser.find_element(By.XPATH, "/html/body/div/div/div/div/div[2]/div[1]/div[3]/div/div[1]/div/form/div/div[4]/div/input")
                self.browser.execute_script(f"arguments[0].setAttribute('value','{date}')", trade_date)
                
                # add price
                if not isBonus:
                    price = self.browser.find_element(By.XPATH, "/html/body/div/div/div/div/div[2]/div[1]/div[3]/div/div[1]/div/form/div/div[6]/div/input")
                    price.send_keys(cost)

                # click save
                WebDriverWait(self.browser, 3).until(EC.invisibility_of_element(
                    (By.XPATH, "//div[@class='swal2-container swal2-top-end swal2-backdrop-show']")))
                self.browser.execute_script("arguments[0].click();", WebDriverWait(self.browser, 3).until(EC.element_to_be_clickable(
                    (By.ID, "savePortFolioBtn"))))

                if not check:
                    try:
                        # click continue
                        continue_button =WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.ID, "saveUserPortfolio")))
                        sleep(0.5)
                        continue_button.click()
                        break

                    except :   
                            print(f"NEPSEALPHA :: Couldnot add: {name} | {amount} | {type} | ({index+1}/{total})")
                            logs.append(f"NEPSEALPHA :: Couldnot add: {name} | {amount} | {type} | ({index+1}/{total})")
                            while True:
                                try:
                                    self.browser.get('https://nepsealpha.com/tradingusers/portfolio-tracker')
                                    sleep(2)
                                    WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.ID, 'trans_typeOpt')))
                                    break
                                except:
                                    print(f"NEPSEALPHA :: Couldnot Refresh Browser: {name} | {amount} | {type} | ({index+1}/{total})")
                                    logs.append(f"NEPSEALPHA :: Couldnot Refresf Browser: {name} | {amount} | {type} | ({index+1}/{total})")
                                    continue
                            continue
                break
            # click sure
            sleep(0.5)
            sure_button = WebDriverWait(self.browser, 3).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div[6]/button[1]")))
            sure_button.click()
            sleep(1)

            action = ActionChains(self.browser)
            action.click(on_element= None)
            action.click(on_element= None)
            action.click(on_element= None)
            action.perform()

            
            print(f"NEPSEALPHA :: Added: {name} | {amount} | {type} | ({index+1}/{total})")
            logs.append(f"NEPSEALPHA :: Added: {name} | {amount} | {type} | ({index+1}/{total})")
        return logs


    def start_nepse_alpha(self,ID):
        try:
            self.browser.get('https://nepsealpha.com/tradingusers/portfolio-tracker')
            print('NEPSEALPHA :: Request success to nepsealpha')
        except:
            print('NEPSEALPHA :: Request failed to nepsealpha')
            return False

        logged_in = self.login(ID)

        if not logged_in:
            print("NEPSEALPHA :: Login Failed")
            return False
        print("NEPSEALPHA :: Logged In")
        
        return self.add_stocks()