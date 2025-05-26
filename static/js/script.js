window.addEventListener('scroll', function () {
    if (window.scrollY > 50) {
        document.querySelector('.navbar').classList.add('scrolled');
    } else {
        document.querySelector('.navbar').classList.remove('scrolled');
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const adminLabel = document.querySelector('.admin-label');
    if (adminLabel) {
        setTimeout(() => {
            adminLabel.style.textShadow = '0 0 8px #7CFC00';
            setTimeout(() => {
                adminLabel.style.textShadow = 'none';
            }, 1000);
        }, 500);
    }
});
