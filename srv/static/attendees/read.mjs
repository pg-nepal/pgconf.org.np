
export function getTicketDetails(slug) {
    fetch(`/registered/ticket/${slug}`).then(function (response) {
        if (200 == response.status) {
            return response.json()
        }
    }).then( function(json){
        updateTicketTable (json)
        updateReceiptTable (slug, json)
    })
}


function updateTicketTable(json){
    const ticketContainer = document.getElementById('ticket-container')
    ticketContainer.innerHTML = ''

    let total = 0
    let paid = 0
    let inReview = 0
    let currency = ''

    json.data.forEach(function (row) {
        const ticketDiv = document.createElement('div')
        ticketDiv.className = 'ticket'

        const ticketFieldContainer = document.createElement('div')
        ticketFieldContainer.className = 'field-container'

        const wrapperContainer = document.createElement('div')
        wrapperContainer.className = 'wrapper'

        const ticketLogo = document.createElement('img')
        ticketLogo.src = '/static/images/pgconf_logo.png'
        ticketLogo.className = 'ticket-logo'

        row.forEach(function (cell, i) {
    
            const fieldName = json.headers[i]
    
            const fieldDiv = document.createElement('div')
            fieldDiv.className = 'ticket-field'

            if(fieldName !=='pk'){
                if (fieldName === 'Amount') {
                    if (cell !== null) {
                                 total += cell
                        cell = cell.toLocaleString()
                             }
                         }
         
                if (fieldName === 'Currency' && cell !== null) {
                    currency = cell
                }


                switch (fieldName === 'Payment Status') {
                    case 'unpaid':
                        total += cell
                        eTd.innerHTML = cell.toLocaleString()
                        break
                    case 'in review':
                        inReview += cell
                        eTd.innerHTML = cell.toLocaleString()
                        break
                    case 'paid':
                        paid += cell
                        eTd.innerHTML = cell.toLocaleString()
                        break
                }
        
                if (['Ordered Date', 'Updated Date', 'Date From', 'Date To'].includes(fieldName) && cell !== null) {
                    const date = new Date(cell)
                    cell = date.toDateString()
                         }

                         fieldDiv.innerHTML = `<p><strong>${fieldName}:</strong> ${cell}</p>`
                         ticketFieldContainer.appendChild(fieldDiv)
            }
    
                 })
            ticketDiv.append(ticketFieldContainer)
            ticketContainer.appendChild(ticketDiv)
            wrapperContainer.appendChild(ticketLogo)
            ticketDiv.appendChild(wrapperContainer)
    })

    ticketContainer.style.display = 'block'

    document.getElementById('total-amount').innerText = `${currency} ${total.toLocaleString()}`
    document.getElementById('in-review-amount').innerText = `${currency} ${inReview.toLocaleString()}`
    document.getElementById('paid-amount').innerText = `${currency} ${paid.toLocaleString()}`

    return json
}


function updateReceiptTable(slug, json){
    const eReceiptTable = document.getElementById('receipt-table')

    const iMap = {}

    json.headers.forEach(function (h, i) {
        iMap[h] = i

        switch (h) {
        case 'Event':
        case 'Currency':
        case 'Amount':
        case 'Payment Status':
            const eTh = document.createElement('th')
            eTh.innerHTML = h
            eReceiptTable.children[0].children[0].append(eTh)
        }
    })
    const eTh = document.createElement('th')
    eTh.innerHTML = 'Action'
    eReceiptTable.children[0].children[0].append(eTh)

    json.data.forEach(function (row) {
        const eTr = document.createElement('tr')
        row.forEach(function (cell, i) {

            switch (json.headers[i]) {
            case 'Event':
            case 'Currency':
            case 'Amount':
            case 'Payment Status':
                const eTd = document.createElement('td')
                eTd.innerHTML = cell
                eTr.append(eTd)
            }
        })

        const eTd = document.createElement('td')

        if(row[iMap['Payment Status']] != null){
            if(row[iMap['Payment Status']] == 'unpaid'){
                const eButton = document.createElement('button')
                eButton.id = 'event'+row[iMap['pk']]
                eButton.value = row[iMap['pk']]
                eButton.classList = 'button'
                eButton.innerHTML = 'Upload Receipt'

                eButton.onclick = function () {
                    const eInput_file = document.createElement('input')
                    eInput_file.type = 'file'
                    eInput_file.id = row[iMap['pk']]
                    eInput_file.click()

                    eInput_file.onchange = function (event) {
                        const event_pk = document.getElementById('event'+row[iMap['pk']]).value

                        const file = event.target.files[0]
                        if (undefined === file) return

                        const validMimeTypes = ['image/jpeg', 'image/png', 'application/pdf'];
                        if(!validMimeTypes.includes(file.type)) {
                            alert("Invalid file type. Please upload jpeg, png or pdf file")
                            return
                        }

                        if (5 <= Math.round((file.size / 1024 / 1024))) {
                            if (!confirm('Recommened file size limited to 5 MB. Do you want to continue ?')) {
                                eRoot.remove()
                                return
                            }
                        }

                        const formData = new FormData()
                        formData.append('file', file)
                        formData.append('event_pk', event_pk)

                        fetch(`/registered/receipt_upload/${slug}`, {
                            method   : 'POST',
                            body : formData,
                        }).then(function (response){
                            location.reload()
                        })
                    }
                }
                eTd.append(eButton)
                eTr.append(eTd)
                eReceiptTable.children[1].append(eTr)
            }
            else{
                const eButton = document.createElement('button')
                eButton.id = 'event'+row[iMap['pk']]
                eButton.value = row[iMap['pk']]
                eButton.classList = 'button'
                eButton.innerHTML = 'View Receipt'

                eButton.onclick = function () {
                    const event_pk = document.getElementById('event'+row[iMap['pk']]).value

                    fetch(`/registered/receipt_view/${slug}`, {
                        method   : 'POST',
                        headers : { 'Content-Type' : 'application/json' },
                        body : JSON.stringify({
                            event_pk : event_pk,
                        }),
                    }).then(function (response){
                        return response.json()
                    }).then(function (json){
                        const receipt = 'data:'+ json.receiptType +';base64,' + json.image;
                        const newWindow = window.open();

                        if(json.receiptType == 'application/pdf'){
                            newWindow.document.write('<embed src="' + receipt + '" width="100%" height="100%" type="application/pdf">');
                        }
                        else{
                            newWindow.document.write('<img src="' + receipt + '" />');
                        }
                    })
                }
                eTd.append(eButton)
                eTr.append(eTd)
                eReceiptTable.children[1].append(eTr)
            }
        }
    })
    eReceiptTable.style.display = ''
}


// registration_thanks
export function sendEmail(slug, emailType) {
    fetch(
        `/api/mbox/queue_email`, {
            method  : 'POST',
            headers : { 'Content-Type' : 'application/json' },
            body    : JSON.stringify({
                slug : slug,
                type : emailType
            })
    }).then(function (response) {
        response.json().then(function(jsonResponse){
            alert(jsonResponse.message)
        })
    })
}
