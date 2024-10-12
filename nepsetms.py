from PIL import Image, ImageEnhance
import pytesseract
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\PDF24\\tesseract\\tesseract.exe"
limit = list(range(48, 58)) + list(range(65, 91)) + list(range(97, 123))


class Tms:
    def __init__(self, browser, start_date, end_date):
        self.browser = browser
        self.start_date = start_date
        self.end_date = end_date

    def get_screenshot(self):
        try:
            self.browser.find_element(By.XPATH, "/html/body/app-root/app-login/div/div/div[2]/form/div[3]/div[2]/div/img")
            ele = self.browser.find_element(By.XPATH, "/html/body/app-root/app-login/div/div/div[2]/form/div[3]/div[2]")
            self.browser.execute_script("document.body.style.zoom='150%'")
            self.browser.execute_script('arguments[0].scrollIntoView({block: "center"});', ele)
            self.browser.get_screenshot_as_file('Captcha\captcha.png')
            self.browser.execute_script("document.body.style.zoom='100%'")
            return True
        except:
            return False

    def get_improve_image(self):
        factor = 1.2
        box = (215, 265, 415, 340)
        image = Image.open('Captcha\captcha.png')

        sized_image = image.resize((800, 600))
        cropped_image = sized_image.crop(box)

        # filter = ImageEnhance.Brightness(contrast_image)

        filter = ImageEnhance.Brightness(cropped_image)
        brightened_image = filter.enhance(factor)
        # img  = brightened_image

        filter = ImageEnhance.Contrast(brightened_image)
        contrast_image = filter.enhance(3)
        img = contrast_image

        width = img.size[0]
        height = img.size[1]
        for i in range(0, width):  # process all pixels
            for j in range(0, height):
                data = img.getpixel((i, j))
                # if (data [0] != 255 and data [1] != 255 and data [2] != 255):
                # if (248 > data[0]> 75 and 248 > data[1] > 75 and 248> data[2] > 75):
                if (250 > data[0] > 5 and 250 > data[1] > 5 and 250 > data[2] > 5):
                    img.putpixel((i, j), (255, 255, 255))

        # sized_image.save('sized_captcha.png')
        # cropped_image.save('cropped_captcha.png')
        brightened_image.save("bright.png")
        contrast_image.save("contrast.png")
        img.save("Captcha\improved_captcha.png")
        return img

    def get_captcha(self):
        img = self.get_improve_image()

        text = pytesseract.image_to_string(img, lang="eng")
        temp = ""
        for letter in text:
            if not ord(letter) in limit:
                continue
            temp += letter
        text = temp
        if len(text) != 6:
            return text, False

        return text, True

    def login(self):
        while True:
            ss_complete = self.get_screenshot()
            if not ss_complete:
                print("TMS :: Could not screen shot captcha!")
                continue

            captcha, solved = self.get_captcha()

            if not solved:
                # print(len(captcha))
                print(f"TMS :: Captcha Couldnot be solved : {captcha}")
                self.browser.find_element(By.XPATH, "/html/body/app-root/app-login/div/div/div[2]/form/div[3]/div[2]/div/div/a[2]").click()
                sleep(1)
                continue

            username = self.browser.find_element(By.XPATH, "/html/body/app-root/app-login/div/div/div[2]/form/div[1]/input")
            username.clear()
            username.send_keys("20210704927")
            passwd = self.browser.find_element(By.XPATH, "/html/body/app-root/app-login/div/div/div[2]/form/div[2]/input")
            passwd.send_keys("Kaycee@logang5")

            verify = self.browser.find_element(By.XPATH, "/html/body/app-root/app-login/div/div/div[2]/form/div[3]/div[1]/div/input")
            verify.send_keys(f"{captcha}")
            self.browser.find_element(By.XPATH, "/html/body/app-root/app-login/div/div/div[2]/form/div[4]/input").click()
            try:
                self.browser.implicitly_wait(1)
                self.browser.find_element(By.XPATH, "/html/body/app-root/xtoastr/ng2-toasty/div/ng2-toast")
                self.browser.find_element(By.XPATH, "/html/body/app-root/xtoastr/ng2-toasty/div/ng2-toast/div/div[1]").click()
                print(f"TMS :: Invalid Captcha: {captcha}")
                sleep(1)
                continue
            except:
                print(f"TMS :: Captcha solved : {captcha}")
                return True

    def set_order_book(self):
        # self.browser.get('https://tms01.nepsetms.com.np/tms/me/trade-book-history')
        # sleep(1)
        try:
            # click order management
            self.browser.find_element(By.XPATH, "/html/body/app-root/tms/app-menubar/aside/nav/ul/li[11]/a").click()
            self.browser.implicitly_wait(1)
            # click historic order book
            self.browser.find_element(By.XPATH, "/html/body/app-root/tms/app-menubar/aside/nav/ul/li[11]/ul/li[2]/a").click()

            self.browser.implicitly_wait(6)
            # set start date and end date
            start_date = self.browser.find_element(By.XPATH, "/html/body/app-root/tms/main/div/div/app-trade-book-history/app-trade-book-history-prime/div/div/kendo-grid/kendo-grid-toolbar/div[2]/div[2]/div/div[2]/form/div[2]/div/input")
            start_date.send_keys(f"{self.start_date}")
            end_date = self.browser.find_element(By.XPATH, "/html/body/app-root/tms/main/div/div/app-trade-book-history/app-trade-book-history-prime/div/div/kendo-grid/kendo-grid-toolbar/div[2]/div[2]/div/div[2]/form/div[3]/div/input")
            end_date.send_keys(f"{self.end_date}")
            # click search
            self.browser.find_element(By.XPATH, "/html/body/app-root/tms/main/div/div/app-trade-book-history/app-trade-book-history-prime/div/div/kendo-grid/kendo-grid-toolbar/div[2]/div[2]/div/div[3]/button").click()
            self.browser.implicitly_wait(2)
            # click all
            option = Select(self.browser.find_element(By.XPATH, "/html/body/app-root/tms/main/div/div/app-trade-book-history/app-trade-book-history-prime/div/div/kendo-grid/kendo-pager/kendo-pager-page-sizes/select"))
            option.select_by_value('All')
            sleep(1)
            return True
        except:
            return False

    def get_data_order_book(self):

        data = []

        # table_class = self.browser.find_element(By.CLASS_NAME, 'k-grid-table')
        table_body = self.browser.find_element(By.XPATH, '/html/body/app-root/tms/main/div/div/app-trade-book-history/app-trade-book-history-prime/div/div/kendo-grid/div/kendo-grid-list/div/div[1]/table/tbody')
        # list of row data
        rows = table_body.find_elements(By.TAG_NAME, "tr")

        try:
            for row in rows:
                # list of columun data
                col = row.find_elements(By.TAG_NAME, "td")
                name, type, quantity, price, transact_id = col[3].text, col[7].text, int(col[8].text), col[9].text.replace(',', ''), col[4].text
                date = col[4].text[:4] + '-' + col[4].text[4:6] + '-' + col[4].text[6:8]
                updated = self.check_if_exist(name, type, quantity, price, date, transact_id, data)
                if not updated:
                    data.append([name, type, quantity, price, date, transact_id])

            for item in data:
                # change quantity from int to string
                item[2] = str(item[2])
                # remove transaction id from data
                item.pop()
            return data
        except:
            return False

    def check_if_exist(self, name, type, quantity, price, date, transact_id, data):
        for item in data:
            if not name in item:
                continue
            if item[5] == transact_id:
                return True
            if price == item[3] and date == item[4] and type == item[1]:
                item[2] += quantity
                return True
        return False

    def start_tms(self):
        self.browser.get('https://tms01.nepsetms.com.np/login')
        print('TMS :: Request success to nepsetms')

        logged_in = self.login()

        if not logged_in:
            print('TMS :: Couldnot login')
            return False

        print('TMS :: Logged In')

        if not self.set_order_book():
            print('TMS :: Order Book could not be set')
            return False

        print('TMS :: Order Book successfully set')
        data = self.get_data_order_book()
        if not data:
            print('TMS :: No records found!')
            return False
        print('TMS :: Order Book data successfully extracted')
        return data
