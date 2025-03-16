
function createRow(headers, row, baseURL) {
    const eTr = document.createElement('tr')

    for (const [i, v] of Object.entries(row)) {
        const eTd = document.createElement('td')

        switch (headers[i]) {
            case 'pk':
                const eA = document.createElement('a')
                eA.innerText = v
                eA.href = `/proposals/${v}`
                eTd.append(eA)
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
                const eButton = document.createElement('button')
                eButton.classList = 'button'
                eButton.innerText = 'Accept'
                eButton.onclick = function(){
                    fetch(`/proposals/accept/${row[0]}`).then(function (response){
                        if (!response.ok) {
                            throw new Error('Error');
                        }
                        return response.text();
                    }).then(function(text){
                        alert(text)
                    })
                }
                eTd.append(eButton)
                break

            default:
                eTd.innerHTML = v
        }
        eTr.append(eTd)
    }

    return eTr
}


export function load(id, baseURL) {
    const api = `/api${baseURL}`
    fetch(api).then(function (response) {
        if (!response.ok) {
            alert(`${response.status} ${response.statusText} `)
        }
        return response.json()
    }).then(function (json) {
        const eTable = document.getElementById(id)

        for (const h of json.headers) {
            const eTh = document.createElement('th')
            eTh.innerHTML = h
            eTable.children[0].children[0].append(eTh)
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
