from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


def getForenameDecade(url):
    options = webdriver.ChromeOptions()
    options.headless = True
    with webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()), options=options
    ) as driver:
        driver.get(url)

        print("Scraping:", driver.current_url)
        table = driver.find_element(By.CLASS_NAME, "t-stripe")
        rows = table.find_elements(By.TAG_NAME, "tr")
        tableData = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            rowData = []
            for cell in cells:
                rowData.append(cell.text)
            if len(rowData) > 1 and rowData[0].isdigit():
                tableData.append(rowData)
    return tableData


def writeForenameFile(year):
    url = f"https://www.ssa.gov/OACT/babynames/decades/names{year}s.html"
    fileName = f"forenames_{year}s.csv"
    header = "rank,maleName,number,femaleName,number"
    data = getForenameDecade(url)
    with open(fileName, "w", encoding="UTF8") as f:
        f.write(f"{url}\n")
        f.write(f"{header}\n")
        for row in data:
            row[0] = int(row[0])
            row[2] = int(row[2].replace(",", ""))
            row[4] = int(row[4].replace(",", ""))
            f.write(f"{row[0]},{row[1]},{row[2]},{row[3]},{row[4]}\n")


for year in range(1880, 2020, 10):
    writeForenameFile(year)
