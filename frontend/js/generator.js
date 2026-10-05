
let mode="pw";
function opts(){return {length:+$("len").value,upper:$("u").checked,lower:$("l").checked,digits:$("d").checked,symbols:$("s").checked}}
async function gen(){
  const j=await post("/api/generate-password",mode==="pp"?{mode:"passphrase",words:+$("words").value}:opts());
  $("out").textContent=j.password;$("kind").textContent=j.kind==="passphrase"?"Passphrase":"Password";
  const r=await post("/api/analyze",{password:j.password}),i=NAMES.indexOf(r.classification);
  $("sc").textContent=r.score;$("cl").textContent=r.classification;$("cl").style.color=COLORS[i];
  document.querySelectorAll("#meter i").forEach((e,k)=>e.style.background=k<=i?COLORS[i]:"");
  $("m1").textContent=r.metrics.length;$("m2").textContent=r.metrics.entropy_bits+" bits";$("m3").textContent=r.metrics.character_type_count;$("m4").textContent=r.policy.result;
  fill($("sg"),r.findings.map(f=>li(f.description,f.severity)));
}
document.querySelectorAll("[data-m]").forEach(b=>b.onclick=()=>{mode=b.dataset.m;$("pwopts").hidden=mode==="pp";$("ppopts").hidden=mode!=="pp";gen()});
$("go").onclick=gen;$("copy").onclick=()=>{navigator.clipboard?.writeText($("out").textContent);$("copy").textContent="Copied";setTimeout(()=>$("copy").textContent="Copy",1500)};
$("hide").onclick=()=>{const o=$("out");o.hidden=!o.hidden;$("hide").textContent=o.hidden?"Reveal":"Hide"};
gen();
