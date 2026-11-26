/* Filmy w tle (Pexels): Ostrów Tumski w hero, most Grunwaldzki w pasie przed cennikiem.
   Mniejsze pliki na telefonie; wyłączone przy "ogranicz ruch" i oszczędzaniu danych. */
(function(){
  var rm=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  var sd=navigator.connection&&navigator.connection.saveData;
  if(rm||sd)return;
  var small=Math.min(screen.width,innerWidth)<=820;
  function load(v){if(!v.src){v.src=small?v.getAttribute('data-sm'):v.getAttribute('data-lg');v.load()}}
  [].forEach.call(document.querySelectorAll('.n-vbg video'),function(v){
    var hero=!!v.closest('.n-hero');
    if(hero)load(v);
    function play(){v.classList.add('on');var p=v.play();if(p&&p.catch)p.catch(function(){})}
    if(!('IntersectionObserver' in window)){load(v);play();return}
    new IntersectionObserver(function(e){
      if(e[0].isIntersecting){load(v);play()}else if(v.src){v.pause()}
    },{rootMargin:hero?'0px':'300px 0px'}).observe(v);
  });
  document.addEventListener('visibilitychange',function(){
    if(document.hidden)[].forEach.call(document.querySelectorAll('.n-vbg video'),function(v){v.pause()});
  });
})();
