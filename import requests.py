import requests
import re

def decode_google_doc_grid(url: str):
    # Step 1: Fetch the document's text content
    response = requests.get(url)
    response.raise_for_status()
    html = response.text

    # Step 2: Extract character and coordinates using regex
    pattern = re.compile(r"(.),\s*x=(\d+),\s*y=(\d+)")
    matches = pattern.findall(html)

    # Step 3: Convert to list of (char, x, y)
    points = [(char, int(x), int(y)) for char, x, y in matches]

    # Step 4: Determine the size of the grid
    max_x = max(x for _, x, _ in points)
    max_y = max(y for _, _, y in points)

    # Step 5: Initialize a grid filled with spaces
    grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    # Step 6: Fill the grid with characters
    for char, x, y in points:
        grid[y][x] = char

    # Step 7: Print the grid row by row
    for row in grid:
        print("".join(row))

# Run the function with the given Google Doc URL
decode_google_doc_grid("https://docs.google.com/document/d/e/2PACX-1vTER-wL5E8YC9pxDx43gk8eIds59GtUUk4nJo_ZWagbnrH0NFvMXIw6VWFLpf5tWTZIT9P9oLIoFJ6A/pub")