/* Khiops site — backgrounds, CRISP wheel, tabs, animations */
/* Khiops site — i18n dictionary, language switch, and CRISP phase content */

/* ── Geometric canvas background: radial glows + dot grid + slow rotating arcs ──
   Appelé sur #bgC (hero) et #v11C (section V11).
   crispC n'existe pas : la zone CRISP est claire, pas de canvas.
   opts = {
     glows : [{x, y, r, col:'rgba(R,G,B,__)', a:'opacité_string'}],
     rings : [{x, y, n, r0, gap, a, speed, accent, col}],
     grid  : true (défaut)
   }
*/
function initGeoBg(id, opts){
  const c=document.getElementById(id); if(!c)return;
  const wrap=c.parentElement, ctx=c.getContext('2d');
  let W,H,t=0,last=0,raf=0,inView=true;
  const targetFrameMs=1000/30;
  function resize(){W=wrap.offsetWidth;H=wrap.offsetHeight;c.width=W;c.height=H;}
  function drawArrow(x,y,a,col){
    ctx.save();ctx.translate(x,y);ctx.rotate(a);ctx.beginPath();
    ctx.moveTo(0,0);ctx.lineTo(-8,-4);ctx.lineTo(-6,0);ctx.lineTo(-8,4);ctx.closePath();
    ctx.fillStyle=col;ctx.fill();ctx.restore();
  }
  function roundedRect(x,y,w,h,r){
    ctx.beginPath();ctx.moveTo(x+r,y);ctx.lineTo(x+w-r,y);ctx.quadraticCurveTo(x+w,y,x+w,y+r);
    ctx.lineTo(x+w,y+h-r);ctx.quadraticCurveTo(x+w,y+h,x+w-r,y+h);ctx.lineTo(x+r,y+h);
    ctx.quadraticCurveTo(x,y+h,x,y+h-r);ctx.lineTo(x,y+r);ctx.quadraticCurveTo(x,y,x+r,y);ctx.closePath();
  }
  function drawLink(a,b,col,flip){
    const sway=Math.sin(t*0.9+(flip?1.8:0))*5;
    const c1x=a.x+(b.x-a.x)*0.45, c1y=a.y+(flip?-64:64)+sway;
    const c2x=a.x+(b.x-a.x)*0.65, c2y=b.y+(flip?64:-64)-sway;
    ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.bezierCurveTo(c1x,c1y,c2x,c2y,b.x,b.y);
    ctx.strokeStyle=col;ctx.lineWidth=1.1;ctx.setLineDash([6,9]);ctx.stroke();ctx.setLineDash([]);
    drawArrow(b.x,b.y,Math.atan2(b.y-c2y,b.x-c2x),col);
  }
  function drawTable(tbl){
    const x=tbl.x,y=tbl.y,w=tbl.w,h=tbl.h;
    ctx.save();ctx.translate(x,y);
    ctx.fillStyle='rgba(20,22,36,0.22)';ctx.strokeStyle=tbl.stroke;ctx.lineWidth=1;
    ctx.shadowColor=tbl.glow;ctx.shadowBlur=10;
    roundedRect(0,0,w,h,8);ctx.fill();ctx.shadowBlur=0;ctx.stroke();
    ctx.fillStyle=tbl.fill;ctx.fillRect(1,1,w-2,25);
    ctx.fillStyle='rgba(237,234,248,0.42)';ctx.font='600 10px Inter, sans-serif';ctx.letterSpacing='0px';ctx.fillText(tbl.name,12,17);
    ctx.strokeStyle='rgba(255,255,255,0.06)';ctx.beginPath();ctx.moveTo(0,26);ctx.lineTo(w,26);ctx.stroke();
    for(let i=0;i<tbl.rows;i++){
      const yy=40+i*18;
      ctx.fillStyle=i===0?'rgba(255,121,0,0.24)':'rgba(255,255,255,0.1)';ctx.fillRect(13,yy-5,18,3);
      ctx.fillStyle=i===0?'rgba(255,121,0,0.16)':'rgba(255,255,255,0.06)';ctx.fillRect(39,yy-5,w-58-(i%2)*18,3);
    }
    ctx.restore();
  }
  function drawSchema(){
    const baseX=Math.max(W*.42,Math.min(W*.5,W-690)), baseY=H*.48;
    const drift=Math.sin(t*.6)*4;
    const tables=[
      {name:'CUSTOMER',x:baseX+74,y:baseY+22+drift,w:138,h:118,rows:4,stroke:'rgba(255,121,0,0.24)',fill:'rgba(255,121,0,0.09)',glow:'rgba(255,121,0,0.08)'},
      {name:'CONTRACT',x:baseX+330,y:baseY+52-drift,w:132,h:102,rows:3,stroke:'rgba(62,207,160,0.24)',fill:'rgba(62,207,160,0.08)',glow:'rgba(62,207,160,0.08)'},
      {name:'EVENT',x:baseX+182,y:baseY+282+drift,w:158,h:140,rows:5,stroke:'rgba(255,121,0,0.2)',fill:'rgba(255,121,0,0.08)',glow:'rgba(255,121,0,0.07)'},
      {name:'PRODUCT',x:baseX+478,y:baseY+245-drift,w:126,h:96,rows:3,stroke:'rgba(144,128,255,0.24)',fill:'rgba(144,128,255,0.08)',glow:'rgba(144,128,255,0.08)'},
      {name:'CHANNEL',x:baseX-8,y:baseY+198-drift,w:118,h:92,rows:3,stroke:'rgba(255,255,255,0.14)',fill:'rgba(255,255,255,0.04)',glow:'rgba(255,121,0,0.05)'},
      {name:'TRANSACTION',x:baseX+402,y:baseY+426+drift,w:152,h:122,rows:4,stroke:'rgba(255,121,0,0.18)',fill:'rgba(255,121,0,0.06)',glow:'rgba(255,121,0,0.06)'}
    ];
    ctx.save();ctx.globalAlpha=.56;
    drawLink({x:tables[0].x+tables[0].w,y:tables[0].y+44},{x:tables[1].x,y:tables[1].y+44},'rgba(255,121,0,0.38)',false);
    drawLink({x:tables[0].x+72,y:tables[0].y+tables[0].h},{x:tables[2].x+46,y:tables[2].y},'rgba(255,121,0,0.34)',false);
    drawLink({x:tables[1].x+82,y:tables[1].y+tables[1].h},{x:tables[3].x+26,y:tables[3].y},'rgba(62,207,160,0.34)',true);
    drawLink({x:tables[4].x+tables[4].w,y:tables[4].y+42},{x:tables[2].x,y:tables[2].y+62},'rgba(144,128,255,0.3)',true);
    drawLink({x:tables[2].x+tables[2].w,y:tables[2].y+92},{x:tables[5].x,y:tables[5].y+44},'rgba(255,121,0,0.3)',false);
    drawLink({x:tables[3].x+58,y:tables[3].y+tables[3].h},{x:tables[5].x+112,y:tables[5].y},'rgba(144,128,255,0.28)',true);
    tables.forEach(drawTable);
    ctx.restore();
  }
  function draw(now=0){
    if(document.hidden||!inView){raf=requestAnimationFrame(draw);return;}
    if(now-last<targetFrameMs){raf=requestAnimationFrame(draw);return;}
    const dt=Math.min((now-last)/16.67||1,2);
    last=now;
    ctx.clearRect(0,0,W,H);
    /* soft radial glows */
    (opts.glows||[]).forEach(g=>{
      const gr=ctx.createRadialGradient(W*g.x,H*g.y,0,W*g.x,H*g.y,Math.min(W,H)*g.r);
      gr.addColorStop(0,g.col.replace('__',g.a));
      gr.addColorStop(1,g.col.replace('__','0'));
      ctx.fillStyle=gr;ctx.fillRect(0,0,W,H);
    });
    /* fine dot grid */
    if(opts.grid!==false){
      ctx.fillStyle='rgba(255,255,255,0.07)';
      const gs=44;
      for(let x=gs/2;x<W;x+=gs)for(let y=gs/2;y<H;y+=gs)ctx.fillRect(x,y,1.3,1.3);
    }
    /* concentric rings: static circles + one slow drifting dashed accent arc */
    (opts.rings||[]).forEach(r=>{
      const cx=W*r.x, cy=H*r.y;
      ctx.setLineDash([]);
      for(let i=0;i<r.n;i++){
        ctx.beginPath();
        ctx.strokeStyle=r.col.replace('__',(r.a*(1-i/(r.n+0.5))).toFixed(3));
        ctx.lineWidth=1;
        ctx.arc(cx,cy,r.r0+i*r.gap,0,Math.PI*2);
        ctx.stroke();
      }
      /* accent: one dashed arc, very slow drift */
      const rad=r.r0+(r.accent!==undefined?r.accent:1)*r.gap;
      const off=t*(r.speed||0.05);
      ctx.beginPath();
      ctx.setLineDash([2,9]);
      ctx.strokeStyle=r.col.replace('__',(r.a*1.4).toFixed(3));
      ctx.lineWidth=1.6;
      ctx.arc(cx,cy,rad,off,off+Math.PI*0.66);
      ctx.stroke();
      ctx.setLineDash([]);
    });
    if(opts.schema)drawSchema();
    t+=0.003*dt;
    raf=requestAnimationFrame(draw);
  }
  const io=new IntersectionObserver(entries=>{inView=entries[0]?.isIntersecting!==false;},{threshold:0});
  io.observe(c);
  resize(); raf=requestAnimationFrame(draw);
  window.addEventListener('resize',resize);
}

/* Hero — glow orange haut-gauche + cyan bas-droit + arcs orange droite */
initGeoBg('bgC',{
  glows:[
    {x:.1, y:.15,r:.65,col:'rgba(255,100,0,__)',a:'.16'},
    {x:.88,y:.8, r:.5, col:'rgba(41,196,196,__)',a:'.08'}
  ],
  schema:true
});

/* V11 section — glow violet haut-droit + orange bas-gauche + arcs violets */
initGeoBg('v11C',{
  glows:[
    {x:.82,y:.25,r:.5, col:'rgba(144,110,255,__)',a:'.15'},
    {x:.12,y:.85,r:.45,col:'rgba(255,100,0,__)',  a:'.11'}
  ],
  rings:[{x:.88,y:.3,n:3,r0:110,gap:52,span:1,a:.26,speed:.05,accent:1,col:'rgba(144,128,255,__)'}]
});

let cur=-1;

function setCounter(i){
  const c=document.getElementById('ccount');
  if(c)c.textContent=`Phase ${String(i+1).padStart(2,'0')} / 06`;
}

function activate(i){
  if(i===cur)return;
  cur=i;
  const ph=PH[i],info=document.getElementById('cinfo'),idle=document.getElementById('idleMsg');
  setCounter(i);
  gsap.killTweensOf(idle);
  gsap.to(idle,{opacity:0,duration:.15,onComplete:()=>{idle.style.visibility='hidden';idle.style.display='none';}});

  /* segments */
  for(let j=0;j<6;j++){
    const s=document.getElementById('s'+j);
    if(j===i){s.setAttribute('fill',`url(#${PH[j].grad})`);s.setAttribute('filter','url(#segGlow)');s.setAttribute('stroke-width','1.5');}
    else{s.setAttribute('fill',`rgba(255,255,255,0.018)`);s.removeAttribute('filter');s.setAttribute('stroke-width','1');}
  }
  /* label boxes: highlight active */
  for(let j=0;j<6;j++){
    const rect=document.querySelector(`#lbl-${j} rect`);
    if(!rect)continue;
    rect.style.opacity = j===i ? '1' : '0.6';
  }

  /* pulse dot */
  const d=document.getElementById('pulDot');
  d.setAttribute('cx',ph.dot.x);d.setAttribute('cy',ph.dot.y);d.setAttribute('fill',ph.lc);
  gsap.fromTo(d,{attr:{r:0}},{attr:{r:7},duration:.3,ease:'back.out(2)'});

  /* progress dots */
  document.querySelectorAll('.pdot').forEach((dd,j)=>{dd.classList.remove('on','past');if(j===i)dd.classList.add('on');else if(j<i)dd.classList.add('past');});

  /* content */
  const L=ph[LANG];
  const tg=['#ptag','#pttl','#pbdy','#pcaps'];
  gsap.to(tg,{opacity:0,y:-6,duration:.13,onComplete:()=>{
    const t=document.getElementById('ptag');t.className='ptag '+ph.tc;t.textContent=L.tag;
    document.getElementById('pttl').innerHTML=L.ttl;
    document.getElementById('pbdy').innerHTML=L.bdy;
    document.getElementById('pcaps').innerHTML=L.caps.map(c=>`<div class="cap"><div class="cap-i ${c.c}">${c.svg}</div><div class="cap-t"><strong>${c.t}</strong>${c.b}</div></div>`).join('')+(L.extra||'');
    info.classList.add('active');
    gsap.fromTo(tg,{opacity:0,y:14},{opacity:1,y:0,duration:.4,stagger:.07,ease:'power2.out'});
  }});
}

function deactivate(){
  cur=-1;
  const info=document.getElementById('cinfo'),idle=document.getElementById('idleMsg');
  const tg=['#ptag','#pttl','#pbdy','#pcaps'];
  info.classList.remove('active');gsap.killTweensOf([idle,...tg]);
  gsap.set(tg,{opacity:0,y:14});
  idle.style.display='flex';idle.style.visibility='visible';gsap.to(idle,{opacity:1,duration:.3});
  gsap.to('#pulDot',{attr:{r:0},duration:.2});
  document.querySelectorAll('.pdot').forEach(d=>d.classList.remove('on','past'));
  for(let j=0;j<6;j++){
    const s=document.getElementById('s'+j);
    const fills=['rgba(200,160,32,0.04)','rgba(255,121,0,0.04)','rgba(255,150,48,0.04)','rgba(62,207,160,0.04)','rgba(41,196,196,0.04)','rgba(144,128,255,0.04)'];
    s.setAttribute('fill',fills[j]);s.removeAttribute('filter');s.setAttribute('stroke-width','1');
  }
  for(let j=0;j<6;j++){const rect=document.querySelector(`#lbl-${j} rect`);if(rect)rect.style.opacity='0.6';}
}

function showPrev(){activate((cur+5)%6);}
function showNext(){activate((cur+1)%6);}
function bindSwipe(el){
  if(!el)return;
  let sx=0,sy=0,down=false;
  el.addEventListener('touchstart',e=>{if(!e.touches[0])return;down=true;sx=e.touches[0].clientX;sy=e.touches[0].clientY;},{passive:true});
  el.addEventListener('touchend',e=>{
    if(!down||!e.changedTouches[0])return;down=false;
    const dx=e.changedTouches[0].clientX-sx,dy=e.changedTouches[0].clientY-sy;
    if(Math.abs(dx)>40&&Math.abs(dx)>Math.abs(dy)){if(dx<0)showNext();else showPrev();}
  },{passive:true});
}

document.querySelectorAll('.cseg').forEach((s,i)=>{
  s.addEventListener('click',()=>activate(i));
  s.addEventListener('mouseenter',()=>activate(i));
});
document.querySelectorAll('.pdot').forEach((d,i)=>d.addEventListener('click',()=>activate(i)));
const prev=document.getElementById('cprev'),next=document.getElementById('cnext'),cinfo=document.getElementById('cinfo'),crispSvg=document.getElementById('crispSvg');
if(prev)prev.addEventListener('click',showPrev);
if(next)next.addEventListener('click',showNext);
if(cinfo){
  cinfo.addEventListener('keydown',e=>{
    if(e.key==='ArrowLeft'){e.preventDefault();showPrev();}
    if(e.key==='ArrowRight'){e.preventDefault();showNext();}
  });
}
bindSwipe(cinfo);
bindSwipe(crispSvg);
activate(0);

function showTab(n,btn){
  document.querySelectorAll('.ptab').forEach(t=>t.classList.remove('on'));btn.classList.add('on');
  document.getElementById('tc').style.display=n==='code'?'':'none';
  const bv=document.getElementById('tb');
  if(n==='bench'){bv.style.display='block';setTimeout(()=>['b0','b1','b2'].forEach(id=>{const el=document.getElementById(id);el.style.width=el.getAttribute('data-w')+'%';}),60);}
  else bv.style.display='none';
}

window.addEventListener('load',()=>{
  const ids=['eN','e0','e1','e2','e3','e4','e5','e7'];
  gsap.set(ids.map(id=>'#'+id),{opacity:0,y:22});
  gsap.to(ids.map(id=>'#'+id),{opacity:1,y:0,duration:.6,stagger:.08,ease:'power3.out',delay:.1});

  const animateOnEnter=(target,from,to,threshold=.2)=>{
    const el=typeof target==='string'?document.querySelector(target):target;
    if(!el)return;
    gsap.set(target,from);
    const io=new IntersectionObserver((entries)=>{
      if(!entries[0]||!entries[0].isIntersecting)return;
      gsap.to(target,to);
      io.disconnect();
    },{threshold});
    io.observe(el);
  };

  animateOnEnter('#crispSec .s-eye',{opacity:0,y:22},{opacity:1,y:0,duration:.6,ease:'power2.out'},.2);
  animateOnEnter('#crispSec .s-title',{opacity:0,y:22},{opacity:1,y:0,duration:.6,ease:'power2.out',delay:.08},.2);
  animateOnEnter('#crispSec .s-sub',{opacity:0,y:22},{opacity:1,y:0,duration:.6,ease:'power2.out',delay:.16},.2);
  animateOnEnter('.crisp-layout',{opacity:0,y:28},{opacity:1,y:0,duration:.8,ease:'power2.out'},.2);
  animateOnEnter('#v11Grid .vcard',{opacity:0,y:24},{opacity:1,y:0,duration:.6,stagger:.12,ease:'power2.out'},.2);
});

/* ── Transitions « dent » : dunes pleine largeur + pyramide pleine à taille fixe ── */
(function buildToothTransitions(){
  /* Transition « dent » façon v23 : un plateau (couleur de la zone qui ARRIVE) remplit le bas ;
     une encoche triangulaire est découpée vers le haut → la zone du DESSUS apparaît par
     transparence et forme la pyramide, toujours en contraste. Arêtes wireframe + point d'apex
     par-dessus. Pyramide décalée à droite. */
  const APX = 1080, BASE_L = 968, BASE_R = 1192, SEAM = 96, APEXY = 14;  // geometry in viewBox units
  document.querySelectorAll('.tooth-transition').forEach((el, idx) => {
    const plateau = el.getAttribute('data-plateau') || '#F6F3EC';
    const edgeId = 'pyrEdge' + idx;
    /* plateau path with a triangular notch cut up to the apex (offset right) */
    const plateauPath =
      `M0,${SEAM} L${BASE_L},${SEAM} L${APX},${APEXY} L${BASE_R},${SEAM} L1440,${SEAM} L1440,160 L0,160 Z`;
    /* mid edge for 3/4 look (apex to a point right of centre on the seam) */
    const midX = APX + 26;
    el.innerHTML = `
      <svg class="horizon-svg" viewBox="0 0 1440 160" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
        <defs><linearGradient id="${edgeId}" x1="0" y1="1" x2="0" y2="0">
          <stop offset="0" stop-color="#FF7900" stop-opacity="0.25"/>
          <stop offset="1" stop-color="#FF7900" stop-opacity="0.9"/>
        </linearGradient></defs>
        <path fill="${plateau}" d="${plateauPath}"/>
        <g fill="none" stroke="url(#${edgeId})" stroke-width="1.4" stroke-linejoin="round" vector-effect="non-scaling-stroke">
          <path d="M${APX},${APEXY} L${BASE_L},${SEAM} M${APX},${APEXY} L${BASE_R},${SEAM}"/>
          <line x1="${APX}" y1="${APEXY}" x2="${midX}" y2="${SEAM}" stroke="#FF7900" stroke-opacity="0.4"/>
          <line x1="${APX-34}" y1="${APEXY+38}" x2="${APX+30}" y2="${APEXY+38}" stroke="#FF7900" stroke-opacity="0.35"/>
          <line x1="${APX-58}" y1="${APEXY+66}" x2="${APX+54}" y2="${APEXY+66}" stroke="#FF7900" stroke-opacity="0.25"/>
        </g>
        <circle cx="${APX}" cy="${APEXY}" r="2.6" fill="#FF7900"/>
      </svg>
      ${idx===0?`<div class="dive-hint"><span>Beneath surface</span><span class="ti-svg" aria-hidden="true"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="m7 8 5 5 5-5"/><path d="m7 13 5 5 5-5"/></svg></span></div>`:""}`;
  });
})();
