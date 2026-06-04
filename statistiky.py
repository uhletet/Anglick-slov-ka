import json
import os


class Statistiky:

    def __init__(self):

        self.soubor = "statistiky.json"

        self.data = {
            "spravne": 0,
            "spatne": 0,
            "rekord": 0,
            "spusteni": 0
        }

        self.nacti()

    def nacti(self):

        if not os.path.exists(self.soubor):
            self.uloz()
            return

        try:

            with open(
                    self.soubor,
                    "r",
                    encoding="utf-8"
            ) as f:

                self.data = json.load(f)

        except:

            self.uloz()

    def uloz(self):

        with open(
            self.soubor,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.data,
                f,
                ensure_ascii=False,
                indent=4
            )

    def pridej_spravne(self, pocet=1):

        self.data["spravne"] += pocet
        self.uloz()

    def pridej_spatne(self, pocet=1):

        self.data["spatne"] += pocet
        self.uloz()

    def pridej_spusteni(self):

        self.data["spusteni"] += 1
        self.uloz()

    def nastav_rekord(self, rekord):

        if rekord > self.data["rekord"]:

            self.data["rekord"] = rekord
            self.uloz()

    def ziskej_spravne(self):

        return self.data["spravne"]

    def ziskej_spatne(self):

        return self.data["spatne"]

    def ziskej_rekord(self):

        return self.data["rekord"]

    def ziskej_spusteni(self):

        return self.data["spusteni"]

    def uspesnost(self):

        celkem = (
            self.data["spravne"] +
            self.data["spatne"]
        )

        if celkem == 0:
            return 0

        return round(
            self.data["spravne"] /
            celkem * 100,
            1
        )

    def reset(self):

        self.data = {
            "spravne": 0,
            "spatne": 0,
            "rekord": 0,
            "spusteni": 0
        }

        self.uloz()