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
    attachWishlistEventListeners();
    var index = 0;
    document.querySelectorAll('.store-image').forEach((image) => {
        index %= 8;
        image.setAttribute('src', `/static/images/store-default-${(index++)}.jpg`);
    });
    console.log("halo")
}

async function toggleWishlist(storeId, button) {
    const isAdding = button.classList.contains('add'); // Check if it's currently adding

    try {
        const response = await fetch(isAdding ? `/wishlist/add/${storeId}/` : `/wishlist/remove/${storeId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            },
        });
        const data = await response.json();
        if (isAdding){
            button.innerText = "- Remove";
            button.classList.remove('add');
            button.classList.remove('bg-green-500');
            button.classList.add('remove', 'bg-red-500');
        } else {
            button.innerText = "+ Wishlist";
            button.classList.remove('remove');
            button.classList.remove('bg-red-500');
            button.classList.add('add', 'bg-green-500');
        }
    } catch (error) {
        console.error('Error toggling wishlist:', error);
    }
}

// Attach event listeners to dynamically loaded buttons
function attachWishlistEventListeners() {
    document.querySelectorAll('.wishlist-btn').forEach((button) => {
        button.addEventListener('click', function() {
            const storeId = this.getAttribute('data-store-id');
            toggleWishlist(storeId, this); 
        });
    });
}



// Get CSRF token helper function
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Initially populate the stores content container with all stores
refreshStoresContent();