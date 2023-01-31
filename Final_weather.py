from bs4 import *
from requests_html import HTMLSession
import requests
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
LANGUAGE = "en-US,en;q=0.5"

class Weather_scrapping:
    def internet_check(url, Internet=False):
        timeout = 5
        try:
            request = requests.get(url ,timeout=timeout)
            Internet = True
            print("Connected to the Internet")
        except (requests.ConnectionError, requests.Timeout) as exception:
            Internet = False
            print("No internet connection.")
        return Internet

    def get_weather_data(url):
        session = HTMLSession()
        session.headers['User-Agent'] = USER_AGENT
        session.headers['Accept-Language'] = LANGUAGE
        session.headers['Content-Language'] = LANGUAGE

        response = session.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        result = {}
        result['region'] = soup.find("div", attrs={"id": "wob_loc"}).text
        result['temp_now'] = soup.find("span", attrs={"id": "wob_tm"}).text
        result['dayhour'] = soup.find("div", attrs={"id": "wob_dts"}).text
        result['weather_now'] = soup.find("span", attrs={"id": "wob_dc"}).text

        result['precipitation'] = soup.find("span", attrs={"id": "wob_pp"}).text
        result['humidity'] = soup.find("span", attrs={"id": "wob_hm"}).text
        result['wind'] = soup.find("span", attrs={"id": "wob_ws"}).text

        next_days = []
        days = soup.find("div", attrs={"id": "wob_dp"})
        for day in days.findAll("div", attrs={"class": "wob_df"}):
            # extract the name of the day
            day_name = day.findAll("div")[0].attrs['aria-label']
            # get weather status for that day
            weather = day.find("img").attrs["alt"]
            temp = day.findAll("span", {"class": "wob_t"})
            max_temp = temp[0].text
            min_temp = temp[2].text
            next_days.append({"name": day_name, "weather": weather, "max_temp": max_temp, "min_temp": min_temp})

        result['next_days'] = next_days
        return result


if __name__ == "__main__":
    tempat = str(input("cuaca daerah yang ingin diketahui: "))
    URL = "https://www.google.com/search?q=weather+"+tempat

    print(URL)
    Weather_scrapping.internet_check(URL)
    import argparse

    parser = argparse.ArgumentParser(description="Parser")
    parser.add_argument("region", nargs="?", help="", default="")
    args = parser.parse_args()
    region = args.region
    URL += region
    # get data
    data =Weather_scrapping.get_weather_data(URL)
    Internet = True
    if Internet is True:
        print("Cuaca daerah:", data["region"])
        print("Cuaca hari:", data["dayhour"])
        print(f"Suhu terkini: {data['temp_now']}°C")
        print("Cuaca terkini:", data['weather_now'])
        print("Kelembapan:", data["humidity"])
        print("Angin:", data["wind"])

        print(" ")
        print("Prakiraan cuaca untuk seminggu kedepan:")
        if "Monday" in data["dayhour"] or "Senin" in data["dayhour"]:
            i = 0
        elif "Tuesday" in data["dayhour"] or "Selasa" in data["dayhour"]:
            i = 1
        elif "Wednesday" in data["dayhour"] or "Rabu" in data["dayhour"]:
            i = 2
        elif "Thursday" in data["dayhour"] or "Kamis" in data["dayhour"]:
            i = 3
        elif "Friday" in data["dayhour"] or "Jumat" in data["dayhour"]:
            i = 4
        elif "Saturday" in data["dayhour"] or "Sabtu" in data["dayhour"]:
            i = 5
        elif "Sunday" in data["dayhour"] or "Minggu" in data["dayhour"]:
            i = 6

        week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        safe = i
        while i < 7:
            next_url = "https://www.google.com/search?q=" + week[i] + "+weather+" + tempat
            next_data = Weather_scrapping.get_weather_data(next_url)
            weather_next_dict = {
                "region": next_data["region"],
                "day_hour": next_data["dayhour"],
                "weather_description": next_data['weather_now'],
                "precipitation": next_data["precipitation"],
                "humidity": next_data["humidity"],
                "wind": next_data["wind"]
            }
            print("Cuaca daerah:", next_data["region"])
            print("Cuaca hari:", next_data["dayhour"])
            print(f"Suhu terkini: {next_data['temp_now']}°C")
            print("Cuaca terkini:", next_data['weather_now'])
            print("Kelembapan:", next_data["humidity"])
            print("Angin:", next_data["wind"])
            print("-"*10)
            i += 1
        i = 0
        while i < safe:
            next_url = "https://www.google.com/search?q=" + week[i] + "+weather+" + tempat
            next_data = Weather_scrapping.get_weather_data(next_url)
            weather_next_dict = {
                "region": next_data["region"],
                "day_hour": next_data["dayhour"],
                "weather_description": next_data['weather_now'],
                "precipitation": next_data["precipitation"],
                "humidity": next_data["humidity"],
                "wind": next_data["wind"]
            }
            print("Cuaca daerah:", next_data["region"])
            print("Cuaca hari:", next_data["dayhour"])
            print(f"Suhu terkini: {next_data['temp_now']}°C")
            print("Cuaca terkini:", next_data['weather_now'])
            print("Kelembapan:", next_data["humidity"])
            print("Angin:", next_data["wind"])
            print("-"*10)
            i += 1