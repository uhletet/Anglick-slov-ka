import csv


class SpravaSlovicek:

    def __init__(self, soubor="slovicka.csv"):

        self.soubor = soubor
        self.slovicka = []

        self.nacti()

    def nacti(self):

        self.slovicka.clear()

        try:
            with open(self.soubor, "r", encoding="utf-8") as f:

                ctecka = csv.DictReader(f, delimiter=";")

                for radek in ctecka:
                    self.slovicka.append(radek)

        except FileNotFoundError:

            with open(
                self.soubor,
                "w",
                newline="",
                encoding="utf-8"
            ) as f:

                zapisovac = csv.writer(f, delimiter=";")

                zapisovac.writerow(
                    ["english", "czech"]
                )

    def uloz(self):

        with open(
            self.soubor,
            "w",
            newline="",
            encoding="utf-8"
        ) as f:

            zapisovac = csv.writer(f, delimiter=";")

            zapisovac.writerow(
                ["english", "czech"]
            )

            for slovo in self.slovicka:

                zapisovac.writerow([
                    slovo["english"],
                    slovo["czech"]
                ])

    def pridej(self, english, czech):

        english = english.strip()
        czech = czech.strip()

        if english == "" or czech == "":
            return False

        self.slovicka.append({
            "english": english,
            "czech": czech
        })

        self.uloz()

        return True

    def smaz(self, index):

        if 0 <= index < len(self.slovicka):

            del self.slovicka[index]

            self.uloz()

            return True

        return False

    def uprav(
        self,
        index,
        nove_anglicky,
        nove_cesky
    ):

        if 0 <= index < len(self.slovicka):

            self.slovicka[index] = {

                "english": nove_anglicky.strip(),

                "czech": nove_cesky.strip()

            }

            self.uloz()

            return True

        return False

    def vsechna(self):

        return self.slovicka

    def pocet(self):

        return len(self.slovicka)

    def import_text(self, text):

        radky = text.splitlines()

        pridano = 0

        for radek in radky:

            if ";" in radek:

                casti = radek.split(";")

                if len(casti) >= 2:

                    anglicky = casti[0].strip()
                    cesky = casti[1].strip()

                    if anglicky and cesky:

                        self.slovicka.append({
                            "english": anglicky,
                            "czech": cesky
                        })

                        pridano += 1

        self.uloz()

        return pridano