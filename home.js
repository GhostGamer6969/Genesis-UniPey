// Select elements
const menuIcon = document.querySelector('.menu-icon');
const mobileMenu = document.querySelector('.mobile-menu');

// Toggle mobile menu on clicking the hamburger menu icon
menuIcon.addEventListener('click', () => {
    mobileMenu.classList.toggle('active');
});


