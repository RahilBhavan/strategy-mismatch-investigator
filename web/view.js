export const $ = selector => document.querySelector(selector);
export function esc(value) { return String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }
export function selection(value) { return value === null ? 'All values' : value.length ? value.join(', ') : 'No values'; }
export function amount(value) { return value === null || value === undefined ? 'Null' : new Intl.NumberFormat('en-US', {maximumFractionDigits:6}).format(value); }
// Value strings remain authoritative in the packet; the visual formatter must not coerce large exact decimals.
export function exact(value) {
  if (value === null || value === undefined) return 'Null';
  const text = String(value), negative = text.startsWith('-');
  const [whole, fraction] = text.replace(/^-/, '').split('.');
  return (negative ? '−' : '') + whole.replace(/\B(?=(\d{3})+(?!\d))/g, ',') + (fraction && !/^0+$/.test(fraction) ? '.' + fraction : '');
}
export const signed = value => (String(value).startsWith('-') || /^0(\.0+)?$/.test(String(value)) ? '' : '+') + exact(value);
// A nonzero change that rounds to 0.00% reads as "under 0.01%" rather than a misleading zero.
export function percent(value, delta) {
  const text=String(value), zero=/^-?0(\.0+)?$/;
  if(!zero.test(text)) return text.replace(/^-/,'−')+'%';
  return zero.test(String(delta)) ? '0%' : 'less than 0.01% '+(String(delta).startsWith('-')?'below':'above');
}
export const matches = (row, filters) => Object.entries(filters).every(([key, values]) => values === null || values.includes(row[key]));
// Records the transient selection brings into B: the visible link between the source table and the ledger.
export function addedRecords(job, source) {
  const exp = job.result?.experiment;
  if (!exp) return [];
  const before = job.result.originals[1].filters;
  return source.case.records.filter(row => matches(row, exp.result.filters) && !matches(row, before));
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
  const reports=source.case.reports, sameUnit=Boolean(reports[0].unit)&&reports[0].unit===reports[1].unit;
  $('#comparison').innerHTML = r.originals.length ? `<table class="report-table" role="table"><caption class="hint">${sameUnit?'Illustrative values, computed':'Computed'} from synthetic orders.${sameUnit?'':!reports[0].unit||!reports[1].unit?` ${!reports[0].unit?'A':'B'}’s unit is not provided.`:' The units differ; each total shows its own.'}${reports[0].snapshot===reports[1].snapshot?` Snapshot for both: <span class="nowrap">${esc(reports[0].snapshot||'not provided')}</span>.`:''}</caption><thead role="rowgroup"><tr role="row"><th scope="col" role="columnheader">Captured report</th><th scope="col" role="columnheader">Total</th></tr></thead><tbody role="rowgroup">${r.originals.map((o,i)=>`<tr role="row"><td role="cell"><strong><span class="report-letter">${i?'B':'A'}</span>${esc(o.name)}</strong><div class="subline">Status: ${esc(selection(o.filters.status))}</div><div class="subline">Region: ${esc(selection(o.filters.region))}</div>${reports[0].snapshot===reports[1].snapshot?'':`<div class="subline">Snapshot: <span class="nowrap">${esc(reports[i].snapshot||'not provided')}</span></div>`}</td><td role="cell"><span class="amount">${esc(exact(o.total)).replace(/,/g,',<wbr>')}</span><span class="unit">${esc(reports[i].unit || 'Unit not provided')}${!o.complete?' · incomplete':''}</span></td></tr>`).join('')}</tbody></table><div class="difference"><p>Difference <span class="muted">(B − A)</span>${r.percent_delta===null?'':'<br>'+esc(percent(r.percent_delta,r.delta))+(/^less/.test(percent(r.percent_delta,r.delta))?' A':' relative to A')}</p><strong>${r.delta===null?'Not comparable':esc(exact(r.delta))}</strong></div>` : '<div class="empty"><h3>These totals need more context.</h3><p>The calculation or metadata is outside the supported scope.</p></div>';
  let headline=r.status==='candidate'?'One selection differs. Does it explain the gap?':r.status==='demonstrated'?'The status selection explains the gap.':r.status==='equal'?'The captured totals agree.':'The evidence does not isolate a cause.';
  const changes=r.differences.map(d=>`<div class="selection-diff"><span><b>A ${esc(d.field)}:</b> ${esc(selection(d.a))}</span><span><b>B ${esc(d.field)}:</b> ${esc(selection(d.b))}</span></div>`).join('');
  $('#source-tag').textContent=r.status==='unresolved'?'Context needs review':'Fixed synthetic snapshot';
  const exp=r.experiment, [a,b]=r.originals;
  const added=addedRecords(job,source);
  const addedNote=added.length?`Adds ${added.slice(0,3).map(row=>`${esc(row.id)} (${esc(row.status)}, ${esc(exact(row.amount))})`).join(', ')}${added.length>3?` and ${added.length-3} more`:''}`:'Adds no records';
  const ledger=exp?`<table class="ledger"><caption>Reconciliation, step by step</caption><tbody>
<tr data-row="b"><th scope="row"><span class="report-letter">B</span>${esc(b.name)} <span class="muted">as captured</span></th><td class="num">${esc(exact(b.total))}</td></tr>
<tr data-row="impact" class="step"><th scope="row">With A’s status selection: ${esc(selection(exp.after))}<span class="subline">${addedNote}</span></th><td class="num">${esc(signed(exp.impact))}</td></tr>
<tr data-row="variant" class="sum"><th scope="row">B rerun with A’s status selection</th><td class="num">${esc(exact(exp.result.total))}</td></tr>
<tr data-row="a"><th scope="row"><span class="report-letter">A</span>${esc(a.name)} <span class="muted">as captured</span></th><td class="num">${esc(exact(a.total))}</td></tr>
<tr data-row="residual" class="total"><th scope="row">Remaining difference <span class="muted">(rerun B − A)</span></th><td class="num">${esc(exact(r.residual))}</td></tr>
</tbody></table><p class="caution">The original report definitions were not changed. Region and every other setting stayed as captured.</p>`:'';
  $('#diagnosis').innerHTML=`<article class="finding ${r.status} result-enter"><p class="eyebrow">${r.status==='demonstrated'?'Numerical cause demonstrated on synthetic data':r.status==='candidate'?'Candidate · not yet tested':r.status==='equal'?'Equal result · not semantic equivalence':'Unresolved · more evidence needed'}</p><h3 id="finding-title" tabindex="-1">${headline}</h3>${changes}${ledger}${r.status==='candidate'?'<button id="diagnose" class="primary">Test the status selection →</button><p class="hint">Rerun B with only A’s status selection. Preserve every other setting.</p>':''}${r.unknowns.length?`<ul class="unknowns">${r.unknowns.map(x=>`<li>${esc(x)}</li>`).join('')}</ul>`:''}</article>`;
  if(job.stale) message('Report context changed. Capture a new comparison.',true);
}
