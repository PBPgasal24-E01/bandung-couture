
const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
async function getMainForumEntry(){
    const forumJsonUrl = `/forum/show_json_by_id/${pk}/`;
    
    return fetch(forumJsonUrl).then((res) => res.json());
}


async function refreshMainForumEntry(){
    const card = document.getElementById(`card-${pk}`);
    const item = await getMainForumEntry();
    
    const title = DOMPurify.sanitize(item.fields.title);
    const details = DOMPurify.sanitize(item.fields.details);
    let forum_username = item.fields.username;
    let maxLength = 15
    if (window.innerWidth <= 768) { // Adjust the width as per your requirement for mobile
        forum_username = forum_username.length > maxLength ? forum_username.slice(0, maxLength) + '...' : forum_username;
    } 

    const htmlString = `
        <div class="relative break-inside-avoid" id="card-${pk}" >
            <div class="px-10 py-6 bg-white rounded-lg shadow-md">
                <div class="flex justify-between items-center">
                    <span class="font-light text-gray-600">${item.fields.time}</span>
                    ${item.fields.is_author ? `
                        <div class="absolute top-2 right-2 flex space-x-1">
                            <button onclick='editForum("${pk}")' type="button" class="bg-yellow-500 hover:bg-yellow-600 text-white rounded-full p-2 transition duration-300 shadow-md">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-9 w-9" viewBox="0 0 20 20" fill="currentColor">
                                    <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                                </svg>
                            </button>
                            <button onclick="deleteForum('${pk}')" class="bg-red-500 hover:bg-red-600 text-white rounded-full p-2 transition duration-300 shadow-md">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-9 w-9" viewBox="0 0 20 20" fill="currentColor">
                                    <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                                </svg>
                            </button>
                        </div>
                    ` : ''}
                </div>
                <div class="mt-2">
                    <a class="text-2xl text-gray-700 font-bold hover:underline" href="#">${title}</a>
                    <p class="mt-2 text-gray-600 text-wrap">${details}</p>
                    <p hidden id="details-${pk}">${details}</p>
                </div>
                <div class="flex justify-end w-right items-center mt-4">
                    <div>
                        <a class="flex items-center">
                            <p class="text-gray-600">by  @</p>
                            <h1 class="text-gray-700 font-bold">${forum_username}</h1>
                        </a>
                    </div>
                </div>
            </div>
        </div>
    `


    card.outerHTML = htmlString;
}

async function getChildForumEntries(){
    const forumJsonUrl = `/forum/show_json_childs_by_id/${pk}/`;
    return fetch(forumJsonUrl).then((res) => res.json());
}


async function refreshChildForumEntries() {
    document.getElementById("child-forums").innerHTML = "";
    document.getElementById("child-forums").className = "";
    const forumEntries = await getChildForumEntries();

    const style = document.createElement('style');
    style.textContent = `
        .text-wrap {
            word-wrap: break-word;       
            overflow-wrap: break-word;  
            white-space: normal;        
            max-width: 100%;            
        }
    `;
    document.head.append(style);

    let htmlString = "";
    let classNameString = "";
    classNameString =
    "columns-1 gap-4 space-y-6 w-full";
    htmlString += `<div id="forum_entry_form"></div>`
    forumEntries.forEach((item) => {
            const title = DOMPurify.sanitize(item.fields.title);
            const details = DOMPurify.sanitize(item.fields.details);

            let forum_username = item.fields.username;

            htmlString += `
                <div class="relative break-inside-avoid" id="card-${item.pk}">
                    <div class="px-10 py-6 bg-white rounded-lg shadow-md">
                        <div class="flex justify-between items-center">
                            <span class="font-light text-gray-600">${item.fields.time}</span>
                            ${item.fields.is_author ? `
                                <div class="absolute top-2 right-2 flex space-x-1"> <!-- Adjusted to top-right -->
                                    <button onclick='editForum("${item.pk}")' type="button" class="bg-yellow-500 hover:bg-yellow-600 text-white rounded-full p-2 transition duration-300 shadow-md">
                                        <svg xmlns="http://www.w3.org/2000/svg" class="h-9 w-9" viewBox="0 0 20 20" fill="currentColor">
                                            <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                                        </svg>
                                    </button>
                                    <button onclick="deleteForum('${item.pk}')" class="bg-red-500 hover:bg-red-600 text-white rounded-full p-2 transition duration-300 shadow-md">
                                        <svg xmlns="http://www.w3.org/2000/svg" class="h-9 w-9" viewBox="0 0 20 20" fill="currentColor">
                                            <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" />
                                        </svg>
                                    </button>
                                </div>
                            ` : ''}
                        </div>
                        <div class="mt-2">
                            <h1 class="text-gray-700">@${forum_username}</h1>
                            <p class="mt-2 text-gray-600 text-wrap">${details}</p>
                            <p hidden id="details-${item.pk}">${details}</p>
                        </div>
                    </div>
                </div>
            `;
    });
    
    document.getElementById("child-forums").className = classNameString;
    document.getElementById("child-forums").innerHTML = htmlString;
}

refreshMainForumEntry();
refreshChildForumEntries();

async function editForum(itemPk=null) {
    // Get the existing card
    const card = document.getElementById(`card-${itemPk}`);
    const detailsElement = document.getElementById(`details-${itemPk}`);
    const details = detailsElement.textContent; 


    // Create the editing form HTML
    const editFormHTML = `
        <div class="relative break-inside-avoid" id="card-${itemPk}">
            <div class="px-10 py-6 bg-white rounded-lg shadow-md">
                <div class="flex justify-between items-center">
                    <span class="font-light text-gray-600">Editing Forum</span>
                </div>
                <div class="mt-2">
                    <textarea id="details-${itemPk}" class="border rounded w-full p-2 mt-2" placeholder="Add your Details">${details}</textarea>
                </div>
                <div class="flex gap-3 items-left mt-4">
                    <button onclick="saveForumEdit('${itemPk}')" class="bg-indigo-700 hover:bg-indigo-600 text-white rounded-full p-2 transition duration-300 shadow-md">Save</button>
                    <button onclick="cancelEdit()" class="bg-red-500 hover:bg-red-600 text-white rounded-full p-2 transition duration-300 shadow-md">Cancel</button>
                </div>
            </div>
        </div>
    `;

    card.outerHTML = editFormHTML;
}

async function addForumEntry() {
    const details = document.getElementById(`comment`).value;
    document.getElementById(`comment`).value = '';
    const formData = new FormData();
    formData.append('title', "Empty");
    formData.append('details', details);
    formData.append('parent', pk);

    await fetch(`/forum/add_forum_entry_ajax/`, {
        method: 'POST',
        headers : {
            'X-CSRFToken': csrfToken,
        },
        body: formData,
    }).then((response) => refreshChildForumEntries());
    
}

async function saveForumEdit(itemPk) {
    const details = document.getElementById(`details-${itemPk}`).value;

    const formData = new FormData();
    formData.append('title', "Empty");
    formData.append('details', details);
    formData.append('pk', itemPk);

    await fetch(`/forum/edit_forum/ `, {
        method: 'POST',
        headers : {
            'X-CSRFToken': csrfToken,
        },
        body: formData,
    }).then((response) => {
        if(itemPk == pk){
            refreshMainForumEntry();
        } 
        else {
            refreshChildForumEntries();
        }
    });
}

async function cancelEdit() {
    refreshMainForumEntry();
    refreshChildForumEntries();
}

async function deleteForum(itemPk) {
    const formData = new FormData();
    formData.append('pk', itemPk);

    await fetch(`/forum/delete_forum/`, {
        method: 'POST',
        headers : {
            'X-CSRFToken': csrfToken,
        },
        body: formData,
    }).then((response) => {
        if(itemPk == pk){
            window.location.href = `/forum/show/`;
        } 
        else {
            refreshChildForumEntries()
        }
    });
}



