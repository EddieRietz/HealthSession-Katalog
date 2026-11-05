// Health Session – Katalog-Validator
// Aufruf: bun scripts/validate.ts            → prüft alles, Exit 1 bei Fehlern
//         bun scripts/validate.ts --report   → schreibt zusätzlich build/report.json (Nährwerte, Wochenvolumen)

import { readFileSync, mkdirSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const ROOT = join(import.meta.dir, "..");
const errors: string[] = [];
const warnings: string[] = [];
const err = (m: string) => errors.push(m);
const warn = (m: string) => warnings.push(m);

// ---------- CSV ----------
function parseCsv(text: string): Record<string, string>[] {
  const rows: string[][] = [];
  let row: string[] = [], cell = "", quoted = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (quoted) {
      if (c === '"' && text[i + 1] === '"') { cell += '"'; i++; }
      else if (c === '"') quoted = false;
      else cell += c;
    } else if (c === '"') quoted = true;
    else if (c === ",") { row.push(cell); cell = ""; }
    else if (c === "\n" || c === "\r") {
      if (c === "\r" && text[i + 1] === "\n") i++;
      row.push(cell); cell = "";
      if (row.some((v) => v !== "")) rows.push(row);
      row = [];
    } else cell += c;
  }
  if (cell !== "" || row.length) { row.push(cell); rows.push(row); }
  const [head, ...body] = rows;
  return body.map((r) => Object.fromEntries(head.map((h, i) => [h, r[i] ?? ""])));
}

const num = (v: string | undefined) => (v === undefined || v === "" ? null : Number(v));
const load = (f: string) => JSON.parse(readFileSync(join(ROOT, f), "utf8"));

// ---------- Produkte ----------
const produkte = parseCsv(readFileSync(join(ROOT, "produkte.csv"), "utf8"));
const P = new Map<string, Record<string, string>>();
const KATEGORIEN = new Set(["Protein", "Huelsenfrucht", "Gemuese", "Obst", "Getreide", "Brot", "Fett", "Nuesse", "Getraenk", "Wuerze", "Ballaststoff", "Supplement"]);
const AMPEL = new Set(["gruen", "bedingt", "rot", "info", "pruefen"]);
const NUMERIC = ["kcal", "kj", "fett_g", "ges_fett_g", "mufa_g", "pufa_g", "kh_g", "zucker_g", "ballaststoffe_g", "protein_g", "salz_g", "dichte_g_ml", "stueck_g", "portion_menge", "packung_menge"];
const istZahlenspalte = (k: string) => NUMERIC.includes(k) || k === "basis" || /_(g|mg|ug)$/.test(k);

for (const p of produkte) {
  if (!/^[a-z0-9-]+$/.test(p.id)) err(`Produkt-ID ungültig: "${p.id}"`);
  if (P.has(p.id)) err(`Produkt-ID doppelt: ${p.id}`);
  P.set(p.id, p);
  if (!KATEGORIEN.has(p.kategorie)) err(`${p.id}: unbekannte Kategorie "${p.kategorie}"`);
  if (!AMPEL.has(p.ampel)) err(`${p.id}: unbekannte Ampel "${p.ampel}"`);
  for (const k of Object.keys(p).filter(istZahlenspalte)) {
    if (p[k] === "") continue;
    const x = Number(p[k]);
    if (!Number.isFinite(x)) err(`${p.id}: ${k} ist keine Zahl ("${p[k]}")`);
    else if (x < 0) err(`${p.id}: ${k} ist negativ`);
  }
  // Teiler in Skalierung und Küchenmaßen: 0 ergäbe NaN in der App.
  if (!(Number(p.basis || 100) > 0)) err(`${p.id}: basis muss größer als 0 sein`);
  for (const k of ["dichte_g_ml", "stueck_g"]) if (p[k] !== "" && !(Number(p[k]) > 0)) err(`${p.id}: ${k} muss größer als 0 sein`);
  if (!p.quelle) err(`${p.id}: Quelle fehlt`);
  if (p.basis_einheit === "g" || p.basis_einheit === "ml") {
    for (const k of ["kcal", "fett_g", "kh_g", "protein_g", "salz_g"]) if (p[k] === "") err(`${p.id}: Pflichtwert ${k} fehlt`);
    const f = (k: string) => num(p[k]) ?? 0;
    if (f("ges_fett_g") > f("fett_g") + 0.05) err(`${p.id}: gesättigte Fettsäuren > Fett`);
    if (f("zucker_g") > f("kh_g") + 0.05) err(`${p.id}: Zucker > Kohlenhydrate`);
    const calc = 9 * f("fett_g") + 4 * f("kh_g") + 4 * f("protein_g") + 2 * f("ballaststoffe_g");
    const kcal = f("kcal");
    if (kcal > 20 && Math.abs(calc - kcal) / kcal > 0.12) warn(`${p.id}: Etikett ${kcal} kcal, aus Makros ${Math.round(calc)} kcal`);
    if (p.ballaststoffe_g === "") warn(`${p.id}: Ballaststoffe nicht deklariert`);
    if (p.kategorie !== "Supplement" && p.dichte_g_ml === "" && p.stueck_g === "") warn(`${p.id}: weder Dichte noch Stückgewicht – Küchenmaße nicht möglich`);
  }
}

// ---------- Gerichte ----------
const G = load("gerichte.json");
const ROLLEN = new Set(Object.keys(G.rollen));
const SKAL = new Set(Object.keys(G.skalierung));
const TYPEN = new Set(["haupt", "beilage", "snack"]);
const gerichtIds = new Set<string>();
type Naehr = Record<string, number>;
const NKEYS = ["kcal", "protein_g", "fett_g", "ges_fett_g", "kh_g", "zucker_g", "ballaststoffe_g", "salz_g"];
const naehrwerte: Record<string, Naehr & { ballaststoffe_unvollstaendig: number }> = {};

for (const g of G.gerichte) {
  if (gerichtIds.has(g.id)) err(`Gericht-ID doppelt: ${g.id}`);
  gerichtIds.add(g.id);
}
for (const g of G.gerichte) {
  if (!TYPEN.has(g.typ)) err(`${g.id}: unbekannter Typ ${g.typ}`);
  if (!g.bausteine?.length) err(`${g.id}: keine Bausteine`);
  if (g.typ === "haupt") {
    if (!g.bausteine.some((b: any) => b.rolle === "protein")) err(`${g.id}: Hauptgericht ohne Proteinbaustein`);
    if (!g.bausteine.some((b: any) => b.rolle === "gemuese")) err(`${g.id}: Hauptgericht ohne Gemüse`);
    if (!g.schritte?.length) err(`${g.id}: keine Zubereitungsschritte`);
  }
  const t: any = Object.fromEntries(NKEYS.map((k) => [k, 0]));
  t.ballaststoffe_unvollstaendig = 0;
  for (const b of g.bausteine) {
    if (!ROLLEN.has(b.rolle)) err(`${g.id}: unbekannte Rolle ${b.rolle}`);
    if (!SKAL.has(b.skalierung)) err(`${g.id}: unbekannte Skalierung ${b.skalierung}`);
    if (!(b.menge_g > 0)) err(`${g.id}: Menge für ${b.produkt} fehlt`);
    const p = P.get(b.produkt);
    if (!p) { err(`${g.id}: Produkt ${b.produkt} existiert nicht`); continue; }
    if (p.kategorie === "Supplement") err(`${g.id}: Supplement ${b.produkt} als Zutat`);
    if (p.ampel === "rot") err(`${g.id}: ${b.produkt} steht auf der roten Liste`);
    if (p.ampel === "bedingt" && b.menge_g > (num(p.portion_menge) ?? 0) * 1.01) warn(`${g.id}: ${b.produkt} (bedingt) mit ${b.menge_g} g über Standardportion ${p.portion_menge} g`);
    for (const alt of b.tausch ?? []) if (!P.has(alt)) err(`${g.id}: Tausch-Alternative ${alt} existiert nicht`);
    for (const k of NKEYS) t[k] += (num(p[k]) ?? 0) * b.menge_g / 100;
    if (p.ballaststoffe_g === "") t.ballaststoffe_unvollstaendig = 1;
  }
  for (const be of g.beilagen ?? []) {
    const ziel = G.gerichte.find((x: any) => x.id === be);
    if (!ziel) err(`${g.id}: Beilage ${be} existiert nicht`);
    else if (ziel.typ !== "beilage") err(`${g.id}: ${be} ist keine Beilage`);
  }
  if (g.typ === "haupt" && !(g.beilagen ?? []).length) warn(`${g.id}: keine empfohlene Beilage`);
  for (const k of NKEYS) t[k] = Math.round(t[k] * 10) / 10;
  naehrwerte[g.id] = t;
  if (t.kcal > 150 && (t.ges_fett_g * 9) / t.kcal > 0.1) warn(`${g.id}: gesättigtes Fett ${Math.round((t.ges_fett_g * 900) / t.kcal)} % der kcal (Tagesziel < 7 %)`);
  if (t.salz_g > 2.5) warn(`${g.id}: ${t.salz_g} g Salz in einer Mahlzeit`);
}

// ---------- Training ----------
const GE = load("geraete.json").geraete;
const U = load("uebungen.json").uebungen;
// Vegetarisch: nur pflanzlich, Eier und Milchprodukte (Skyr/Quark). Fleisch und Fisch nie.
const HERKUNFT = ["pflanzlich", "ei", "milch", "unklar"];
for (const p of produkte) {
  if (!HERKUNFT.includes(p.herkunft)) err(`${p.id}: herkunft "${p.herkunft}" nicht erlaubt (nur ${HERKUNFT.join(", ")})`);
  else if (p.herkunft === "unklar" && p.kategorie !== "Supplement") warn(`${p.id}: herkunft unklar – Zutatenliste prüfen`);
  if (p.herkunft === "pflanzlich" && p.vegan !== "ja" && p.kategorie !== "Supplement") warn(`${p.id}: pflanzlich, aber nicht als vegan markiert`);
}

const E = load("einheiten.json");
const geraetIds = new Set(GE.map((x: any) => x.id));
const U_MAP = new Map<string, any>();
for (const u of U) {
  if (U_MAP.has(u.id)) err(`Übungs-ID doppelt: ${u.id}`);
  U_MAP.set(u.id, u);
  if (!u.geraete?.length) err(`${u.id}: kein Gerät`);
  for (const ge of u.geraete ?? []) if (!geraetIds.has(ge)) err(`${u.id}: Gerät ${ge} existiert nicht`);
  if (!u.hinweise?.length) err(`${u.id}: keine Ausführungshinweise`);
  if (!(Array.isArray(u.wdh) && u.wdh.length === 2 && u.wdh[0] <= u.wdh[1])) err(`${u.id}: Wiederholungsbereich ungültig`);
}
const einheitIds = new Set(E.einheiten.map((x: any) => x.id));
for (const e of E.einheiten) {
  for (const s of e.slots) {
    if (!s.uebungen?.length) err(`${e.id}/${s.id}: Slot ohne Übung`);
    for (const id of s.uebungen) {
      const u = U_MAP.get(id);
      if (!u) err(`${e.id}/${s.id}: Übung ${id} existiert nicht`);
      else if (u.muster !== s.muster) err(`${e.id}/${s.id}: ${id} hat Muster ${u.muster}, Slot erwartet ${s.muster}`);
    }
    if (s.uebungen.length < 2) warn(`${e.id}/${s.id}: nur eine Übung – kein Tausch möglich`);
  }
}
const HAUPT = ["ruecken", "brust", "quadrizeps", "beinbeuger", "gesaess", "seitliche-schulter", "bizeps", "trizeps"];
const TAGE = ["mo", "di", "mi", "do", "fr", "sa", "so"];
const volumen: Record<string, Record<string, number>> = {};
const volumenFokus: Record<string, Record<string, Record<string, number>>> = {};
const satzProEinheit: Record<string, Record<string, number>> = {};
const freq = new Set<number>();
const effSaetze = (basis: number, delta: number) =>
  delta > 0 && basis >= 3 ? basis + delta : delta < 0 && basis <= 2 ? Math.max(1, basis + delta) : basis;
const FOKUS = E.training?.fokus ?? [{ id: "ausgewogen", anpassung: {} }];
for (const fo of FOKUS) {
  for (const m of Object.keys(fo.anpassung ?? {}))
    if (!U.some((u: any) => u.muster === m)) err(`Fokus ${fo.id}: Muster ${m} unbekannt`);
  for (const s of fo.zusatz?.slots ?? []) for (const id of s.uebungen) {
    const u = U_MAP.get(id);
    if (!u) err(`Fokus ${fo.id}/${s.id}: Übung ${id} existiert nicht`);
    else if (u.muster !== s.muster) err(`Fokus ${fo.id}/${s.id}: ${id} hat Muster ${u.muster}, Slot erwartet ${s.muster}`);
  }
}
const SCHMERZ = E.training?.schmerz_regionen ?? [];
if (!SCHMERZ.length) err("training.schmerz_regionen fehlt");
const schmerzIDs = new Set<string>();
for (const r of SCHMERZ) {
  if (!r.id || !r.name) err(`schmerz_regionen: id/name fehlt`);
  if (schmerzIDs.has(r.id)) err(`schmerz_regionen: ${r.id} doppelt`);
  schmerzIDs.add(r.id);
  if (!r.muster?.length) err(`schmerz_regionen/${r.id}: keine Muster`);
  for (const m of r.muster ?? []) if (!U.some((u: any) => u.muster === m)) err(`schmerz_regionen/${r.id}: Muster ${m} unbekannt`);
}
const A = E.training?.anstrengung;
if (!A?.grund?.rir || !A?.isolation?.rir) err("training.anstrengung: RIR-Ziele fehlen");
const MAX_MUSKEL = E.training?.volumen?.max_pro_muskel_einheit ?? 11;
if (!FOKUS.some((fo: any) => fo.id === E.training?.standard_fokus)) err(`training.standard_fokus verweist auf keinen Fokus`);
for (const w of E.wochenplaene) {
  if (!(w.frequenz >= 2 && w.frequenz <= 7)) err(`Wochenplan ${w.id}: frequenz ${w.frequenz} außerhalb 2–7`);
  if (freq.has(w.frequenz)) err(`Wochenplan ${w.id}: frequenz ${w.frequenz} doppelt`);
  freq.add(w.frequenz);
  if (w.rotation?.length !== w.frequenz) err(`Wochenplan ${w.id}: ${w.rotation?.length} Einheiten in der Rotation, erwartet ${w.frequenz}`);
  if (w.tage_default?.length !== w.frequenz) err(`Wochenplan ${w.id}: ${w.tage_default?.length} Default-Tage, erwartet ${w.frequenz}`);
  for (const t of w.tage_default ?? []) if (!TAGE.includes(t)) err(`Wochenplan ${w.id}: Tag ${t} unbekannt`);
  if (new Set(w.tage_default).size !== w.tage_default?.length) err(`Wochenplan ${w.id}: Tag doppelt`);
  for (const fo of FOKUS) {
    const v: Record<string, number> = {};
    const spe: Record<string, number> = {};
    let zusatzRest = fo.zusatz?.max_pro_woche ?? 0;
    for (const id of w.rotation ?? []) {
      if (!einheitIds.has(id)) { if (fo === FOKUS[0]) err(`Wochenplan ${w.id}: Einheit ${id} existiert nicht`); continue; }
      const e = E.einheiten.find((x: any) => x.id === id);
      let summe = 0;
      const proMuskel: Record<string, number> = {};
      const mitZusatz = zusatzRest > 0 && e.slots.some((s: any) => (fo.zusatz?.in_einheiten_mit_muster ?? []).includes(s.muster));
      if (mitZusatz) zusatzRest--;
      const zs = fo.zusatz?.slots ?? [];
      const slots = mitZusatz ? [...e.slots, zs[((fo.zusatz.max_pro_woche ?? 0) - zusatzRest - 1) % zs.length]] : e.slots;
      for (const s of slots) {
        const istZusatz = !e.slots.includes(s);
        const n = istZusatz ? s.saetze : Math.max(1, effSaetze(s.saetze, w.satz_delta ?? 0) + (fo.anpassung?.[s.muster] ?? 0));
        const u = U_MAP.get(s.uebungen[0]);
        if (!u || u.muster === "cardio") continue;
        summe += n;
        v[u.muskel_primaer] = (v[u.muskel_primaer] ?? 0) + n;
        proMuskel[u.muskel_primaer] = (proMuskel[u.muskel_primaer] ?? 0) + n;
        for (const m of u.muskel_sekundaer) { v[m] = (v[m] ?? 0) + n * 0.5; proMuskel[m] = (proMuskel[m] ?? 0) + n * 0.5; }
      }
      spe[id] = summe;
      for (const [m, x] of Object.entries(proMuskel)) if (x > MAX_MUSKEL) warn(`Wochenplan ${w.id}/${id} (${fo.id}): ${m} ${x} Sätze in einer Einheit (über ${MAX_MUSKEL})`);
      if (summe > 24) warn(`Wochenplan ${w.id}/${id} (${fo.id}): ${summe} Sätze in einer Einheit (über 24)`);
    }
    (volumenFokus[fo.id] ??= {})[w.id] = v;
    if (fo.id === "ausgewogen") { volumen[w.id] = v; satzProEinheit[w.id] = spe; }
    for (const m of HAUPT) {
      const x = v[m] ?? 0;
      const min = (m === "brust" || m === "trizeps") && fo.id === "schulter-nacken" ? 4 : m === "bizeps" || m === "trizeps" ? 6 : 8; // Haltung: weniger Druck = bewusst weniger Brust und Trizeps
      if (x < min) warn(`Wochenplan ${w.id} (${fo.id}): ${m} ${x} Sätze/Woche (unter ${min})`);
      if (x > 24) warn(`Wochenplan ${w.id} (${fo.id}): ${m} ${x} Sätze/Woche (über 24)`);
    }
    if (fo.id === "schulter-nacken" && (v.ruecken ?? 0) < 1.5 * (v.brust ?? 0)) warn(`Wochenplan ${w.id} (haltung): Rücken ${v.ruecken} < 1,5 × Brust ${v.brust}`);
  }
}
for (let n = 2; n <= 7; n++) if (!freq.has(n)) err(`Kein Wochenplan für ${n}x pro Woche`);
if (!freq.has(E.training?.standard_frequenz)) err(`training.standard_frequenz verweist auf keinen Plan`);

// Begriffe (Info im Training)
const BG = load("begriffe.json");
const begriffIds = new Set<string>();
for (const g of BG.gruppen) for (const b of g.begriffe) {
  if (begriffIds.has(b.id)) err(`Begriff doppelt: ${b.id}`);
  begriffIds.add(b.id);
  if (!b.begriff?.trim() || !b.erklaerung?.trim()) err(`Begriff ${b.id}: Name oder Erklärung fehlt`);
  if (b.erklaerung.length > 320) warn(`Begriff ${b.id}: Erklärung über 320 Zeichen`);
}

const summary = { produkte: produkte.length, gerichte: G.gerichte.length, geraete: GE.length, uebungen: U.length, einheiten: E.einheiten.length, begriffe: begriffIds.size };
// Versionen werden als Text verglichen; ein Tippfehler würde jeden späteren Katalog verdrängen.
const morgen = new Date(Date.now() + 86_400_000).toISOString().slice(0, 10);
for (const f of ["gerichte.json", "geraete.json", "uebungen.json", "einheiten.json", "begriffe.json"]) {
  const v = load(f).version;
  if (!/^\d{4}-\d{2}-\d{2}$/.test(v) || v > morgen) err(`${f}: Version "${v}" ist kein Datum JJJJ-MM-TT bis morgen`);
}
console.log(`Katalog ${G.version}:`, summary);
for (const w of warnings) console.log("WARN ", w);
for (const e of errors) console.log("FEHLER", e);
console.log(`${errors.length} Fehler, ${warnings.length} Warnungen`);

if (process.argv.includes("--report")) {
  mkdirSync(join(ROOT, "build"), { recursive: true });
  writeFileSync(join(ROOT, "build/report.json"), JSON.stringify({ version: G.version, summary, errors, warnings, naehrwerte, wochenvolumen: volumen, wochenvolumen_fokus: volumenFokus, saetze_pro_einheit: satzProEinheit }, null, 2));
  console.log("→ build/report.json");
}
process.exit(errors.length ? 1 : 0);
