const statusText={running:'▶ Em execução',waiting:'⏸ Aguardando limite',finished:'✓ Concluído',failed:'✗ Falhou',done:'✓ Concluída',incomplete:'! Incompleta',skipped:'– Pulada',pending:'· Pendente'};
const $=s=>document.querySelector(s); let selected='current', logOffsets=new Map(), followLogs=true;
function esc(value){return String(value??'—').replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]))}
function status(value){return `<span class="${esc(value)}">${statusText[value]||esc(value)}</span>`}
function count(state){let total=0,done=0;state.phases.forEach(p=>p.tasks.forEach(t=>{total++;if(t.status==='done')done++}));return{total,done}}
function bar(label,done,total){const p=total?Math.round(done*100/total):0;return `<div class="bar-row"><span>${label}</span><div class="bar" role="progressbar" aria-label="${label}" aria-valuenow="${p}" aria-valuemin="0" aria-valuemax="100"><i style="width:${p}%"></i></div><span>${p}%</span></div>`}
function render(state){
  const run=state.run||{meta:{}};
  const m=run.meta||{}, phases=state.phases||[];
  const pc={total:phases.length,done:phases.filter(p=>p.status==='done'||p.status==='skipped').length}, tc=count(state);
  $('#notice').textContent=state.run?'':'Nenhuma execução encontrada neste repositório.';
  $('#summary').innerHTML=`<div><b>Projeto:</b> ${esc(m.project)}<br><b>Engine:</b> ${esc(m.engine)}<br><b>Modelo:</b> ${esc(m.model)}<br><b>Perfil:</b> ${esc(m.profile)}<br><b>Status:</b> ${status(m.status||'pending')}</div><div><b>Run:</b> ${esc(run.id||m.run)}<br><b>PID:</b> ${esc(m.pid)}<br><b>Failovers:</b> ${esc(m.failovers||'0')}<br><b>Duração:</b> ${duration(m.started,m.ended)}</div>`;
  $('#progress').innerHTML=bar('Fases',pc.done,pc.total)+bar('Tasks',tc.done,tc.total)+`<p class="muted">Teste: ${esc(m.test_cmd)}</p>`;
  const current=phases.find(p=>p.number===m.phase_cur)||{};
  $('#current').innerHTML=`<dt>Fase</dt><dd>${current.number?`${current.number} · ${esc(current.title)}`:'—'}</dd><dt>Ciclo</dt><dd>${esc(m.cycle)}/${esc(m.cycle_max)}</dd><dt>Gate</dt><dd>${esc(m.gate)}</dd><dt>Atividade</dt><dd>${esc(m.activity)}</dd><dt>Último erro</dt><dd class="failed">${esc(m.last_error)}</dd>`;
  $('#tasks').innerHTML=phases.flatMap(p=>{const phase=`<tr class="phase ${p.status==='running'?'active':''}"><td>F${esc(p.number)}</td><td>${esc(p.title)}</td><td>${status(p.status)}</td><td>${esc(p.attempt==='0'?'–':p.attempt)}</td><td class="gates">${p.gates.map((g,i)=>`G${i} ${g==='pass'?'✓':g==='fail'?'✗':g==='run'?'⋯':'·'}`).join(' ')}</td></tr>`;const tasks=p.tasks.map(t=>`<tr class="task ${t.status==='running'?'active':''}"><td>T${esc(t.number)}</td><td>↳ ${esc(t.title)}</td><td>${status(t.status)}</td><td>–</td><td>–</td></tr>`);return[phase,...tasks]}).join('');
  $('#updated').textContent=`Atualizado ${new Date(state.updated_at*1000).toLocaleTimeString()}`;
}
function duration(start,end){if(!start)return'—';let s=Math.max(0,(Number(end)||Math.floor(Date.now()/1000))-Number(start));const h=Math.floor(s/3600),m=Math.floor(s%3600/60);return h?`${h}h ${m}m`:`${m}m ${s%60}s`}
function nearLogEnd(){const logs=$('#logs');return logs.scrollHeight-logs.scrollTop-logs.clientHeight<40}
function scrollLogsToEnd(){const logs=$('#logs');requestAnimationFrame(()=>{logs.scrollTop=logs.scrollHeight})}
function setFollowLogs(value){followLogs=value;const button=$('#follow-logs');button.classList.toggle('active',value);button.setAttribute('aria-pressed',String(value));button.textContent=value?'Seguindo':'Seguir logs';$('#log-status').textContent=value?'Seguindo novas linhas':'Rolagem pausada para leitura';if(value)scrollLogsToEnd()}
function renderLogs(text,replace){const logs=$('#logs');if(replace){logs.textContent=text||'Aguardando logs…';logs.dataset.placeholder=text?'false':'true'}else if(text){if(logs.dataset.placeholder==='true')logs.textContent='';logs.textContent+=text;logs.dataset.placeholder='false'}if(followLogs)scrollLogsToEnd()}
async function refreshRuns(){const data=await fetch('/api/v1/runs',{cache:'no-store'}).then(r=>r.json());const select=$('#runs'), previous=selected;select.replaceChildren(...data.runs.map(run=>{const opt=document.createElement('option');opt.value=run.current?'current':run.id;opt.textContent=`${run.current?'● ':''}${run.id||'legado'} · ${run.status||'sem estado'}`;return opt}));if([...select.options].some(o=>o.value===previous))select.value=previous;else {selected=select.value||'current'};}
async function refresh(){try{await refreshRuns();const url=selected==='current'?'/api/v1/runs/current':`/api/v1/runs/${encodeURIComponent(selected)}`;const state=await fetch(url,{cache:'no-store'}).then(r=>r.json());render(state);const runId=state.run?.id;if(runId){const after=logOffsets.get(runId)||0;const logs=await fetch(`/api/v1/runs/${encodeURIComponent(runId)}/logs?after=${after}`,{cache:'no-store'}).then(r=>r.json());renderLogs(logs.text,logs.truncated||after===0);logOffsets.set(runId,logs.next_offset);}}catch(error){$('#notice').textContent=`Falha ao ler o estado: ${error.message}`}}
$('#runs').addEventListener('change',e=>{selected=e.target.value;$('#logs').textContent='Aguardando logs…';$('#logs').dataset.placeholder='true';setFollowLogs(true);refresh()});
$('#logs').addEventListener('scroll',()=>{if(followLogs&&!nearLogEnd())setFollowLogs(false);else if(!followLogs&&nearLogEnd())setFollowLogs(true)});
$('#follow-logs').addEventListener('click',()=>setFollowLogs(!followLogs));
$('#jump-logs').addEventListener('click',()=>setFollowLogs(true));
$('#logs').dataset.placeholder='true';
refresh();setInterval(refresh,1000);
