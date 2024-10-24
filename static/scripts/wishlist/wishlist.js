document.addEventListener("DOMContentLoaded", function () {
    const categoriesContainer = document.querySelector('.carousel-items');
    const toggleButton = document.getElementById('toggleButton');
    const carouselContainer = document.querySelector('.carousel-container');
    const categories = Array.from(categoriesContainer.children);
    const initialVisibleCount = 5;
    let isExpanded = false;
   
    const expandedState = localStorage.getItem('categoriesExpanded');
    if (expandedState === 'true') {
        isExpanded = true;
        categories.forEach(category => {
            category.style.display = 'flex';
        });
        carouselContainer.classList.add('mt-20');
    } else {
        showInitialCategories();
    }

    function showInitialCategories() {
        categories.forEach((category, index) => {
            category.style.display = (index < initialVisibleCount) ? 'flex' : 'none';
        });
    }

    function toggleCategories() {
        console.log("Toggle button clicked. Current state:", isExpanded);
        if (isExpanded) {
            console.log("Collapsing categories...");
            showInitialCategories();
            carouselContainer.classList.remove('mt-20');
            carouselContainer.classList.add('mt-10');
            toggleButton.style.borderLeftColor = 'black';
            localStorage.setItem('categoriesExpanded', 'false');
        } else {
            console.log("Expanding categories...");
            categories.forEach(category => {
                category.style.display = 'flex';
            });
            carouselContainer.classList.remove('mt-10');
            carouselContainer.classList.add('mt-20');
            toggleButton.style.borderLeftColor = 'gray';
            localStorage.setItem('categoriesExpanded', 'true');
        }
        isExpanded = !isExpanded;
    }

    toggleButton.addEventListener('click', toggleCategories);
    refreshStoresContent();

    async function refreshStoresContent(category = null) {
        let url = `/wishlist/filter/all`;

        if (category != null) {
            url = `/wishlist/filter/${category}`;
        }

        const response = await fetch(url);
        const text = await response.text();

        if (text){
            document.querySelector('.products').innerHTML = text;
            attachWishlistEventListeners();
        }

        refreshRecommendations();

        let index = 0;
        document.querySelectorAll('.store-images').forEach((item) => {
            index %= 8;
            item.setAttribute('src', `/static/images/store-default-${index}.jpg`);
            index++;
        });
    }

    document.querySelectorAll('.wishlist-categories').forEach((item) => {
        item.addEventListener('click', () => {
            lastCarouselClicked = item;
            refreshStoresContent(item.getAttribute('data-category'));
        });
    });

    async function refreshRecommendations() {
        const response = await fetch('/wishlist/recommended_wishlist/');
        const recommendedStoresHtml = await response.text();

        if (recommendedStoresHtml) {
        document.querySelector('.recommend').innerHTML = recommendedStoresHtml;
        attachWishlistEventListeners2(); 
        }

        document.querySelectorAll('.recommend-images').forEach((item) => {
            let randomInt = Math.floor(Math.random() * 8); 
            item.setAttribute('src', `/static/images/store-default-${randomInt}.jpg`);
        });
    }

    async function addWishlist(storeId) {
        try {
            const response = await fetch(`/wishlist/add/${storeId}/` , {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
            });
            await refreshStoresContent();
        } catch (error) {
            console.error('Error toggling wishlist:', error);
        }
    }

    async function removeWishlist(storeId) {
        try {
            const response = await fetch(`/wishlist/remove/${storeId}/` , {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json',
                },
            });
            await refreshStoresContent();
        } catch (error) {
            console.error('Error toggling wishlist:', error);
        }
    }

    function attachWishlistEventListeners() {
        document.querySelectorAll('.wishlist-btn').forEach(button => {
            button.addEventListener('click', function () {
                const storeId = this.getAttribute('data-store-id');
                removeWishlist(storeId);
            });
        });
    }

    function attachWishlistEventListeners2() {
        document.querySelectorAll('.wishlist-btn2').forEach(button => {
            button.addEventListener('click', function () {
                const storeId = this.getAttribute('data-store-id');
                addWishlist(storeId);
            });
        });
    }

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
});