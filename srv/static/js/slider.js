function init(containerId, interval=3000, direction=1) {
    const container = document.getElementById(containerId)
    const slides = container.querySelectorAll('.slides')
    let currentSlide = 0

    function slider() {
        slides[currentSlide].classList.remove('show')
        currentSlide = currentSlide + direction

        if (currentSlide < 0) {
            currentSlide = slides.length - 1
        } else if (currentSlide > slides.length - 1) {
            currentSlide = 0
        }

        slides[currentSlide].classList.add('show')
    }

    setInterval(slider, interval)
}


function initNewsTicker(){
    const newsSingleAll = document.querySelectorAll(".news-container .news-single")

    let currentActive = 0
    const totalNews = newsSingleAll.length
    const duration = 5000 // 5 sec

    const removeAllActive = () => {
        newsSingleAll.forEach((n) => {
            n.classList.remove("active")
        })
    }

    const changeNews = () => {
        if (currentActive >= totalNews - 1)  currentActive = 0
        else currentActive += 1
        removeAllActive()
        newsSingleAll[currentActive].classList.add("active")
    }

    setInterval(changeNews, duration)
}
