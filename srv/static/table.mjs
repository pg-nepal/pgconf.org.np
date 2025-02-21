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

            case 'email':
                if (null == v) break
                const eA_email = document.createElement('a')
                eA_email.innerText = v
                eA_email.href = `mailto:${v}`
                eTd.append(eA_email)
                break

            case 'avg(rating)':
                const pk = row[headers.indexOf('pk')]
                const rateLink = document.createElement('a')
                if (null == v){
                    console.log(pk)
                    rateLink.innerText = `No Ratings`
                    eTd.append(rateLink)
                }
                    
                let stars = '';
                for (let i = 0; i < 5; i++) {
                    if (i < v) {
                        stars += '⭐'
                    } else {
                        stars += ''
                    }
                }
                const ed = document.createElement('div')
                ed.style.justifyContent = 'space-between'
                eTd.append(stars)
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

        const eP = document.createElement('p')
        eP.innerHTML = `${count} rows`
        eTable.after(eP)
    })
}
