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

        for (const row of json.data) {
            const eTr = document.createElement('tr')


            for (const [i, v] of Object.entries(row)) {
                const eTd = document.createElement('td')

                switch (json.headers[i]) {
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
                        if (null == v) break
                        const averageRating = v
                        let stars = '';
                        for (let i = 0; i < 5; i++) {
                            if(i < averageRating){
                                stars += '⭐'
                            } else {
                                stars += ''
                            }
                        }

                        console.log(stars)
                        eTd.append(stars)
                        break

                    default:
                        eTd.innerHTML = v

                }
                eTr.append(eTd)
            }

            eTable.children[1].append(eTr)
        }
    })
}
