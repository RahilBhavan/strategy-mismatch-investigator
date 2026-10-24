import {$,esc,message,reportPicks,clearResult,renderResult} from './view.js';
import {renderEvidence,download,readable} from './evidence.js';
let source=null, job=null, busy=false, dirty=false, generation=0;
async function api(path,method='GET',body) {
 const response=await fetch(path,{method,headers:body===undefined?{}:{'Content-Type':'application/json'},body:body===undefined?undefined:JSON.stringify(body)});
 const result=await response.json();
 if(!response.ok)throw new Error(result.error?.message||'Could not reach the local investigation. Retry.');
 return result;
}
function setBusy(value){busy=value;for(const el of document.querySelectorAll('#report-0,#report-1,#amount,#condition,#case-file,#packet-file'))el.disabled=value;$('#compare').disabled=value;$('#cancel').hidden=!value;$('#scenario').disabled=value;$('#save-amount').disabled=value||!source?.case.records.some(r=>r.status==='refunded');const d=$('#diagnose');if(d)d.disabled=value;}
function address(){const url=new URL(location.href);url.searchParams.set('case',source.id);if(job)url.searchParams.set('job',job.id);else url.searchParams.delete('job');history.replaceState(null,'',url);}
function markDirty(){dirty=true;message('Report context changed. Capture a new comparison.',true);for(const button of document.querySelectorAll('#export-json,#export-report,#diagnose'))button.disabled=true;}
function present(focusResult=false){
 if(!job)return;
 if(job.state==='complete'){
  if(job.stale){clearResult();message('Report context changed. Capture a new comparison.',true);address();return;}
  renderResult(job,source);renderEvidence(job,source);address();
  if(focusResult)$('#worksheet-title').focus({preventScroll:true});
  $('#diagnose')?.addEventListener('click',()=>run('diagnose'));
  $('#export-json')?.addEventListener('click',async()=>{try{const packet=await api(`/api/jobs/${job.id}/export`);download('synthetic-investigation.json',JSON.stringify(packet,null,2));}catch(e){message(e.message,true);}});
  $('#export-report')?.addEventListener('click',async()=>{try{const packet=await api(`/api/jobs/${job.id}/export`);download('synthetic-investigation.html',readable(packet),'text/html');}catch(e){message(e.message,true);}});
 }else if(['failed','canceled','interrupted'].includes(job.state)){
  clearResult();message(job.error?.message||'Could not reproduce this report.',true);
  $('#message').insertAdjacentHTML('beforeend','<button id="retry" class="secondary">Retry investigation</button>');
  $('#retry').addEventListener('click',()=>run(job.phase));
 }
}
async function poll(token){
 while(token===generation){
  const value=await api(`/api/jobs/${job.id}`);
  if(token!==generation)return;
  job=value;
  if(!['running','queued'].includes(job.state)){setBusy(false);message('');present(true);return;}
  await new Promise(resolve=>setTimeout(resolve,120));
 }
}
async function run(phase='compare'){
 if(busy)return;
 try{
  const picks=[$('#report-0').value,$('#report-1').value];
  if(picks[0]===picks[1])throw new Error('Choose two different report references.');
  if(dirty){
   const original=source.case.reports;
   const updated=structuredClone(source.case);
   updated.reports=picks.map(id=>original.find(r=>r.id===id));
   source=await api(`/api/cases/${source.id}`,'PUT',updated);dirty=false;
  }
  setBusy(true);clearResult();message('Reproducing the report totals…');
  if(innerWidth<=700)$('#workspace').scrollIntoView({behavior:'instant',block:'start'});
  const token=++generation;
  job=await api('/api/jobs','POST',{case_id:source.id,fingerprint:source.fingerprint,phase,mode:$('#condition').value});
  address();await poll(token);
 }catch(e){setBusy(false);message(e.message,true);}
}
async function catalog(){
 const data=await api('/api/catalog');
 $('#scenario').innerHTML=data.cases.map(c=>`<option value="${esc(c.id)}">${esc(c.name)}</option>`).join('');
}
async function load(key){
 ++generation;source=await api(`/api/cases/${encodeURIComponent(key)}`);job=null;dirty=false;
 $('#scenario').value=key;reportPicks(source);clearResult();message('');setBusy(false);address();
 $('#report-0').addEventListener('change',markDirty);$('#report-1').addEventListener('change',markDirty);
}
async function fileJSON(input){const file=input.files[0];if(!file)return null;if(file.size>20*1024*1024)throw new Error('File exceeds 20 MB.');try{return JSON.parse(await file.text());}catch{throw new Error('Choose a valid synthetic JSON file.');}}
$('#compare').addEventListener('click',()=>run());
$('#scenario').addEventListener('change',async()=>{try{await load($('#scenario').value);}catch(e){message(e.message,true);}});
$('#condition').addEventListener('change',()=>message('Injected condition changed. Run the comparison to exercise it.'));
$('#cancel').addEventListener('click',async()=>{try{if(job)await api(`/api/jobs/${job.id}/cancel`,'POST',{});}catch(e){message(e.message,true);}});
$('#save-amount').addEventListener('click',async()=>{
 try{
  const changed=structuredClone(source.case);const row=changed.records.find(r=>r.status==='refunded');
  if(!row)throw new Error('This example has no refunded order.');row.amount=$('#amount').value;
  source=await api(`/api/cases/${source.id}`,'PUT',changed);dirty=false;
  if(job)job.stale=true;
  reportPicks(source);$('#report-0').addEventListener('change',markDirty);$('#report-1').addEventListener('change',markDirty);
  clearResult();
  message('Report context changed. Capture a new comparison.',true);
 }catch(e){message(e.message,true);}
});
$('#case-file').addEventListener('change',async()=>{
 try{const data=await fileJSON($('#case-file'));if(!data)return;const saved=await api('/api/cases','POST',data);await catalog();await load(saved.id);message('Synthetic case loaded. Run the comparison.');}catch(e){message(e.message,true);}
});
$('#packet-file').addEventListener('change',async()=>{
 try{const data=await fileJSON($('#packet-file'));if(!data)return;const saved=await api('/api/restore','POST',data);await catalog();await load(saved.case_id);job=saved;present();message(saved.import_note);}catch(e){message(e.message,true);}
});
window.addEventListener('popstate',()=>location.reload());
(async()=>{
 try{
  const params=new URLSearchParams(location.search);const remembered=params.get('job');
  await catalog();await load(params.get('case')||'status');
  if(remembered){job=await api(`/api/jobs/${remembered}`);if(job.case_id!==source.id)throw new Error('Investigation does not match this case.');if(['queued','running'].includes(job.state)){setBusy(true);message('Resuming the local investigation…');await poll(++generation);}else present();}
 }catch(e){message(e.message,true);}
})();
