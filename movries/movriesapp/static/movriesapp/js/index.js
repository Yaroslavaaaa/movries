window.addEventListener('scroll', e => {
    document.body.style.cssText += `--scrollTop: ${this.scrollY}px`
})



var replyBtns = document.querySelectorAll('.reply-btn');
replyBtns.forEach(function (replyBtn) {
    replyBtn.addEventListener('click', function () {
        var commentId = this.getAttribute('data-id');
        var replyForm = document.querySelector('#reply-form-' + commentId);
        replyForm.style.display = replyForm.style.display === 'none' ? 'block' : 'none';
    });
});


var flkty = new Flickity('.gallery', {
    wrapAround: true,
    imagesLoaded: true
});

flkty.on('scroll', function () {
    $('.gallery-cell').each(function () {
        var $cell = $(this);
        var cellCenter = $cell.position().left + $cell.width() / 2;
        var galleryCenter = flkty.x + flkty.width / 2;

        var delta = Math.abs(cellCenter - galleryCenter) / flkty.width;
        var scale = 1 - delta * 0.3; // Увеличиваем масштаб центрального элемента

        $cell.css('transform', 'scale(' + scale + ')');
    });
});


document.addEventListener('DOMContentLoaded', function () {
    const slideWrapper = document.querySelector('.carousel-wrapper');
    const slideWidth = document.querySelector('.carousel-container').offsetWidth / 4; // Ширина одного слайда
    let currentIndex = 0;
    let targetIndex = 0;

    document.querySelector('.next-btn').addEventListener('click', function () {
        targetIndex = (currentIndex + 1) % 4;
        animateCarousel();
    });

    document.querySelector('.prev-btn').addEventListener('click', function () {
        targetIndex = (currentIndex - 1 + 4) % 4;
        animateCarousel();
    });

    function animateCarousel() {
        const startTime = performance.now();
        const duration = 500; // Длительность анимации в миллисекундах

        function update() {
            const currentTime = performance.now();
            const progress = (currentTime - startTime) / duration;

            if (progress < 1) {
                const newPosition = currentIndex * slideWidth + (targetIndex - currentIndex) * slideWidth * progress;
                slideWrapper.style.transform = 'translateX(' + -newPosition + 'px)';
                requestAnimationFrame(update);
            } else {
                currentIndex = targetIndex;
                slideWrapper.style.transform = 'translateX(' + -currentIndex * slideWidth + 'px)';
            }
        }

        update();
    }
});
































