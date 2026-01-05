document.addEventListener('DOMContentLoaded', function(){
  const lightbox = document.getElementById('lightbox');
  const img = lightbox.querySelector('.lightbox-img');
  const caption = lightbox.querySelector('.lightbox-caption');
  const closeBtn = lightbox.querySelector('.lightbox-close');

  function openLightbox(src, alt){
    img.src = src;
    img.alt = alt || '';
    caption.textContent = alt || '';
    lightbox.setAttribute('aria-hidden','false');
    lightbox.classList.add('open');
    document.body.style.overflow = 'hidden';
  }

  function closeLightbox(){
    lightbox.setAttribute('aria-hidden','true');
    lightbox.classList.remove('open');
    img.src = '';
    caption.textContent = '';
    document.body.style.overflow = '';
  }

  closeBtn.addEventListener('click', closeLightbox);
  lightbox.addEventListener('click', function(e){
    if(e.target === lightbox) closeLightbox();
  });

  // Only attach lightbox behavior to explicit links with class .lightbox-link
  // This prevents images from opening on click unless intentionally marked.
  function attachTo(el){
    if(!el) return;
    // set pointer cursor only for anchors
    if (el.tagName === 'A') el.style.cursor = 'pointer';
    el.addEventListener('click', function(e){
      // allow links to still be followed with ctrl/cmd/shift click
      if (e.metaKey || e.ctrlKey || e.shiftKey) return;
      e.preventDefault();
      const src = el.href;
      openLightbox(src, el.getAttribute('title') || el.getAttribute('aria-label') || 'Photo');
    });
  }

  // Attach only to explicit lightbox links
  document.querySelectorAll('.lightbox-link').forEach(function(a){ attachTo(a); });
});
