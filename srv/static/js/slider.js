function init(containerId, interval = 3000, direction = 1) {
    const container = document.getElementById(containerId);
    console.log(container)
    const slides = container.querySelectorAll(".slides");
    let currentSlide = 0;

    function slider() {
        // console.log(slides, currentSlide, direction)
        slides[currentSlide].classList.remove('show')
        currentSlide = currentSlide + direction
    
        if (currentSlide < 0) {
            currentSlide = slides.length - 1
        } else if (currentSlide > slides.length - 1) {
            currentSlide = 0
        }
    
        slides[currentSlide].classList.add('show')
    }

    setInterval(slider, interval);
}
