This is a Django Rest Framework based API for scraping the Products from Amazon using asin for different products.

**Features**
Scraps Products details from Amazon based on asins given for different PIN codes. pin codes and city names are not mandatory.

**Prerequisites**
Ensure You have following installed on your system.
Python 3.10.x
pip
virtualenv(optional but recommended)
django
djangorestframework
pandas
selenium
djangorestframework-simplejwt

**Setup Instructions**
Clone the repository
pip install requirements.txt
python manage.py runserver

**To Generate Authorization token, hit the following endpoint using any api testing tool like Postman**
http://127.0.0.1:8000/api/token/
give the username and password in body as following
{ "username":"Your username"
   "password":"Your password"
 }
 
 You will get a refreshtoken and accesstoken in response as following manner.
 {"refresh":"Your refresh token"
  "access":"Your access token"
 }
 Use that accesstoken in request headers while hitting the api endpoint as following
 "Authorization":"Bearer Your accesstoken"
 
 If the accesstoken is expired, You can generate another access token using the refresh token as follows.
 hit the endpoint http://127.0.0.1:8000/api/token/refresh/ with body as {"refresh":"Your refresh token"}
 
 **Test the api**
 to test the api, hit the endpoint: 
 http://127.0.0.1:8000/api/scrape/
 give the access token in Header:
 "Authorization":"Bearer Your accesstoken"
 give asin, pincode and cityname (not mandatory) in Body as follows.
 {
 "asin":["asin1","asin2",..],
 "pincode":"Your pincode",
 "city_name":"Your cityname"
 }
 **You have to provide your directory to store the json file**
 
