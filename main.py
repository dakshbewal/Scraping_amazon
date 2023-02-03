from bs4 import BeautifulSoup
import requests
import time
import csv
import re




url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%252"
headers = {}

headers.update({ "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"})
headers.update({"accept-encoding": "gzip, deflate, br"})
headers.update({"session-token":"78zgvHLa3Q1wvXpb6SCmLkgh1+1/TK/qIOHQPKeLNXXzT/WtXUfYn3UqwketGLd6chkcJ4n419nKNk/V23rY6H2AkBCAgk0MoJGPW+SD21lq4zhgKoS3F7HeKdPsnjkOuTGGyEjDFSH0eu9Yv4A7/dP33ewLOW21/ScMPADYJX1QLICrkUVs/k6CzfZkUMasDTvM/I5QQWqqu7TGRToP41Kgfi3W7qGoi7HWukYVwefQfu74azll6A=="})
headers.update({"cookie": "lc-acbin=en_IN; ubid-acbin=257-2271288-2112718; session-id=258-1238619-2146911; s_vnum=2100519533504%26vn%3D2; s_nr=1670387917711-Repeat; s_dslv=1670387917711; csd-key=eyJ3YXNtVGVzdGVkIjp0cnVlLCJ3YXNtQ29tcGF0aWJsZSI6dHJ1ZSwid2ViQ3J5cHRvVGVzdGVkIjpmYWxzZSwidiI6MSwia2lkIjoiMjk5ZWQ5Iiwia2V5IjoiUDduTzB0SWh5U1haRXZvbWhVSitHeWRnRm8yRUt5Rm44UDg1bUNTNVBkdldNRmgwU3BLZ0M5MlZidGp0K2tPOHRoU0lEQXRtclpWenJSRUJkQm9OM2hldTNUVFRQVlM4QTBUTXNqWjVYWkRGS2oxWlNlVWRHbVdENDNHaVRlK3RCbHVDNkNaNFZlL2lYc3l3eW9XZ29zUHAxanlaZXJTTnQ2aThxOVJXd0JvYjlDd3dJK0tvUU9Palp1RFVrdUdKakNVYlN6NlRlTlB4N2pxTXZ2T2x4cFhWb0hnTmZiaU1zWVhWZlpGK2tOMjRvaTF3ZVdxbWZBR2FzRURSbytVbUlnakkyOHVkYjgrWFB5OXZocGtJUG9aODQ1Q1hDNkdXVlJNcmY5d2V6NDFLQmRmbS84Z1FhbnlNYm5LTnl0cE1BNTI2cTM1SkhnczN3ZFE5MnRzY2pBPT0ifQ==;"})
headers.update({"session-token":"z4yMtWZjfKyWLdbLr4HjBY214bpYvZ9p1SL2vCINip0E4YYJUHLaUuuMujYKNAxnxQ1kpbXrlAjVKRvt5gKz+/gzBg7OedLMd7/8MZlffZqZRfVM8n+amhntOzTV0UsbToe7y6YHpLZjME9ZdIdCxsRjxdSKxwytYODik8DDKjqAxDJhN+f0tBR3YqlmCsW4/VqV/hrbB+dFef12zkCHCujjbbGjrtmrEYy0Bg/Heq9ISDgIJgudzA=="})
headers.update({"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"})

res = requests.get(url, headers= headers)

soup = BeautifulSoup(res.content, 'html.parser')

table = soup.find('div', attrs = {'class':'s-main-slot s-result-list s-search-results sg-row'})

page_data = []

def getAllPageDetails():
    res1 = requests.get(url1, headers=headers)

    soup1 = BeautifulSoup(res1.content, 'html.parser')
    # print(soup1.prettify())

    table1 = soup1.find('div', attrs={'class': 's-main-slot s-result-list s-search-results sg-row'})
    # for loop to find all the desired data
    for row in table1.find_all('div',
                              attrs={'class': 'sg-col sg-col-4-of-12 sg-col-8-of-16 sg-col-12-of-20 s-list-col-right'}):

        p = {}
        p['product name'] = row.find('span', attrs={'class':'a-size-medium a-color-base a-text-normal'}).text

        p['url'] = "https://www.amazon.in" + row.find('a', attrs={
            'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})['href']


        # To bypass AttributeError caused by blanked data
        try:
            p['product price'] = row.find('span', attrs=
                                                {'class': 'a-price-whole'}).text
        except AttributeError:
            p['product price'] = 0

        try:
            p['Rating'] = row.find('span', attrs={'class': 'a-icon-alt'}).text
        except AttributeError:
            p['Rating'] = 0
        try:
            p['No. of reviews'] = \
                    row.find('span', attrs={'class': 'a-size-base s-underline-text'}).text
        except AttributeError:
            p['No. of reviews'] = 0

        page_data.append(p)


count = 1
# for loop for getting data of 20 pages
for i in range(20):
    page_url = table.find('a', attrs={'class': 's-pagination-item s-pagination-button'})
    final_page_url = page_url['href'].split("page")[0]
    url1 = f"https://www.amazon.in{final_page_url}page={count}"
    getAllPageDetails()
    count += 1
    time.sleep(0.000001)


filename = 'all_data.csv'

with open(filename, 'w',encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f,['product name', 'url', 'product price', 'Rating', 'No. of reviews'])
    w.writeheader()
    for quote in page_data:
        w.writerow(quote)


print(page_data[0])
all_url = []


with open('all_data.csv','r', encoding="utf-8") as file:
    csvreader = csv.reader(file)
    for row in csvreader:
        if "www" in row[1]:
            all_url.append(row[1])

selected_url = all_url[5]
print(selected_url)
response = requests.get(selected_url, headers=headers)

url_data = []

soup2 = BeautifulSoup(response.content, 'html.parser')
table1 = soup2.find(id='a-page')
url_count = 1

# Function to get data from each url
def urlData():
    selected_url = all_url[url_count]
    response = requests.get(selected_url, headers=headers)

    url_data = []

    soup2 = BeautifulSoup(response.content, 'html.parser')
    table1 = soup2.find(id='a-page')
    for row in table1.find_all('div', attrs={'id': 'dp-container'}):
        # print(row)
        product = {}
        desc = row.find(id="feature-bullets").text
        product['desc'] = desc
        try:
            product['Manufacturer'] = row.find('span', string=re.compile('.*Manufacturer.*')).next_sibling.next_sibling.text
        except AttributeError:
            product['Manufacturer'] = "Unknown"

        try:
            product['Asin'] = row.find('span', string=re.compile('.*ASIN.*')).next_sibling.next_sibling.text

        except AttributeError:
            product['Asin'] = "Unknown"

        print(product)
        url_data.append(product)

for i in range(200):
    urlData()
    url_count += 1
    time.sleep(0.0000000000001)

print(url_data)

filename1 = 'allurlData.csv'
with open(filename1, 'w',encoding="utf-8", newline="") as data:
    w = csv.DictWriter(data,['desc', 'Manufacturer', 'Asin'])
    w.writeheader()
    for data_url in url_data:
        w.writerow(data_url)