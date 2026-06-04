from databaze import (
    pridej_slovicko,
    nacti_slovicka,
    smaz_slovicko,
    uprav_slovicko
)


class SpravaSlovicek:

    def __init__(self):

        self.slovicka = []

        self.nacti()

    def nacti(self):

        self.slovicka.clear()

        data = nacti_slovicka()

        for radek in data:

            self.slovicka.append({

                "id": radek[0],

                "english": radek[1],

                "czech": radek[2]

            })

    def pridej(self, english, czech):

        english = english.strip()
        czech = czech.strip()

        if english == "" or czech == "":
            return False

        pridej_slovicko(
            english,
            czech
        )

        self.nacti()

        return True

    def smaz(self, index):

        if 0 <= index < len(self.slovicka):

            id_slova = self.slovicka[index]["id"]

            smaz_slovicko(
                id_slova
            )

            self.nacti()

            return True

        return False

    def uprav(
        self,
        index,
        nove_anglicky,
        nove_cesky
    ):

        if 0 <= index < len(self.slovicka):

            id_slova = self.slovicka[index]["id"]

            uprav_slovicko(
                id_slova,
                nove_anglicky.strip(),
                nove_cesky.strip()
            )

            self.nacti()

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

                        pridej_slovicko(
                            anglicky,
                            cesky
                        )

                        pridano += 1

        self.nacti()

        return pridano