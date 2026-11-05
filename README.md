# Health Session – Katalog

Daten für die App **Health Session**: Produkte, Gerichte, Geräte, Übungen und Trainingseinheiten. Getrennt vom App-Code, damit neue Gerichte oder Übungen kein App-Release brauchen.

Der Katalog ist **vegetarisch**: pflanzlich plus Eier und Milchprodukte (Skyr, Quark). Fleisch und Fisch kommen nicht vor; die CI bricht ab, wenn ein Produkt eine andere `herkunft` hat.

Nichts Persönliches gehört hier hinein. Ziele, Ausschlussliste, Favoriten, kalibrierte Dichten, Gerätepark und Gewichte liegen nur lokal in der App.

## Dateien

| Datei | Inhalt |
|---|---|
| `produkte.csv` | Zutaten und Supplemente mit Nährwerten pro Basis (100 g, 100 ml oder Dosis), Dichte und Stückgewicht für Küchenmaße |
| `gerichte.json` | Haupt-, Beilagen- und Snack-Vorlagen aus Bausteinen mit Rollen |
| `geraete.json` | Gerätetypen im Gym mit Lastart und Default-Gewichtsstufe |
| `uebungen.json` | Übungen mit Bewegungsmuster, Muskelgruppen, Geräten, Wiederholungsbereich, Hinweisen |
| `begriffe.json` | Erklärungen für das Info-„i“ im Training (RIR, harter Satz, Deload …) |
| `einheiten.json` | Einheiten als Vorlagen aus Slots, plus je ein Wochenplan für 2–7 Trainingstage |

## produkte.csv

- `id`: stabil, kebab-case. Rezepte und App verweisen nur darauf.
- `basis` + `basis_einheit`: Bezug aller Nährwerte (`100 g`, `100 ml`, bei Supplementen `1 Tablette` / `Tagesdosis`).
- Leeres Feld = **nicht deklariert**, nicht null.
- `kategorie`: `Protein`, `Huelsenfrucht`, `Gemuese`, `Obst`, `Getreide`, `Brot`, `Fett`, `Nuesse`, `Getraenk`, `Wuerze`, `Ballaststoff`, `Supplement`.
- `herkunft`: `pflanzlich`, `ei`, `milch`, `unklar` (nur bei Supplementen geduldet, z. B. Kapselhülle unbekannt).
- Mischungen, die immer zusammen gegessen werden, sind **ein** Produkt mit gewichteten Werten, z. B. `proteinmix-erbse-reis` (2 Teile Erbse : 1 Teil Reis).
- `ampel`: `gruen`, `bedingt` (nur bis Standardportion), `rot` (nie in Gerichten), `info`, `pruefen`.
- `dichte_g_ml`, `stueck_g`: Richtwerte für die Umrechnung von Küchenmaßen; die App kalibriert sie lokal.
- `quelle`: Etikett (mit Foto-ID) oder Datenbank.
- Aminosäuren bei Proteinpulvern sind auf 100 g Pulver umgerechnet.

## gerichte.json

```json
{ "id": "linsen-dal", "typ": "haupt", "kueche": "indisch", "slots": ["mittag","abend"],
  "bausteine": [{ "rolle": "protein", "produkt": "rote-linsen-lidl", "menge_g": 90, "skalierung": "protein", "tausch": [] }],
  "aromen": [...], "schritte": [...], "beilagen": ["gurken-skyr-salat"], "tags": [...] }
```

- `typ`: `haupt`, `beilage`, `snack`.
- `rolle`: `protein`, `saettigung`, `gemuese`, `fett`, `geschmack`, `topping`, `basis`. Tauschen geht nur innerhalb einer Rolle.
- `skalierung`: `protein` (aufs Proteinziel der Mahlzeit), `min` (Untergrenze, darf wachsen), `frei` (passt sich dem Kalorienbudget an), `fix`.
- `menge_g`: Basisportion; die App skaliert und rundet auf Küchenmaße.
- `aromen`: Gewürze und Kräuter ohne Nährwertbeitrag.

## einheiten.json

- Einheit = Slots mit Bewegungsmuster; `uebungen` in Reihenfolge der Präferenz, die erste ist Default.
- Übungen bleiben einen Block lang fest (`blocklaenge_wochen`), Tauschen ist die Ausnahme.
- Die Historie hängt an der Übungs-ID, nicht am Slot.
- `training`: Standard-Frequenz, Blocklänge, Progressionsregel, Pausen.
- `wochenplaene`: ein Plan pro Frequenz (`2x` … `7x`). In der App wählt man, wie oft pro Woche trainiert wird, und die Wochentage; die App nimmt den passenden Plan und verteilt die `rotation` der Reihe nach auf die gewählten Tage (`tage_default` ist nur der Vorschlag).
- `satz_delta` passt den Workload an die Frequenz an: `+1` erhöht Hauptslots (≥ 3 Sätze) um einen Satz (2x), `−1` senkt Isolationsslots (≤ 2 Sätze) um einen Satz (6x, 7x).

| Frequenz | Split | Sätze pro Einheit |
|---|---|---|
| 2x | Ganzkörper A/B | 24 |
| 3x | Ganzkörper A/B/C | 19 |
| 4x | Ober-/Unterkörper A/B | 14–21 |
| 5x | Push/Pull/Beine + Ober/Unter | 14–21 |
| 6x | Push/Pull/Beine ×2 | 13–15 |
| 7x | wie 6x + leichter Core-/Rudertag | 4–15 |

**Schmerz-Regionen (`training.schmerz_regionen`)**: Auswahl im Schnellcheck vor dem Training. Jede Region nennt die Bewegungsmuster, die sie belastet; Übungen mit diesen Mustern werden nur für heute gegen die nächste Übung im Slot getauscht.

**Schwerpunkt (`training.fokus`)**: „Ausgewogen“ oder „Schulter & Nacken“. Letzteres nimmt jedem Slot mit horizontalem Drücken einen Satz weg, gibt jedem Slot mit horizontalem Zug (Rudern, Face Pulls, Reverse Flys) einen dazu und hängt an bis zu 3 Einheiten pro Woche mit Zug einen kurzen Zusatz-Slot an, abwechselnd Nacken (Shrugs) und Unterarm (Handgelenk strecken/beugen). Vorbild sind die Studien zu gezieltem Krafttraining bei Nacken-/Schulterbeschwerden im Büro. Bewusst keine Regler pro Muskel.

**Anstrengung (`training.anstrengung`)**: Ziel-RIR (Wiederholungen im Tank) Grundübungen 1–2, Isolation 0–1; nur Sätze mit ≤ 3 RIR zählen als hart. Pausen Grundübungen 120 s, Isolation 75 s. Progression erst, wenn alle Sätze oben im Bereich und beim Ziel-RIR sind.

**Volumen (`training.volumen`)**: Minimum 8 harte Sätze pro Muskel und Woche, Ziel 10–16 (in der Diät 10–14), höchstens 11 pro Muskel und Einheit. Im Defizit wird Volumen gehalten, nicht gesteigert.

**Deload (`training.deload`)**: 7 Tage mit 60 % der Sätze, Last halten, RIR 3–4. Wird am Blockende vorgeschlagen, wenn Übungen stocken und die Erholung schlecht ist.

Ziel: jede große Muskelgruppe ≥ 8 harte Sätze pro Woche (Arme ≥ 6, weil Zug- und Druckübungen sie mittrainieren), keine Einheit über 24 Sätze. Sekundäre Muskeln zählen halb.

## Prüfen

```bash
bun scripts/validate.ts            # Fehler → Exit 1
bun scripts/validate.ts --report   # zusätzlich build/report.json
```

Geprüft wird u. a.: IDs eindeutig und vorhanden, Pflichtwerte, Zucker ≤ KH, ges. Fett ≤ Fett, kcal plausibel zu den Makros, keine Supplemente oder rote Liste in Gerichten, Beilagen sind Beilagen, Slots passen zum Muster der Übung, nur vegetarische Herkunft, ein Plan für jede Frequenz 2–7, Wochenvolumen pro Plan und Muskelgruppe, Sätze pro Einheit.

## Auslieferung

Bei jedem Merge auf `main` prüft die CI. Die App lädt die Dateien per ETag von

```
https://raw.githubusercontent.com/EddieRietz/HealthSession-Katalog/main/
```

(änderbar unter Einstellungen → Katalog). Ein Snapshot liegt im App-Bundle und gilt, bis ein Download klappt. Gerechnet wird immer mit dem neuesten Katalog; Pläne merken sich nur, mit welcher `version` sie erstellt wurden.

## Generatoren

- `scripts/gen_training.py` erzeugt `geraete.json`, `uebungen.json` und `einheiten.json`. Änderungen am Training dort machen und neu generieren (`python3 scripts/gen_training.py`).
- `scripts/gen_begriffe.py` erzeugt `begriffe.json`.
- `produkte.csv` und `gerichte.json` werden direkt bearbeitet.
