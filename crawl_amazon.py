from lxml import html  
import csv,os,json
import codecs
import requests
from exceptions import ValueError
from time import sleep

import sys
reload(sys)
sys.setdefaultencoding('utf8')

def AmzonParser(url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    page = requests.get(url,headers=headers)
    while True:
        sleep(3)
        try:
            doc = html.fromstring(page.content)
            XPATH_NAME = '//h1[@id="title"]//text()'
            XPATH_SALE_PRICE = '//span[contains(@id,"ourprice") or contains(@id,"saleprice")]/text()'
            XPATH_ORIGINAL_PRICE = '//td[contains(text(),"List Price") or contains(text(),"M.R.P") or contains(text(),"Price")]/following-sibling::td/text()'
            XPATH_CATEGORY = '//a[@class="a-link-normal a-color-tertiary"]//text()'
            XPATH_AVAILABILITY = '//div[@id="availability"]//text()'
            XPATH_AVGSTAR = '//*[@id="summaryStars"]/a/i/span//text()'
            
            #omit tbody which is auto inserted
            XPATH_5STAR = '//*[@id="histogramTable"]/tr[1]/td[3]/a//text()'
            XPATH_4STAR = '//*[@id="histogramTable"]/tr[2]/td[3]/a//text()'
            XPATH_3STAR = '//*[@id="histogramTable"]/tr[3]/td[3]/a//text()'
            XPATH_2STAR = '//*[@id="histogramTable"]/tr[4]/td[3]/a//text()'
            XPATH_1STAR = '//*[@id="histogramTable"]/tr[5]/td[3]/a//text()'


            RAW_NAME = doc.xpath(XPATH_NAME)
            RAW_SALE_PRICE = doc.xpath(XPATH_SALE_PRICE)
            RAW_CATEGORY = doc.xpath(XPATH_CATEGORY)
            RAW_ORIGINAL_PRICE = doc.xpath(XPATH_ORIGINAL_PRICE)
            RAw_AVAILABILITY = doc.xpath(XPATH_AVAILABILITY)
            RAW_AVGSTAR = doc.xpath(XPATH_AVGSTAR)
            RAW_5STAR = doc.xpath(XPATH_5STAR)
            RAW_4STAR = doc.xpath(XPATH_4STAR)
            RAW_3STAR = doc.xpath(XPATH_3STAR)
            RAW_2STAR = doc.xpath(XPATH_2STAR)
            RAW_1STAR = doc.xpath(XPATH_1STAR)


            NAME = ' '.join(''.join(RAW_NAME).split()) if RAW_NAME else None
            SALE_PRICE = ' '.join(''.join(RAW_SALE_PRICE).split()).strip() if RAW_SALE_PRICE else None
            CATEGORY = ' > '.join([i.strip() for i in RAW_CATEGORY]) if RAW_CATEGORY else None
            ORIGINAL_PRICE = ''.join(RAW_ORIGINAL_PRICE).strip() if RAW_ORIGINAL_PRICE else None
            AVAILABILITY = ''.join(RAw_AVAILABILITY).strip() if RAw_AVAILABILITY else None
            AVGSTAR = ' '.join(''.join(RAW_AVGSTAR).split()) if RAW_AVGSTAR else None

            STAR5 = int(' '.join(''.join(RAW_5STAR).split())) if RAW_5STAR else 0 # assign 0 is no star
            STAR4 = int(' '.join(''.join(RAW_4STAR).split())) if RAW_4STAR else 0
            STAR3 = int(' '.join(''.join(RAW_3STAR).split())) if RAW_3STAR else 0
            STAR2 = int(' '.join(''.join(RAW_2STAR).split())) if RAW_2STAR else 0
            STAR1 = int(' '.join(''.join(RAW_1STAR).split())) if RAW_1STAR else 0


            if not ORIGINAL_PRICE:
                ORIGINAL_PRICE = SALE_PRICE

            if page.status_code!=200:
                raise ValueError('captha')
            data = {
                    'NAME':NAME,
                    'SALE_PRICE':SALE_PRICE,
                    'CATEGORY':CATEGORY,
                    'ORIGINAL_PRICE':ORIGINAL_PRICE,
                    'AVAILABILITY':AVAILABILITY,
                    'URL':url,
                    'AVGSTAR': AVGSTAR,
                    'STAR_5': STAR5,
                    'STAR_4': STAR4,
                    'STAR_3': STAR3,
                    'STAR_2': STAR2,
                    'STAR_1': STAR1,
                    }

            return data
        except Exception as e:
            print (e)

def ReadAsin():
    # AsinList = csv.DictReader(open(os.path.join(os.path.dirname(__file__),"Asinfeed.csv")))
    AsinList = ['B00DTP2HGI',
    'B01KJ8EVIE',
    ]

    ## 'B01KJ138C6', 'B01M5LB4YT',
    extracted_data = []
    for i in AsinList:
        url = "http://www.amazon.co.jp/dp/"+i
        print ("Processing: "+url)
        extracted_data.append(AmzonParser(url))
        sleep(5)

    # dump as json
    with codecs.open('amazon_jp_data.json', 'w', encoding='utf-8') as f:
        json.dump(extracted_data, f, indent=4, ensure_ascii=False)

    # dump as csv

    with codecs.open("amazon_jp_data.csv", "w", encoding='utf-8') as f:
        csv_file = csv.writer(f)
        csv_file.writerow(
            ['Name', 
            'Category', 
            'Sale Price', 
            'Average Stars', 
            'Num of 5 Stars', 
            'Num of 4 Stars', 
            'Num of 3 Stars', 
            'Num of 2 Stars', 
            'Num of 1 Stars']
            )
        for item in extracted_data:
            csv_file.writerow([
                item['NAME'], 
                item['CATEGORY'],
                item['SALE_PRICE'], 
                item['AVGSTAR'],
                item['STAR_5'],
                item['STAR_4'],
                item['STAR_3'],
                item['STAR_2'],
                item['STAR_1'],
                ])


if __name__ == "__main__":
    ReadAsin()