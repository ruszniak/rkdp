/* RKDP – płynny ruch: Lenis (płynne przewijanie) + GSAP ScrollTrigger + efekty w stylu React Bits
   (BlurText, CountUp, Magnet, SpotlightCard). Wyłączone przy „ogranicz ruch”. */
(function(){
  if(!window.gsap || !window.ScrollTrigger) return;
  var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine=matchMedia('(hover:hover) and (pointer:fine)').matches;
  gsap.registerPlugin(ScrollTrigger);
  document.documentElement.classList.add('mo-on');

  /* 1. Lenis – płynne przewijanie */
  var lenis=null;
  if(window.Lenis && !reduce){
    lenis=new Lenis({lerp:.09,smoothWheel:true,wheelMultiplier:.95,
      prevent:function(n){return !!(n.closest&&n.closest('dialog,.nav-links.open,#inline-container'))}});
    lenis.on('scroll',ScrollTrigger.update);
    gsap.ticker.add(function(t){lenis.raf(t*1000)}); gsap.ticker.lagSmoothing(0);
    // kotwice (#kontakt, #cennik…) płynnie, z miejscem na nagłówek
    document.addEventListener('click',function(e){
      var a=e.target.closest&&e.target.closest('a[href*="#"]'); if(!a||a.hasAttribute('data-booking-open')) return;
      var u=new URL(a.href,location.href); if(u.pathname!==location.pathname||!u.hash) return;
      var t=document.querySelector(u.hash); if(!t) return;
      e.preventDefault(); lenis.scrollTo(t,{offset:-90,duration:1.3}); history.replaceState(null,'',u.hash);
    });
    var dlg=document.getElementById('booking-modal');
    if(dlg) new MutationObserver(function(){dlg.open?lenis.stop():lenis.start()}).observe(dlg,{attributes:true,attributeFilter:['open']});
  }

  /* 2. Pasek postępu przewijania */
  var bar=document.createElement('div'); bar.className='mo-progress'; bar.setAttribute('aria-hidden','true'); document.body.appendChild(bar);
  gsap.to(bar,{scaleX:1,ease:'none',scrollTrigger:{start:0,end:'max',scrub:.3}});

  if(reduce) return;

  /* 3. Hero – tekst odpływa i wygasza się przy przewijaniu */
  var copy=document.getElementById('n-copy');
  if(copy) gsap.to(copy,{yPercent:-14,opacity:.15,ease:'none',scrollTrigger:{trigger:'#n-hero',start:'top top',end:'bottom top',scrub:true}});
  var wav=document.getElementById('n-wav');
  if(wav) gsap.to(wav,{yPercent:40,opacity:0,ease:'none',scrollTrigger:{trigger:'#n-hero',start:'top top',end:'bottom top',scrub:true}});

  /* 4. BlurText – nagłówki sekcji wchodzą słowo po słowie z rozmycia */
  function split(h){
    var out=document.createDocumentFragment();
    function words(txt,gold){
      txt.split(/(\s+)/).forEach(function(p){
        if(!p) return;
        if(/^\s+$/.test(p)){out.appendChild(document.createTextNode(' '));return;}
        var w=document.createElement('span'); w.className='mo-w'+(gold?' n-goldtx':''); w.textContent=p; out.appendChild(w);
      });
    }
    Array.prototype.slice.call(h.childNodes).forEach(function(n){
      if(n.nodeType===3) words(n.textContent,false);
      else if(n.nodeName==='BR') out.appendChild(n.cloneNode());
      else if(n.classList&&n.classList.contains('n-goldtx')){ if(getComputedStyle(n).display==='block') out.appendChild(document.createElement('br')); words(n.textContent,true); }
      else { var w=document.createElement('span'); w.className='mo-w'; w.appendChild(n.cloneNode(true)); out.appendChild(w); }
    });
    h.setAttribute('aria-label',h.textContent.replace(/\s+/g,' ').trim());
    h.innerHTML=''; h.appendChild(out);
    return h.querySelectorAll('.mo-w');
  }
  var blurIn={opacity:1,y:0,filter:'blur(0px)',duration:.9,ease:'power3.out'};
  // nagłówki z własnym układem linii: animujemy całe linie, bez dzielenia na słowa
  document.querySelectorAll('#cennik .n-big, .n-ct-h, .n-dial-h').forEach(function(h){
    var ls=h.children.length?h.children:[h];
    gsap.fromTo(ls,{opacity:0,y:'0.35em',filter:'blur(10px)'},Object.assign({stagger:.12,scrollTrigger:{trigger:h,start:'top 86%',once:true}},blurIn));
  });
  document.querySelectorAll('.x-hd h2, .x-fr h2').forEach(function(h){
    var ws=split(h);
    gsap.fromTo(ws,{opacity:0,y:'0.45em',filter:'blur(10px)'},{opacity:1,y:0,filter:'blur(0px)',duration:.9,ease:'power3.out',stagger:.06,
      scrollTrigger:{trigger:h,start:'top 86%',once:true}});
  });

  /* 5. CountUp – ceny liczą się od zera */
  document.querySelectorAll('.n-pr b').forEach(function(b){
    var tn=Array.prototype.find.call(b.childNodes,function(n){return n.nodeType===3&&/\d/.test(n.textContent)});
    if(!tn) return; var m=tn.textContent.match(/(\d+(?:[ \u00a0]\d{3})*)/); if(!m) return;
    var val=parseInt(m[1].replace(/\s/g,''),10); if(!val) return;
    var pre=tn.textContent.slice(0,m.index), post=tn.textContent.slice(m.index+m[1].length), o={v:0};
    tn.textContent=pre+'0'+post;
    gsap.to(o,{v:val,duration:1.6,ease:'power2.out',scrollTrigger:{trigger:b,start:'top 90%',once:true},
      onUpdate:function(){tn.textContent=pre+Math.round(o.v)+post}});
  });

  /* 7. Zdjęcie doradcy – delikatny parallax */
  var ph=document.querySelector('.n-me-ph');
  if(ph) gsap.fromTo(ph,{y:40},{y:-40,ease:'none',scrollTrigger:{trigger:'#o-kancelarii',start:'top bottom',end:'bottom top',scrub:true}});

  if(!fine) return;

  /* 8. Magnet – przyciski lekko przyciągają się do kursora */
  document.querySelectorAll('.btn-primary, .btn-outline, .x-btn').forEach(function(btn){
    if(btn.closest('.nav-links')) return;
    btn.style.transition='background .2s, box-shadow .25s, color .2s, border-color .2s';
    var qx=gsap.quickTo(btn,'x',{duration:.5,ease:'power3'}), qy=gsap.quickTo(btn,'y',{duration:.5,ease:'power3'});
    btn.addEventListener('mousemove',function(e){var r=btn.getBoundingClientRect();qx((e.clientX-r.left-r.width/2)*.28);qy((e.clientY-r.top-r.height/2)*.4)});
    btn.addEventListener('mouseleave',function(){qx(0);qy(0)});
  });

  /* 9. SpotlightCard – światło za kursorem na kartach */
  document.querySelectorAll('.x-card, .n-pr, #n-dcard').forEach(function(c){
    c.classList.add('mo-spot');
    c.addEventListener('mousemove',function(e){var r=c.getBoundingClientRect();c.style.setProperty('--sx',(e.clientX-r.left)+'px');c.style.setProperty('--sy',(e.clientY-r.top)+'px')});
  });

  window.addEventListener('load',function(){ScrollTrigger.refresh()});
})();
