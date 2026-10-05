function render(r){
  const i=NAMES.indexOf(r.classification),empty=!r.metrics.length;
  document.querySelectorAll("#meter i").forEach((e,k)=>e.style.background=!empty&&k<=i?COLORS[i]:"");
  $("score").textContent=r.score;$("cls").textContent=empty?"—":r.classification;$("cls").style.color=empty?"":COLORS[i];
  const m=r.metrics,T=[["Length",m.length??0],["Length band",m.length_label||"—"],["Character types",m.character_type_count??"—"],["Unique ratio",m.unique_character_ratio??"—"],["Entropy estimate",empty?"—":m.entropy_bits+" bits"],["Guess resistance",empty?"—":m.guess_resistance.split(" (")[0]]];
  $("tiles").replaceChildren(...T.map(([a,b])=>{const d=document.createElement("div");d.className="tile";const s=document.createElement("span"),v=document.createElement("b");s.textContent=a;v.textContent=b;d.append(s,v);return d}));
  fill($("finds"),empty?[li("Type a password to see detected weaknesses.")]:r.findings.map(f=>li(f.description,f.severity)));
  fill($("sugg"),r.suggestions.map(s=>li(s,"tip")));
  const pts=(r.breakdown&&r.breakdown.points)||{};
  $("bd").replaceChildren(...Object.keys(MAX).map(k=>{const d=document.createElement("div");d.className="bar";const a=document.createElement("span"),b=document.createElement("div"),n=document.createElement("span");a.textContent=LBL[k];b.innerHTML="<i></i>";b.firstChild.style.width=((pts[k]||0)/MAX[k]*100)+"%";n.textContent=(pts[k]||0)+"/"+MAX[k];d.append(a,b,n);return d}));
  const pen=Object.entries((r.breakdown&&r.breakdown.penalties)||{});
  if(pen.length){const p=document.createElement("p");p.className="note";p.textContent="Penalties: "+pen.map(([k,v])=>k+" −"+v).join(", ");$("bd").append(p)}
  $("pol").textContent=empty?"POLICY —":r.policy.result;
  fill($("polf"),r.policy.failures.length?r.policy.failures.map(f=>li(f,"high")):[li(empty?"Min 12 characters, common-password and personal-info checks.":"All configured checks passed.",empty?"":"good")]);
}
let t;const ctx=()=>({first_name:$("nm").value,birth_year:$("by").value,organization:$("og").value});
async function analyze(record){
  const r=await fetch("/api/analyze",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({password:$("pw").value,context:ctx(),record:!!record})});
  if(r.ok)render(await r.json());return r.ok}
function queue(){clearTimeout(t);t=setTimeout(()=>analyze(false).catch(()=>{}),150)}
["pw","nm","by","og"].forEach(id=>$(id).addEventListener("input",queue));
$("eye").onclick=()=>{const h=$("pw").type==="password";$("pw").type=h?"text":"password";$("eye").textContent=h?"Hide":"Show";$("eye").setAttribute("aria-pressed",h)};
$("save").onclick=async()=>{if(!$("pw").value){$("saved").textContent="Type a password first.";return}await analyze(true);$("saved").textContent="Saved score, class and length only. See it on the Dashboard.";loadStats()};
post("/api/analyze",{password:""}).then(render);
["123456","Password123!","aaaaaaaaaaaaaaaa","qwerty2026!","velvet-galaxy-harbor-orchid"].forEach(p=>{const b=document.createElement("button");b.className="alt";b.textContent=p;b.onclick=()=>{$("pw").value=p;analyze(false)};$("ex").append(b)});
