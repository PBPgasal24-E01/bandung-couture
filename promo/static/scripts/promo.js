


async function getPromoEntries(){
    return fetch("{% url 'promo:show_json' %}").then((res) => res.json())
}


// Function to sanitize input
function sanitizeInput(input) {
    return DOMPurify.sanitize(input);
}

// Create Promo Entry
async function createPromoEntry() {
    const formElement = document.querySelector('#promoEntryForm');
    const formData = new FormData(formElement);

    // Sanitize input fields
    const name = sanitizeInput(formData.get('name'));
    const description = sanitizeInput(formData.get('description'));
    formData.set('name', name);
    formData.set('description', description);

    // Send AJAX request
    fetch("{% url 'promo:add_promo_entry_ajax' %}", {
        method: "POST",
        body: formData,
    })
    .then(response => {
        if (response.ok) {
            alert('Promo berhasil ditambahkan!');
            document.getElementById("promoEntryForm").reset(); // Reset form after success
        } else {
            alert('Gagal menambahkan promo.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Gagal menambahkan promo: ' + error.message);
    });

    return false;
}

// Update Promo Entry
async function updatePromoEntry(id) {
    const formElement = document.querySelector(`#promoEntryForm-${id}`);
    const formData = new FormData(formElement);

    // Sanitize input fields
    const name = sanitizeInput(formData.get('name'));
    const description = sanitizeInput(formData.get('description'));
    formData.set('name', name);
    formData.set('description', description);

    // Send AJAX request
    fetch(`/update-promo/${id}`, {
        method: "POST",
        body: formData,
    })
    .then(response => {
        if (response.ok) {
            alert('Promo berhasil diupdate!');
            location.reload(); // Reload page after success
        } else {
            alert('Gagal mengupdate promo.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Gagal mengupdate promo: ' + error.message);
    });

    return false;
}

// Fetch and display rewards promo
async function fetchRewardsPromo() {
    fetch("{% url 'promo:rewards_promo_view' %}", {
        method: "GET",
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.status) {
            document.getElementById("streakDisplay").textContent = `Streak: ${data.streak}`;
            document.getElementById("remainingDisplay").textContent = `Remaining for next streak: ${data.remaining_for_next_streak}`;
        } else {
            alert('Gagal mengambil data rewards promo.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Gagal mengambil data rewards promo: ' + error.message);
    });
}

// Fetch and display promo history
async function fetchPromoHistory() {
    fetch("{% url 'promo:history_promo_view' %}", {
        method: "GET",
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.status) {
            const historyList = data.history;
            const historyContainer = document.getElementById("historyContainer");
            historyContainer.innerHTML = ''; // Clear current content

            historyList.forEach(historyItem => {
                historyContainer.innerHTML += `
                    <div class="history-item">
                        <p><strong>Promo:</strong> ${sanitizeInput(historyItem.promo_name)}</p>
                        <p><strong>Date Redeemed:</strong> ${historyItem.date_redeemed}</p>
                    </div>
                `;
            });
        } else {
            alert('Gagal mengambil riwayat promo.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Gagal mengambil riwayat promo: ' + error.message);
    });
}

// Event Listeners
document.getElementById("promoEntryForm").addEventListener("submit", function (e) {
    e.preventDefault(); 
    createPromoEntry();
});

document.querySelectorAll(".updatePromoForm").forEach(form => {
    form.addEventListener("submit", function (e) {
        e.preventDefault();
        const promoId = this.dataset.promoId;
        updatePromoEntry(promoId);
    });
});

// Call fetch functions where necessary
fetchRewardsPromo();
fetchPromoHistory();
