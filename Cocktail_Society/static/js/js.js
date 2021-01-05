const navSlide = () => {
    const burger = document.querySelector('.burger');
    const nav = document.querySelector('.nav-links-account');
    const navLinks = document.querySelectorAll('.nav-links-account li');

    burger.addEventListener('click', () => {
    //Toggle nav
        nav.classList.toggle('nav-active');
        //Animate links
            navLinks.forEach((link, index) => {
        if (link.style.animation) {
            link.style.animation = '';
        } else {
            link.style.animation = `navLinkFade 0.5s ease forwards ${index / 7 + 1.5}s`;
        }
    });
    //Burger animation
    burger.classList.toggle('toggle');
    });
}

navSlide();


$('.rating a').on('click', function(e){let value = $(this).data('value');
    %.ajax({
        url:})})