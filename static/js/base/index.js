var carousel = document.querySelector('[data-te-carousel-init]');
var carouselItems = carousel.querySelectorAll('[data-te-carousel-item]');

var activeIndex = carouselItems.length - 1;

function updateCarousel() {
  carouselItems.forEach(function (item, index) {
    item.style.transform = 'translateX(' + (activeIndex - index) * 100 + '%)';
  });
}

function goToNextSlide() {
  activeIndex = (activeIndex - 1 + carouselItems.length) % carouselItems.length;
  updateCarousel();
}

function goToPrevSlide() {
  activeIndex = (activeIndex + 1) % carouselItems.length;
  updateCarousel();
}

document.addEventListener('DOMContentLoaded', function() {
  updateCarousel();

  var prevButton = document.querySelector('[data-te-slide="prev"]');
  prevButton.addEventListener('click', goToPrevSlide);

  var nextButton = document.querySelector('[data-te-slide="next"]');
  nextButton.addEventListener('click', goToNextSlide);
});