function getFlagEmoji(countryCode) {
    const codePoints = countryCode.split('').map(function(char) {
        return 127397 + char.charCodeAt()
    })
    return String.fromCodePoint(...codePoints)
}


export function add_countries_opts(datalist) {
    const A = 65
    const Z = 90
    const countryName = new Intl.DisplayNames(['en'], { type: 'region' });

    for (let i = A; i <= Z; ++i) {
        for (let j = A; j <= Z; ++j) {
            let code = String.fromCharCode(i) + String.fromCharCode(j)
            let name = countryName.of(code)
            if (code !== name) {
                const option = document.createElement('option')
                option.value = name
                option.innerText = `${getFlagEmoji(code)} ${name}`
                datalist.appendChild(option)
            }
        }
    }
}


export function ajax(fetch_promise, onPass, onFail) {
    fetch_promise.then(function (response) {
        if (500 <= response.status) {
            throw new Error(response.statusText)
        }

        if (200 > response.status || 300 <= response.status) {
            return response.text().then(function (text) {
                alert(text)
            })
        }

        if (true == response.redirected) {
            alert('submitted successfully')
            window.location = response.url
        }
    }).catch(function (error) {
        console.error(error)
        alert('Oops! something went wrong')
    })
}
