const carouselTrack = document.querySelector('.carousel-track');
const carouselItems = document.querySelector('.carousel-items');

const leftButton = document.querySelector('.left-button');
const rightButton = document.querySelector('.right-button');

const carouselItemsCount = document.querySelectorAll('.carousel-item').length;

var lastCarouselClicked = null;

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
        if (lastCarouselClicked != null) {
            lastCarouselClicked.classList.replace('translate-y-4', 'translate-y-0');
        }
        item.classList.remove('translate-y-0');
        item.classList.add('translate-y-4');
        lastCarouselClicked = item;
        refreshStoresContent(item.getAttribute('data-category'));
    });
});

//initially populate the stores content container with all stores
refreshStoresContent();

async function refreshStoresContent(category = null) {
    var url = `/stores/deliver-all-stores-content-component`;
    if (category != null) {
        url = url.concat('?category=' + category);
        document.querySelector('.category-title').innerHTML = category;
    }
    var response = await fetch(url);
    var text = await response.text();
    document.querySelector('.stores-content').innerHTML = text;

    var index = 0;
    document.querySelectorAll('.store-image').forEach((image) => {
        index %= 8;
        image.setAttribute('src', `/static/images/store-default-${(index++)}.jpg`);
    });
}