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
    fetch(`/api/rates/mine/${proposal_pk}`).then(function (response) {
        return response.json()
    }).then(function (jsonData) {
        const eDiv = document.getElementById('rating')
        for (let i = 1; i <= 5; i++) {
            const eSpan = document.createElement('span')
            eSpan.id = `star-${i}`
            eSpan.onclick = function () {
                rateUpdate(proposal_pk, i)
            }
            eSpan.classList = 'rating__star'
            if (i <= jsonData) eSpan.classList.add('active')
            eSpan.innerText = '⭐'
            eDiv.append(eSpan)
        }
    })
}
