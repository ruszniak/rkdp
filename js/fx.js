/* RKDP – efekty podstron: animowane tło, gilosz w nagłówku, płynne pojawianie się */
(function(){
  var lite=matchMedia('(prefers-reduced-motion: reduce)').matches||(navigator.connection&&navigator.connection.saveData)||(navigator.hardwareConcurrency&&navigator.hardwareConcurrency<=2)||(navigator.deviceMemory&&navigator.deviceMemory<=2);
  if(lite)document.documentElement.classList.add('n-lite');
  var NS='http://www.w3.org/2000/svg';
  // odcienie tła przy przewijaniu
  var a=document.getElementById('n-aura');
  if(a){var P=[[[134,148,174],[128,148,188],[188,202,230],[155,170,200],[207,217,237]],[[171,187,220],[140,162,206],[204,215,236],[134,151,184],[214,223,240]],[[195,207,231],[132,152,192],[219,226,241],[164,180,212],[167,184,219]]];
    var tk=false;function u(){tk=false;var max=document.documentElement.scrollHeight-innerHeight,p=max>0?scrollY/max:0,f=p*(P.length-1),i=Math.min(P.length-2,Math.floor(f)),t=f-i;t=t*t*(3-2*t);
      for(var k=0;k<5;k++){var A=P[i][k],B=P[i+1][k];a.style.setProperty('--h'+(k+1),Math.round(A[0]+(B[0]-A[0])*t)+','+Math.round(A[1]+(B[1]-A[1])*t)+','+Math.round(A[2]+(B[2]-A[2])*t))}}
    addEventListener('scroll',function(){if(!tk){tk=true;requestAnimationFrame(u)}},{passive:true});u();}
  // gilosz w nagłówku podstrony
  var hero=document.querySelector('.page-hero');
  if(hero){var svg=document.createElementNS(NS,'svg');svg.setAttribute('class','n-phros');svg.setAttribute('viewBox','-400 -400 800 800');svg.setAttribute('aria-hidden','true');
    [[318,11,14,22],[372,6,26,14],[262,8,10,12]].forEach(function(c,gi){var g=document.createElementNS(NS,'g');svg.appendChild(g);for(var n=0;n<c[3];n++){var ph=n*Math.PI*2/c[3]/c[2],d='';for(var t=0;t<=360;t++){var an=t/360*Math.PI*2,r=c[0]+c[1]*Math.sin(c[2]*an+ph*c[2]);d+=(t?'L':'M')+(r*Math.cos(an)).toFixed(1)+' '+(r*Math.sin(an)).toFixed(1)}
      var e=document.createElementNS(NS,'path');e.setAttribute('d',d+'Z');e.setAttribute('pathLength','1');e.style.transitionDelay=(gi*.3+n*.035)+'s';e.style.setProperty('--d',((n*1.37+gi*3)%16).toFixed(2));g.appendChild(e)}});
    hero.insertBefore(svg,hero.firstChild);
    requestAnimationFrame(function(){requestAnimationFrame(function(){svg.classList.add('in');if(!lite)setTimeout(function(){svg.classList.add('n-flowing')},3400)})});}
  // płynne pojawianie się
  if(!lite&&'IntersectionObserver' in window){document.documentElement.classList.add('n-rv');
    var els=document.querySelectorAll('.prose>*, .aside>*, .team-card, .price-card, .price-group, .cta-box, .related .card, .faq-block details');
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.08,rootMargin:'0px 0px -5% 0px'});
    [].forEach.call(els,function(el){io.observe(el)});}
})();
