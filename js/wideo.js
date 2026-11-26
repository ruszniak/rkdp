/* Filmy w tle (Pexels, kopie w /video). Hero: 3 ujęcia Wrocławia na zmianę (Ostrów Tumski, katedra o zachodzie, Odra z lotu ptaka).
   Pas przed cennikiem: most Grunwaldzki. Na telefonie w hero tylko pierwsze ujęcie (mniejszy plik).
   Wyłączone przy "ogranicz ruch" i oszczędzaniu danych. */
(function(){
  var rm=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  var sd=navigator.connection&&navigator.connection.saveData;
  if(rm||sd)return;
  var small=Math.min(screen.width,innerWidth)<=820;
  function src(v){return small&&v.getAttribute('data-sm')?v.getAttribute('data-sm'):v.getAttribute('data-lg')}
  function load(v){if(!v.src){v.src=src(v);v.load()}}
  // fragment filmu: data-start / data-end (sekundy) – np. żeby pominąć ujęcie przez kratę
  function seg(v){if(v._seg)return;v._seg=1;var a=parseFloat(v.getAttribute('data-start'))||0,b=parseFloat(v.getAttribute('data-end'));
    if(!a&&!b)return;
    v.addEventListener('loadedmetadata',function(){if(v.currentTime<a)v.currentTime=a});
    v.addEventListener('timeupdate',function(){if(b&&v.currentTime>=b)v.currentTime=a});}
  function play(v){seg(v);var r=parseFloat(v.getAttribute('data-rate'));if(r){v.defaultPlaybackRate=r;v.playbackRate=r}v.classList.add('on');var p=v.play();if(p&&p.catch)p.catch(function(){})}

  // pas z mostem (i każde pojedyncze wideo poza hero)
  [].forEach.call(document.querySelectorAll('.n-vbg:not(.n-vplay) video'),function(v){
    if(!('IntersectionObserver' in window)){load(v);play(v);return}
    new IntersectionObserver(function(e){if(e[0].isIntersecting){load(v);play(v)}else if(v.src){v.pause()}},{rootMargin:'300px 0px'}).observe(v);
  });

  // hero: playlista z płynnym przejściem
  var box=document.querySelector('.n-vplay');
  if(!box)return;
  var vids=[].slice.call(box.querySelectorAll('video'));
    if(!vids.length)return;
  var i=0,timer=null,visible=true,SHOW=9000;
  vids.forEach(function(v){v.loop=true;v.addEventListener('error',function(){v.dataset.bad=1})});
  function next(){
    if(!visible)return;
    var cur=vids[i],j=i;
    do{j=(j+1)%vids.length}while(vids[j].dataset.bad&&j!==i);
    if(j===i){timer=setTimeout(next,SHOW);return}
    var nv=vids[j];load(nv);
    function go(){load(vids[(j+1)%vids.length]);nv.currentTime=parseFloat(nv.getAttribute('data-start'))||0;play(nv);setTimeout(function(){cur.classList.remove('on');cur.pause()},1600);i=j;timer=setTimeout(next,SHOW)}
    if(nv.readyState>=3)go();else{var t=setTimeout(function(){nv.removeEventListener('canplay',ok);timer=setTimeout(next,SHOW)},8000);function ok(){clearTimeout(t);go()}nv.addEventListener('canplay',ok,{once:true})}
  }
  load(vids[0]);play(vids[0]);
  if(vids.length>1){
    // kolejne ujęcia dociągamy w tle dopiero po starcie pierwszego
    vids[0].addEventListener('playing',function(){setTimeout(function(){load(vids[1])},2500)},{once:true});
    timer=setTimeout(next,SHOW);
  }
  if('IntersectionObserver' in window) new IntersectionObserver(function(e){
    visible=e[0].isIntersecting;
    if(visible){play(vids[i]);if(vids.length>1&&!timer)timer=setTimeout(next,SHOW)}else{vids[i].pause();clearTimeout(timer);timer=null}
  }).observe(box);
  document.addEventListener('visibilitychange',function(){
    if(document.hidden)[].forEach.call(document.querySelectorAll('.n-vbg video'),function(v){v.pause()});
    else if(visible)play(vids[i]);
  });
})();
