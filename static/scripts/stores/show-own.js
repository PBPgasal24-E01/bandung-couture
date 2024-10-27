const modalShowButton = document.querySelector('.modal-show-button');
const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
const modal = document.querySelector('.modal');
const modalForm = document.querySelector('.modal-form');

refreshStoresContent();

async function refreshStoresContent() {
    var response = await fetch('/stores/deliver-own-stores-content-component');
    var text = await response.text();
    document.querySelector('.stores-content').innerHTML = text;
    
    initializeStoresContent();
}

//script follow-up after stores-content component insertion to DOM 
function initializeStoresContent() {

    //set the image of every store card
    var index = 0;
    document.querySelectorAll('.store-image').forEach((image) => {
        index %= 8;
        image.setAttribute('src', `/static/images/store-default-${(index++)}.jpg`);
    });

    document.querySelectorAll('.delete-store-button').forEach((button) => {
        button.addEventListener('click', () => {

            //this will delete the product with given pk in server side
            fetch(button.getAttribute('data-href'), {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                },
            }).then((response) => {
                if (response.ok) {
                    //refresh the content
                    refreshStoresContent();
                }
                else {
                    window.alert(response.status);
                }
            }).catch((err) => {
                window.alert(err);
            });
        });
    });

    //add listener for every store edit button
    document.querySelectorAll('.edit-store-button').forEach((button) => {
        button.addEventListener('click', () => {

            //get the store form with instance specified by given pk
            fetch(button.getAttribute('data-href')).then((response) => {
                return response.text();
            //convert the response to text => html DOM
            }).then((form) => {
                showModal(form, button.getAttribute('data-pk'));
            }).catch((err) => {
                window.alert(err);
            });
        });
    });
}

modalShowButton.addEventListener('click', () => {
    //get the store form with instance specified by given pk
    fetch('/stores/deliver-store-form').then((response) => {
        return response.text();
    //convert the response to text => html DOM
    }).then((form) => {
        showModal(form);
    }).catch((err) => {
        window.alert(err);
    });
});

document.addEventListener('click', (event) => {
    if (event.target != modalShowButton && !modal.contains(event.target) && modal.classList.contains('fixed')) {
        hideModal();
    }
});

function showModal(form, pk=null) {
    modalForm.innerHTML= `
        <div class="w-full flex flex-col items-center">
            <div class="h-10 bg-gray-700 w-full rounded-t-md flex justify-center items-center text-2xl text-white mb-2">${pk == null ? 'Add Store' : 'Edit Store'}</div>
            <div class="w-[90%] flex flex-col">${form}</div>
            <button type="button" class="store-crud-button text-white w-1/4 h-10 mt-2 rounded bg-gray-700 hover:bg-gray-600">${pk == null ? 'Add Store' : 'Edit Store'}</button>
        </div>
    `
    modalForm.querySelector('.store-crud-button').addEventListener('click', () => {
        if (pk == null) {
            addStore();
        }
        else {
            editStore(pk);
        }
    });
    modal.classList.replace('hidden', 'fixed');
}   

function hideModal() {
    modalForm.innerHTML = "";
    modal.classList.replace('fixed', 'hidden');
}

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
            window.alert(response.status);
        }
    }).catch((err) => {
        window.alert();
    });
}

async function editStore(pk) {
    fetch(`/stores/edit/${pk}`, {
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
            window.alert(response.status);
        }
    }).catch((err) => {
        window.alert();
    });
}