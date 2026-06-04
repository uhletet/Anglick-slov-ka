import csv
import random
import os


class Slovicka:

    def __init__(self):

        self.soubor = "slovicka.csv"
        self.rekord_soubor = "rekord.txt"

        self.slovicka = []
        self.zasobnik = []

        self.body = 0
        self.spatne = 0
        self.zivoty = 3

        self.rekord = 0

        # True = EN -> CZ
        # False = CZ -> EN
        self.smer = True

        self.aktualni = None

        self.nacti_slovicka()
        self.nacti_rekord()

    def nacti_slovicka(self):

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

        self.zasobnik = self.slovicka.copy()

    def nacti_rekord(self):

        if not os.path.exists(self.rekord_soubor):
            with open(self.rekord_soubor, "w") as f:
                f.write("0")

            self.rekord = 0
            return

        with open(self.rekord_soubor, "r") as f:

            obsah = f.read().strip()

            if obsah == "":
                self.rekord = 0
            else:
                self.rekord = int(obsah)

    def uloz_rekord(self):

        if self.body > self.rekord:

            self.rekord = self.body

            with open(self.rekord_soubor, "w") as f:
                f.write(str(self.rekord))

    def nastav_smer(self, smer):

        self.smer = smer

    def restart_hry(self):

        self.body = 0
        self.spatne = 0
        self.zivoty = 3

        self.zasobnik = self.slovicka.copy()

    def dalsi_slovo(self):

        if len(self.zasobnik) == 0:
            return None

        self.aktualni = random.choice(self.zasobnik)

        if self.smer:
            return self.aktualni["english"]
        else:
            return self.aktualni["czech"]

    def zkontroluj(self, odpoved):

        odpoved = odpoved.lower().strip()

        if self.smer:
            spravna = self.aktualni["czech"].lower().strip()
        else:
            spravna = self.aktualni["english"].lower().strip()

        if odpoved == spravna:

            self.body += 1

            if self.aktualni in self.zasobnik:
                self.zasobnik.remove(self.aktualni)

            self.uloz_rekord()

            return True, f"Správně! (+1 bod)"

        else:

            self.spatne += 1
            self.zivoty -= 1

            return False, f"Špatně! Správně je: {spravna}"

    def konec_hry(self):

        if self.zivoty <= 0:
            return True

        if len(self.zasobnik) == 0:
            return True

        return False

    def procenta(self):

        celkem = self.body + self.spatne

        if celkem == 0:
            return 0

        return round((self.body / celkem) * 100, 1)

    def pocet_slovicek(self):

        return len(self.slovicka)

    def zbyva_slovicek(self):

        return len(self.zasobnik)

    def progress(self):

        celkem = len(self.slovicka)

        if celkem == 0:
            return 0

        hotovo = celkem - len(self.zasobnik)

        return int((hotovo / celkem) * 100)