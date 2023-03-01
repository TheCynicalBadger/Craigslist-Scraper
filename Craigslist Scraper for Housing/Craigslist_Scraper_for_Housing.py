# loading libraries
import time
import datetime
import os
import pandas as pd
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

#### SPECIFICATIONS OF SEARCH

    ### Possible Values (slo, orangecounty)
print("What is the city/area you would like to search in?")
print("Possible values could be slo, orangecounty, bakersfield")
print("You can also find this value by going to the craigslist website for the area you would like to search and looking at the word before .craigslist.org")
location_craigs = input("Please input desired value:")
    
    ### Basic Parameters of Search
        ### These can be found by making search filters on craigslist and copying the value between "apa" and "#"
        ### https://orangecounty.craigslist.org/search/apa?min_bedrooms=3#search=1~gallery~0~0
            ### Correct value would be "?min_bedrooms=3"
            ### IF NONE THEN LEAVE PARENTHESES WITH NOTHING INSIDE
                ### ''
print("\n"+"What are the parameters for your search?")
print("You can find these parameters by making a search on craigslist with the filters you want applied")
print("After completing the search paste the value in between the end of apa and #")
print("An example of this would be https://slo.craigslist.org/search/apa?min_bedrooms=3#search=1~gallery~0~0")
print("The correct value for parameter is ?min_bedrooms=3 and the ? MUST be included")
search_param_craigs = input("If no parameters are desired, press enter:")
#'?lat=35.2888&lon=-120.6611&min_bedrooms=3&search_distance=1.8'

#### PROGRAM DIRECTORY
current_directory = os.getcwd()

#### TIMESTAMP
timestamp = time.strftime("%m-%d-%Y %H_%M")

# loading webdriver for chrome
options = Options()
options.add_argument('--headless=new');
driver = webdriver.Chrome(options = options)



# Navigate to the Craigslist search results page
base_url_craigs = 'https://{0}.craigslist.org/search/apa{1}#search=1~gallery~'.format(location_craigs, search_param_craigs)
base_url_craigs_no_search_param = 'https://{0}.craigslist.org/search/apa#search=1~gallery~'.format(location_craigs)

## RUN FOR SEARCH WITH PARAMETERS SPECIFIED
driver.get(base_url_craigs)
print("\n"+f"Base URL: {base_url_craigs}")
# Wait for the page to load
time.sleep(1)

# Find total number of listings
results = driver.find_elements(By.CSS_SELECTOR,'div.cl-search-paginator')
total_listings = None
for result in results:
    total_count_str = result.find_element(By.CSS_SELECTOR,'span.cl-page-number').text
    a,b,c,d,total_listings = total_count_str.split(' ')
print(f"Total Number of Listings with Search Parameters: {total_listings}")

# Extract the search result items
apartment_listings = []

## Create loop and link for pages
page_string_craig_total = (int(total_listings) // 120) + 1
for page_string_craig in range(0,page_string_craig_total):
    driver.get(base_url_craigs+str(page_string_craig))
    print(f"Scraping Page {page_string_craig+1} at URL: {base_url_craigs+str(page_string_craig)}")

    listings = driver.find_elements(By.CSS_SELECTOR, 'li.cl-search-result')

    for listing in listings:
    # Title of listing
        title = listing.find_element(By.CSS_SELECTOR, 'a.titlestring').text
    # </div> class='meta' contains 3 pieces of data split by the character '·'
        # This element extracts those values and separates them
        posttime_info_city = listing.find_element(By.CSS_SELECTOR, 'div.meta').text
        try:
            posttime,randinfo,city = posttime_info_city.split('·')
        # Exception is required because sometimes the 'randinfo' is missing and there are only 2 pieces of data to split
        except ValueError:
            posttime,city = posttime_info_city.split('·')
        posttime = posttime
        city = city
    # Hyperlink to listing       
        link = listing.find_element(By.CSS_SELECTOR, 'a.titlestring').get_attribute('href')
    # Price of listing, sometimes no price is listed so exception must be handled
        try:
            price = listing.find_element(By.CSS_SELECTOR, 'span.priceinfo').text
        except NoSuchElementException:
                price = 'None Listed'
    # Number of bedrooms of listing, sometimes no bedrooms are listed so exception must be handled
        try:
            bedrooms = listing.find_element(By.CSS_SELECTOR, 'span.post-bedrooms').text
        except NoSuchElementException:
                bedrooms = 'None Listed'
    # Sqft of listing, sometimes none is listed so exception must be handled
        try:
            sqft = listing.find_element(By.CSS_SELECTOR, 'span.post-sqft').text
        except NoSuchElementException:
                sqft = 'None Listed'

        apartment_listings.append({'Title': title, 'Price':price, '# of Bedrooms':bedrooms, 'sqft':sqft, 'City':city, 'Post Date':posttime, "Link":link})

# Save the results to a CSV file
df = pd.DataFrame(apartment_listings)
df.to_csv(f"craigslist_listings_filtered_for_{location_craigs}_{timestamp}.csv", index=False)

print("\n"+f"The above search with parameters has been saved to the path '{current_directory}' with the name craigslist_listings_filtered_for_{location_craigs}_{timestamp}.csv")
continue_exec_1 = input(f"Press any key to continue and scrape data for ALL listings in {location_craigs} or type 'exit' to quit:")
if continue_exec_1:
    continue_exec_1='exit'
    exit()


## RUN FOR SEARCH WITH NO PARAMETERS
    ## This means there will be a separate csv with ALL listings showed
driver.get(base_url_craigs_no_search_param)
print(f"Base URL with no parameters: {base_url_craigs_no_search_param}")
# Wait for the page to load
time.sleep(1)

# Find total number of listings
results = driver.find_elements(By.CSS_SELECTOR,'div.cl-search-paginator')
total_listings_no_param = None
for result in results:
    total_count_str_no_param = result.find_element(By.CSS_SELECTOR,'span.cl-page-number').text
    a,b,c,d,total_listings_no_param = total_count_str_no_param.split(' ')
print(f"Total Number of Listings with no Search Parameters: {total_listings_no_param}")

# Extract the search result items
apartment_listings_no_param = []

## Create loop and link for pages
total_listings_no_param = total_listings_no_param.replace(",", "")
page_string_craig_total_no_param = (int(total_listings_no_param) // 120) + 1
for page_string_craig_no_param in range(0,page_string_craig_total_no_param):
    driver.get(base_url_craigs_no_search_param+str(page_string_craig_no_param))
    print(f"Scraping Page {page_string_craig_no_param+1} at URL: {base_url_craigs_no_search_param+str(page_string_craig_no_param)}")
    
    listings = driver.find_elements(By.CSS_SELECTOR, 'li.cl-search-result')

    for listing in listings:
    # Title of listing
        title = listing.find_element(By.CSS_SELECTOR, 'a.titlestring').text
    # </div> class='meta' contains 3 pieces of data split by the character '·'
        # This element extracts those values and separates them
        posttime_info_city = listing.find_element(By.CSS_SELECTOR, 'div.meta').text
        try:
            posttime,randinfo,city = posttime_info_city.split('·')
        # Exception is required because sometimes the 'randinfo' is missing and there are only 2 pieces of data to split
        except ValueError:
            posttime,city = posttime_info_city.split('·')
        posttime = posttime
        city = city
    # Hyperlink to listing       
        link = listing.find_element(By.CSS_SELECTOR, 'a.titlestring').get_attribute('href')
    # Price of listing, sometimes no price is listed so exception must be handled
        try:
            price = listing.find_element(By.CSS_SELECTOR, 'span.priceinfo').text
        except NoSuchElementException:
                price = 'None Listed'
    # Number of bedrooms of listing, sometimes no bedrooms are listed so exception must be handled
        try:
            bedrooms = listing.find_element(By.CSS_SELECTOR, 'span.post-bedrooms').text
        except NoSuchElementException:
                bedrooms = 'None Listed'
    # Sqft of listing, sometimes none is listed so exception must be handled
        try:
            sqft = listing.find_element(By.CSS_SELECTOR, 'span.post-sqft').text
        except NoSuchElementException:
                sqft = 'None Listed'
    # Append extracted data to csv to be saved in next chunk   
        apartment_listings_no_param.append({'Title': title, 'Price':price, '# of Bedrooms':bedrooms, 'sqft':sqft, 'City':city, 'Post Date':posttime, "Link":link})

    
# Save the results to a CSV file
df = pd.DataFrame(apartment_listings_no_param)
df.to_csv(f"all_craigslist_listings_for_{location_craigs}_{timestamp}.csv", index=False)

print("\n"+f"The above search with no parameters has been saved to the path '{current_directory}' with the name all_craigslist_listings_for_{location_craigs}_{timestamp}.csv")

# Script Exit
print("\n"+"COMPLETE")
exit_prg = input("Press any key to exit:")
if exit_prg:
    driver.quit()
    exit()