import cloudscraper
import pandas as pd
import datetime
import time
import os
from bs4 import BeautifulSoup


START_DATE = datetime.date(2016, 12, 23)
END_DATE = datetime.date(2022, 2, 25)


def dates_gen():
    date = START_DATE

    while date <= END_DATE:
        new_date = date + datetime.timedelta(days=7)
        yield f'{date}--{new_date}'
        date = new_date


def get_df(soup):
    """Parses single Spotify Charts page.
    Exports rank table info pd.DataFrame.
    """

    data = {'position': [], 'track_id': [], 'title': [], 'artist': [], 'n_streams': []}

    rows = soup.find_all(class_='chart-table')[0].tbody.find_all('tr')
    for row in rows:
        position = row.find_all(class_='chart-table-position')[0].text
        data['position'].append(position)

        track_link = row.find_all(class_='chart-table-image')[0].a['href']
        track_id = track_link.split('/')[-1]
        data['track_id'].append(track_id)

        track_info = row.find_all(class_='chart-table-track')[0]
        title = track_info.strong.text
        data['title'].append(title)
        artist = ' '.join(track_info.span.text.split()[1:])
        data['artist'].append(artist)

        n_streams = row.find_all(class_='chart-table-streams')[0].text
        data['n_streams'].append(int(n_streams.replace(',', '')))

    return pd.DataFrame.from_dict(data)


if __name__ == '__main__':
    scraper = cloudscraper.create_scraper() # returns a CloudScraper instance

    req = scraper.get('https://spotifycharts.com/regional')
    soup = BeautifulSoup(req.content, 'html.parser')
    codes_html = soup.find_all(class_='responsive-select')[0].ul
    country_codes = [li['data-value'] for li in codes_html.find_all('li')]
    
    for country_code in country_codes:
        print(f'Scraping for {country_code}...')
        if os.path.isdir(f'./scraped_data/{country_code}'):
            print(f'Already scraped for {country_code}, skipping to next country...')
            continue

        os.mkdir(f'./scraped_data/{country_code}')

        for date in dates_gen():
            req = scraper.get(f'https://spotifycharts.com/regional/{country_code}/weekly/{date}')
            if not req.ok:
                print(f'No rank table for: {country_code}/weekly/{date}')
                time.sleep(1)
                continue

            soup = BeautifulSoup(req.content, 'html.parser')
            
            df = get_df(soup)
            df.to_csv(f'./scraped_data/{country_code}/{date}', index=False, sep=';')

            time.sleep(1)
        time.sleep(5)




    
    

