function createRow(headers, row, baseURL, actionList) {
    const eTr = document.createElement('tr')

    for (const [i, v] of Object.entries(row)) {
        const eTd = document.createElement('td')

        if (headers[i] in actionList) {
            const action = actionList[headers[i]]
            const eA = document.createElement('a')
            eA.href = headers.reduce((url, header, i) => url.replace('{' + header + '}', row[i]), action.url);
            eA.target = action.target ?? '_self'
            eA.innerText = v
            eTd.append(eA)
        } else if (headers[i] == 'pk') {
            const eA = document.createElement('a')
            eA.innerText = v
            eA.href = `${baseURL}/${v}`
            eTd.append(eA)
        } else if (headers[i] == 'createdOn') {
            eTd.innerHTML = getLocalDate(v)
        } else if (headers[i] == 'avg(rating)') {
            eTd.innerHTML = getRating(v)
        } else {
            eTd.innerHTML = v
        }

        eTr.append(eTd)

    }

    return eTr
}


function getLocalDate(v) {
    if (null == v) return ''
    const date = new Date(v)
    return date.toString().substring(0, 24)
}


function getRating(v) {
    if (null == v) return ''
    let stars = '';
    for (let i = 0; i < 5; i++) {
        if (i < v) {
            stars += '⭐'
        } else {
            stars += ''
        }
    }
    return stars
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


export function load(id, baseURL, actions) {
    const api = `/api${baseURL}`
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

        const actionList = JSON.parse(actions)

        for (const row of json.data) {
            eTable.children[1].append(createRow(json.headers, row, baseURL, actionList))
            count += 1
        }

        const eP = document.getElementById('count')
        eP.innerHTML = `${count} rows`
    })
}
