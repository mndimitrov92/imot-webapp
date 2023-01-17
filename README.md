# This is only the UI layer of the imot tracker application
The data population part is handled in a separate repo. 
## Purpose is to only start a localhost server and visualize the data that was collected in the database
# Usage
1) Setup environment : ```python -m venv <envrionment name> ```
2) Activate environment
3) Install dependancies: ``` pip install -r depencencies.txt ```
4) Generate test data: ``` python generate_test_db.py ```
5) Run the app: ``` python app.py ```

# Any new crawlers added in the data collection layer must also include their corresponding:
        1) css specifics that will be used in the templates (styles.css)
        2) constants file definition

# Provided APIs
The app provides a couple of endpoints to visualize all and only the new ad listings as well as filters for the collected listings based on source, type, size, price and location. 
There is also the download endpoint to save all or filtered data to a csv file. 

The endpoints are:
* ```/all-ads``` - visualizes all collected listings data
* ```/new-ads``` - visualizes all collected new listings data which is based on the last crawl run 
* ```/download-all-ads``` - download all collected new listings data
* ```/download-new-ads``` - download all collected new listings data which is based on the last crawl run 
* ```/data``` - will display additional location data (ex air poultion, traffic etc) NOT READY YET
* ```/docs``` - show the documentation of all endpoints

The supported query parametes are(every on of them is *optional*):
 - ```source_name``` - the place where the listing was scraped from 
 - ```price``` - maximum allowed price point in EUR (will visualize all listing with prices lower than the provided one)
 - ```location``` - location where the apartment is situated
 - ```home_size``` - Minimum apartment size of the listings (will show all listing with size bigger than the provided one)
 - ```home_type``` - the type of the apartment 
 - ```limit``` - the amount of ad listing that will be shown

### NOTE: 
The location and home_type parameters should be in bulgarian. 
Only one entry for each parameters is supported.

More information can be found in the /docs endpoint.



## Example request:

http://127.0.0.1:8000/new-ads?location=%D0%A0%D0%B5%D0%B4%D1%83%D1%82%D0%B0&source_name=yavlena&home_type=%D0%94%D0%B2%D1%83%D1%81%D1%82%D0%B0%D0%B5%D0%BD&home_size=90&price=30000