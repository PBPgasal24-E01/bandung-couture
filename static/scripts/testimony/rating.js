const rating = document.getElementById("rating")

async function getRating(params) {
    return fetch(`/testimony/get_rating/${pk}/`).then((res) => res.json())
}

async function refresh() {
    const data = await getRating()
    console.log(pk, data)
    rating.innerHTML = data + "/5"
}

refresh()