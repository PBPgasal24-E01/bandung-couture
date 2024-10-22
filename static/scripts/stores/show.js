const carouselTrack = document.querySelector('.carousel-track');
const carouselItems = document.querySelector('.carousel-items');

const leftButton = document.querySelector('.left-button');
const rightButton = document.querySelector('.right-button');

const carouselItemsCount = document.querySelectorAll('.carousel-item').length;

if(carouselItemsCount <= 4){
    rightButton.classList.add('invisible')
}

let dx = 0;
document.querySelector('.left-button').addEventListener('click', () => {
    if(dx > 0){
        dx--;
        carouselItems.style.transform = `translateX(-${(dx * 24.8)}%)`
    }
    if(dx == 0){
        leftButton.classList.add('invisible')
    }
    if(dx == carouselItemsCount - 5){
        rightButton.classList.remove('invisible');
    }
});
document.querySelector('.right-button').addEventListener('click', () => {
    if(dx < carouselItemsCount - 4){
        dx++;
        carouselItems.style.transform = `translateX(-${dx * 24.8}%)`
    }
    if(dx == 1){
        leftButton.classList.remove('invisible')
    }
    if(dx == carouselItemsCount - 4){
        rightButton.classList.add('invisible');
    }
});

let index = 0 
document.querySelectorAll('.carousel-item').forEach((item) => {
    item.style.backgroundImage = `url('/static/images/category-default-${index}.jpg')`;

    index = ++index % 5

    item.addEventListener('click', () => {
        window.location.href = `/stores/show?category=${item.getAttribute('data-category')}`
    });
});