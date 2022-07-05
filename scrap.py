from bs4 import BeautifulSoup as bs
import requests
from fake_useragent import UserAgent

import json
import os


ua = UserAgent()

class Scraper:
    def __init__(self):
        self.total_received = 0
        self.approved_percent = 0
        self.average_weekly_approved = 0
        self.approved = 0
        self.declined = 0
        self.total_declined = 0
        self.declined_percentage = 0

        self.people_included = 0
        self.people_aproved = 0
        self.people_aproved_percent = 0
        self.people_average_weekly = 0
        self.base_dir = os.getcwd()

    def base_soup(self):
        url = 'https://www.immigration.govt.nz/new-zealand-visas/waiting-for-a-visa/how-long-it-takes-to-process-your-visa-application/2021-resident-visa-processing-times#:~:text=We%20are%20committed%20to%20processing,most%20being%20processed%20much%20faster.'
        request = requests.get(url, ua.random)
        soup = bs(request.text, 'html.parser')
        return soup

    def get_table_data(self):
        soup = self.base_soup()
        table = soup.find('table')
        tr = table.find_all('tr')
        return tr

    def get_data_from_rows(self):
        data = self.get_table_data()
        p = [row.find_all('p') for row in data]
        last_update = p[2][0].text
        json_context = []
        print(p[1][-1].text)
        for index,row in enumerate(p):
            if index > 1:
                json_context.append({
                    'date': row[0].text,
                    'applications_received': row[1].text.replace(',',''),
                    'total_people_included':row[2].text.replace(',',''),
                    'applications_approved':row[3].text.replace(',',''),
                    'people_approved': row[4].text.replace(',',''),
                    'declined': row[5].text.replace(',','')
                })
                self.total_received += int(str(row[1].text).replace(',',''))
                self.approved += int(str(row[3].text).replace(',',''))
                self.people_included += int(str(row[2].text).replace(',',''))
                self.people_aproved += int(str(row[4].text).replace(',',''))
            

        self.approved_percent = round(self.approved * 100 / self.total_received,2)
        self.declined_percentage = round(float(p[1][-1].text) * 100 / self.total_received,2)
        print(self.declined_percentage)
        self.average_weekly_approved = self.approved / len(p)-3

        self.people_aproved_percent = round(self.people_aproved * 100 / self.people_included, 2)
        self.people_average_weekly = self.people_aproved / len(p)-3

        
        
        context = {
            'total_approved':self.approved,
            'total_applied':self.total_received,
            'percent_aproved': self.approved_percent,
            'average_aproved': round(self.average_weekly_approved,1),
            'declined': self.declined,
            'percent_declined': self.declined_percentage,
            'total_declined': p[1][-1].text,
            'people_included': self.people_included,
            'people_approved':self.people_aproved,
            'people_percent' : self.people_aproved_percent,
            'people_average' : round(self.people_average_weekly,1),

            'time_process_total': round(((self.total_received - self.approved )/ self.average_weekly_approved)/52,1),
            'last_update':last_update
        }
        # json_context.reverse()
        self.jsonify_data(json_context)
        return context

    def jsonify_data(self,data):
        path = os.path.join(self.base_dir, "static/")
        with open(f"{path}visa_2021.json", "w") as file:
            file.write(json.dumps(data))


if __name__ == '__main__':
    app = Scraper()
    