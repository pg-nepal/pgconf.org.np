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
