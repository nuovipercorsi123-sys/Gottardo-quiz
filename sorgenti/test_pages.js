const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const exp = require('/home/claude/build/out/expected.json');
(async () => {
  const browser = await chromium.launch();
  let problems = 0, ok = 0;
  const shots = [];
  for (const [slug, e] of Object.entries(exp)) {
    const ctx = await browser.newContext({ viewport: { width: 390, height: 800 } });
    const page = await ctx.newPage();
    const errs = [];
    page.on('pageerror', x => errs.push(String(x)));
    page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    await page.goto('file:///home/claude/gottardo-quiz/' + slug + '.html');
    await page.click('button.btn:has-text("Inizia")');
    // tentativo 1: sbagliato di proposito (prima opzione che NON è corretta, all'ultimo quesito)
    async function runAttempt(wrongAt, expectHelp) {
      const n = Object.keys(e.qs).length;
      for (let i = 0; i < n; i++) {
        const qtext = await page.locator('.q').innerText();
        const info = e.qs[qtext];
        if (!info) { console.log('QUESITO NON TROVATO', slug, qtext); problems++; return; }
        const help = await page.locator('.hint').count();
        if (expectHelp !== (help > 0)) { console.log('AIUTO', slug, 'atteso', expectHelp, 'trovato', help); problems++; }
        if (expectHelp) {
          const h = await page.locator('.hint').innerText();
          if (!h.includes('pagina ' + info.p)) { console.log('PAGINA AIUTO ERRATA', slug, h, info.p); problems++; }
        }
        const opts = await page.locator('.opt').allInnerTexts();
        // le etichette A-D sono nel primo span: togli la prima riga
        const texts = opts.map(t => t.replace(/^[A-E]\s*\n?/, '').trim());
        let idx = texts.findIndex(t => t === info.ok);
        if (idx < 0) { console.log('OPZIONE CORRETTA NON TROVATA', slug, qtext, texts); problems++; return; }
        if (i === wrongAt) idx = (idx + 1) % texts.length;
        await page.locator('.opt').nth(idx).click();
        await page.locator('.btn:not(.ghost)').click();
      }
    }
    await runAttempt(0, false);
    let t = await page.locator('h1').innerText();
    if (t !== 'Non ancora') { console.log('ATTESO FALLIMENTO', slug, t); problems++; }
    let body = await page.locator('main').innerText();
    if (body.includes(e.word)) { console.log('PAROLA TRAPELATA', slug); problems++; }
    await page.click('button.btn:has-text("Ricomincia")');
    await runAttempt(1, false);
    t = await page.locator('h1').innerText();
    if (t !== 'Non ancora') { console.log('ATTESO FALLIMENTO 2', slug, t); problems++; }
    body = await page.locator('main').innerText();
    if (!body.includes('Al prossimo tentativo troverete un aiuto')) { console.log('MANCA AVVISO AIUTO', slug); problems++; }
    await page.click('button.btn:has-text("Ricomincia")');
    await runAttempt(-1, true);
    t = await page.locator('h1').innerText();
    if (!t.startsWith('Giusto')) { console.log('ATTESO SUCCESSO', slug, t); problems++; }
    body = await page.locator('main').innerText();
    if (!body.includes(e.word) || !body.toLowerCase().includes('parola n. ' + e.pos)) { console.log('PAROLA ERRATA', slug); problems++; }
    if (slug === Object.keys(exp)[0] || slug === Object.keys(exp)[11]) { await page.screenshot({ path: '/home/claude/build/out/shot_' + slug + '_ok.png', fullPage: true }); }
    if (errs.length) { console.log('ERRORI JS', slug, errs); problems++; }
    else ok++;
    await ctx.close();
  }
  // schermate di esempio: intro, quesito, aiuto
  const ctx = await browser.newContext({ viewport: { width: 390, height: 800 } });
  const page = await ctx.newPage();
  const slug = Object.keys(exp)[0];
  await page.goto('file:///home/claude/gottardo-quiz/' + slug + '.html');
  await page.screenshot({ path: '/home/claude/build/out/shot_intro.png', fullPage: true });
  await page.click('button.btn:has-text("Inizia")');
  await page.locator('.opt').nth(1).click();
  await page.screenshot({ path: '/home/claude/build/out/shot_q.png', fullPage: true });
  // verifica che l'ordine delle risposte cambi tra tentativi
  const orders = new Set();
  for (let k = 0; k < 8; k++) {
    await page.goto('file:///home/claude/gottardo-quiz/' + slug + '.html');
    await page.click('button.btn:has-text("Inizia")');
    orders.add((await page.locator('.q').innerText()) + '|' + (await page.locator('.opt').allInnerTexts()).join('/'));
  }
  console.log('ordini distinti su 8 aperture:', orders.size);
  await browser.close();
  console.log('pagine ok:', ok, 'problemi:', problems);
})();
