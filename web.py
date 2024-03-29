import requests
from bs4 import BeautifulSoup
import csv
import re
from unidecode import unidecode
from urllib.parse import unquote

with open('data.csv', 'w', newline='\n', encoding="utf-8") as csv_file:
    csv_writer = csv.writer(csv_file)
# URL of the Wikipedia article
url = "https://en.wikipedia.org/wiki/List_of_computer_scientists"

# HTTP GET request to the URL
response = requests.get(url)

if response.status_code == 200:
    # Parsing the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    mw_parser_output = soup.find('div', {'class': 'mw-parser-output'})

    # Find all the headings (section titles) within the "mw-parser-output" div
    list_items = mw_parser_output.find_all(['li'])

    scientist_links = []

    for item in list_items:
        link = item.find('a', href=True)
        if link:
            scientist_links.append("https://en.wikipedia.org" + link['href'])


    for link in scientist_links:
        scientist_response = requests.get(link)
        if scientist_response.status_code == 200:
            scientist_soup = BeautifulSoup(scientist_response.text, 'html.parser')

            # Extract info
            infobox_table = scientist_soup.find('table', {'class': 'infobox biography vcard'})

            if infobox_table:
                name1 = link.split("/")[-1].replace("_", " ")
                modified_name = re.sub(r'\([^)]*\)', '', name1).strip()
                name = unquote(modified_name)
                alma_mater = []
                awards = None

                for row in infobox_table.find_all("tr"):
                    header = row.find('th', {'class': 'infobox-label'})
                    data = row.find("td")
                    
                    if header and data:
                        header_text = header.get_text(strip=True)
                        data_text = data.get_text(strip=True)

                        if re.search(r"Alma\s*?mater", header_text, re.I):  # Match "Alma mater" with optional spaces ???? -> ερωτηση2
                            alma_mater_values = [almamater.get_text(strip=True) for almamater in data.find_all('a')] # get rid of: (BA, MA, PhD)
                            alma_mater.extend(alma_mater_values)

                        elif header_text == "Awards":
                            awards_count = len(data.find_all('a'))
                            awards = awards_count
                if awards is None:
                    awards = 0
                if not alma_mater:
                    continue
                alma_mater_final = [item for item in alma_mater if item not in ["MS", "BS", "BSc", "MSc", "PhD", "B.S.", "M.S.", "[1]", "BA", "MA", "[2]"]]
                alma_mater_str = '@'.join([value.replace(', ', ' ') for value in alma_mater_final])
                with open('data.csv', 'a', newline='\n', encoding="utf-8") as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow([name, alma_mater_str, awards])                
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

# to be solved
# -> some names have (computer scientist) next to them
# -> only latin characters