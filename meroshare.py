from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys



class MeroShare:

    def __init__(self, browser):
        self.browser = browser

    def login(self,DP,USERNAME, PASSWD):
        self.browser.find_element(
        By.XPATH, "/html/body/app-login/div/div/div/div/div/div/div[1]/div/form/div/div[1]/div/div/select2/span/span[1]/span").click()
    # Dp feild
        dp = self.browser.find_element(By.CLASS_NAME, "select2-search__field")
        dp.send_keys(f"{DP}")
        dp.send_keys(Keys.RETURN)

        # Username filed
        username = self.browser.find_element(By.ID, "username")
        username.send_keys(f"{USERNAME}")

        # Password feild
        passwd = self.browser.find_element(By.ID, "password")
        passwd.send_keys(f"{PASSWD}")

        # Login button
        self.browser.find_element(By.XPATH, "/html/body/app-login/div/div/div/div/div/div/div[1]/div/form/div/div[4]/div/button").click()
        self.browser.implicitly_wait(4)
        self.browser.find_element(By.XPATH, "/html/body/app-dashboard/div/div[1]/nav/ul/li[4]/a").click()
        return

    def get_shares(self):
        data = []
        while True:
            try:
                self.browser.get('https://meroshare.cdsc.com.np/#/transaction')
                self.browser.implicitly_wait(1.5)
                # click on date radio button
                self.browser.find_element(By.XPATH, '/html/body/app-dashboard/div/main/div/app-transaction-history/div/div[2]/div/div/div/div/form/div[1]/div/div[2]/div[1]/label[2]/span').click()
                self.browser.implicitly_wait(2.5)

                table_body = self.browser.find_element(By.XPATH, '/html/body/app-dashboard/div/main/div/app-transaction-history/div/div[4]/div/div/table/tbody')
                    # list of row data
                rows = table_body.find_elements(By.TAG_NAME, "tr")

                for row in rows:
                    col = row.find_elements(By.TAG_NAME, "td")
                    name, date, quantity, isCA = col[1].text, col[2].text, col[3].text, col[6].text.split(' ')[0]

                    if 'CA' not in isCA:
                        continue
                    if "Bonus" in isCA:
                        data.append([name,'Bonus',quantity,'0', date])
                        continue
                    if "Right" in isCA:
                        data.append([name,'Right',quantity,'100', date])
                return data
            except:
                print('Some Error occured while getting data!')


    def start_meroshare(self):
        DP = "13700"
        USERNAME = "03522757"
        PASSWD = "Kaycee@logang1"
        self.browser.get("https://meroshare.cdsc.com.np/#/login")
        while True:
            try:
                self.browser.refresh()
                sleep(2.5)
                self.login(DP, USERNAME, PASSWD)
                break
            except:
                print(f"*************Site didnot load*****************")
        sleep(2)
        return self.get_shares()
        
