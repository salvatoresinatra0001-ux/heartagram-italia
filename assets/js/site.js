"use strict";
(()=>{
const menu=document.querySelector('[data-menu]');const nav=document.querySelector('#site-nav');
if(menu&&nav){menu.addEventListener('click',()=>{const open=nav.classList.toggle('is-open');menu.setAttribute('aria-expanded',String(open));menu.textContent=open?'Chiudi ×':'Menu ☰';});}
const grid=document.querySelector('[data-gallery-grid]');if(!grid)return;
const count=document.querySelector('[data-gallery-count]'),search=document.querySelector('[data-gallery-search]');
const filters=[...document.querySelectorAll('[data-gallery-filter]')];
const dialog=document.querySelector('#photo-viewer'),big=document.querySelector('#viewer-image'),caption=document.querySelector('#viewer-caption'),meta=document.querySelector('#viewer-meta');
let photos=[],current=[],selected=0,active='all',lastTrigger=null;
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function filtered(){const q=(search?.value||'').toLocaleLowerCase('it').trim();return photos.filter(p=>(active==='all'||p.group===active||(active==='highres'&&p.width>=1200))&&(!q||(p.title+' '+p.year+' '+p.group).toLocaleLowerCase('it').includes(q)));}
function show(p){if(!dialog)return;selected=current.findIndex(x=>x.id===p.id);big.src=p.src;big.alt=p.title;caption.textContent=p.title;meta.textContent=p.year+' · '+p.width+' × '+p.height+' px · Attribuzione in verifica';if(!dialog.open)dialog.showModal();}
function move(delta){if(!current.length)return;selected=(selected+delta+current.length)%current.length;show(current[selected]);}
function render(){current=filtered();count.textContent=current.length+' fotografie visualizzate · '+photos.length+' file disponibili';grid.replaceChildren();if(!current.length){const empty=document.createElement('p');empty.className='empty';empty.textContent='Nessuna fotografia corrisponde alla ricerca.';grid.append(empty);return;}
const fragment=document.createDocumentFragment();for(const p of current){const figure=document.createElement('figure');figure.className='gallery-item';const btn=document.createElement('button');btn.className='gallery-open';btn.type='button';btn.setAttribute('aria-label','Ingrandisci '+p.title);const img=document.createElement('img');img.src=p.thumb;img.alt=p.title;img.loading='lazy';img.decoding='async';img.width=p.width;img.height=p.height;btn.append(img);btn.addEventListener('click',()=>{lastTrigger=btn;show(p)});const figcaption=document.createElement('figcaption');figcaption.innerHTML='<span class="eyelabel">'+esc(p.year)+' / ARCHIVIO</span><strong>'+esc(p.title)+'</strong><small>'+p.width+' × '+p.height+' px · Originale disponibile</small>';figure.append(btn,figcaption);fragment.append(figure);}grid.append(fragment);}
filters.forEach(b=>b.addEventListener('click',()=>{active=b.dataset.galleryFilter;filters.forEach(x=>x.setAttribute('aria-pressed',String(x===b)));render();}));search?.addEventListener('input',render);
document.querySelector('#viewer-close')?.addEventListener('click',()=>dialog.close());document.querySelector('#viewer-prev')?.addEventListener('click',()=>move(-1));document.querySelector('#viewer-next')?.addEventListener('click',()=>move(1));dialog?.addEventListener('close',()=>{big.removeAttribute('src');lastTrigger?.focus();});dialog?.addEventListener('click',e=>{if(e.target===dialog)dialog.close();});document.addEventListener('keydown',e=>{if(!dialog?.open)return;if(e.key==='ArrowRight')move(1);if(e.key==='ArrowLeft')move(-1);});
fetch('/data/photos.json').then(r=>{if(!r.ok)throw Error('Catalogo non disponibile');return r.json()}).then(data=>{photos=data.photos||[];render();}).catch(()=>{count.textContent='Impossibile caricare il catalogo fotografico.';});
})();
