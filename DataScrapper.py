from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

capab = DesiredCapabilities.CHROME
"""This will make Selenium WebDriver to wait until the initial HTML document has been completely loaded and parsed, 
and discards loading of stylesheets, images and sub-frames."""
capab["pageLoadStrategy"] = "eager"

"""The headless option will run everything in background. """
chrome_options = Options()
# chrome_options.add_argument("--headless")


class Scrapper:
    def __init__(self):
        self.url = "https://www.nasdaq.com/market-activity/quotes/historical"

    @staticmethod
    def stock_list():
        no_of_stocks = int(input("Enter no of stocks:"))
        stocks = []
        if no_of_stocks > 1:
            print("Enter Stock Symbols:")
        elif no_of_stocks < 1:
            print("No stocks entered, Quiting..")
            quit()
        elif no_of_stocks == 1:
            print("Enter Stock Symbol:")

        for i in range(no_of_stocks):
            stock = input()
            stocks.append(stock)
        return stocks

    def scrape(self):
        stocks = self.stock_list()
        driver = Chrome("C:\\Users\\gopib\\Downloads\\chromedriver.exe", desired_capabilities=capab,
                        options=chrome_options)


        for stock in stocks:
            driver.get(self.url)
            driver.maximize_window()
            # The below statement is for stopping the page load
            driver.execute_script("window.stop()")
            # We are finding the search box to enter the stock symbol
            driver.find_element_by_id(
                "find-symbol-input-dark").send_keys(
                str(stock), Keys.ENTER)

            if "No Results Found" in driver.page_source:
                print("Enter Correct Stock Symbol")
                quit()
            else:
                # To click the Historical quotes link, the cookie message which is appearing,
                # is blocking Historical Quotes from being interactable
                # So Clicking the "I Understand" Cookie button
                # time.sleep is for the cookie button to load
                # try catch block is needed since, when we are looping for multiple stocks, the cookie button does not appear the 2nd time and program will raise an exception

                time.sleep(5)
                try:
                    driver.find_element_by_id("_evidon-decline-button").click()
                except:
                    continue

                # The below is the Historical Quotes Links full Xpath
                driver.find_element_by_xpath(
                    "/html/body/div[2]/div/main/div[2]/div[4]/div/section/div/div[3]/ul/li[2]/a/span").click()
                time.sleep(5)
                # Click on 1 Year Tab
                driver.find_element_by_xpath("/html/body/div[2]/div/main/div[2]/div[4]/div[3]/div/div[1]/div/div[1]/div[3]/div/div/div/button[4]").click()

                # Creating the file to save data
                file_columns = ["Date", "Close/Last", "Volume", "Open", "High", "Low"]
                with open(str(stock) + '.csv', 'w') as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow(file_columns)
                    #Determing the number of times to loop by counting the number of buttons/pages in pagination
                    pagecount=1
                    while driver.find_element_by_class_name("pagination__next").is_enabled():
                        time.sleep(1)
                        try:
                            driver.find_element_by_class_name("pagination__next").click()
                            pagecount += 1
                        except:
                            break

                    # Click on 1 Year Tab again to loop for data this time, we have created a speerate loop since for recent ipo stocks, which are only in one page , it is easier to handle with seperate loops
                    driver.find_element_by_xpath("/html/body/div[2]/div/main/div[2]/div[4]/div[3]/div/div[1]/div/div[1]/div[3]/div/div/div/button[4]").click()
                    #if page count is greater than 1 we iterate by cliking pagination_next
                    if pagecount>1:
                        for i in range(pagecount):
                            trs = driver.find_elements_by_xpath('/html/body/div[2]/div/main/div[2]/div[4]/div[3]/div/div[1]/div/div[1]/div[4]/div[2]/div/table/tbody[2]')
                            data = []
                            for tr in trs:
                                data = str(tr.text).split()
                                print(data)
                            driver.find_element_by_class_name("pagination__next").click()
                           #sleep is added below to avoid reading the same page again
                            time.sleep(2)
                        print("No of scraped pages for",stock,"are",pagecount)
                    # if page count is less than 1 we read that page once
                    else:
                        trs = driver.find_elements_by_xpath('/html/body/div[2]/div/main/div[2]/div[4]/div[3]/div/div[1]/div/div[1]/div[4]/div[2]/div/table/tbody[2]')
                        data=[]
                        for tr in trs:
                            data = str(tr.text).split()
                            print(data)
                        print("No of scraped pages for", stock, "are", pagecount)










                    # #reclicking on 1 year tab again, for some reason using one loop is making the program read data multiple times in the middle pages
                    # driver.find_element_by_xpath("/html/body/div[2]/div/main/div[2]/div[4]/div[3]/div/div[1]/div/div[1]/div[3]/div/div/div/button[4]").click()
                    # for i in range(buttoncount):
                    #     time.sleep(1)
                    # # Find Elements under data rows,  i.e., with historical-data__row, ignore the column names tbody tag, we should find data under tr tag
                    #     trs = driver.find_elements_by_xpath('/html/body/div[2]/div/main/div[2]/div[4]/div[3]/div/div[1]/div/div[1]/div[4]/div[2]/div/table/tbody[2]')
                    #     data=[]
                    #     for tr in trs:
                    #         data=str(tr.text).split()
                    #         print (data)
                    #     time.sleep(1.5)
                    #     driver.find_element_by_class_name("pagination__next").click()














if __name__ == "__main__":
    obj = Scrapper()
    obj.scrape()