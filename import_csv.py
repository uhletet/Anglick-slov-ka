import csv

from databaze import pridej_slovicko

with open(
    "slovicka.csv",
    "r",
    encoding="utf-8"
) as f:

    ctecka = csv.DictReader(
        f,
        delimiter=";"
    )

    for radek in ctecka:

        pridej_slovicko(
            radek["english"],
            radek["czech"]
        )

print("Hotovo")