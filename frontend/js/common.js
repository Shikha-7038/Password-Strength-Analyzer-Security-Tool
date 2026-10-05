const COLORS=["#d64545","#e8833a","#e5b93c","#3fa66b","#1e7f5c"],NAMES=["VERY WEAK","WEAK","MODERATE","STRONG","VERY STRONG"];
const $=id=>document.getElementById(id);
function li(t,c){const e=document.createElement("li");e.textContent=t;if(c)e.className=c;return e}
function fill(ul,items){ul.replaceChildren(...items)}
const LBL={length:"Length",unique_ratio:"Unique chars",diversity:"Variety",pattern_resistance:"Pattern resistance",not_common:"Not common",unpredictability:"Unpredictability"},MAX={length:35,diversity:15,unique_ratio:10,pattern_resistance:20,not_common:10,unpredictability:10};

const PAGES=[["index.html","Analyzer"],["dashboard.html","Dashboard"],["generator.html","Generator"],["learn.html","Learn"]];
(()=>{const n=document.getElementById("nav");if(!n)return;const cur=location.pathname.split("/").pop()||"index.html";
 PAGES.forEach(([h,t])=>{const a=document.createElement("a");a.href=h;a.textContent=t;if(h===cur)a.setAttribute("aria-current","page");n.append(a)})})();
async function post(url,body){return (await fetch(url,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)})).json()}
