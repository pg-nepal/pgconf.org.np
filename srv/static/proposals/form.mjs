import * as main from '/static/main.mjs'


export function post(formData, idx) {
    const jsonData = {
        ...Object.fromEntries(formData),
        idx : idx,
    }

    return fetch('/proposals/call/add', {
        method  : 'POST',
        headers : { 'content-type': 'application/json' },
        body    : JSON.stringify(jsonData),
    })
}


export function init() {
    main.add_countries_opts(document.getElementById('countries'))
}
