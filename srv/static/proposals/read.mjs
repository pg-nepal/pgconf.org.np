function rateUpdate(proposal_pk, value) {
    fetch(`/api/rates/mine/${proposal_pk}`, {
        method  : 'POST',
        headers : { 'Content-Type' : 'application/json' },
        body    : JSON.stringify({value:value}),
    }).then(function (response) {
        return response.text()
    }).then(function (textData) {
        for (let i = 1; i <= 5; i++) {
            const eSpan = document.getElementById(`star-${i}`)
            if (i <= value) eSpan.classList.add('active')
            else eSpan.classList.remove('active')
        }
    })
}


export function rateRead(proposal_pk) {
    fetch(`/api/rates/average/${proposal_pk}`).then(function (response) {
        return response.json()
    }).then(function (jsonData) {
        const averageRate = +jsonData.average_rating
        const eDiv = document.getElementById('rating')
        for (let i = 1; i <= 5; i++) {
            const eSpan = document.createElement('span')
            eSpan.id = `star-${i}`
            eSpan.classList = 'rating__star'
            if (i <= averageRate) eSpan.classList.add('active')
            eSpan.innerText = '⭐'
            eDiv.append(eSpan)
        }
    })
}

export function rateReadAndUpdate(proposal_pk){
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


export function reviewReadAll(proposal_pk) {
    fetch(`/api/reviews/mine/${proposal_pk}`).then(function (response) {
        return response.json()
    }).then(function (jsonData) {
        const eDiv_root = document.getElementById('comment-section')
        for (let [pk, comment, date, user] of jsonData.data) {
            const eDiv = document.createElement('div')

            const eCreatedBy = document.createElement('p')
            eCreatedBy.innerHTML = `
            👤 <strong>${user}</strong>
            `
            eCreatedBy.innerHTML = `
            👤 <strong>${user}</strong>
            `
            eDiv.append(eCreatedBy)

            const eP = document.createElement('p')
            eP.innerHTML = comment
            eDiv.append(eP)
            
            const fd = document.createElement('div')
            fd.style.display = 'flex'
            fd.style.justifyContent = 'space-between'
            const eSpan = document.createElement('p')
            eSpan.innerText = (new Date(date)).toString().substring(0, 24)
            eSpan.style.fontWeight = 200
            eSpan.style.fontWeight = 200

            const options = document.createElement('div')
            const updatebtn = document.createElement('button')
            updatebtn.classList.add = 'button'
            updatebtn.innerText = 'Delete'
            updatebtn.setAttribute('onClick', `reviewDelete(${pk})`)
            options.append(updatebtn)

            fd.append(eSpan)
            fd.append(options)
            eDiv.append(fd)

            eDiv_root.append(eDiv)
        }
    })
}

export function reviewDelete(pk){
    fetch(`/reviews/delete/${pk}`, {
        method: 'DELETE'
    }).then(function(response){
        alert('Comment deleted successfully.')
        location.reload()
    }).catch(function(error){
        console.log(error)
        alert(error.message)
    })
}