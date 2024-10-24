// wishlist.js
document.addEventListener("DOMContentLoaded", function() {
    const categoriesContainer = document.querySelector('.carousel-items');
    const toggleButton = document.getElementById('toggleButton');
    const categories = Array.from(categoriesContainer.children); // Convert HTMLCollection to Array
    const initialVisibleCount = 5; // Number of categories to show initially
    let isExpanded = false; // State to track if the view is expanded

    // Function to show only the first 'n' categories
    function showInitialCategories() {
        categories.forEach((category, index) => {
            category.style.display = (index < initialVisibleCount) ? 'flex' : 'none';
        });
    }

    // Function to toggle categories display
    function toggleCategories() {
    console.log("Toggle button clicked. Current state:", isExpanded);
    if (isExpanded) {
        console.log("Collapsing categories...");
        categories.forEach((category, index) => {
            category.style.display = (index < initialVisibleCount) ? 'flex' : 'none';
        });
        toggleButton.style.borderLeftColor = 'black'; // Change arrow color (optional)
    } else {
        console.log("Expanding categories...");
        categories.forEach(category => {
            category.style.display = 'flex';
        });
        toggleButton.style.borderLeftColor = 'gray'; // Change arrow color (optional)
    }
    isExpanded = !isExpanded; // Toggle the state
}


    // Initialize the view by showing initial categories
    showInitialCategories();

    // Add event listener to the toggle button
    toggleButton.addEventListener('click', toggleCategories);
});
