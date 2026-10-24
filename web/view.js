export const $ = selector => document.querySelector(selector);
export function esc(value) { return String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }
export function selection(value) { return value === null ? 'All values' : value.length ? value.join(', ') : 'No values'; }
export function amount(value) { return value === null || value === undefined ? 'Null' : new Intl.NumberFormat('en-US', {maximumFractionDigits:6}).format(value); }
// Value strings remain authoritative in the packet; the visual formatter must not coerce large exact decimals.
export function exact(value) {
  if (value === null || value === undefined) return 'Null';
  const [whole, fraction] = String(value).split('.');
  return whole.replace(/\B(?=(\d{3})+(?!\d))/g, ',') + (fraction && !/^0+$/.test(fraction) ? '.' + fraction : '');
}
export function message(text, error=false) {
  $('#message').className = text ? 'message' + (error ? ' error' : '') : '';
  $('#message').innerHTML = text ? `<p>${esc(text)}</p>` : '';
}
export function reportPicks(source) {
  $('#report-picks').className='report-picks';
  $('#report-picks').innerHTML = source.case.reports.map((report, index) => `<div class="report-pick"><label for="report-${index}">Report ${index ? 'B' : 'A'}</label><select id="report-${index}">${source.case.reports.map(r=>`<option value="${esc(r.id)}" ${r.id===report.id?'selected':''}>${esc(r.name)}</option>`).join('')}</select></div>`).join('');
  const refund=source.case.records.find(row=>row.status==='refunded');
  $('#amount').value=refund?.amount ?? '';
  $('#save-amount').disabled=!refund;
}
export function clearResult() {
  $('#comparison').innerHTML='<div class="empty"><p class="empty-mark" aria-hidden="true">A / B</p><h3>Ready to compare.</h3><p>Choose two reports to investigate. Their totals and context will appear here.</p></div>';
  $('#diagnosis').innerHTML=''; $('#evidence').innerHTML='';
}
export function renderResult(job, source) {
  const r=job.result;
  if(!r) return;
  const reports=source.case.reports;
  $('#comparison').innerHTML = r.originals.length ? `<table class="report-table"><caption class="hint">Illustrative values, computed from synthetic orders. Snapshot: ${esc(reports[0].snapshot||'not provided')}.</caption><thead><tr><th scope="col">Captured report</th><th scope="col">Total</th></tr></thead><tbody>${r.originals.map((o,i)=>`<tr><td><strong><span class="report-letter">${i?'B':'A'}</span>${esc(o.name)}</strong><div class="subline">Status: ${esc(selection(o.filters.status))}</div><div class="subline">Region: ${esc(selection(o.filters.region))}</div></td><td><span class="amount">${esc(exact(o.total))}</span><span class="unit">${esc(reports[i].unit || 'Unit not provided')}${!o.complete?' · incomplete':''}</span></td></tr>`).join('')}</tbody></table><div class="difference"><p>Difference <span class="muted">(B − A)</span>${r.percent_delta===null?'':'<br>'+esc(r.percent_delta)+'% relative to A'}</p><strong>${r.delta===null?'Not comparable':esc(exact(r.delta))}</strong></div>` : '<div class="empty"><h3>These totals need more context.</h3><p>The calculation or metadata is outside the supported scope.</p></div>';
  let headline=r.status==='candidate'?'One selection differs. Does it explain the gap?':r.status==='demonstrated'?'The status selection explains the gap.':r.status==='equal'?'The captured totals agree.':'The evidence does not isolate a cause.';
  const changes=r.differences.map(d=>`<div class="selection-diff"><span><b>A ${esc(d.field)}:</b> ${esc(selection(d.a))}</span><span><b>B ${esc(d.field)}:</b> ${esc(selection(d.b))}</span></div>`).join('');
  $('#source-tag').textContent=r.status==='unresolved'?'Context needs review':'Fixed synthetic snapshot';
  const exp=r.experiment;
  $('#diagnosis').innerHTML=`<article class="finding ${r.status} result-enter"><p class="eyebrow">${r.status==='demonstrated'?'Numerical cause demonstrated on synthetic data':r.status==='candidate'?'Candidate · not yet tested':r.status==='equal'?'Equal result · not semantic equivalence':'Unresolved · more evidence needed'}</p><h3>${headline}</h3><p>${esc(r.summary)}</p>${changes}${exp?`<dl class="experiment-values"><div><dt>B with A’s status selection</dt><dd>${esc(exact(exp.result.total))}</dd></div><div><dt>Measured change to B <small>(variant − original B)</small></dt><dd>${esc(exact(exp.impact))}</dd></div><div><dt>Remaining difference <small>(variant − A)</small></dt><dd>${esc(exact(r.residual))}</dd></div></dl><p class="caution">The original report definitions were not changed.</p>`:''}${r.status==='candidate'?'<button id="diagnose" class="primary">Test the status selection →</button><p class="hint">Rerun B with only A’s status selection. Preserve every other setting.</p>':''}${r.unknowns.length?`<ul class="unknowns">${r.unknowns.map(x=>`<li>${esc(x)}</li>`).join('')}</ul>`:''}</article>`;
  if(job.stale) message('Report context changed. Capture a new comparison.',true);
}
