import requests
from bs4 import BeautifulSoup

def decode_google_doc_grid(url: str):
    # Step 1: Fetch the document
    response = requests.get(url)
    response.raise_for_status()
    html = response.text

    # Step 2: Parse with BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")

    # Step 3: Find all table rows
    rows = soup.find_all("tr")

    points = []
    for row in rows:
        cells = row.find_all("td")
        if len(cells) != 3:
            continue  # Skip malformed rows

        try:
            x = int(cells[0].get_text(strip=True))
            char = cells[1].get_text(strip=True)
            y = int(cells[2].get_text(strip=True))
            points.append((char, x, y))
        except ValueError:
            continue  # Skip rows with bad data

    if not points:
        print("No character-position data found.")
        return

    # Step 4: Build grid
    max_x = max(x for _, x, _ in points)
    max_y = max(y for _, _, y in points)
    grid = [[" " for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    for char, x, y in points:
        grid[y][x] = char

    # Step 5: Print the secret message
    for row in grid:
        print("".join(row))


decode_google_doc_grid("https://docs.google.com/document/d/e/2PACX-1vTER-wL5E8YC9pxDx43gk8eIds59GtUUk4nJo_ZWagbnrH0NFvMXIw6VWFLpf5tWTZIT9P9oLIoFJ6A/pub")
