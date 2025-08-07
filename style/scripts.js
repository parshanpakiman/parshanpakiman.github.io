
const Utils = {

  addClass: function(element, theClass) {
    element.classList.add(theClass);
  },

  removeClass: function(element, theClass) {
    element.classList.remove(theClass);
  },

  showMore: function(element, excerpt) {
    element.addEventListener("click", event => {
      const linkText = event.target.textContent.toLowerCase();
      event.preventDefault();

      console.log(this);
      if (linkText == "show more") {
        element.textContent = "Show less";
        this.removeClass(excerpt, "excerpt-hidden");
        this.addClass(excerpt, "excerpt-visible");
      } else {
        element.textContent = "Show more";
        this.removeClass(excerpt, "excerpt-visible");
        this.addClass(excerpt, "excerpt-hidden");
      }
    });
  }
};

const ExcerptWidget = {
  showMore: function(showMoreLinksTarget, excerptTarget) {
   const showMoreLinks = document.querySelectorAll(showMoreLinksTarget);

   showMoreLinks.forEach(function(link) {
     const excerpt = link.previousElementSibling.querySelector(excerptTarget);
     Utils.showMore(link, excerpt);
   });
  }
};

ExcerptWidget.showMore('.js-show-more', '.js-excerpt');



function loadText(fileName, paragraphId) {
    fetch(fileName)
        .then(response => response.text())
        .then(data => {
            document.getElementById(paragraphId).innerText = data;
        })
        .catch(error => console.error('Error loading text:', error));
}






// scripts/timeline.js
(() => {
  'use strict';

  const container = document.querySelector('.timeline-container');
  const items = container ? Array.from(container.querySelectorAll('.timeline-item')) : [];
  const research = document.getElementById('research-content');
  if (!container || items.length === 0 || !research) return;

  const GAP = 300; // ms between each item

  // Reduced motion: reveal everything immediately
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    items.forEach(el => el.classList.add('show'));
    research.classList.add('show');
    return;
  }

  // Reveal items when the timeline enters the viewport
  const io = new IntersectionObserver(([entry]) => {
    if (!entry.isIntersecting) return;

    items.forEach((el, i) => {
      setTimeout(() => el.classList.add('show'), i * GAP);
    });

    // After the LAST item finishes its transition, reveal research
    const last = items[items.length - 1];
    const onEnd = (e) => {
      if (e.propertyName !== 'opacity') return; // wait for fade to finish
      research.classList.add('show');
      last.removeEventListener('transitionend', onEnd);
    };
    last.addEventListener('transitionend', onEnd);

    io.disconnect();
  }, { threshold: 0.2 });

  io.observe(container);
})();