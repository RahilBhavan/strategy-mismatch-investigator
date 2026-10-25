# Checks that need a person

The automated checks cover Firefox, Chromium and WebKit on Linux and WebKit on macOS, plus axe-core rules, touch emulation and emulated forced colours. They cannot stand in for the checks below. Record each result in `verification/ACCEPTANCE-RECEIPT.md` with the date, device and software version. Leave a check marked unverified until someone has run it.

Start the demo with `python -m app.server --port 8807` and open http://127.0.0.1:8807. For a phone on your tailnet, start a separate throwaway instance on this machine's Tailscale address, and stop it afterwards:

```bash
python -m app.server --host "$(tailscale ip -4)" --port 8808 --db ~/scratch/smi-phone.sqlite3
```

Then open `http://<that address>:8808` on the phone.

## 1. Safari on a Mac (10 minutes)

1. To let the existing checks drive real Safari, run `safaridriver --enable` once in Terminal (it asks for your password). Or turn on Safari Settings › Advanced › "Show features for web developers", then Develop › "Allow Remote Automation". Either one is a deliberate security choice, so the agent did not change it for you.
2. By hand: run the first example (Compare totals, then Test the status selection). Check:
   - the result heading takes focus and sits below the dark banner;
   - the report menus are 44 px tall with an arrow;
   - Option+Tab reaches every button and link.

   Then open each evidence section and both exports.
3. Safari › Settings › Advanced › "Press Tab to highlight each item": switch it on and repeat with plain Tab.

## 2. VoiceOver (15 minutes)

Turn it on with Cmd+F5 and use Safari.

1. Press VO+U, then choose Headings. You should find "Explain the difference.", "Report comparison", the finding heading and "What this result rests on".
2. Activate Compare totals. VoiceOver should move to "Report comparison". Activate Test the status selection. It should read "The status selection explains the gap."
3. Read the reconciliation table with VO+arrows. Each row should be announced as a row header plus a number: 180, +40, 220, 220, 0.
4. Choose "Evidence unavailable" under Source & test controls and compare. The status message should be announced without moving focus.
5. Note anything read twice, read out of order, or not read at all. `verification/a11y-tree.txt` is the expected tree.

## 3. A phone (10 minutes)

Use any iPhone or Android phone in portrait.

- Tap through the first example. The answer should land on screen, with the ledger starting above the fold.
- No sideways page scroll. The records table may scroll sideways inside its panel, with a shadow at the edge.
- Every control should be easy to hit with a thumb.
- Pinch-zoom to 200%. The text should reflow, not clip.

## 4. Windows High Contrast (5 minutes)

On Windows, open Settings › Accessibility › Contrast themes, choose Night sky and use Edge. Check:

- the ledger rules and the double rule above "Remaining difference";
- the "Differs" and "Added by the test" marks;
- button borders and the focus outline.

The emulated version is `verification/r5-forced-colors-390-chromium.png`.

## 5. A session with a Strategy user (20 minutes)

The aim is to learn whether this answers a question they really have, not to demonstrate the tool. Ask someone who builds or checks Strategy reports. Don't help unless they're stuck for more than a minute.

1. "Tell me about the last time two reports disagreed. How did you find out why, and how long did it take?" Write down the minutes and the steps.
2. Hand over the first example with no explanation: "These two reports disagree. Find out why." Time how long they take to reach the ledger. Note where they hesitate.
3. "What would you send to whoever asked?" See whether they use the exports.
4. Switch to "Two selections differ". "What does the tool tell you here? Do you trust that?"
5. "What would it need to know about your reports to be useful on Monday?" Probe for the following:
   - prompts;
   - security filters;
   - derived metrics;
   - caching;
   - access rights.
6. "Would you use this instead of what you do now? What would stop you?"

Record the answers without paraphrasing, plus the times. One session doesn't establish usefulness. Treat three or more consistent sessions as a signal worth acting on.
