import os
import json, html
G=[("saetze","Sätze & Wiederholungen",[
 ("wiederholung","Wiederholung (Wdh.)","Die Bewegung einmal ganz ausführen, z. B. einmal die Stange runterziehen und wieder hochlassen."),
 ("satz","Satz","Mehrere Wiederholungen am Stück, danach Pause. „3 × 8–12“ heißt: 3 Sätze mit je 8 bis 12 Wiederholungen."),
 ("wiederholungsbereich","Wiederholungsbereich","Die Spanne, in der du bleiben sollst, z. B. 8–12. Schaffst du überall das obere Ende, wird das Gewicht erhöht."),
 ("rir","RIR","„Reps in Reserve“: wie viele Wiederholungen du am Ende des Satzes noch sauber geschafft hättest. RIR 2 = noch 2 drin, RIR 0 = keine mehr. Die App fragt das nach dem letzten Satz einer Übung ab."),
 ("harter-satz","Harter Satz","Ein Satz, der nah an deine Grenze geht: höchstens 3 Wiederholungen im Tank. Nur harte Sätze zählen fürs Wochenvolumen."),
 ("pause","Pause","Zeit zwischen zwei Sätzen. Grundübungen 120 s, Isolationsübungen 75 s. Die Watch zählt mit."),
]),("fortschritt","Gewicht & Fortschritt",[
 ("arbeitsgewicht","Arbeitsgewicht","Das Gewicht, mit dem du die Sätze einer Übung gerade machst."),
 ("progression","Steigern (Progression)","Erst werden die Wiederholungen mehr, dann das Gewicht: Schaffst du alle Sätze am oberen Ende des Bereichs beim Ziel-RIR, schlägt die App die nächste Gewichtsstufe vor."),
 ("gewichtsstufe","Gewichtsstufe","Der kleinste Sprung, den ein Gerät erlaubt, z. B. 2,5 kg am Kabelzug. Stellst du im Gerätepark ein."),
 ("stockt","Stockt","Eine Übung hat 3 Wochen oder länger weder bei Gewicht noch bei Wiederholungen zugelegt. Das fließt in die Blockauswertung ein."),
 ("einstiegswoche","Einstiegswoche","Die erste Woche, wenn die App deine Gewichte noch nicht kennt. Du tastest dich Satz für Satz an ein Gewicht heran, bei dem noch 2–3 Wiederholungen im Tank sind."),
]),("plan","Plan",[
 ("grunduebung","Grundübung","Übung, die mehrere Gelenke und große Muskeln bewegt, z. B. Beinpresse, Rudern, Latzug, Brustpresse."),
 ("isolation","Isolationsübung","Übung für einen einzelnen Muskel, z. B. Bizepscurls, Seitheben, Beinbeuger."),
 ("slot","Slot","Ein Platz in der Einheit für ein Bewegungsmuster, z. B. „horizontaler Zug“. Im Slot stehen mehrere passende Übungen; die erste ist dein Standard, die anderen sind zum Tauschen."),
 ("wochenvolumen","Wochenvolumen","Wie viele harte Sätze ein Muskel pro Woche bekommt. Ziel 10–16. Hilft ein Muskel nur mit (z. B. Bizeps beim Rudern), zählt der Satz halb."),
 ("split","Split","Wie die Muskeln auf die Trainingstage verteilt werden: Ganzkörper (alles an jedem Tag), Ober-/Unterkörper oder Push/Pull/Beine (Drücken, Ziehen, Beine). Die App wählt ihn nach deinen Trainingstagen."),
 ("block","Block","4–8 Wochen (Standard 6), in denen deine Übungen gleich bleiben. So lässt sich Fortschritt messen. Am Ende gibt es eine Auswertung."),
 ("deload","Deload","Eine leichtere Woche zum Erholen: gleiches Gewicht, aber nur etwa 60 % der Sätze und mehr Luft im Tank."),
 ("schwerpunkt","Schwerpunkt","„Ausgewogen“ oder „Schulter & Nacken“: weniger Brustdrücken, mehr Rudern, dazu kurze Übungen für Nacken und Unterarm."),
]),("koerper","Körper & Erholung",[
 ("muskelkater","Muskelkater","Ziehen im Muskel 1–3 Tage nach dem Training. Normal und harmlos. Starker Muskelkater fließt in den Schnellcheck ein."),
 ("ruhepuls","Ruhepuls","Dein Puls in Ruhe, gemessen von der Watch. Steigt er über Tage an, ist das oft ein Zeichen für zu wenig Erholung."),
 ("hrv","HRV","Herzfrequenzvariabilität: wie stark der Abstand zwischen Herzschlägen schwankt. Höher als dein eigener Schnitt ist meist gut erholt. Die App vergleicht nur mit deinem eigenen Wochentrend."),
 ("magermasse","Magermasse","Alles außer Fett: Muskeln, Wasser, Knochen, Organe. Beim Abnehmen soll möglichst wenig davon verloren gehen."),
])]
json.dump({"version":"2026-11-05","gruppen":[{"id":g,"name":n,"begriffe":[{"id":i,"begriff":b,"erklaerung":e} for i,b,e in t]} for g,n,t in G]},
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","begriffe.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)
