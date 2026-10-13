(function(){
  var $=function(s,r){return (r||document).querySelector(s);}, $$=function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s));};

  // Menu mobilne
  var btn=$('.menu-btn'), menu=$('#menu');
  if(btn && menu){
    btn.addEventListener('click',function(){
      var open=menu.classList.toggle('open');
      btn.setAttribute('aria-expanded',open);
      btn.setAttribute('aria-label',open?'Zamknij menu':'Otwórz menu');
    });
    menu.addEventListener('click',function(e){
      var top=e.target.closest('.nav-top');
      if(top && window.matchMedia('(max-width:1024px)').matches){ e.preventDefault(); top.parentElement.classList.toggle('open'); return; }
      if(e.target.closest('a')){menu.classList.remove('open');btn.setAttribute('aria-expanded','false');btn.setAttribute('aria-label','Otwórz menu');}
    });
  }

  // Rezerwacja w okienku
  var modal=$('#booking-modal'), frame=modal?$('iframe',modal):null;
  function openBooking(e){
    if(!modal || typeof modal.showModal!=='function') return;
    e.preventDefault();
    if(!frame.src) frame.src=frame.dataset.src;
    modal.showModal();
  }
  $$('[data-booking-open]').forEach(function(el){el.addEventListener('click',openBooking);});
  if(modal){
    $('[data-booking-close]',modal).addEventListener('click',function(){modal.close();});
    modal.addEventListener('click',function(e){if(e.target===modal) modal.close();});
  }

  var y=$('#year'); if(y) y.textContent=new Date().getFullYear();

  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine=window.matchMedia('(hover: hover) and (pointer: fine)').matches;

  // Pojawianie się elementów przy przewijaniu
  var revealEls=$$(['.hero-copy','.hero-visual','.control-box','.about-left','.about-right','.specs-head','.spec','.faq-left','.faq-list details',
    '.contact-card','.contact-side','.booking-copy','.steps li','.pillar','.tile','.how li','.plan','.person','.post-card','.section-head','.law-strip'].join(','));
  if(!reduce && 'IntersectionObserver' in window){
    revealEls.forEach(function(el){
      el.classList.add('reveal');
      var i=el.parentElement?Array.prototype.indexOf.call(el.parentElement.children,el):0;
      if(i%3===1) el.classList.add('reveal-d1'); else if(i%3===2) el.classList.add('reveal-d2');
    });
    var io=new IntersectionObserver(function(entries){
      entries.forEach(function(en){ if(en.isIntersecting){ en.target.classList.add('in'); io.unobserve(en.target); } });
    },{threshold:.1,rootMargin:'0px 0px -40px 0px'});
    revealEls.forEach(function(el){ io.observe(el); });
  }

  if(!fine || reduce) return;

  // Kafelki 3D
  $$('.spec').forEach(function(card){
    card.classList.add('tilt');
    card.addEventListener('mousemove',function(e){
      var r=card.getBoundingClientRect(), x=(e.clientX-r.left)/r.width, yy=(e.clientY-r.top)/r.height;
      card.classList.add('is-tilting');
      card.style.setProperty('--ry',((x-.5)*12).toFixed(2)+'deg');
      card.style.setProperty('--rx',((.5-yy)*12).toFixed(2)+'deg');
      card.style.setProperty('--mx',(x*100).toFixed(1)+'%');
      card.style.setProperty('--my',(yy*100).toFixed(1)+'%');
    });
    card.addEventListener('mouseleave',function(){
      card.classList.remove('is-tilting');
      card.style.setProperty('--rx','0deg'); card.style.setProperty('--ry','0deg');
    });
  });

  // Podświetlenie za kursorem na kafelkach i dużych blokach
  $$('.tile,.control-box,.booking-box').forEach(function(box){
    box.addEventListener('mousemove',function(e){
      var r=box.getBoundingClientRect();
      box.style.setProperty('--mx',(e.clientX-r.left)+'px');
      box.style.setProperty('--my',(e.clientY-r.top)+'px');
    });
  });

  // Zdjęcie w nagłówku: 3D i parallax karty
  var hero=$('.hero'), photo=$('.hero-photo'), hcard=$('.hero-card');
  if(hero && photo){
    hero.addEventListener('mousemove',function(e){
      var r=hero.getBoundingClientRect(), x=(e.clientX-r.left)/r.width-.5, yy=(e.clientY-r.top)/r.height-.5;
      photo.style.setProperty('--pry',(x*10).toFixed(2)+'deg');
      photo.style.setProperty('--prx',(-yy*8).toFixed(2)+'deg');
      if(hcard){ hcard.style.setProperty('--ctx',(x*-24).toFixed(1)+'px'); hcard.style.setProperty('--cty',(yy*-16).toFixed(1)+'px'); }
    });
    hero.addEventListener('mouseleave',function(){
      photo.style.setProperty('--pry','0deg'); photo.style.setProperty('--prx','0deg');
      if(hcard){ hcard.style.setProperty('--ctx','0px'); hcard.style.setProperty('--cty','0px'); }
    });
  }

  // Reflektor za kursorem, punkty w sekcji ciemnej, parallax kul w tle
  var glow=$('.cursor-glow');
  if(glow){
    var gx=-999, gy=-999, tx=-999, ty=-999, running=false;
    var loop=function(){ gx+=(tx-gx)*.12; gy+=(ty-gy)*.12; glow.style.transform='translate3d('+gx.toFixed(1)+'px,'+gy.toFixed(1)+'px,0)';
      if(Math.abs(tx-gx)>.5||Math.abs(ty-gy)>.5){requestAnimationFrame(loop);} else {running=false;} };
    window.addEventListener('mousemove',function(e){ tx=e.clientX; ty=e.clientY; if(gx<-900){gx=tx;gy=ty;} glow.classList.add('on'); if(!running){running=true;requestAnimationFrame(loop);} },{passive:true});
    document.addEventListener('mouseleave',function(){ glow.classList.remove('on'); });
  }
  $$('.specs').forEach(function(sp){
    sp.addEventListener('mousemove',function(e){ var r=sp.getBoundingClientRect();
      sp.style.setProperty('--sx',(e.clientX-r.left)+'px'); sp.style.setProperty('--sy',(e.clientY-r.top)+'px'); });
  });
  var orbs=$$('.bg-fx .orb'), ticking=false;
  window.addEventListener('scroll',function(){ if(ticking) return; ticking=true; requestAnimationFrame(function(){
    var sy=window.scrollY; orbs.forEach(function(o,i){ o.style.translate='0 '+(-sy*(.06+i*.04)).toFixed(1)+'px'; }); ticking=false; }); },{passive:true});
})();
