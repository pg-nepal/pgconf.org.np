function createRow(headers, row, baseURL) {
    const eTr = document.createElement('tr')

    for (const [i, v] of Object.entries(row)) {
        const eTd = document.createElement('td')

        switch (headers[i]) {
            case 'pk':
                const eA = document.createElement('a')
                eA.innerText = v
                eA.href = `${baseURL}/${v}`
                eTd.append(eA)
                break

            case 'createdOn':
                if (null == v) break
                const date = new Date(v)
                eTd.innerHTML = date.toString().substring(0, 24)
                break

            case 'avg(rating)':
                if (null == v) break
                let stars = '';
                for (let i = 0; i < 5; i++) {
                    if (i < v) {
                        stars += '⭐'
                    } else {
                        stars += ''
                    }
                }

                eTd.append(stars)
                break

            case 'Action':
                const eAcceptButton = document.createElement('button')
                eAcceptButton.classList = 'button'
                eAcceptButton.innerText = 'Accept'
                eAcceptButton.onclick = function(){
                    if(!confirm('Do you want to accept this proposal?')){return}

                    fetch(`/proposals/evaluation/${row[0]}`, {
                        method  : 'POST',
                        headers : { 'content-type': 'application/json' },
                        body    : JSON.stringify({
                            "status" : "accepted",
                        })
                    }).then(function (response){
                        if (!response.ok) {
                            throw new Error('Error');
                        }
                        return response.text();
                    }).then(function(text){
                        location.reload()
                    })
                }
                eTd.append(eAcceptButton)

                const eRejectButton = document.createElement('button')
                eRejectButton.classList = 'button delete'
                eRejectButton.innerText = 'Reject'
                eRejectButton.onclick = function(){
                    if(!confirm('Do you want to reject this proposal?')){return}

                    fetch(`/proposals/evaluation/${row[0]}`, {
                        method  : 'POST',
                        headers : { 'content-type': 'application/json' },
                        body    : JSON.stringify({
                            "status" : "rejected",
                        })
                    }).then(function (response){
                        if (!response.ok) {
                            throw new Error('Error');
                        }
                        return response.text();
                    }).then(function(text){
                        location.reload()
                    })
                }
                eTd.append(eRejectButton)

                break

            default:
                eTd.innerHTML = v
        }
        eTr.append(eTd)
    }
    return eTr
}


function filterFromURL(search) {
    const sp = new URLSearchParams(search)
    const body = {}
    for (let k of sp.keys()) {
        let vals = sp.getAll(k)
        if (1 < vals.length) {
            body[k] = vals.map(function (e) { return ('' == e) ? null : e })
        } else {
            body[k] = ('' == vals[0]) ? null : vals[0]
        }
    }
    return body
}


export function load(id, baseURL, extendedURL) {
    let api = `/api${baseURL}`

    if(extendedURL !== 'None'){
        api = `/api${baseURL}`+`${extendedURL}`
    }

    fetch(api, {
        method  : 'POST',
        headers : { 'content-type' : 'application/json' },
        body    : JSON.stringify({
            filter : filterFromURL(location.search),
        })
    }).then(function (response) {
        if (!response.ok) {
            alert(`${response.status} ${response.statusText} `)
        }
        return response.json()
    }).then(function (json) {
        const eTable = document.getElementById(id)
        const searchParams = new URLSearchParams(location.search)

        for (const h of json.headers) {
            const eTh = document.createElement('th')
            eTable.children[0].children[0].append(eTh)
            const eA = document.createElement('a')
            eTh.append(eA)
            eA.innerText = h

            if (h in json?.filters) {
                eA.href = '#'
                eA.onclick = function (event) {
                    const eForm = document.getElementById('dt-params')

                    const eSelect = document.createElement('select')
                    eForm.replaceChildren(eSelect)
                    eSelect.addEventListener('change', function (event) {
                        const sp = new URLSearchParams(location.search)
                        sp.set(h, eSelect.value)
                        location.search = `?${sp.toString()}`
                    })

                    for (let o of json.filters[h]) {
                        const eOption = document.createElement('option')
                        eOption.selected = (o == searchParams.get(h))
                        eOption.innerText = o
                        eSelect.appendChild(eOption)
                    }

                    document.getElementById('dialog-filter').showModal()
                }
            }
        }

        let count = 0
        for (const row of json.data) {
            eTable.children[1].append(createRow(json.headers, row, baseURL))
            count += 1
        }

        const eP = document.getElementById('count')
        eP.innerHTML = `${count} rows`
    })
}
