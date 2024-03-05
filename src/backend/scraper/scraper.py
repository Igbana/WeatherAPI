from bs4 import BeautifulSoup
from urllib.request import urlopen
from pprint import pprint


class Weather_API:
    '''
    Egg Inc.

    Weather API created by Egg Inc, a data analysis and soft technology startup company geering towards solving daily automation problems.
    Send feedbacks to igbanaaondosoo13@gmail.com and we will reply you soonest

    Neon at Egg Inc.
    '''
    def __init__(self, location):
        html = urlopen(f'https://www.msn.com/en-xl/weather/forecast/in-{location}')
        self.bs = BeautifulSoup(html.read(), 'html.parser')
        self.init_data()

    def init_data(self):
        '''
        Initializes variables from scraped data. Returns True if successful else false
        '''
        try:
            self.temps = self.bs.find(class_="tempLabels-E1_1").text.split('°')[:13]
            self.labels = self.bs.find(class_="newTimeLabels-E1_1").text
            self.rain = self.bs.find(class_="precipLabels-E1_1").text.split(';')[:13]
            self.wind = self.bs.find(id="CurrentDetailLineWindValue").text
            self.humidity = self.bs.find(id="CurrentDetailLineHumidityValue").text
            

            self.card = self.bs.find(class_="cardContainer-E1_2")
            self.card_labels = [i.text for i in self.bs.find_all(class_="headerV3-E1_1")]
            self.card_weathers = [i.attrs['title'] for i in self.bs.find_all(class_="iconTempPartIcon-E1_1")]
            self.card_svgs = [i.attrs['src'] for i in self.bs.find_all(class_="iconTempPartIcon-E1_1")]
            self.card_high_temp = [i.text for i in self.bs.find_all(class_="temp-E1_1")][::2]
            self.card_low_temp = [i.text for i in self.bs.find_all(class_="temp-E1_1")][1::2]
            print('Init Success')
            return True

        except Exception as e:
            print(e)
            self.init_data()
            return False
    
    def get_hourly_result(self):
        '''
        Method to get hourly weather results... To read return rain data from dict, get_hourly_result()[7am][rain]
        '''
        lbl = []
        for i in self.labels:
            if i == ' ':
                if not lbl[-2].isdigit():
                    lbl.insert(len(lbl)-1, i)
                else:
                    lbl.insert(len(lbl)-2, i)
            else:
                lbl.append(i.lower())
        self.labels = ''.join(lbl).split(' ')

        return {
            self.labels[i]: {
                'temp': self.temps[i],
                'rain': self.rain[i]
            } for i in range(len(self.labels))
        }

    def get_weather_result(self):
        '''
        Method to get daily weather results... To read return weather from dict, get_daily_result()[now][weather]
        '''
        return {
            self.card_labels[i]: {
                'wind': self.wind if self.card_labels[i] == 'today' else None,
                'humidity': self.humidity if self.card_labels[i] == 'today' else None,
                'time': self.get_hourly_result() if self.card_labels[i] == 'today' else None,
                'weather': self.card_weathers[i],
                'high_temp': self.card_high_temp[i],
                'low_temp': self.card_low_temp[i],
                'svg': self.card_svgs[i]
            }for i in range(len(self.card_labels))
        }


if __name__ == '__main__':
    obj = Weather_API('makurdi')
    print('Testing daily results:')
    pprint(obj.get_weather_result())