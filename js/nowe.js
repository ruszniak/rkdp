/* Nowe moduły: asystent sprawy, kalkulator terminu, pojawianie się */
(function(){
  var d=document;
  var ARR='<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';
  // pojawianie się
  var rv=d.querySelectorAll('.x-rv,.x-steps');
  if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.15});[].forEach.call(rv,function(e){io.observe(e)})}
  else [].forEach.call(rv,function(e){e.classList.add('in')});

  // otwarcie kalendarza rezerwacji (ten sam modal co reszta strony)
  d.addEventListener('click',function(e){var b=e.target.closest('.x-book');if(!b)return;var o=d.querySelector('a[data-booking-open]:not(.x-book)');if(o){e.preventDefault();o.click()}});

  // dni wolne i przesunięcie terminu (art. 12 § 5 Ordynacji podatkowej)
  function easter(y){var a=y%19,b=Math.floor(y/100),c=y%100,dd=Math.floor(b/4),e=b%4,f=Math.floor((b+8)/25),g=Math.floor((b-f+1)/3),h=(19*a+b-dd-g+15)%30,i=Math.floor(c/4),k=c%4,l=(32+2*e+2*i-h-k)%7,m=Math.floor((a+11*h+22*l)/451),mo=Math.floor((h+l-7*m+114)/31),da=((h+l-7*m+114)%31)+1;return new Date(y,mo-1,da)}
  var HC={};function holidays(y){if(HC[y])return HC[y];var s={},add=function(dt){s[dt.getMonth()+'-'+dt.getDate()]=1};
    [[0,1],[0,6],[4,1],[4,3],[7,15],[10,1],[10,11],[11,25],[11,26]].forEach(function(x){add(new Date(y,x[0],x[1]))});if(y>=2025)add(new Date(y,11,24));
    var e=easter(y);[0,1,49,60].forEach(function(o){add(new Date(y,e.getMonth(),e.getDate()+o))});return HC[y]=s}
  function free(dt){var w=dt.getDay();return w===0||w===6||holidays(dt.getFullYear())[dt.getMonth()+'-'+dt.getDate()]}
  function shift(dt){var x=new Date(dt);while(free(x))x.setDate(x.getDate()+1);return x}
  var MON=['stycznia','lutego','marca','kwietnia','maja','czerwca','lipca','sierpnia','września','października','listopada','grudnia'],DOW=['niedziela','poniedziałek','wtorek','środa','czwartek','piątek','sobota'];
  function fmt(x){return x.getDate()+' '+MON[x.getMonth()]}
  function today(){var t=new Date();t.setHours(0,0,0,0);return t}
  function diff(a,b){return Math.round((b-a)/864e5)}
  function dni(n){return n===1?'1 dzień':n+' dni'}

  var cd=d.getElementById('x-date'),cr=d.getElementById('x-res');
  if(cd&&cr){var term=7,t0=today();cd.value=new Date(t0.getTime()-t0.getTimezoneOffset()*6e4).toISOString().slice(0,10);
    var bs=d.querySelectorAll('.x-terms button');
    [].forEach.call(bs,function(b){b.addEventListener('click',function(){term=+b.dataset.t;[].forEach.call(bs,function(x){x.setAttribute('aria-pressed',x===b)});calc()})});
    cd.addEventListener('input',calc);
    function calc(){if(!cd.value){cr.innerHTML='';return}var p=cd.value.split('-'),end=new Date(+p[0],p[1]-1,+p[2]);end.setDate(end.getDate()+term);var real=shift(end),left=diff(today(),real),moved=real-end!==0;
      cr.innerHTML='<div><label>Ostatni dzień na odpowiedź</label><div class="big">'+fmt(real)+' '+real.getFullYear()+'</div><span class="dow">'+DOW[real.getDay()]+(moved?' – przesunięty z dnia wolnego ('+fmt(end)+')':'')+'</span></div>'+
        '<span class="x-left'+(left<=3?' hot':'')+'">'+(left<0?'termin minął '+dni(-left)+' temu':left===0?'to dziś!':'zostało '+dni(left))+'</span>'+
        '<p class="x-note">Liczymy od dnia następującego po doręczeniu (art. 12 § 1 Ordynacji podatkowej). Gdy koniec terminu wypada w sobotę lub dzień wolny, przesuwa się na najbliższy dzień roboczy (art. 12 § 5). Termin jest zachowany, jeśli przed jego upływem nadasz pismo w polskiej placówce operatora wyznaczonego lub wyślesz je przez e-Urząd Skarbowy. Kalkulator ma charakter pomocniczy – zawsze sprawdź termin wskazany w piśmie.</p>'}
    calc()}

  var A={
    wezwanie:{tag:['hot','Liczy się termin'],h:'Wezwanie z urzędu skarbowego to zwykle czynności sprawdzające – dobrze poprowadzone kończą sprawę na tym etapie.',s:['Sprawdź datę doręczenia i termin w piśmie – policz go w kalkulatorze terminu.','Nie odpowiadaj „na szybko” – każde zdanie trafia do akt sprawy.','Prześlij nam skan pisma – ocenimy, czy wystarczą wyjaśnienia, czy potrzebna jest korekta.'],l:'/czynnosci-sprawdzajace/',lt:'Wezwanie z urzędu – jak działamy'},
    kontrola:{tag:['hot','Działaj przed wszczęciem'],h:'Zawiadomienie o kontroli daje 7–30 dni na przygotowanie. Do dnia wszczęcia możesz jeszcze złożyć korektę.',s:['Nie czekaj na kontrolerów – umów spotkanie z doradcą jeszcze w tym tygodniu.','Przejrzymy rozliczenia za kontrolowany okres i ocenimy ryzyko.','Zgłosimy pełnomocnictwo – kontakt z urzędem przejdzie przez nas.'],l:'/kontrola-podatkowa/',lt:'Kontrola podatkowa krok po kroku'},
    decyzja:{tag:['hot','14 dni na odwołanie'],h:'Od decyzji urzędu skarbowego masz 14 dni na odwołanie, a od decyzji dyrektora izby – 30 dni na skargę do WSA.',s:['Zapisz datę doręczenia decyzji – od niej liczy się termin.','Nie płać „dla świętego spokoju”, zanim doradca oceni szanse odwołania.','Przygotujemy odwołanie lub skargę i poprowadzimy sprawę do końca.'],l:'/odwolanie-od-decyzji/',lt:'Odwołania i skargi do WSA'},
    optymalizacja:{tag:['calm','Planowo'],h:'Legalnie płacić mniej to najczęściej kwestia formy działalności i sposobu wypłaty pieniędzy z firmy.',s:['Porównamy skalę, liniowy, ryczałt i estoński CIT na liczbach Twojej firmy.','Sprawdzimy najtańszą drogę wypłaty: wynagrodzenie zarządu, art. 176 KSH, dywidenda, najem.','Zmiany wdrożymy tak, żeby były bezpieczne przy ewentualnej kontroli.'],l:'/forma-opodatkowania/',lt:'Forma opodatkowania'},
    ksiegowosc:{tag:['calm','Planowo'],h:'Księgowość prowadzona pod nadzorem doradcy podatkowego – gdy przyjdzie pismo z urzędu, zajmuje się nim ta sama kancelaria.',s:['Bezpłatna 20-minutowa rozmowa i wycena dopasowana do liczby dokumentów.','Przejmiemy dokumentację od obecnego biura – bez przerwy w rozliczeniach.','Masz stały dostęp do doradcy, a nie tylko do księgowej.'],l:'/cennik/',lt:'Zobacz ceny abonamentów'},
    fundacja:{tag:['calm','Planowo'],h:'Fundacja rodzinna prowadzi pełne księgi i ma własne zasady CIT – rozliczamy ją księgowo i podatkowo w jednym miejscu.',s:['Sprawdzimy, czy planowana działalność mieści się w katalogu działalności dozwolonej.','Poprowadzimy księgi, sprawozdanie finansowe i rozliczenia CIT, w tym podatek od świadczeń.','Doradzimy, jak bezpiecznie wypłacać świadczenia beneficjentom.'],l:'#fundacje',lt:'Fundacje rodzinne – zakres'},
    sukcesja:{tag:['calm','Planowo'],h:'Przekazanie firmy dzieciom można przeprowadzić bez zbędnego podatku – trzeba to tylko dobrze zaplanować.',s:['Ocenimy, czy lepsza będzie darowizna, zarząd sukcesyjny czy fundacja rodzinna.','Przygotujemy plan krok po kroku, z kosztami i terminami.','Zadbamy o to, żeby firma działała bez przerwy w trakcie zmian.'],l:'/firmy-rodzinne-sukcesja/',lt:'Firmy rodzinne i sukcesja'}
  };
  var ans=d.getElementById('x-ans'),chips=d.querySelectorAll('.x-chip');
  function show(k){var a=A[k];if(!a||!ans)return;ans.classList.remove('swap');void ans.offsetWidth;
    ans.innerHTML='<span class="x-tag '+a.tag[0]+'">'+(a.tag[0]==='hot'?'<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>':'')+a.tag[1]+'</span><h4>'+a.h+'</h4><ol>'+a.s.map(function(x){return '<li>'+x+'</li>'}).join('')+'</ol><div class="x-row"><a class="x-btn x-book" href="/#termin" data-booking-open>Umów konsultację '+ARR+'</a><a class="x-more" href="'+a.l+'">'+a.lt+'</a></div>';
    ans.classList.add('swap');[].forEach.call(chips,function(c){c.setAttribute('aria-pressed',c.dataset.k===k)})}
  [].forEach.call(chips,function(c){c.addEventListener('click',function(){show(c.dataset.k)})});
  if(ans)show('wezwanie');
})();
