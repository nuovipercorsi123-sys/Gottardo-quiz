# Sorgenti dell'attività Gottardo

Cartella di conservazione del lavoro (non serve al funzionamento del sito).

- `quizzes.py`: domande, risposte (la prima opzione è la corretta), pagine, punti chiave e frasi dei 4 gruppi.
- `template.html`: modello della pagina del quiz.
- `build_pages.py`: genera le 20 pagine HTML e `index.html`.
- `mappa.json`: quale codice (nome della pagina) corrisponde a quale quiz. Va tenuto: così i QR restano uguali.
- `build_docs.py`, `build_teacher.py`: generano le schede degli alunni e la guida per il docente.
- `test_pages.js`, `expected.json`: prova automatica dei 20 quiz.
- `qr/`: i 20 codici QR.
- `verifica_docente.docx`: guida per il docente con frasi e soluzioni.

Nota: i percorsi nei programmi puntano alla cartella di lavoro originale (`/home/claude/...`) e vanno adattati per rieseguirli. Le schede degli alunni (con le immagini del libro) non sono qui: vanno conservate a parte.
