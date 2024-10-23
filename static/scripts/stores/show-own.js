const addModal = document.querySelector('.add-modal');
const modalShowButton = document.querySelector('.modal-show-button');
const modalForm = document.querySelector('form');
const storeAddButton = document.querySelector('.store-add-button');

const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

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
    if (!modalForm.contains(event.target) && event.target != modalShowButton){
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
        }
        else {
            window.alert('not ok');
        }
    }).catch((error) => {
        window.alert('fetch fail');
    });
}