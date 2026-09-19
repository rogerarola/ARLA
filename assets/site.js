/* arlamusic.com: menu, reveal-on-scroll, artwork tilt, year. No scroll listeners. */
(function(){
  var yr=document.getElementById('yr');if(yr)yr.textContent=new Date().getFullYear();

  var btn=document.getElementById('menu-btn'),menu=document.getElementById('menu');
  if(btn&&menu){
    menu.hidden=false;
    var setMenu=function(open){
      document.body.classList.toggle('menu-open',open);
      btn.setAttribute('aria-expanded',open?'true':'false');
      btn.setAttribute('aria-label',open?'Close menu':'Open menu');
    };
    btn.addEventListener('click',function(){setMenu(!document.body.classList.contains('menu-open'))});
    menu.addEventListener('click',function(e){if(e.target.closest('a'))setMenu(false)});
    document.addEventListener('keydown',function(e){if(e.key==='Escape')setMenu(false)});
    window.addEventListener('resize',function(){if(window.innerWidth>860)setMenu(false)});
  }

  /* Pages without a full-bleed hero keep the nav backdrop on from the start. */
  var nav=document.querySelector('.nav');
  if(nav&&!document.querySelector('.hero'))nav.classList.add('solid');

  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Artwork leans a few degrees toward the pointer (desktop only).
     Same values as pulso-studios.com: 2.5deg at the edge, 1100px perspective. */
  if(!reduce&&window.matchMedia('(hover: hover) and (pointer: fine)').matches){
    document.querySelectorAll('.tilt').forEach(function(media){
      var raf=0;
      media.addEventListener('pointermove',function(e){
        if(raf)return;
        raf=requestAnimationFrame(function(){
          raf=0;
          var r=media.getBoundingClientRect();
          var x=(e.clientX-r.left)/r.width-0.5;
          var y=(e.clientY-r.top)/r.height-0.5;
          var MAX_TILT=2.5; /* degrees at the very edge of the cover */
          media.style.setProperty('--ry',(x*2*MAX_TILT).toFixed(2)+'deg');
          media.style.setProperty('--rx',(y*-2*MAX_TILT).toFixed(2)+'deg');
        });
      });
      media.addEventListener('pointerleave',function(){
        media.style.setProperty('--rx','0deg');
        media.style.setProperty('--ry','0deg');
      });
    });
  }

  /* Credits sentence: words rise once when it comes into view. */
  var splits=document.querySelectorAll('[data-split]');
  if(splits.length){
    if(!('IntersectionObserver' in window)||reduce){splits.forEach(function(el){el.classList.add('in')});}
    else{
      var so=new IntersectionObserver(function(entries){
        entries.forEach(function(e){if(e.isIntersecting||e.boundingClientRect.top<0){e.target.classList.add('in');so.unobserve(e.target)}});
      },{threshold:0.35});
      splits.forEach(function(el){so.observe(el)});
    }
  }

  var items=document.querySelectorAll('.rv');
  if(!items.length)return;
  if(!('IntersectionObserver' in window)||reduce){
    items.forEach(function(el){el.classList.add('in')});return;
  }
  var io=new IntersectionObserver(function(entries){
    entries.forEach(function(e){
      if(e.isIntersecting||e.boundingClientRect.top<0){
        var sibs=Array.prototype.slice.call(e.target.parentNode.children).filter(function(n){return n.classList.contains('rv')});
        var i=Math.min(sibs.indexOf(e.target),6);
        e.target.style.transitionDelay=(i>0?i*0.08:0)+'s';
        e.target.classList.add('in');
        io.unobserve(e.target);
      }
    });
  },{threshold:0.12,rootMargin:'0px 0px -6% 0px'});
  items.forEach(function(el){io.observe(el)});
})();
