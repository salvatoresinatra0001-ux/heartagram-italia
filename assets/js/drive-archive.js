"use strict";
const root=document.getElementById("items"),counter=document.getElementById("count");
let records=[];
function render(filter){const selected=filter==="all"?records:records.filter(x=>x.category===filter);root.replaceChildren();counter.textContent=selected.length+" elementi catalogati";for(const x of selected){const card=document.createElement("article");card.className="item";const category=document.createElement("small");category.textContent=x.category;const title=document.createElement("h2");title.textContent=x.filename;const subject=document.createElement("p");subject.textContent=x.subject+" · Diritti da verificare";card.append(category,title,subject);root.append(card)}}
document.querySelectorAll("[data-filter]").forEach(b=>b.addEventListener("click",()=>{document.querySelectorAll("[data-filter]").forEach(x=>x.setAttribute("aria-pressed",String(x===b)));render(b.dataset.filter)}));
fetch("../../data/drive-photo-catalog.json").then(r=>{if(!r.ok)throw Error("Catalogo non disponibile");return r.json()}).then(data=>{records=data.items||[];render("all")}).catch(()=>{counter.textContent="Impossibile caricare il catalogo. Riprova più tardi."});
