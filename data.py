import requests
import csv
from bs4 import BeautifulSoup

# URL of the website with the table
url = 'https://merolagani.com/LatestMarket.aspx'

# Send a GET request to the website
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find the table element by its class name
table = soup.find_all('table', {'class': 'table table-hover table-index'})[2]



with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Loop through the rows in the table
        # Extract the data from each cell in the row
    th = table.find_all('th')
    if th:
        writer.writerow([x.text for x in th])
        print([x.text for x in th])

    # Loop through the rows in the table
    for row in table.find_all('tr'):
        # Extract the data from each cell in the row
        cells = row.find_all('td')
        if cells:
            # Write the data from the cells in the row to the CSV file
            writer.writerow([x.text for x in cells])