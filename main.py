import os
import time
from datetime import datetime

from nepsetms import Tms
from nepsealpha import NepseAlpha
# from meroshare import MeroShare

from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service


DIR_PATH = os.getcwd()
data_path = f"{DIR_PATH}\Data"
PATH = f"{DIR_PATH}\Edge Driver\msedgedriver.exe"
options = ['Y','YES']
working_week_days = ['0','1','2','3','4','6']
working_time = ['10','11','12','01','02','03']

ser = Service(PATH)
option = Options()
option.use_chromium = True
option.add_experimental_option('excludeSwitches', ['enable-logging'])
option.add_argument('--disable-extensions')
option.add_argument('--disable-gpu')


def get_data_from_tms(browser, start_date, end_date):
    user = Tms(browser, start_date, end_date)
    data = user.start_tms()
    if not data:
        return False
    try:
        with open('Data\shares.txt', 'w') as fp:
            for item in data:
                text = ",".join(item)
                fp.write(text)
                fp.write('\n')
                fp.write('\n')
    except:
        print()
        print('MAIN :: Could not write TMS data!')
        print()
    return data


def read_tms_data():
    data = []
    try:
        with open('Data\shares.txt', 'r') as fp:
            lines = fp.read().splitlines()
            for line in lines:

                temp = line.split(',')
                if len(temp) != 5:
                    continue
                data.append(temp)
        return data
    except:
        return False


# def get_data_from_meroshare(browser):
#     user = MeroShare(browser)
#     bonus_data = user.start_meroshare()
#     try:
#         with open('Data\\bonus_shares.txt', 'w') as fp:
#             for item in bonus_data:
#                 text = ",".join(item)
#                 fp.write(text)
#                 fp.write('\n')
#                 fp.write('\n')
#     except:
#         print('Could write Meroshare data!')
#     return bonus_data


# def read_meroshare_data():
#     bonus_data = []
#     with open('Data\\bonus_shares.txt', 'r') as fp:
#         lines = fp.read().splitlines()
#         for line in lines:
#             temp = line.split(',')
#             if len(temp) != 5:
#                 continue
#             bonus_data.append(temp)
#     return bonus_data


def write_data(data):
    with open('Data\clean.txt', 'w') as fp:
        for item in data:
            text = " ".join(item)
            text = '[ ' + text + ' ]'
            fp.write(text)
            fp.write('\n')
            fp.write('\n')

def write_logs(logs):
    with open('Data\logs.txt', 'w') as fp:
        fp.write('\n')
        for item in logs:
            fp.write(item)
            fp.write('\n')

def add_to_nepsealpha(browser, data, ID):
    user = NepseAlpha(browser, data)
    return user.start_nepse_alpha(ID)

def main():
    today = datetime.today().strftime('%Y-%m-%d')
    current_time = datetime.today().strftime('%I')
    week_day = str(datetime.today().weekday())

    # bonus_data = get_data_from_meroshare(browser)
    # bonus_data = read_meroshare_data()

    data = []
    bonus_data= []

    if week_day in working_week_days:
        if current_time in working_time:
            print('Please try after market is closed!')
            input()
            return

    from_tms = input('Would you like to get data from TMS (Y/N): ').upper()

    

    if not from_tms in options:
        tms_data = read_tms_data()
        if not tms_data:
            print('Please get the data from tms first !')
            input()
            return
    else:
        print()
        print('Format: YYYY-MM-DD | 2022-01-30')
        print()
        start_date = input('Enter start date: ')
        end_date = input('Enter end date: ')

        print()

        if len(start_date.split('-')) != 3:
            start_date = today
        if len(end_date.split('-')) != 3:
            end_date = today
        if start_date < '2021-01-01':
            start_date = today
        if  end_date > today:
            end_date = today
        if start_date > end_date:
            start_date = end_date

        browser = webdriver.Edge(service=ser, options=option)
        browser.minimize_window()
        tms_data = get_data_from_tms(browser, start_date, end_date)
        browser.quit()
    
    option.add_argument('headless')
    browser = webdriver.Edge(service=ser, options=option)

    if not tms_data:
        print('No data to add!')
        input()
        return

    data = tms_data + bonus_data
    data = sorted(data, key=lambda x: x[4]+x[1])

    print()
    print(f"Total Shares: {len(data)}")
    print()

    try:
        ID = int(input('Enter nepsealpha id: '))
        if len(str(ID)) != 5:
            raise Exception
        ID = str(ID)
    except:
        ID = '50136'
    os.system('cls')

    print(f'ID: {ID}')
    print()
    
    start = time.time()
    logs = add_to_nepsealpha(browser,data,ID)
    end = time.time()

    if not logs:
        return

    time_delta = (end - start)
    minutes, seconds = divmod(time_delta,60)

    print()
    print(f"Execution time: {minutes:.0f} minutes {seconds:.1f} seconds")
    print()
    write_data(data)
    write_logs(logs)
    return

if __name__ == "__main__":
    try:
        main()
        exit(0)
    except KeyboardInterrupt:
        print('Interrupted!')
        exit(0)

