from bs4 import BeautifulSoup
import urllib.request
import re

wiki_url = "https://hearthstone.gamepedia.com/Battlegrounds"

'''
fetch the list of active BG heroes from gamepedia
'''
def fetch_hero_list():
    page = urllib.request.urlopen(wiki_url)
    soup = BeautifulSoup(page, 'html.parser')

    def hero_table(table):
        return table and table.th and re.compile("Hero").search(str(table.th.contents))

    tables = soup.find_all(hero_table)

    hero_table = tables[-1]

    table_rows = hero_table.td.find_all('div')

    heroes = []
    for row in table_rows:
        heroes.append(str(row.a.contents[0]))

    return heroes

if __name__ == "__main__":
    active_heroes = fetch_hero_list()
