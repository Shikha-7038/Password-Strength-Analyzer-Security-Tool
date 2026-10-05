let charts={};function draw(id,cfg){charts[id]?.destroy();charts[id]=new Chart($(id),cfg)}
async function loadStats(){
  const s=await (await fetch("/api/dashboard/stats")).json(),K=[["Total analyses",s.total,"#2b59ff"],["Average score",s.average_score,"#14213d"],...NAMES.map((n,k)=>[n,s.classes[n],COLORS[k]])];
  $("kpis").replaceChildren(...K.map(([a,b,c])=>{const d=document.createElement("div");d.className="kpi";d.style.setProperty("--k",c);const v=document.createElement("b"),l=document.createElement("span");v.textContent=b;l.textContent=a;d.append(v,l);return d}));
  const opt={plugins:{legend:{display:false}},scales:{x:{grid:{display:false}},y:{beginAtZero:true,ticks:{precision:0}}}};
  draw("c1",{type:"doughnut",data:{labels:NAMES,datasets:[{data:NAMES.map(n=>s.classes[n]),backgroundColor:COLORS,borderWidth:0}]},options:{cutout:"62%",plugins:{legend:{position:"right",labels:{boxWidth:10}}}}});
  draw("c2",{type:"bar",data:{labels:["0-9","10-19","20-29","30-39","40-49","50-59","60-69","70-79","80-89","90+"],datasets:[{data:s.score_distribution,backgroundColor:"#2b59ff",borderRadius:5}]},options:opt});
  draw("c3",{type:"bar",data:{labels:Object.keys(s.length_distribution),datasets:[{data:Object.values(s.length_distribution),backgroundColor:"#3fa6a0",borderRadius:5}]},options:opt});
  const w=s.weaknesses,names=w.map(x=>x.type.replace(/_/g," "));
  draw("c4",{type:"bar",data:{labels:names,datasets:[{data:w.map(x=>x.count),backgroundColor:"#e8833a",borderRadius:5}]},options:{...opt,indexAxis:"y",scales:{x:{beginAtZero:true,ticks:{precision:0}},y:{grid:{display:false}}}}});
  draw("c5",{type:"polarArea",data:{labels:names,datasets:[{data:w.map(x=>x.count),backgroundColor:["#d64545cc","#e8833acc","#e5b93ccc","#3fa66bcc","#2b59ffcc","#7a5af8cc","#3fa6a0cc","#c2547fcc"]}]},options:{plugins:{legend:{position:"right",labels:{boxWidth:10}}}}});
}

async function loadRecent(){const rows=await (await fetch("/api/analytics/recent")).json(),tb=$("recent");
 tb.replaceChildren(...rows.map(r=>{const tr=document.createElement("tr"),i=NAMES.indexOf(r.classification);
  [r.analysis_id,r.created_at,r.score,r.classification,r.password_length,r.weakness_count].forEach((v,k)=>{const td=document.createElement("td");
   if(k===3){const p=document.createElement("span");p.className="pill";p.style.background=COLORS[i];p.textContent=v;td.append(p)}else td.textContent=v;tr.append(td)});return tr}))}
loadStats();loadRecent();
