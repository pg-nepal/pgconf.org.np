export function rateRead_summary(proposal_pk) {
    fetch(`/api/rates/summary/${proposal_pk}`).then(function (response) {
        return response.json()
    }).then(function (json) {
        document.getElementById('rating-avg').innerText = json.avg.toFixed(2)
        document.getElementById('rating-count').innerText = json.count
        const stars = document.getElementById('rating-avg-star')

        Object.assign(stars.style, {
            'background'              : `linear-gradient(to right, #fc0 0% ${json.percent}%, gray ${json.percent}% 100%)`,
            '-webkit-background-clip' : 'text',
            '-webkit-text-fill-color' : 'transparent',
        })
    })
}


function rateUpdate(proposal_pk, value) {
    fetch(`/api/rates/mine/${proposal_pk}`, {
        method  : 'POST',
        headers : { 'Content-Type' : 'application/json' },
        body    : JSON.stringify({value:value}),
    }).then(function (response) {
        return response.text()
    }).then(function (text) {
        for (let i = 1; i <= 5; i++) {
            const eSpan = document.getElementById(`star-${i}`)
            if (i <= value) eSpan.classList.add('active')
            else eSpan.classList.remove('active')
        }
    })
}


export function rateRead(proposal_pk) {
    return fetch(`/api/rates/mine/${proposal_pk}`).then(function (response) {
        return response.json()
    })
}


export function reviewReadAll(proposal_pk) {
    fetch(`/api/reviews/mine/${proposal_pk}`).then(function (response) {
        return response.json()
    }).then(function (json) {
        const eDiv_root = document.getElementById('comment-section')
        for (let [pk, comment, date, user] of json.data) {
            const eDiv = document.createElement('div')

            const eP_user = document.createElement('p')
            eP_user.innerHTML = `👤 <strong>${user}</strong>`
            eDiv.append(eP_user)

            const eP = document.createElement('p')
            eP.innerHTML = comment
            eDiv.append(eP)

            const eDiv_bottom = document.createElement('div')
            eDiv_bottom.style.display = 'flex'
            eDiv_bottom.style.justifyContent = 'space-between'
            eDiv.append(eDiv_bottom)

            const eSpan = document.createElement('span')
            eSpan.innerText = (new Date(date)).toString()
            eSpan.style.fontWeight = 200
            eDiv_bottom.append(eSpan)

            const eButton = document.createElement('button')
            eButton.classList = 'button'
            eButton.innerText = 'Delete'
            eButton.setAttribute('onClick', `reviewDelete(${pk})`)
            eDiv_bottom.append(eButton)

            eDiv_root.append(eDiv)
        }
    })
}


export function reviewUpdate(eForm, proposal_pk) {
    event.preventDefault()
    fetch(`/reviews/add/${proposal_pk}`, {
        method : 'POST',
        body   : new FormData(eForm),
    }).then(function (response) {
        return response.text()
    }).then(function (textData) {
        console.log(textData)
        location.reload()
    })
}


export function reviewDelete(pk){
    if (!confirm('Do you really want to delete this comment?')) return

    fetch(`/reviews/delete/${pk}`, {
        method : 'DELETE'
    }).then(function(response){
        alert('Comment deleted successfully.')
        location.reload()
    })
}


function proposalLoad(row) {
    document.getElementById('createdOn.local').innerText = (new Date(row.createdOn)).toString()

    for (let [key, val] of Object.entries(row)) {
        const element = document.getElementById(`row.${key}`)
        if (null === element) continue
        element.innerHTML = val
    }
}


export function init(pk) {
    return fetch(`/api/proposals/${pk}`, {
    }).then(function (response) {
        return response.json()
    }).then(function (json) {
        proposalLoad(json)
        rateRead_summary(json.pk)
        return json
    })
}
