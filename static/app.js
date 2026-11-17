
async function getData(){
  const r = await fetch('/api/status');
  return await r.json();
}
function setBar(id,v){document.getElementById(id).style.width = Math.min(v,100)+'%';}
function formatUptime(s){
  const d=Math.floor(s/86400), h=Math.floor(s%86400/3600), m=Math.floor(s%3600/60);
  return `${d}d ${h}h ${m}m`;
}
async function refreshData(){
  try{
    const d=await getData();
    document.getElementById('cpu').textContent=d.system.cpu;
    document.getElementById('memory').textContent=d.system.memory;
    document.getElementById('disk').textContent=d.system.disk;
    document.getElementById('service').textContent=d.service;
    document.getElementById('serviceState').textContent=d.service_status.toUpperCase();
    setBar('cpuBar',d.system.cpu); setBar('memBar',d.system.memory); setBar('diskBar',d.system.disk);
    const overall=document.getElementById('overall');
    const healthy=d.service_status==='active';
    overall.textContent=healthy?'● HEALTHY':'● ATTENTION';
    overall.style.background=healthy?'#1f6b4d':'#8c394b';
    document.getElementById('logs').textContent=d.logs.length?d.logs.join('\n'):'No log entries yet.';
  }catch(e){document.getElementById('message').textContent='Backend connection error: '+e}
}
async function action(url){
  document.getElementById('message').textContent='Working...';
  const r=await fetch(url,{method:'POST'});
  const d=await r.json();
  document.getElementById('message').textContent=d.message || 'Request completed.';
  setTimeout(refreshData,1000);
}
function demoFailure(){action('/api/demo-failure')}
function recover(){action('/api/recover')}
refreshData();
setInterval(refreshData,5000);
