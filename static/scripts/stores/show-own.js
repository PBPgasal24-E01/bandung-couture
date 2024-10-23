const addModal = document.querySelector('.add-modal');
const modalShowButton = document.querySelector('.modal-show-button');
const modalForm = document.querySelector('form');
const storeAddButton = document.querySelector('.store-add-button');

const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

refreshStoresContent();

function showModal() {
    addModal.classList.remove('hidden');   
    addModal.classList.add('fixed');
}

function hideModal() {
    addModal.classList.add('hidden');
    addModal.classList.remove('fixed');
}

modalShowButton.addEventListener('click', () => {
    showModal();
});

document.addEventListener('click', (event) => {
    if (!modalForm.contains(event.target) && event.target != modalShowButton && !addModal.classList.contains('hidden')) {
        hideModal();
    }
});

storeAddButton.addEventListener('click', () => {
    addStore();
});

async function addStore() {
    fetch('/stores/add', {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
        },
        body: new FormData(modalForm),
    }).then((response) => {
        if (response.ok) {
            modalForm.reset();
            hideModal();
            refreshStoresContent();
        }
        else {
            window.alert('not ok');
        }
    }).catch((err) => {
        window.alert();
    });
}

async function refreshStoresContent() {
    var response = await fetch('/stores/deliver-own-stores-content-component');
    var text = await response.text();
    document.querySelector('.stores-content').innerHTML = text;
    
    initializeStoresContent();
}

//script follow-up after stores-content component insertion to DOM 
function initializeStoresContent() {
    var index = 0;
    document.querySelectorAll('.store-image').forEach((image) => {
        index %= 8;
        image.setAttribute('src', `/static/images/store-default-${(index++)}.jpg`);
    });

    document.querySelectorAll('.delete-store-button').forEach((button) => {
        button.addEventListener('click', () => {
            fetch(button.getAttribute('data-href'), {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                },
            }).then((response) => {
                if (response.ok) {
                    refreshStoresContent();
                }
                else {
                    window.alert('not ok');
                }
            }).catch((err) => {
                window.alert();
            });
        });
    });
}