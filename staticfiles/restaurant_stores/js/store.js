// JavaScript for carousel functionality
let currentIndex = 0;
const items = document.querySelectorAll(".carousel-item");

function showSlide(index) {
  items.forEach((item, i) => {
    item.style.transform = `translateX(${100 * (i - index)}%)`;
  });
}

function prevSlide() {
  currentIndex = currentIndex > 0 ? currentIndex - 1 : items.length - 1;
  showSlide(currentIndex);
}

function nextSlide() {
  currentIndex = currentIndex < items.length - 1 ? currentIndex + 1 : 0;
  showSlide(currentIndex);
}

// Initialize carousel
showSlide(currentIndex);
