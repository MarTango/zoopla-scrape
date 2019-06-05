import csv
import os
from pprint import pprint

from zoopla import Zoopla

with open("listings.csv", "r") as f:
    reader = csv.DictReader(f)
    rows = [
        r
        for r in reader
        if "garage" in r["description"].lower() and int(r["num_bathrooms"]) > 1
    ]

print(len(rows))


def pull():
    """Populate listings.csv with results
    """
    zoopla = Zoopla(os.environ["API_KEY"])

    request = {
        "minimum_beds": 3,
        "maximum_price": 600,
        "page_size": 100,
        "listing_status": "rent",
        "area": "Soho, London",
        "radius": 7,
    }

    page_number = 1

    with open("listings.csv", "w") as f:
        writer = csv.DictWriter(f, [])

        while True:
            search = zoopla.property_listings({"page_number": page_number, **request})
            if not search.listing:
                break

            for i, result in enumerate(search.listing):
                if i == 0 and page_number == 1:
                    writer.fieldnames = result.keys()
                    writer.writeheader()
                    writer.writerow(result)

                    page_number += 1
