    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    async function getForumEntries() {
        if( document.getElementById('user-forum').checked) 
            return fetch('/forum/show_root_json_filter_user/').then((res) => res.json());
        else 
            return fetch('/forum/show_root_json/').then((res) => res.json());
    }
    async function refreshForumEntries() {
        document.getElementById("forum_entry_cards").innerHTML = "";
        document.getElementById("forum_entry_cards").className = "";
        const forumEntries = await getForumEntries();

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
        if (forumEntries.length === 0) {
          htmlString = `
                <div id="empty-card">
                    <div class="flex flex-col items-center justify-center min-h-[24rem] p-6">
                        <p class="text-center text-gray-600 mt-4">Belum ada data forum. Silahkan buat forum.</p>
                    </div>
                </div>
            `;
        } else {
          classNameString =
            "columns-1 gap-6 space-y-6 w-full";
            htmlString += `<div id="forum_entry_form"></div>`
            forumEntries.forEach((item) => {
                    const title = DOMPurify.sanitize(item.fields.title);
                    const details = DOMPurify.sanitize(item.fields.details);

                    let forum_username = item.fields.username;
                    let maxLength = 15
                    if (window.innerWidth <= 768) { 
                        forum_username = forum_username.length > maxLength ? forum_username.slice(0, maxLength) + '...' : forum_username;
                    }
                    
                    details_trunc = details.length > 300 ? details.slice(0, 300) + '...' : details; 
                    
                    

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
                                    <a class="text-2xl text-gray-700 font-bold hover:underline" href="${item.pk}">${title}</a>
                                    <p class="mt-2 text-gray-600 text-wrap">${details_trunc}</p>
                                    <p hidden id="details-${item.pk}">${details}</p>
                                </div>
                                <div class="flex justify-between items-center mt-4">
                                    <a class="text-blue-500 hover:underline" href="${item.pk}">Read more</a>
                                    <div>
                                        <a class="flex items-center">
                                            <p class="text-gray-600">by  @</p>
                                            <h1 class="text-gray-700 font-bold">${forum_username}</h1>
                                        </a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                    
            });
        }
        document.getElementById("forum_entry_cards").className = classNameString;
        document.getElementById("forum_entry_cards").innerHTML = htmlString;
    }
    refreshForumEntries();
    
    async function addForumEntry() {
        const title = document.getElementById(`add-forum-title`).value;
        const details = document.getElementById(`add-forum-details`).value;

        const formData = new FormData();
        formData.append('title', title);
        formData.append('details', details);

        await fetch('/forum/add_forum_entry_ajax/', {
            method: 'POST',
            headers : {
                'X-CSRFToken': csrfToken,
            },
            body: formData,
        }).then((response) => refreshForumEntries());
        
        const card = document.getElementById(`add-forum`);
        const stringHTML = `<div id="forum_entry_form" class="none"></div>`
        card.outerHTML = stringHTML;
    }

    async function cancelAdd(){
        const card = document.getElementById(`add-forum`);
        const stringHTML = `<div id="forum_entry_form" class="none"></div>`
        card.outerHTML = stringHTML;
    }
    
    async function showForumForm() {
        let card = document.getElementById(`forum_entry_form`);
        if(card == null) {
            card = document.getElementById('empty-card');
        }
        const addForumHTML = `
            <div class="relative break-inside-avoid" id="add-forum">
                <div class="px-10 py-6 bg-white rounded-lg shadow-md ">
                    <div class="flex justify-between items-center">
                        <span class="font-light text-gray-600">Add Forum</span>
                    </div>
                    <div class="mt-2">
                        <input type="text" id="add-forum-title" class="border rounded w-full p-2" placeholder="Enter your Title"/>
                        <textarea id="add-forum-details" class="border rounded w-full p-2 mt-2" placeholder="Add your Details"></textarea>
                    </div>
                    <div class="flex gap-3 items-left mt-4">
                        <button onclick="addForumEntry()" class="bg-indigo-700 hover:bg-indigo-600 text-white rounded-full p-2 transition duration-300 shadow-md">Save</button>
                        <button onclick="cancelAdd()" class="bg-red-500 hover:bg-red-600 text-white rounded-full p-2 transition duration-300 shadow-md">Cancel</button>
                    </div>
                </div>
            </div>
        `;
        card.outerHTML = addForumHTML;
    }
    
    async function editForum(itemPk=null) {
        const card = document.getElementById(`card-${itemPk}`);
        const title = card.querySelector('.text-2xl').textContent;
        const detailsElement = document.getElementById(`details-${itemPk}`);
        const details = detailsElement.textContent; 
        const forumUsername = card.querySelector('.font-bold').textContent;
    
        const editFormHTML = `
            <div class="relative break-inside-avoid" id="card-${itemPk}">
                <div class="px-10 py-6 bg-white rounded-lg shadow-md">
                    <div class="flex justify-between items-center">
                        <span class="font-light text-gray-600">Editing Forum</span>
                    </div>
                    <div class="mt-2">
                        <input type="text" id="title-${itemPk}" class="border rounded w-full p-2" placeholder="Enter your Title" value="${title}" />
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
    
    async function saveForumEdit(itemPk) {
        const title = document.getElementById(`title-${itemPk}`).value;
        const details = document.getElementById(`details-${itemPk}`).value;
    

        const formData = new FormData();
        formData.append('title', title);
        formData.append('details', details);
        formData.append('pk', itemPk);
    
        await fetch('/forum/edit_forum/', {
            method: 'POST',
            headers : {
                'X-CSRFToken': csrfToken,
            },
            body: formData,
        }).then((response) => refreshForumEntries());
    }
    
    async function cancelEdit() {

        refreshForumEntries();
    }

    async function deleteForum(itemPk) {
        const formData = new FormData();
        formData.append('pk', itemPk);

        await fetch('/forum/delete_forum/', {
            method: 'POST',
            headers : {
                'X-CSRFToken': csrfToken,
            },
            body: formData,
        }).then((response) => refreshForumEntries());
    }

    async function checkShowMyForum(){
        const checked = document.getElementById('user-forum').checked;
        document.getElementById('user-forum').checked = !checked;

        refreshForumEntries();
    }
