const root = document.getElementById("header")
const add = document.getElementById("add-testimony")
const btnAdd = document.getElementById("handleAdd")
const btnSubmit = document.getElementById("handleSubmit")
const form = document.getElementById("add_form")
const content = document.getElementById("content")
const closeBtn = document.getElementById("close-button")
const ratingDiv = document.getElementById("rating")
// console.log("TEst", closeBtn)

window.onclick = function (event) {
    if (event.target === root) {
        add.classList.add('hidden')
        root.classList.add('hidden')
    }
}

// console.log(store)
async function getTestimonies() {
    // console.log("Getting pressed")
    return fetch(`/testimony/merchant_json/${store}/`).then((res) => res.json())
}

async function getRating(params) {
    return fetch(`/testimony/get_rating/${store}/`).then((res) => res.json())
}

async function refresh() {
    const testimonies = await getTestimonies();
    const rating = await getRating()
    ratingDiv.innerHTML = rating.rating + "/5"
    let data = ""

    if (!testimonies || testimonies.length == 0) {
        data += `<div> There is no testimonies yet  </div>`
    }
    else {
        testimonies.map(testimony => {
            data += `
                <div class="relative border border-1 bg-white rounded-xl w-full p-3">
                    ${(testimony.user == user ? `<button onclick="handleDelete(${testimony.pk})" class="rounded-full border border-1 border-red-600 text-red-600 hover:bg-red-600 hover:text-white w-5 h-5 text-sm bg-white cursor-pointer select-none text-center flex items-center justify-center absolute right-2 -top-3">X</button>` : '')}
                    <div class="text-2xl font-bold flex flex-row space-between justify-between">
                        <h1>${testimony.user}</h1>
                        <h1>${testimony.rating}/5</h1>
                    </div>
                    <p>${testimony.testimony}</p>
                </div>
                `
        })

    }
    document.getElementById("content").innerHTML = data
}

refresh()


function handleDelete(id) {
    // console.log(id)
    fetch(`/testimony/delete/${id}/`, {
        method: "DELETE",
        headers: {
            'Content-Type': 'application/json',
        }
    })
        .then(response => {
            refresh()
        })
}

function addTestimony() {
    fetch("/testimony/add_testimony/", {
        method: "POST",
        body: new FormData(document.querySelector("#add_form"))
    })
        .then(response => {
            if (response.ok) {
                refresh()
                form.reset();
                toggle()
            }
            else {
                alert("Form tidak berhasil ditambahkan, Pastikan rating dalam rentang 1-5")
            }
            return
        })

    form.reset();
}

function toggle() {
    if (root.classList.contains('hidden')) {
        add.classList.remove('hidden')
        root.classList.remove('hidden')
    }
    else {
        add.classList.add('hidden')
        root.classList.add('hidden')
    }
}

btnAdd.onclick = function () {
    toggle()
}

closeBtn.onclick = function () {
    add.classList.add('hidden')
    root.classList.add('hidden')
}

btnSubmit.addEventListener("click", (e) => {
    e.preventDefault()
    addTestimony()
})