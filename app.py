from flask import Flask, render_template, request, redirect, send_file, session
from slovicka import Slovicka
from sprava_slovicek import SpravaSlovicek
from statistiky import Statistiky
from databaze import vytvor_db
ADMIN_HESLO = "SLOVO"
vytvor_db()


app = Flask(__name__)
app.secret_key = "tvoje_super_tajne_heslo_2026"

hra = Slovicka()
smer_en_cz = True
sprava = SpravaSlovicek()
stat = Statistiky()

aktualni_slovo = ""


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/procvicovani")
def procvicovani():

    global aktualni_slovo

    hra.nastav_smer(
        smer_en_cz
    )

    aktualni_slovo = hra.dalsi_slovo()

    return render_template(
        "procvicovani.html",
        slovo=aktualni_slovo,
        smer=smer_en_cz
    )


@app.route("/zkontroluj", methods=["POST"])
def zkontroluj():

    if hra.aktualni is None:
        hra.dalsi_slovo()

    odpoved = request.form["odpoved"]

    spravne, zprava = hra.zkontroluj(
        odpoved
    )

    if spravne:

        stat.pridej_spravne()

        stat.nastav_rekord(
            hra.body
        )

    else:

        stat.pridej_spatne()

    if hra.konec_hry():
        return render_template(
            "konec_hry.html",
            body=hra.body,
            rekord=hra.rekord,
            uspesnost=hra.procenta()
        )

    return render_template(
        "vysledek.html",
        zprava=zprava,
        body=hra.body,
        zivoty=hra.zivoty,
        srdicka="❤️" * hra.zivoty,
        progress=hra.progress()
    )
@app.route("/sprava")
def sprava_slovicek():

    if not session.get("admin"):
        return redirect("/login")

    sprava.nacti()

    return render_template(
        "sprava.html",
        slovicka=sprava.vsechna()
    )
@app.route("/pridej", methods=["POST"])
def pridej():
    if not session.get("admin"):
        return redirect("/login")

    anglicky = request.form["english"]
    cesky = request.form["czech"]

    sprava.pridej(
        anglicky,
        cesky
    )

    return render_template(
        "sprava.html",
        slovicka=sprava.vsechna()
    )
@app.route("/smaz/<int:index>")
def smaz(index):
    if not session.get("admin"):
        return redirect("/login")

    sprava.smaz(index)

    return render_template(
        "sprava.html",
        slovicka=sprava.vsechna()
    )
@app.route("/upravit/<int:index>")
def upravit_form(index):
    if not session.get("admin"):
        return redirect("/login")

    slovo = sprava.vsechna()[index]

    return render_template(
        "upravit.html",
        index=index,
        slovo=slovo
    )
@app.route("/uloz_upravu/<int:index>", methods=["POST"])
def uloz_upravu(index):
    if not session.get("admin"):
        return redirect("/login")

    anglicky = request.form["english"]
    cesky = request.form["czech"]

    sprava.uprav(
        index,
        anglicky,
        cesky
    )

    return render_template(
        "sprava.html",
        slovicka=sprava.vsechna()
    )
@app.route("/statistiky")
def statistiky():

    return render_template(
        "statistiky.html",
        spravne=stat.ziskej_spravne(),
        spatne=stat.ziskej_spatne(),
        rekord=stat.ziskej_rekord(),
        uspesnost=stat.uspesnost(),
        spusteni=stat.ziskej_spusteni(),
        pocet_slovicek=sprava.pocet()
    )
@app.route("/nastav_smer", methods=["POST"])
def nastav_smer():

    global smer_en_cz

    smer = request.form["smer"]

    if smer == "en_cz":
        smer_en_cz = True
    else:
        smer_en_cz = False

    return redirect("/procvicovani")

@app.route("/nova_hra")
def nova_hra():

    hra.restart_hry()

    return redirect("/procvicovani")

@app.route("/zalohovat")
def zalohovat():

    return send_file(
        "slovicka.csv",
        as_attachment=True
    )
@app.route("/obnovit", methods=["POST"])
def obnovit():
    if not session.get("admin"):
        return redirect("/login")

    soubor = request.files["soubor"]

    if soubor:

        soubor.save("slovicka.csv")

        sprava.nacti()
        hra.nacti_slovicka()

    return redirect("/sprava")
@app.route("/login")
def login():

    return render_template(
        "login.html"
    )


@app.route("/prihlasit", methods=["POST"])
def prihlasit():

    heslo = request.form["heslo"]

    if heslo == ADMIN_HESLO:

        session["admin"] = True

        return redirect("/sprava")

    return redirect("/login")
@app.route("/logout")
def logout():

    session.pop(
        "admin",
        None
    )

    return redirect("/")
if __name__ == "__main__":
    app.run(debug=True)

