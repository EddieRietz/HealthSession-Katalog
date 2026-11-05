import json

import os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
V = "2026-11-06"

# ---------------- Geraete (Typen; welches Gym was hat, steht lokal in der App) ----------------
geraete = [
    {"id": "latzugmaschine", "name": "Latzugmaschine", "kategorie": "maschine", "last": "steckgewicht", "stufe_kg": 5},
    {"id": "kabelzug", "name": "Kabelzug", "kategorie": "maschine", "last": "steckgewicht", "stufe_kg": 2.5},
    {"id": "beinpresse", "name": "Beinpresse", "kategorie": "maschine", "last": "steckgewicht", "stufe_kg": 10},
    {"id": "beinbeuger", "name": "Beinbeuger", "kategorie": "maschine", "last": "steckgewicht", "stufe_kg": 5},
    {"id": "beinstrecker", "name": "Beinstrecker", "kategorie": "maschine", "last": "steckgewicht", "stufe_kg": 5},
    {"id": "brustpresse", "name": "Brustpresse", "kategorie": "maschine", "last": "steckgewicht", "stufe_kg": 5},
    {"id": "schulterpresse", "name": "Schulterpresse", "kategorie": "maschine", "last": "steckgewicht", "stufe_kg": 5},
    {"id": "klimmzug-assistiert", "name": "Klimmzugstation, assistiert", "kategorie": "maschine", "last": "gegengewicht", "stufe_kg": 5},
    {"id": "kurzhanteln", "name": "Kurzhanteln", "kategorie": "frei", "last": "hantel", "stufe_kg": 2},
    {"id": "langhantel", "name": "Langhantel", "kategorie": "frei", "last": "scheiben", "stufe_kg": 2.5},
    {"id": "hantelbank", "name": "Hantelbank (verstellbar)", "kategorie": "zubehoer", "last": "keine", "stufe_kg": None},
    {"id": "matte", "name": "Matte", "kategorie": "zubehoer", "last": "koerpergewicht", "stufe_kg": None},
    {"id": "gewichtsweste", "name": "Gewichtsweste", "kategorie": "zubehoer", "last": "weste", "stufe_kg": 2.5},
    {"id": "ruderergometer", "name": "Ruderergometer", "kategorie": "cardio", "last": "widerstand", "stufe_kg": None},
]

# ---------------- Uebungen ----------------
def u(id, name, muster, primaer, sekundaer, geraete, wdh, hinweise, atmung="Bei Anstrengung ausatmen.", **progression):
    # progression: "assistenz" (Gegengewicht sinkt, bei 0 kg weiter mit `danach`), "zeit" (Sekunden, `zeit_schritt_s`), "keine"
    return {"id": id, "name": name, "muster": muster, "muskel_primaer": primaer, "muskel_sekundaer": sekundaer,
            "geraete": geraete, "wdh": wdh, "hinweise": hinweise, "atmung": atmung, **progression}

uebungen = [
    # vertikaler Zug
    u("latzug-breit", "Latzug, breiter Griff", "vertikaler-zug", "ruecken", ["bizeps", "hintere-schulter"], ["latzugmaschine"], [8, 12],
      ["Stange zur oberen Brust ziehen, nicht in den Nacken.", "Schultern zuerst nach unten ziehen, dann die Arme.", "Oben kontrolliert strecken."]),
    u("latzug-eng", "Latzug, enger Griff", "vertikaler-zug", "ruecken", ["bizeps"], ["latzugmaschine"], [8, 12],
      ["Ellbogen nah am Körper nach unten führen.", "Oberkörper leicht zurückgelehnt, nicht schwingen."]),
    u("klimmzug-assistiert", "Klimmzug, assistiert", "vertikaler-zug", "ruecken", ["bizeps", "core"], ["klimmzug-assistiert"], [6, 10],
      ["Mehr Gegengewicht = leichter.", "Brust zur Stange, unten ganz strecken."],
      progression="assistenz", danach="klimmzug-weste"),
    u("klimmzug-weste", "Klimmzug mit Gewichtsweste", "vertikaler-zug", "ruecken", ["bizeps", "core"], ["gewichtsweste", "klimmzug-assistiert"], [6, 10],
      ["Ohne Gegengewicht, Zusatzgewicht über die Weste.", "Brust zur Stange, unten ganz strecken, nicht schwingen."]),
    # horizontaler Zug
    u("kabelrudern-sitzend", "Rudern am Kabel, sitzend", "horizontaler-zug", "ruecken", ["bizeps", "hintere-schulter"], ["kabelzug"], [8, 12],
      ["Rücken gerade, Brust raus.", "Griff zum Bauchnabel ziehen, Schulterblätter zusammen."]),
    u("kh-rudern-einarmig", "Kurzhantel-Rudern, einarmig", "horizontaler-zug", "ruecken", ["bizeps"], ["kurzhanteln", "hantelbank"], [8, 12],
      ["Knie und Hand auf der Bank, Rücken flach.", "Hantel zur Hüfte ziehen, nicht zur Schulter."]),
    u("face-pulls", "Face Pulls am Kabel", "horizontaler-zug", "hintere-schulter", ["ruecken"], ["kabelzug"], [12, 15],
      ["Seil auf Augenhöhe, Hände neben die Ohren ziehen.", "Leichtes Gewicht, sauber ausführen."]),
    # Bizeps
    u("kh-curls", "Bizepscurls, Kurzhantel", "isolation-arme", "bizeps", [], ["kurzhanteln"], [8, 12],
      ["Ellbogen bleiben am Körper.", "Langsam ablassen, nicht schwingen."]),
    u("hammercurls-kabel", "Hammercurls am Kabel (Seil)", "isolation-arme", "bizeps", ["unterarm"], ["kabelzug"], [10, 15],
      ["Neutraler Griff, weniger Last auf dem Ellbogen.", "Oben kurz halten."]),
    u("kabel-curls", "Bizepscurls am Kabel", "isolation-arme", "bizeps", [], ["kabelzug"], [10, 15],
      ["Konstante Spannung über die ganze Bewegung."]),
    # horizontales Druecken
    u("brustpresse", "Brustpresse", "horizontales-druecken", "brust", ["trizeps", "vordere-schulter"], ["brustpresse"], [8, 12],
      ["Griffe auf Brusthöhe einstellen.", "Schulterblätter an die Lehne, nicht ganz durchstrecken."]),
    u("kh-bankdruecken", "Kurzhantel-Bankdrücken", "horizontales-druecken", "brust", ["trizeps", "vordere-schulter"], ["kurzhanteln", "hantelbank"], [8, 12],
      ["Füße fest am Boden, leichtes Hohlkreuz ok.", "Hanteln kontrolliert bis Brusthöhe ablassen."]),
    u("kh-schraegbank", "Kurzhantel-Schrägbankdrücken", "horizontales-druecken", "brust", ["vordere-schulter", "trizeps"], ["kurzhanteln", "hantelbank"], [8, 12],
      ["Bank auf ca. 30°.", "Ellbogen etwa 45° vom Körper."]),
    # vertikales Druecken
    u("schulterpresse", "Schulterpresse", "vertikales-druecken", "vordere-schulter", ["trizeps", "seitliche-schulter"], ["schulterpresse"], [8, 12],
      ["Griffe auf Schulterhöhe.", "Rücken an der Lehne, nicht ins Hohlkreuz drücken."]),
    u("kh-schulterdruecken", "Kurzhantel-Schulterdrücken, sitzend", "vertikales-druecken", "vordere-schulter", ["trizeps", "seitliche-schulter"], ["kurzhanteln", "hantelbank"], [8, 12],
      ["Bank aufrecht, Hanteln seitlich auf Ohrhöhe starten."]),
    # Schulter-Isolation
    u("seitheben-kh", "Seitheben, Kurzhantel", "isolation-schulter", "seitliche-schulter", [], ["kurzhanteln"], [12, 15],
      ["Arme leicht gebeugt bis Schulterhöhe heben.", "Leichtes Gewicht, kein Schwung."]),
    u("seitheben-kabel", "Seitheben am Kabel", "isolation-schulter", "seitliche-schulter", [], ["kabelzug"], [12, 15],
      ["Kabel hinter dem Körper, gleichmäßige Spannung."]),
    u("reverse-flys-kh", "Reverse Flys, Kurzhantel", "horizontaler-zug", "hintere-schulter", ["ruecken"], ["kurzhanteln", "hantelbank"], [12, 15],
      ["Brust auf die schräge Bank, Arme leicht gebeugt seitlich heben.", "Schulterblätter zusammen, leichtes Gewicht."]),
    # Nacken (Trapez)
    u("shrugs-kh", "Shrugs, Kurzhantel", "nacken", "nacken", [], ["kurzhanteln"], [10, 15],
      ["Schultern gerade nach oben zu den Ohren ziehen, nicht kreisen.", "Oben kurz halten, langsam ablassen."]),
    u("shrugs-kabel", "Shrugs am Kabel", "nacken", "nacken", [], ["kabelzug"], [10, 15],
      ["Griffe tief, Schultern nach oben ziehen.", "Kopf neutral, nicht nach vorn schieben."]),
    # Unterarm
    u("handgelenk-extension-kh", "Handgelenk-Strecken, Kurzhantel", "unterarm", "unterarm", [], ["kurzhanteln", "hantelbank"], [12, 20],
      ["Unterarm auf dem Oberschenkel oder der Bank, Handrücken oben.", "Nur das Handgelenk bewegt sich; sehr leichtes Gewicht."]),
    u("handgelenk-beugen-kh", "Handgelenk-Beugen, Kurzhantel", "unterarm", "unterarm", [], ["kurzhanteln", "hantelbank"], [12, 20],
      ["Unterarm aufgelegt, Handfläche oben.", "Langsam und schmerzfrei, nicht bis zur Ermüdung durchziehen."]),
    # Trizeps
    u("trizepsdruecken-kabel", "Trizepsdrücken am Kabel", "isolation-arme", "trizeps", [], ["kabelzug"], [10, 15],
      ["Ellbogen am Körper fixiert, nur der Unterarm bewegt sich."]),
    u("ueberkopf-trizeps-kabel", "Überkopf-Trizeps am Kabel", "isolation-arme", "trizeps", [], ["kabelzug"], [10, 15],
      ["Seil hinter den Kopf, Ellbogen zeigen nach vorne."]),
    # knie-dominant
    u("beinpresse", "Beinpresse", "knie-dominant", "quadrizeps", ["gesaess", "beinbeuger"], ["beinpresse"], [8, 12],
      ["Füße schulterbreit, Knie zeigen über die Zehen.", "Unten nicht den unteren Rücken abheben, oben nicht durchstrecken."]),
    u("goblet-squat", "Goblet Squat", "knie-dominant", "quadrizeps", ["gesaess", "core"], ["kurzhanteln"], [8, 12],
      ["Hantel vor der Brust, aufrecht bleiben.", "So tief wie mit geradem Rücken möglich."]),
    u("ausfallschritte-kh", "Ausfallschritte, Kurzhantel", "knie-dominant", "quadrizeps", ["gesaess"], ["kurzhanteln"], [8, 12],
      ["Großer Schritt, hinteres Knie Richtung Boden.", "Vorderes Knie bleibt stabil über dem Fuß."]),
    u("beinstrecker", "Beinstrecker", "knie-dominant", "quadrizeps", [], ["beinstrecker"], [10, 15],
      ["Drehpunkt auf Kniehöhe einstellen.", "Oben kurz halten, langsam ablassen."]),
    # hueft-dominant
    u("rdl-kh", "Rumänisches Kreuzheben, Kurzhantel", "hueft-dominant", "beinbeuger", ["gesaess", "unterer-ruecken"], ["kurzhanteln"], [8, 12],
      ["Hüfte nach hinten schieben, Rücken gerade.", "Hanteln nah an den Beinen bis knapp unter die Knie."]),
    u("beinbeuger-maschine", "Beinbeuger", "hueft-dominant", "beinbeuger", [], ["beinbeuger"], [10, 15],
      ["Drehpunkt auf Kniehöhe.", "Hüfte bleibt am Polster."]),
    u("hip-thrust-lh", "Hip Thrust, Langhantel", "hueft-dominant", "gesaess", ["beinbeuger"], ["langhantel", "hantelbank"], [8, 12],
      ["Schulterblätter an der Bank, Kinn zur Brust.", "Oben Gesäß anspannen, kein Hohlkreuz."]),
    # Core
    u("plank", "Unterarmstütz", "core", "core", [], ["matte"], [30, 60],
      ["Körper eine Linie, Bauch und Gesäß anspannen.", "Wiederholungen = Sekunden."], atmung="Ruhig weiteratmen.",
      progression="zeit", zeit_schritt_s=5),
    u("pallof-press", "Pallof Press am Kabel", "core", "core", [], ["kabelzug"], [10, 12],
      ["Seitlich zum Kabel, Griff vor der Brust nach vorne drücken.", "Nicht zum Kabel verdrehen lassen."]),
    u("kabel-crunch", "Kabel-Crunch, kniend", "core", "core", [], ["kabelzug"], [10, 15],
      ["Seil am Kopf, Oberkörper einrollen statt aus der Hüfte ziehen."]),
    # Cardio (Ergaenzung, kein Slot im Krafttraining)
    u("rudern-intervalle", "Rudern, Intervalle", "cardio", "ausdauer", [], ["ruderergometer"], [20, 20],
      ["z. B. 1 Min kräftig, 1 Min locker; Fortschritt über Watt oder 500-m-Zeit.", "Wiederholungen = Minuten gesamt."], atmung="Gleichmäßig atmen.",
      progression="keine"),
]

# ---------------- Einheiten (Vorlagen aus Slots) + Wochenpläne 2x–7x ----------------
def slot(id, name, muster, uebungen, saetze=3):
    return {"id": id, "name": name, "muster": muster, "uebungen": uebungen, "saetze": saetze}

# Übungslisten, erste = Default
KNIE_A = ["beinpresse", "goblet-squat", "ausfallschritte-kh"]
KNIE_B = ["goblet-squat", "ausfallschritte-kh", "beinpresse"]
STRECK = ["beinstrecker", "ausfallschritte-kh"]
HUEFT_A = ["rdl-kh", "hip-thrust-lh"]
HUEFT_B = ["hip-thrust-lh", "rdl-kh"]
BEUGER = ["beinbeuger-maschine", "rdl-kh"]
VZUG_A = ["latzug-breit", "klimmzug-assistiert", "latzug-eng", "klimmzug-weste"]
VZUG_B = ["klimmzug-assistiert", "latzug-eng", "latzug-breit", "klimmzug-weste"]
HZUG_A = ["kabelrudern-sitzend", "kh-rudern-einarmig"]
HZUG_B = ["kh-rudern-einarmig", "kabelrudern-sitzend"]
HINTEN = ["face-pulls", "reverse-flys-kh", "kh-rudern-einarmig"]
HDRUCK_A = ["brustpresse", "kh-bankdruecken", "kh-schraegbank"]
HDRUCK_B = ["kh-schraegbank", "kh-bankdruecken", "brustpresse"]
VDRUCK_A = ["schulterpresse", "kh-schulterdruecken"]
VDRUCK_B = ["kh-schulterdruecken", "schulterpresse"]
SEIT = ["seitheben-kabel", "seitheben-kh"]
SEIT_B = ["seitheben-kh", "seitheben-kabel"]
BIZ = ["kh-curls", "kabel-curls", "hammercurls-kabel"]
BIZ_B = ["hammercurls-kabel", "kh-curls", "kabel-curls"]
TRI = ["trizepsdruecken-kabel", "ueberkopf-trizeps-kabel"]
TRI_B = ["ueberkopf-trizeps-kabel", "trizepsdruecken-kabel"]
CORE = ["pallof-press", "plank", "kabel-crunch"]
CORE_B = ["kabel-crunch", "plank", "pallof-press"]

def E(id, name, slots, dauer):
    return {"id": id, "name": name, "dauer_min": dauer, "slots": slots}

einheiten = [
    # Ganzkörper – für 2x und 3x
    E("ganzkoerper-a", "Ganzkörper A", [
        slot("knie", "Knie-dominant", "knie-dominant", KNIE_A),
        slot("vzug", "Vertikaler Zug", "vertikaler-zug", VZUG_A),
        slot("hdruck", "Horizontales Drücken", "horizontales-druecken", HDRUCK_A),
        slot("huefte", "Hüft-dominant", "hueft-dominant", HUEFT_A),
        slot("seit", "Seitliche Schulter", "isolation-schulter", SEIT, 3),
        slot("bizeps", "Bizeps", "isolation-arme", BIZ, 2),
        slot("hinten", "Hintere Schulter", "horizontaler-zug", HINTEN, 2)], 60),
    E("ganzkoerper-b", "Ganzkörper B", [
        slot("huefte", "Hüft-dominant", "hueft-dominant", HUEFT_B),
        slot("hzug", "Horizontaler Zug", "horizontaler-zug", HZUG_A),
        slot("vdruck", "Vertikales Drücken", "vertikales-druecken", VDRUCK_A),
        slot("knie", "Knie-dominant", "knie-dominant", KNIE_B),
        slot("hdruck", "Horizontales Drücken", "horizontales-druecken", HDRUCK_B),
        slot("beuger", "Beinbeuger", "hueft-dominant", BEUGER, 2),
        slot("seit", "Seitliche Schulter", "isolation-schulter", SEIT_B, 2)], 60),
    E("ganzkoerper-c", "Ganzkörper C", [
        slot("knie", "Knie-dominant", "knie-dominant", ["ausfallschritte-kh", "goblet-squat", "beinpresse"]),
        slot("vzug", "Vertikaler Zug", "vertikaler-zug", VZUG_B),
        slot("hdruck", "Horizontales Drücken", "horizontales-druecken", ["kh-bankdruecken", "brustpresse", "kh-schraegbank"]),
        slot("beuger", "Beinbeuger", "hueft-dominant", BEUGER),
        slot("seit", "Seitliche Schulter", "isolation-schulter", SEIT_B, 3),
        slot("hzug", "Horizontaler Zug", "horizontaler-zug", HZUG_B, 2),
        slot("hinten", "Hintere Schulter", "horizontaler-zug", HINTEN, 2),
        slot("core", "Core", "core", CORE, 2)], 60),
    # Ober-/Unterkörper – für 4x und 5x
    E("oberkoerper-a", "Oberkörper A", [
        slot("hdruck", "Horizontales Drücken", "horizontales-druecken", HDRUCK_A),
        slot("vzug", "Vertikaler Zug", "vertikaler-zug", VZUG_A),
        slot("vdruck", "Vertikales Drücken", "vertikales-druecken", VDRUCK_A),
        slot("hzug", "Horizontaler Zug", "horizontaler-zug", HZUG_A),
        slot("hdruck2", "Schräg drücken", "horizontales-druecken", ["kh-schraegbank", "kh-bankdruecken"], 2),
        slot("seit", "Seitliche Schulter", "isolation-schulter", SEIT, 3),
        slot("bizeps", "Bizeps", "isolation-arme", BIZ, 2),
        slot("trizeps", "Trizeps", "isolation-arme", TRI, 2)], 55),
    E("unterkoerper-a", "Unterkörper A", [
        slot("knie", "Knie-dominant", "knie-dominant", KNIE_A),
        slot("huefte", "Hüft-dominant", "hueft-dominant", HUEFT_B),
        slot("streck", "Quadrizeps", "knie-dominant", STRECK, 2),
        slot("beuger", "Beinbeuger", "hueft-dominant", BEUGER),
        slot("core", "Core", "core", CORE)], 45),
    E("oberkoerper-b", "Oberkörper B", [
        slot("hzug", "Horizontaler Zug", "horizontaler-zug", HZUG_B),
        slot("hdruck", "Horizontales Drücken", "horizontales-druecken", HDRUCK_B),
        slot("vzug", "Vertikaler Zug", "vertikaler-zug", VZUG_B),
        slot("hdruck2", "Maschine drücken", "horizontales-druecken", ["brustpresse", "kh-bankdruecken"], 2),
        slot("seit", "Seitliche Schulter", "isolation-schulter", SEIT_B, 4),
        slot("hinten", "Hintere Schulter", "horizontaler-zug", HINTEN, 2),
        slot("trizeps", "Trizeps", "isolation-arme", TRI_B, 2),
        slot("bizeps", "Bizeps", "isolation-arme", BIZ_B, 2)], 55),
    E("unterkoerper-b", "Unterkörper B", [
        slot("huefte", "Hüft-dominant", "hueft-dominant", HUEFT_B),
        slot("knie", "Knie-dominant", "knie-dominant", KNIE_B),
        slot("beuger", "Beinbeuger", "hueft-dominant", BEUGER),
        slot("streck", "Quadrizeps", "knie-dominant", STRECK, 2),
        slot("core", "Core", "core", CORE_B)], 45),
    # Push / Pull / Beine – für 5x, 6x, 7x
    E("push-a", "Push A", [
        slot("hdruck", "Horizontales Drücken", "horizontales-druecken", HDRUCK_A),
        slot("vdruck", "Vertikales Drücken", "vertikales-druecken", VDRUCK_A),
        slot("hdruck2", "Schräg drücken", "horizontales-druecken", ["kh-schraegbank", "kh-bankdruecken"]),
        slot("seit", "Seitliche Schulter", "isolation-schulter", SEIT),
        slot("trizeps", "Trizeps", "isolation-arme", TRI)], 50),
    E("pull-a", "Pull A", [
        slot("vzug", "Vertikaler Zug", "vertikaler-zug", VZUG_A),
        slot("hzug", "Horizontaler Zug", "horizontaler-zug", HZUG_A),
        slot("hinten", "Hintere Schulter", "horizontaler-zug", HINTEN),
        slot("bizeps", "Bizeps", "isolation-arme", BIZ),
        slot("bizeps2", "Bizeps, neutral", "isolation-arme", BIZ_B, 2)], 50),
    E("beine-a", "Beine A", [
        slot("knie", "Knie-dominant", "knie-dominant", KNIE_A),
        slot("huefte", "Hüft-dominant", "hueft-dominant", HUEFT_B),
        slot("beuger", "Beinbeuger", "hueft-dominant", BEUGER),
        slot("streck", "Quadrizeps", "knie-dominant", STRECK, 2),
        slot("core", "Core", "core", CORE)], 50),
    E("push-b", "Push B", [
        slot("vdruck", "Vertikales Drücken", "vertikales-druecken", VDRUCK_B),
        slot("hdruck", "Horizontales Drücken", "horizontales-druecken", HDRUCK_B),
        slot("hdruck2", "Maschine drücken", "horizontales-druecken", ["brustpresse", "kh-bankdruecken"]),
        slot("seit", "Seitliche Schulter", "isolation-schulter", SEIT_B),
        slot("trizeps", "Trizeps", "isolation-arme", TRI_B)], 50),
    E("pull-b", "Pull B", [
        slot("hzug", "Horizontaler Zug", "horizontaler-zug", HZUG_B),
        slot("vzug", "Vertikaler Zug", "vertikaler-zug", VZUG_B),
        slot("hinten", "Hintere Schulter", "horizontaler-zug", HINTEN),
        slot("bizeps", "Bizeps", "isolation-arme", BIZ_B),
        slot("bizeps2", "Bizeps, Kabel", "isolation-arme", ["kabel-curls", "kh-curls"], 2)], 50),
    E("beine-b", "Beine B", [
        slot("huefte", "Hüft-dominant", "hueft-dominant", HUEFT_B),
        slot("knie", "Knie-dominant", "knie-dominant", KNIE_B),
        slot("beuger", "Beinbeuger", "hueft-dominant", BEUGER),
        slot("streck", "Quadrizeps", "knie-dominant", STRECK, 2),
        slot("core", "Core", "core", CORE_B)], 50),
    # leichter Tag für 7x
    E("core-ausdauer", "Core & Ausdauer (leicht)", [
        slot("cardio", "Rudern", "cardio", ["rudern-intervalle"], 1),
        slot("core", "Core", "core", CORE),
        slot("core2", "Core 2", "core", CORE_B, 2)], 35),
]

def plan(n, name, rotation, tage, satz_delta=0, hinweis=""):
    return {"id": f"{n}x", "frequenz": n, "name": name, "rotation": rotation, "tage_default": tage,
            "satz_delta": satz_delta, "hinweis": hinweis}

wochenplaene = [
    plan(2, "Ganzkörper A/B", ["ganzkoerper-a", "ganzkoerper-b"], ["mo", "do"], 1,
         "Hauptübungen 4 statt 3 Sätze, damit das Wochenvolumen trotz 2 Tagen reicht."),
    plan(3, "Ganzkörper A/B/C", ["ganzkoerper-a", "ganzkoerper-b", "ganzkoerper-c"], ["mo", "mi", "fr"]),
    plan(4, "Ober-/Unterkörper", ["oberkoerper-a", "unterkoerper-a", "oberkoerper-b", "unterkoerper-b"], ["mo", "di", "do", "fr"]),
    plan(5, "Push/Pull/Beine + Ober/Unter", ["push-a", "pull-a", "beine-a", "oberkoerper-b", "unterkoerper-b"], ["mo", "di", "mi", "fr", "sa"]),
    plan(6, "Push/Pull/Beine ×2", ["push-a", "pull-a", "beine-a", "push-b", "pull-b", "beine-b"], ["mo", "di", "mi", "do", "fr", "sa"], -1,
         "Isolationsslots 1 Satz weniger, damit sich die Muskeln zwischen den Tagen erholen."),
    plan(7, "Push/Pull/Beine ×2 + leichter Tag", ["push-a", "pull-a", "beine-a", "push-b", "pull-b", "beine-b", "core-ausdauer"],
         ["mo", "di", "mi", "do", "fr", "sa", "so"], -1, "Wie 6x, der 7. Tag ist bewusst leicht."),
]

training = {
    "standard_frequenz": 3, "blocklaenge_wochen": 6,
    "progression": {"regel": "Alle Sätze am oberen Ende des Wiederholungsbereichs bei Ziel-RIR → nächste Gewichtsstufe des Geräts"},
    "anstrengung": {
        "grund_muster": ["vertikaler-zug", "horizontaler-zug", "horizontales-druecken", "vertikales-druecken", "knie-dominant", "hueft-dominant"],
        "grund": {"rir": [1, 2], "pause_s": 120},
        "isolation": {"rir": [0, 1], "pause_s": 75},
        "hart_bis_rir": 3,
        "hinweis": "RIR = Wiederholungen im Tank am Satzende. Nur Sätze mit höchstens 3 RIR zählen als harte Sätze.",
    },
    "volumen": {"minimum_saetze": 8, "ziel_saetze": [10, 16], "ziel_saetze_diaet": [10, 14], "max_pro_muskel_einheit": 11,
                "regel": "Im Kaloriendefizit Volumen halten, nicht steigern."},
    "deload": {"dauer_tage": 7, "saetze_faktor": 0.6, "last": "halten", "rir": [3, 4],
               "vorschlag": "Am Blockende, wenn Übungen stocken und die Erholung schlecht ist; optional als letzte Blockwoche."},
    "satz_delta_regel": "satz_delta gilt nur für Slots mit Basis ≥ 3 Sätzen bei +1 und nur für Slots mit Basis ≤ 2 Sätzen bei −1 (Minimum 1).",
    "ruhetag": "Spaziergang",
    "schmerz_regionen": [
        {"id": "schulter", "name": "Schulter", "muster": ["horizontales-druecken", "vertikales-druecken", "isolation-schulter", "vertikaler-zug"]},
        {"id": "ellbogen", "name": "Ellbogen", "muster": ["isolation-arme", "unterarm", "vertikaler-zug", "horizontaler-zug", "horizontales-druecken"]},
        {"id": "handgelenk", "name": "Handgelenk", "muster": ["isolation-arme", "unterarm", "vertikaler-zug", "horizontaler-zug", "horizontales-druecken"]},
        {"id": "unterarm", "name": "Unterarm", "muster": ["isolation-arme", "unterarm", "vertikaler-zug", "horizontaler-zug", "horizontales-druecken"]},
        {"id": "knie", "name": "Knie", "muster": ["knie-dominant"]},
        {"id": "huefte", "name": "Hüfte", "muster": ["hueft-dominant", "knie-dominant"]},
        {"id": "ruecken", "name": "unterer Rücken", "muster": ["hueft-dominant", "knie-dominant"]},
        {"id": "nacken", "name": "Nacken", "muster": ["nacken", "vertikales-druecken"]},
    ],
    "standard_fokus": "ausgewogen",
    "fokus": [
        {"id": "ausgewogen", "name": "Ausgewogen", "beschreibung": "Alle Muskelgruppen nach Plan.", "anpassung": {}},
        {"id": "schulter-nacken", "name": "Schulter & Nacken",
         "beschreibung": "Mehr Rudern und hintere Schulter, gezielte Nacken- und Unterarmübungen, weniger Brust. Für viel Sitzen am PC und Verspannungen in Nacken, Schulter und Arm.",
         "anpassung": {"horizontales-druecken": -1, "horizontaler-zug": 1},
         "zusatz": {"slots": [
             {"id": "nacken", "name": "Nacken", "muster": "nacken", "uebungen": ["shrugs-kh", "shrugs-kabel"], "saetze": 2},
             {"id": "unterarm", "name": "Unterarm", "muster": "unterarm", "uebungen": ["handgelenk-extension-kh", "handgelenk-beugen-kh"], "saetze": 2}],
             "in_einheiten_mit_muster": ["horizontaler-zug", "vertikaler-zug"], "max_pro_woche": 3},
         "regel": "Anpassung gilt pro Slot nach satz_delta, Minimum 1 Satz. Pro Einheit mit Zug kommt ein Zusatz-Slot ans Ende, abwechselnd Nacken und Unterarm, höchstens 3x pro Woche. Rücken bekommt mindestens das 1,2- bis 1,5-Fache der Brust."},
    ],
}

json.dump({"version": V, "geraete": geraete}, open(f"{OUT}/geraete.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
json.dump({"version": V, "uebungen": uebungen}, open(f"{OUT}/uebungen.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
json.dump({"version": V, "training": training, "einheiten": einheiten, "wochenplaene": wochenplaene}, open(f"{OUT}/einheiten.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(len(geraete), "Geräte,", len(uebungen), "Übungen,", len(einheiten), "Einheiten")
