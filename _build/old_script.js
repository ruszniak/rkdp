(function(){
  var btn=document.querySelector('.menu-btn'), menu=document.getElementById('menu');
  btn.addEventListener('click',function(){
    var open=menu.classList.toggle('open');
    btn.setAttribute('aria-expanded',open);
    btn.setAttribute('aria-label',open?'Zamknij menu':'Otwórz menu');
  });
  menu.addEventListener('click',function(e){
    if(e.target.closest('a')){menu.classList.remove('open');btn.setAttribute('aria-expanded','false');btn.setAttribute('aria-label','Otwórz menu');}
  });
  var modal=document.getElementById('booking-modal'), frame=modal.querySelector('iframe');
  function openBooking(e){
    if(typeof modal.showModal!=='function') return; // starsza przeglądarka: zostaje przewinięcie do sekcji
    e.preventDefault();
    if(!frame.src) frame.src=frame.dataset.src;
    modal.showModal();
  }
  document.querySelectorAll('[data-booking-open]').forEach(function(el){el.addEventListener('click',openBooking);});
  modal.querySelector('[data-booking-close]').addEventListener('click',function(){modal.close();});
  modal.addEventListener('click',function(e){if(e.target===modal) modal.close();});

  // ===== Efekty: 3D, podświetlenia, pojawianie się =====
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine=window.matchMedia('(hover: hover) and (pointer: fine)').matches;

  // Pojawianie się sekcji przy przewijaniu
  var revealSel=['.hero-copy','.hero-visual','.control-box','.about-left','.about-right','.specs-head','.spec','.faq-left','.faq-list details','.contact-card','.contact-side','.booking-copy','.steps li','.pillar'];
  var revealEls=document.querySelectorAll(revealSel.join(','));
  if(!reduce && 'IntersectionObserver' in window){
    revealEls.forEach(function(el){
      el.classList.add('reveal');
      var sib=el.parentElement?Array.prototype.indexOf.call(el.parentElement.children,el):0;
      if(sib%3===1) el.classList.add('reveal-d1'); else if(sib%3===2) el.classList.add('reveal-d2');
    });
    var io=new IntersectionObserver(function(entries){
      entries.forEach(function(en){ if(en.isIntersecting){ en.target.classList.add('in'); io.unobserve(en.target); } });
    },{threshold:.12,rootMargin:'0px 0px -40px 0px'});
    revealEls.forEach(function(el){ io.observe(el); });
  }

  if(fine && !reduce){
    // Kafelki 3D: przechylenie i podświetlenie za kursorem
    document.querySelectorAll('.spec').forEach(function(card){
      card.classList.add('tilt');
      card.addEventListener('mousemove',function(e){
        var r=card.getBoundingClientRect(), x=(e.clientX-r.left)/r.width, y=(e.clientY-r.top)/r.height;
        card.classList.add('is-tilting');
        card.style.setProperty('--ry',((x-.5)*12).toFixed(2)+'deg');
        card.style.setProperty('--rx',((.5-y)*12).toFixed(2)+'deg');
        card.style.setProperty('--mx',(x*100).toFixed(1)+'%');
        card.style.setProperty('--my',(y*100).toFixed(1)+'%');
      });
      card.addEventListener('mouseleave',function(){
        card.classList.remove('is-tilting');
        card.style.setProperty('--rx','0deg'); card.style.setProperty('--ry','0deg');
      });
    });

    // Światło podążające za kursorem na dużych blokach
    document.querySelectorAll('.control-box,.booking-box').forEach(function(box){
      box.addEventListener('mousemove',function(e){
        var r=box.getBoundingClientRect();
        box.style.setProperty('--mx',(e.clientX-r.left)+'px');
        box.style.setProperty('--my',(e.clientY-r.top)+'px');
      });
    });

    // Zdjęcie w nagłówku: delikatne 3D i parallax karty
    var hero=document.querySelector('.hero'), photo=document.querySelector('.hero-photo'), hcard=document.querySelector('.hero-card');
    if(hero && photo){
      hero.addEventListener('mousemove',function(e){
        var r=hero.getBoundingClientRect(), x=(e.clientX-r.left)/r.width-.5, y=(e.clientY-r.top)/r.height-.5;
        photo.style.setProperty('--pry',(x*10).toFixed(2)+'deg');
        photo.style.setProperty('--prx',(-y*8).toFixed(2)+'deg');
        if(hcard){ hcard.style.setProperty('--ctx',(x*-24).toFixed(1)+'px'); hcard.style.setProperty('--cty',(y*-16).toFixed(1)+'px'); }
      });
      hero.addEventListener('mouseleave',function(){
        ['--pry','--prx'].forEach(function(p){photo.style.setProperty(p,'0deg');});
        if(hcard){ hcard.style.setProperty('--ctx','0px'); hcard.style.setProperty('--cty','0px'); }
      });
    }
  }

  // ===== Tło: reflektor za kursorem, parallax kul, punkty w specjalizacjach =====
  if(fine && !reduce){
    var glow=document.querySelector('.cursor-glow'), gx=-999, gy=-999, tx=-999, ty=-999, running=false;
    function loop(){ gx+=(tx-gx)*.12; gy+=(ty-gy)*.12; glow.style.transform='translate3d('+gx.toFixed(1)+'px,'+gy.toFixed(1)+'px,0)';
      if(Math.abs(tx-gx)>.5||Math.abs(ty-gy)>.5){requestAnimationFrame(loop);} else {running=false;} }
    window.addEventListener('mousemove',function(e){ tx=e.clientX; ty=e.clientY; if(gx<-900){gx=tx;gy=ty;} glow.classList.add('on'); if(!running){running=true;requestAnimationFrame(loop);} },{passive:true});
    document.addEventListener('mouseleave',function(){ glow.classList.remove('on'); });

    var specs=document.querySelector('.specs');
    if(specs) specs.addEventListener('mousemove',function(e){ var r=specs.getBoundingClientRect();
      specs.style.setProperty('--sx',(e.clientX-r.left)+'px'); specs.style.setProperty('--sy',(e.clientY-r.top)+'px'); });

    var orbs=document.querySelectorAll('.bg-fx .orb'), ticking=false;
    window.addEventListener('scroll',function(){ if(ticking) return; ticking=true; requestAnimationFrame(function(){
      var y=window.scrollY; orbs.forEach(function(o,i){ o.style.translate='0 '+(-y*(.06+i*.04)).toFixed(1)+'px'; }); ticking=false; }); },{passive:true});
  }
  document.getElementById('year').textContent=new Date().getFullYear();
})();