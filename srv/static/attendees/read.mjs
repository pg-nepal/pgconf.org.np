
export function getTicketDetails(slug) {
    fetch(`/ticket/${slug}`).then(function (response) {
        if (200 == response.status) {
            response.text()
            .then(function(data) {
               const ticketContainer = document.getElementById('ticket-container')
               ticketContainer.innerHTML = data
            })
        }
    })
}


export function getReceiptDetails(slug) {
    let unpaidAmount = 0
    let reviewAmount = 0
    let paidAmount = 0
    let currency = ''

    fetch(`/registered/receipt/${slug}`).then(function (response) {
        if (200 == response.status) {
            return response.json()
        }
    }).then( function(json){
        updateReceiptTable(slug, json)

        json.data.forEach(function (row) {
            if(row[4] !== null){
                currency = row[4]
            }

            const amount = parseFloat(row[5])
            const paymentStatus = row[6]

            if(!isNaN(amount)){
                if(paymentStatus === 'unpaid'){
                    unpaidAmount += amount
                } else if (paymentStatus === 'in review'){
                    reviewAmount += amount
                } else {
                    paidAmount += amount
                }
            }
        })

        const totalAmountElement = document.getElementById('total-amount');
        const inReviewAmountElement = document.getElementById('in-review-amount');
        const paidAmountElement = document.getElementById('paid-amount');

        if (document.getElementById('total-amount')) {
            document.getElementById('total-amount').innerText = `${currency} ${unpaidAmount.toFixed(2)}`;
        }

        if (document.getElementById('in-review-amount')) {
            document.getElementById('in-review-amount').innerText = `${currency} ${reviewAmount.toFixed(2)}`;
        }

        if (document.getElementById('paid-amount')) {
            document.getElementById('paid-amount').innerText = `${currency} ${paidAmount.toFixed(2)}`;
        }
    })
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

                        if (2 <= Math.round((file.size / 1024 / 1024))) {
                            alert('Please upload file less than 2 MB')
                            eRoot.remove()
                            return
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
