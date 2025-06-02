import * as main from '/static/main.mjs'


const ratingTemplate = {
    'relevance'   : 'Relevance and Alignment with Conference Themes',
    'clarity'     : 'Deliverable Clarity on the abstract',
    'engagement'  : 'Impact and Audience Engagement possibilities',
    'content'     : 'Technicality of content',
}


export function rateRead_summary(proposal_pk) {
    fetch(`/api/rates/summary/${proposal_pk}`).then(function (response) {
        return response.json()
    }).then(function (json) {
        document.getElementById('rating-avg').innerText = json.avg.toFixed(2)
        const count = document.getElementById('rating-count')
        if(count){
            count.innerHTML = json.count
        }
        const stars = document.getElementById('rating-avg-star')
        stars.classList.add('active')

        Object.assign(stars.style, {
            'background'              : `linear-gradient(to right, #fc0 0% ${json.percent}%, gray ${json.percent}% 100%)`,
            '-webkit-background-clip' : 'text',
            '-webkit-text-fill-color' : 'transparent',
        })
    })
}


export function client_rateRead_summary(proposal_pk) {
    fetch(`/api/submitted/rates/summary/${proposal_pk}`).then(function (response) {
        return response.json()
    }).then(function (json) {
        document.getElementById('rating-avg').innerText = json.avg.toFixed(2)
        const count = document.getElementById('rating-count')
        if(count){
            count.innerHTML = json.count
        }
        const stars = document.getElementById('rating-avg-star')
        stars.classList.add('active')

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
    }).then(function (json) {
        const eDiv_tableContainer = document.querySelector('.table-container')
        const eDiv_dialogContainer = document.querySelector('.dialog-container')

        for(let [key, value] of Object.entries(ratingTemplate)) {
            const eDiv_ratingWrapper = document.createElement('tr')
            eDiv_ratingWrapper.classList = 'rating-wrapper'
            eDiv_ratingWrapper.id = key

            const eDiv_label = document.createElement('td')
            eDiv_label.innerText = value
            eDiv_ratingWrapper.appendChild(eDiv_label)

            for(let i=1; i<=5; i++) {
                const eDiv_starWrapper = document.createElement('td')
                const eInput = document.createElement('input')

                eInput.id = `star-${i}`
                eInput.type = 'radio'
                eInput.value = i
                eInput.name = key

                if(json.score != null) {
                    eInput.checked = (i == json.score[key])
                }

                eDiv_starWrapper.appendChild(eInput)
                eDiv_ratingWrapper.appendChild(eDiv_starWrapper)
            }

            eDiv_tableContainer.appendChild(eDiv_ratingWrapper)
        }

        const eDiv_ratingWrapper = document.createElement('div')
        eDiv_ratingWrapper.classList = 'overall-wrapper'
        eDiv_ratingWrapper.id = 'star-value'

        if (json != null){
            eDiv_ratingWrapper.setAttribute('data-value', json.value)
        }

        const eDiv_label = document.createElement('div')
        eDiv_label.innerText = 'Overall Score'

        const eDiv_starWrapper = document.createElement('div')

        for(let i=1; i<=5; i++) {
            const eSpan = document.createElement('span')
            eSpan.id = `star-${i}`
            eSpan.setAttribute('data-value', i)
            eSpan.classList = 'rating__star'
            eSpan.innerText = '⭐'

            if(json != null && json.value >= i) {
                eSpan.classList.add('active')
            }

            eSpan.onclick = changeStar
            eDiv_starWrapper.appendChild(eSpan)
        }

        eDiv_ratingWrapper.appendChild(eDiv_label)
        eDiv_ratingWrapper.appendChild(eDiv_starWrapper)
        eDiv_dialogContainer.appendChild(eDiv_ratingWrapper)

    })
}

function changeStar(e) {
    const parent = e.target.parentElement
    const childrenList = Array.prototype.slice.call(parent.children)
    const clickedOn = e.target.getAttribute('data-value')

    parent.parentElement.setAttribute('data-value', clickedOn)

    for(let i=0; i<childrenList.length; i++) {
        childrenList[i].classList.remove('active')
        if(i < clickedOn) {
            childrenList[i].classList.add('active')
        }
    }
}


export function reviewReadAll (isAdmin, proposal_pk) {
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
            eP.innerHTML = comment.replace(/\n/g, '<br>');
            eDiv.append(eP)

            const eDiv_bottom = document.createElement('div')
            eDiv_bottom.style.display = 'block'
            eDiv.append(eDiv_bottom)

            const eP_date = document.createElement('p')
            eP_date.innerText = (new Date(date)).toString()
            eP_date.style.fontWeight = 200
            eDiv_bottom.append(eP_date)

            if (user === isAdmin) {
                const eButton = document.createElement('button');
                eButton.classList.add('button', 'delete');
                eButton.innerText = 'Delete your comment';
                eButton.addEventListener('click', function () {
                    reviewDelete(pk);
                });
                eDiv_bottom.append(eButton);
            }

            eDiv_root.append(eDiv)
            }
        })
    }


function reviewUpdate(proposal_pk) {
    fetch(`/reviews/add/${proposal_pk}`, {
        method : 'POST',
        body   : new FormData(eForm),
    }).then(function (response) {
        return response.text()
    }).then(function (textData) {
        location.reload()
    })
}

function reviewDelete(pk){
    if (!confirm('Do you really want to delete this comment?')) return

    fetch(`/api/reviews/mine/delete/${pk}`, {
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
        element.innerHTML = val.replaceAll('\n','<br>')
    }

    const profileLink = document.getElementById('profile-link')
    profileLink.href = `/submitted/${row.slug}`


    let coAuthors = row.co_authors
    if(typeof coAuthors == 'string'){
        coAuthors = JSON.parse(coAuthors)
    }

    const coAuthorsElement = document.getElementById('co_authors')
    coAuthorsElement.textContent = row.co_authors?.length ? coAuthors.map(function(author){return author.name}).join(', ') : 'None'

    const selectElement = document.getElementById('wtf-status')
    if(selectElement){
        selectElement.value = row.status
    }
}


export function createAttendee(row) {
    const formData = new FormData()
    formData.append('name', row.name)
    formData.append('type', row.session == 'training' ? 'trainer' : 'speaker')
    formData.append('email', row.email)
    formData.append('country', row.country)

    fetch('/api/attendees/add', {
        method : 'POST',
        body   : formData,
    }).then(function (response){
        if(response.status != 200){
            alert("Failed to copy")
        }
        else{
            return response.json()
        }
    }).then(function (json){
        const pk = row.pk
        const attendeePk = json['pk']
        fetch(`/api/proposals/update/${pk}`, {
            method : 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body   : JSON.stringify({attendeePk})
        }).then(function(response){
            if(response.status != 200){
                alert("Failed to update")
            } else {
                alert('Copied to attendee table successfully.')
                return response.text()
            }
        })
        window.location.href = `/attendees/${json['pk']}`
    })
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

export function proposalEvaluation(slug) {
    return fetch(`/api/submitted/${slug}`, {
    }).then(function (response) {
        return response.json()
    }).then(function (json) {
        client_rateRead_summary(json.pk)
        return json
    })
}

