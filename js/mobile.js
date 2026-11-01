/* RKDP – kompaktowy widok na telefonie: zwijane sekcje i karuzele ze strzałkami */
(function(){
  if(!matchMedia('(max-width:640px)').matches)return;
  var d=document,ARR='<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 6l6 6-6 6"/></svg>';
  function details(title,cls,open){var el=d.createElement('details');el.className='m-acc in '+(cls||'');if(open)el.open=true;var s=d.createElement('summary');s.innerHTML='<span>'+title+'</span><i aria-hidden="true"></i>';el.appendChild(s);return el}
  // 1. treść podstron: każda sekcja z nagłówkiem h2 zwijana
  [].forEach.call(d.querySelectorAll('.prose'),function(pr){var kids=[].slice.call(pr.children),cur=null,first=true;
    kids.forEach(function(k){if(k.tagName==='H2'){cur=details(k.innerHTML,'m-sec',first);first=false;var body=d.createElement('div');body.className='m-body';cur.appendChild(body);pr.insertBefore(cur,k);k.remove();return}
      if(k.matches('.faq-block,.related,.author,section'))return cur=null;if(cur)cur.lastChild.appendChild(k)})});
  // 2. zespół: listy doświadczenia zwijane
  [].forEach.call(d.querySelectorAll('.team-card ul'),function(ul){var dt=details('Doświadczenie i funkcje','m-more');var b=d.createElement('div');b.className='m-body';ul.parentNode.insertBefore(dt,ul);b.appendChild(ul);dt.appendChild(b)});
  // 3. stopka: kolumny linków zwijane
  [].forEach.call(d.querySelectorAll('.footer nav'),function(nv){var k=nv.querySelector('.k');if(!k)return;var dt=details(k.textContent,'m-foot');var b=d.createElement('div');b.className='m-body';[].slice.call(nv.children).forEach(function(c){if(c===k){c.remove();return}b.appendChild(c)});dt.appendChild(b);nv.appendChild(dt)});
  // 4. karuzele ze strzałkami
  function carousel(track){if(!track||track.children.length<2||track.dataset.mc)return;track.dataset.mc=1;track.classList.add('m-track');
    var wrap=d.createElement('div');wrap.className='m-car';track.parentNode.insertBefore(wrap,track);wrap.appendChild(track);
    var nav=d.createElement('div');nav.className='m-nav';nav.innerHTML='<button type="button" class="m-prev" aria-label="Poprzedni">'+ARR+'</button><span class="m-dots"></span><button type="button" class="m-next" aria-label="Następny">'+ARR+'</button>';wrap.appendChild(nav);
    var items=[].slice.call(track.children),dots=nav.querySelector('.m-dots');items.forEach(function(_,i){var b=d.createElement('i');dots.appendChild(b)});
    function idx(){var x=track.scrollLeft,best=0,bd=1e9;items.forEach(function(it,i){var dd=Math.abs(it.offsetLeft-track.offsetLeft-x-0);if(dd<bd){bd=dd;best=i}});return best}
    function upd(){var i=idx();[].forEach.call(dots.children,function(b,j){b.classList.toggle('on',j===i)});nav.querySelector('.m-prev').disabled=i===0;nav.querySelector('.m-next').disabled=i===items.length-1}
    function go(i){i=Math.max(0,Math.min(items.length-1,i));track.scrollTo({left:items[i].offsetLeft-track.offsetLeft,behavior:'smooth'})}
    nav.querySelector('.m-prev').onclick=function(){go(idx()-1)};nav.querySelector('.m-next').onclick=function(){go(idx()+1)};
    track.addEventListener('scroll',function(){clearTimeout(track._t);track._t=setTimeout(upd,60)},{passive:true});upd()}
  ['.n-prs','.price-grid','.related .cards','.prose .facts'].forEach(function(s){[].forEach.call(d.querySelectorAll(s),carousel)});
})();
