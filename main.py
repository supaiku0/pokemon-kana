import requests
import csv
from bs4 import BeautifulSoup
from pprint import pprint

URL = "https://bulbapedia.bulbagarden.net/wiki/List_of_Japanese_Pok%C3%A9mon_names"
POKEMON_TOTAL = 807
OUTPUT_CSV = "pokemon.csv"

def strip(content):
    return content.get_text().strip()

req = requests.get(URL)
if req.status_code == 200:
    parsed = BeautifulSoup(req.content, "html.parser")

    pokelist = [None] * POKEMON_TOTAL

    # Look for tables with "roundy"-class
    tables = parsed.find_all("table", "roundy")

    for table in tables:
        # All name rows have the same style
        rows = table.find_all(style = "background:#FFF")

        for row in rows:
            # Id | Icon | English name | Kana | Romaji | Trademarked name
            data = row.find_all("td")
            pokemon = (
                strip(data[0]),
                strip(data[2]),
                strip(data[3]),
                strip(data[4]),
                strip(data[5])
            )

            pokelist[int(pokemon[0]) - 1] = pokemon

    with open(OUTPUT_CSV, "w+") as output_csv:
        wr = csv.writer(output_csv, quoting = csv.QUOTE_ALL)

        header = ["Id", "English", "Kana", "Romaji", "Trademark"]
        wr.writerow(header)
        wr.writerows(pokelist)

else:
    print(":(")
