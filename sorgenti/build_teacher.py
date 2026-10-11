# -*- coding: utf-8 -*-
import json, sys
sys.path.insert(0, "/home/claude/build")
exec(open("/home/claude/build/build_docs.py", encoding="utf-8").read().split("# ---------- fogli alunno ----------")[0])

def bullets(doc, items, size=10):
    for t in items:
        p = doc.add_paragraph(); pf = p.paragraph_format
        pf.left_indent = Cm(0.6); pf.first_line_indent = Cm(-0.4); pf.space_after = Pt(3)
        set_font(p.add_run("•  "), size, True); set_font(p.add_run(t), size)

def grid(doc, header, rows, widths, hdr_color="#333333", size=9.5):
    t = doc.add_table(rows=1, cols=len(header)); set_widths(t, widths)
    for i, h in enumerate(header):
        c = t.rows[0].cells[i]; shade(c, hdr_color); cell_borders(c); cell_margins(c, 50, 50, 90, 90)
        set_font(first_para(c).add_run(h), size, True, color="#FFFFFF")
    for r in rows:
        cells = t.add_row().cells
        for i, v in enumerate(r):
            e = (4, "BBBBBB"); cell_borders(cells[i], top=e, left=e, bottom=e, right=e); cell_margins(cells[i], 40, 40, 90, 90)
            set_font(first_para(cells[i]).add_run(str(v)), size)
    set_widths(t, widths)
    return t

doc = new_doc()
pass
para(doc, "Dal film al libro: la Ferrovia del Gottardo", 18, True, after=1)
para(doc, "Guida e verifica per il docente", 12, False, True, "555555", after=8)

para(doc, "1. Prima dell’attività", 13, True, before=4, after=3)
bullets(doc, [
 "Attivare Pages (una volta sola): nel repository Gottardo-quiz, Settings → Pages → Branch «main», cartella «/ (root)» → Save. Dopo 1–2 minuti l’indirizzo https://nuovipercorsi123-sys.github.io/Gottardo-quiz/ mostra la scritta «Attività Gottardo».",
 "Prova obbligatoria: scansionare un QR dal foglio con un telefono non collegato a nessun tuo account. Deve aprirsi il quiz, senza chiedere accessi. Stampare i fogli solo dopo la prova.",
 "Stampa: 40 pagine, cioè 20 fogli fronte-retro. Il fronte contiene QR e frase, il retro le domande. In un gruppo cambia solo il QR (e «Alunno n.»).",
 "Gruppi: 4 gruppi da 5 (Escher, Favre, Airolo e Göschenen, Il cantiere). Ogni alunno riceve il foglio con il proprio QR.",
 "Il libro è unico per gruppo: i quiz non portano contenuti, guidano la lettura delle pagine.",
])
para(doc, "2. Come funziona, in breve", 13, True, before=8, after=3)
bullets(doc, [
 "Il titolare del QR legge ad alta voce domanda e risposte; gli altri cercano nel libro e dicono dove sta la risposta.",
 "Domande e risposte cambiano di ordine a ogni apertura. L’esito si vede solo alla fine: se c’è anche un solo errore si ricomincia, senza dire quale. Al terzo tentativo compare, per ogni quesito, la pagina da guardare.",
 "A quiz riuscito compaiono i punti chiave con la pagina e una parola della frase del gruppo, con il suo numero.",
 "Il gruppo scrive la risposta alla domanda con parole proprie e la copia sul foglio di tutti. Alla fine le cinque parole formano la frase.",
 "Le risposte non si registrano da nessuna parte: la verifica è sui fogli (frase + risposte scritte).",
])

para(doc, "3. Frasi di verifica", 13, True, before=10, after=2)
para(doc, "Controlla sui fogli che la frase sia giusta e nell’ordine giusto. Ogni parola può uscire solo da un quiz riuscito. Le frasi sono proposte mie: puoi cambiarle (basta dirmelo e rigenero le pagine).", 9.5, italic=True, color="555555", after=4)
for g in GROUPS:
    para(doc, f'{g["name"]} ({g["pages"]}):  «{" ".join(g["phrase"])}»', 11, True, color=g["color"], before=6, after=3, keep=True)
    rows = []
    for i, d in enumerate(g["domande"], 1):
        rows.append([f'{d["letter"]})', d["short"], f"Alunno {i}", d["pos"], g["phrase"][d["pos"] - 1], mp[f'{g["id"]}-{d["letter"]}']])
    grid(doc, ["", "Domanda", "Alunno", "Posizione", "Parola", "Codice pagina"], rows, [1.0, 6.0, 2.0, 2.2, 3.4, 2.8], g["color"])

doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
para(doc, "4. Scelte fatte e punti da confermare", 13, True, after=3)
bullets(doc, [
 "Domande rinumerate a–e in ogni gruppo. Escher: a) biografia e idea fondamentale, b) Sistema Escher, c) Credito Svizzero, d) anni difficili e memoria (con il dipinto di Koller), e) giudizio storico. La tua numerazione saltava la d) e aveva un «8»: ho letto «8» come giudizio storico.",
 "Cantiere a): «i tre compiti» (perforare, far brillare, allontanare il materiale), perché il testo ne elenca tre. Cantiere d): il perché del caldo non è nel libro, quindi la domanda diventa «che cosa succede alla temperatura e come si cerca di rimediare».",
 "Airolo e Göschenen d): ho aggiunto tra parentesi «prezzi, famiglie, nomi dei luoghi» per distinguerla da a) e b). Il disegno di Nieriker è dentro c).",
 "Favre e): confermato: i due ritratti sono quelli di p. 46 (incisione e disegno nell’ufficio di Göschenen); domanda e quiz sono stati riscritti di conseguenza.",
 "Sesta domanda uguale per tutti (film e libro), senza QR e senza quiz: la svolge il gruppo insieme.",
 "Locandina solo in apertura del foglio.",
 "Gli alunni di un gruppo possono scambiarsi i QR: non è un problema, perché i quesiti sono dello stesso gruppo.",
])
para(doc, "5. Spunti critici dal testo (per la discussione, non nei quiz)", 13, True, before=10, after=3)
bullets(doc, [
 "Airolo: il libro dice che la popolazione «quasi raddoppia» da 1’724 a 3’674, ma 3’674 / 1’724 è circa 2,1: più che raddoppiata. Inoltre i dati di Airolo e di Göschenen riguardano periodi diversi (Göschenen parte dal 1850), quindi i confronti diretti sono falsati.",
 "Göschenen: 2’285 residenti di lingua italiana su 2’843 sono circa l’80%, mentre il libro parla di stranieri «poco meno del 75%». Non tutti gli italofoni sono stranieri, quindi non è per forza un errore, ma è una buona domanda sulle fonti.",
 "Cantiere: il 34 °C è di febbraio 1880, mentre la frase parla di «temperatura media annua».",
 "Favre: otto anni dal contratto del 1872 portano al 1880, i lavori finiscono a fine 1881. Il libro parla di «minimo ritardo», ma con una penale di 10’000 franchi al giorno dopo sei mesi la causa agli eredi diventa comprensibile.",
 "Escher: «tre conflitti» evitati alla nazione è un giudizio del libro, senza spiegare quali.",
 "Immagini come fonti: il dipinto di Koller (1873) è un regalo commissionato dalla Direzione del Nord-Est; quello di Fleischer (1886) è posteriore di quattro anni all’apertura; la cartolina di Favre è celebrativa; il disegno di Nieriker documenta le condizioni di vita. La locandina del film è l’ultima fonte, la più recente e la più «costruita».",
 "Il libro racconta anche la morte di Favre (1879) e di Escher (1882): se la seconda parte del film non è ancora vista, i fogli lo segnalano agli alunni in una riga.",
], 9.5)

doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
para(doc, "6. Chiave delle risposte", 13, True, after=3)
para(doc, "Per ogni quiz: i quesiti con la risposta corretta e la pagina del libro.", 9.5, italic=True, color="555555", after=4)
for g in GROUPS:
    for d in g["domande"]:
        para(doc, f'{g["name"]} · {d["letter"]}) {d["short"]}   (codice {mp[g["id"]+"-"+d["letter"]]})', 10.5, True, color=g["color"], before=7, after=2, keep=True)
        rows = [[i, q["q"], q["o"][0], q["p"]] for i, q in enumerate(d["qs"], 1)]
        grid(doc, ["", "Quesito", "Risposta corretta", "Pagina"], rows, [0.8, 8.0, 7.0, 1.6], g["color"], 8.5)
doc.save(f"{OUT}/verifica_docente.docx")
print("ok")
