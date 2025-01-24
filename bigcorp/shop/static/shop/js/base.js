const date = new Date();
document.querySelector(".year").innerHTML = date.getFullYear();

setTimeout(function () {
  $("#message").fadeOut("slow");
}, 5000);

document.addEventListener('DOMContentLoaded', function () {
    const dropdowns = document.querySelectorAll('.nav-item.dropdown');
    dropdowns.forEach(dropdown => {
        dropdown.addEventListener('mouseenter', function () {
            const menu = this.querySelector('.dropdown-menu');
            const toggle = this.querySelector('.dropdown-toggle');
            menu.classList.add('show');
            toggle.setAttribute('aria-expanded', 'true');
        });
        dropdown.addEventListener('mouseleave', function () {
            const menu = this.querySelector('.dropdown-menu');
            const toggle = this.querySelector('.dropdown-toggle');
            menu.classList.remove('show');
            toggle.setAttribute('aria-expanded', 'false');
        });
    });
});