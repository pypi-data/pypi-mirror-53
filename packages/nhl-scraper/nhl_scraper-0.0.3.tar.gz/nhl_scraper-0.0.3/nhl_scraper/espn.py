#!/usr/bin/python

"""
A script that scrapes projections from ESPNs and outputs them to csv format.
It produces two files:
    espn.skaters.proj.csv   : Projections for all skaters
    espn.goalies.proj.csv   : Projections for all goalies
"""
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd


class ProjectionScraper:
    def __init__(self):
        pass

    def scrape(self, pick_goalies, num_pages):
        driver = webdriver.Chrome()
        file_names = []
        try:
            driver.maximize_window()
            driver.implicitly_wait(15)
            driver.get(self.url())
            driver.find_element_by_css_selector(".btn:nth-child(1) > span") \
                .click()
            if pick_goalies:
                driver.find_element_by_css_selector(
                    ".control:nth-child(4)").click()
            for pg_num in range(num_pages):
                time.sleep(5)
                fn = "espn_proj.{}.pg{}.html".format(
                    "goalies" if pick_goalies else "skaters", pg_num)
                with open(fn, "w") as f:
                    soup = BeautifulSoup(driver.page_source, "lxml")
                    f.write(soup.prettify())
                file_names.append(fn)
                driver.find_element_by_css_selector(
                    ".btn__icon:nth-child(3)").click()
        finally:
            driver.close()
        return file_names

    def url(self):
        return "https://fantasy.espn.com/hockey/players/projections"


class Parser:
    def __init__(self, file_name):
        with open(file_name, "rb") as f:
            self.soup = BeautifulSoup(f, "lxml")

    def parse(self, index_offset):
        names = self.parse_name(index_offset)
        proj = self.parse_projection(index_offset)
        df = names.join(proj)
        # Remove any players with missing projections
        if 'G' in df:
            df = df[df.G != '--']
        elif 'W' in df:
            df = df[df.W != '--']
        return df

    def parse_projection(self, index_offset):
        table = self.soup.find_all('table')[3]
        headings = [th.get_text().strip() for th in
                    table.find_all("thead")[1].find_all("th")]
        table_body = table.find('tbody')
        df = pd.DataFrame(data=[], columns=headings)
        rows = table_body.find_all('tr')
        for i, row in enumerate(rows):
            cols = [ele.text.strip() for ele in row.find_all('td')]
            df = df.append(pd.DataFrame(data=[cols], columns=headings,
                                        index=[i + index_offset]))
        return df

    def parse_name(self, index_offset):
        table = self.soup.find_all('table')[1]
        headings = ["Name", "Tm"]
        table_body = table.find('tbody')
        df = pd.DataFrame(data=[], columns=headings)
        rows = table_body.find_all('tr')
        for i, row in enumerate(rows):
            name = row.find_all('td')[1].text.strip().split("\n")[0]
            tm = row.find_all('td')[1].find_all(
                'span', {"class": "playerinfo__playerteam"})[0].text.strip()
            df = df.append(pd.DataFrame(data=[[name, tm]], columns=headings,
                                        index=[i + index_offset]))
        return df


def scrape_and_parse(pick_goalies, csv_file_name):
    sc = ProjectionScraper()
    file_names = sc.scrape(pick_goalies, 3 if pick_goalies else 5)

    df = None
    for fn in file_names:
        p = Parser(fn)
        if df is None:
            df = p.parse(0)
        else:
            df = df.append(p.parse(len(df.index)))
    df.to_csv(csv_file_name)


if __name__ == "__main__":
    scrape_and_parse(False, "espn.skaters.proj.csv")
    scrape_and_parse(True, "espn.goalies.proj.csv")
