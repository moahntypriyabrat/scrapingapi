from rest_framework.views import APIView
from rest_framework.response import Response
from selenium import webdriver
from selenium.webdriver.common.by import By
from rest_framework import status
import pandas as pd
import json
import time
import datetime
import os
from .serializers import AsinSerializer
from .scrapper_utils import getlinks, product_scraper
from rest_framework.permissions import IsAuthenticated
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager



class MattressScrapperView(APIView):
    # permission_classes = [IsAuthenticated]
    

    # service = Service(GeckoDriverManager().install())
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    # Initialize the GeckoDriver service
    driver = webdriver.Firefox(options=options)
    driver.maximize_window()

    def post(self, request):
        """
        Function to get product urls from main page,
        call product scraper to get raw data and return the response
        """

        serializer = AsinSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Getting the home page url of Amazon and wait to load
        url = "https://www.amazon.in/"
        self.driver.get(url)
        time.sleep(15)

        # Clicking on the delivery to box to change to the desired pin
        self.driver.find_element(By.ID, "nav-global-location-popover-link").click()
        time.sleep(3)
        pin = self.driver.find_element(By.ID, "GLUXZipInputSection").find_element(By.TAG_NAME, "input")
        pin.clear()

        # fetching the pin code from user and wait then apply
        if data.get('pincode') is not None:
            pin.send_keys(data.get('pincode'))
            time.sleep(3)
            self.driver.find_element(By.ID, "GLUXZipInputSection").find_element(By.CLASS_NAME, "a-button-input").click()
            links = getlinks(self.driver, data.get('asin'))

        # Calling the function to get links
        else:
            links = getlinks(self.driver, data.get('asin'))

        # Creating a dataframe to merge all the data which are coming from product scraper
        final_df = pd.DataFrame()
        count = 0

        # Iterating through the list of urls and concating dataframes
        for num, url in enumerate(links):
            if num >= len(final_df):
                df = product_scraper(self.driver, url)
                try:
                    if df == 'No data':
                        continue
                except:
                    pass
                final_df = pd.concat([df, final_df], ignore_index=True)
                count += 1
                print('++++++++++++++', count)

        # Dropping the duplicate rows
        final_df.drop_duplicates(keep='first', inplace=True)

        # Adding Date, Pin, Marketplace and Location to the dataframe
        final_df['Date'] = datetime.date.today().isoformat()
        final_df['MarketPlace'] = 'AMAZON'
        final_df['Pin'] = data.get('pincode')

        if data.get('city_name') is not None:
            final_df['Location'] = data.get('city_name')

        final_df['Location'] = data.get('city_name')
        filled_df = final_df.where(pd.notnull(final_df),None)
        data_dict = filled_df.to_dict(orient='records')
        # removing \n from dict
        for dict1 in data_dict:
            for key in dict1:
                if isinstance(dict1[key], str):
                    dict1[key] = dict1[key].replace('\n', '')

        # saving in file
        # file_path = "D:/AmazonScrapper/amazonscrapper/scrapper/matressJSONfile/AMAZON_Data"+str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))+"_.json"
        # with open(file_path, 'w',encoding='utf-8') as file:
        #     json.dump(data_dict, file, ensure_ascii=False, indent=4)

        return Response(data_dict, status=status.HTTP_200_OK)
