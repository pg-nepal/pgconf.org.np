import * as main from '/static/main.mjs'


export function post(formData, idx) {
    const events = formData.getAll('events')
    const jsonData = {
        ...Object.fromEntries(formData),
        idx    : idx,
        events : events,
    }

    return fetch('/volunteered/add', {
        method  : 'POST',
        headers : { 'content-type': 'application/json' },
        body    : JSON.stringify(jsonData),
    })
}


export function init() {
    main.add_countries_opts(document.getElementById('countries'))
}
