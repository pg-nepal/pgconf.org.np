
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
    fetch(`/registered/tickets/receipt/${slug}`).then(function (response) {
        if (200 == response.status) {
            return response.json()
        }
    }).then( function(json){
        updateReceiptTable(json)
    })
}


export function getReceiptDetailsAdmin(slug) {
    fetch(`/tickets/receipt/${slug}`).then(function (response) {
        if (200 == response.status) {
            return response.json()
        }
    }).then( function(json){
        updateReceiptTableAdmin(json)
    })
}


function updateReceiptTable(json){
    const eReceiptTable = document.getElementById('receipt-table')

    json.headers.forEach(function (h, i) {
        if(h != 'pk' && h!= 'Note'){
            const eTh = document.createElement('th')
            eTh.innerText = h
            eReceiptTable.children[0].children[0].append(eTh)
        }
    })

    json.data.forEach(function (row) {
        if(row['Payment Status'] !== null) {
            const eTr = document.createElement('tr')
            Object.entries(row).forEach(function ([k,v]) {
                if(k != 'pk' && k != 'Note'){
                    const eTd = document.createElement('td')

                    if (k == 'Action') {
                        if (row['Payment Status'] !== 'in review' && row['Payment Status'] !== 'paid') {
                            const uploadBtn = document.createElement('button')
                            uploadBtn.innerText = 'Upload Receipt'
                            uploadBtn.classList = 'button'
                            uploadBtn.style.margin = '1%'
                            uploadBtn.onclick = function () {
                                uploadReceipt(row.pk, row['Payment Status'])
                            }
                            eTd.append(uploadBtn)
                        }
                    }
                    else if (k == 'Receipt') {
                        if (row['Payment Status'] !== 'unpaid') {
                            const viewBtn = document.createElement('button')
                            viewBtn.innerText = 'View'
                            viewBtn.classList = 'button'
                            viewBtn.style.margin = '1%'

                            viewBtn.onclick = function () {
                                viewReceipt(row.pk)
                            }
                            eTd.append(viewBtn)
                        }
                    }
                    else if (k == 'Payment Status') {
                        if (v === 'rejected') {
                            eTd.innerHTML = v + " ℹ️"
                            eTd.title = row['Note']
                        }
                        else{
                            eTd.innerHTML = v
                        }
                    }
                    else if (k =='Ordered Date') {
                        if (v) {
                            eTd.innerText = new Date(v).toDateString();
                        } else {
                            eTd.innerText = '';
                        }
                    }
                    else{
                        eTd.innerHTML = v
                    }
                    eTr.append(eTd)
                    eReceiptTable.children[1].append(eTr)
                }
            })
        eReceiptTable.style.display = ''
    }
})}

function updateReceiptTableAdmin(json){
    const eReceiptTable = document.getElementById('receipt-table')

    json.headers.forEach(function (h, i) {
        if(h != 'pk'){
            const eTh = document.createElement('th')
            eTh.innerText = h
            eReceiptTable.children[0].children[0].append(eTh)
        }
    })

    json.data.forEach(function (row) {
        if(row['Payment Status'] !== null) {
            const eTr = document.createElement('tr')
            Object.entries(row).forEach(function ([k,v]) {
                if(k != 'pk'){
                    const eTd = document.createElement('td')

                    if (k == 'Action') {
                        const uploadBtn = document.createElement('button')
                        uploadBtn.innerText = 'Upload Receipt'
                        uploadBtn.classList = 'button'
                        uploadBtn.style.margin = '1%'
                        uploadBtn.onclick = function () { uploadReceipt(row.pk, row['Payment Status']) }
                        if (row['Payment Status'] !== 'in review' && row['Payment Status'] !== 'paid') {
                            eTd.append(uploadBtn)
                        }
                    }
                    else if (k == 'Receipt') {
                        if(v != null){
                            const viewBtn = document.createElement('button')
                            viewBtn.innerText = 'View'
                            viewBtn.classList = 'button'
                            viewBtn.style.margin = '1%'
                            viewBtn.onclick = function () { viewReceipt(row.pk) }
                            eTd.append(viewBtn)
                        }
                    }
                    else if (k == 'Change Status') {
                        const eButton = document.createElement('button')
                        eButton.innerText = 'Change Status'
                        eButton.id = row.pk
                        eButton.classList = 'button'
                        eButton.style.margin = '1%'

                        const eStatusDialog = document.getElementById('dialog-change-status')
                        eButton.onclick = function () {
                            const id = eButton.id
                            document.getElementById("event_pk").value = id
                            eStatusDialog.showModal()
                        }

                        eTd.append(eButton)
                    }
                    else if (k =='Ordered Date') {
                        if (v) {
                            eTd.innerText = new Date(v).toDateString();
                        } else {
                            eTd.innerText = '';
                        }
                    }
                    else{
                        eTd.innerHTML = v
                    }

                    eTr.append(eTd)
                    eReceiptTable.children[1].append(eTr)
                }
            })
        eReceiptTable.style.display = ''
    }
})}

function uploadReceipt (event_pk, paymentStatus){
    const eInput_file = document.createElement('input')
    eInput_file.type = 'file'
    eInput_file.id = event_pk
    eInput_file.accept = '.jpg, .jpeg, .png, .pdf'
    eInput_file.click()

    eInput_file.onchange = function (event) {

        const file = event.target.files[0]
        if (undefined === file) return

        const validMimeTypes = ['image/jpeg', 'image/png', 'application/pdf'];
        if(!validMimeTypes.includes(file.type)) {
            alert("Invalid file type. Please upload jpeg, png or pdf file")
            return
        }

        if (2 <= Math.round((file.size / 1024 / 1024))) {
            alert('Please upload file less than 2 MB')
            eInput_file.remove()
            return
        }

        const formData = new FormData()
        formData.append('file', file)
        formData.append('event_pk', event_pk)
        formData.append('paymentStatus', paymentStatus)

        fetch(`/registered/receipt_upload/${slug}`, {
            method   : 'POST',
            body : formData,
        }).then(function (response){
            if(response.status === 400){
                response.text().then(responseText => {
                    alert(responseText);
                });
            }
            location.reload()
        })
    }
}

function viewReceipt (event_pk){
    const eButton = document.createElement('button')
    eButton.classList = 'button'
    eButton.innerHTML = 'View Receipt'

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


export function getReceiptHistory(slug) {
    fetch(`/tickets/receipt/history/${slug}`).then(function (response) {
        if (200 == response.status) {
            return response.json()
        }
    }).then( function(json){
        receiptHistory(json)
    })
}

function receiptHistory(json){
    const eReceiptTable = document.getElementById('receipt-history-table')
    eReceiptTable.innerHTML = '<thead><tr></tr></thead><tbody></tbody>'

    json.headers.forEach(function (h, i) {
        if(h != 'pk'){
            const eTh = document.createElement('th')
            eTh.innerText = h
            eReceiptTable.children[0].children[0].append(eTh)
        }
    })

    json.data.forEach(function (row) {
        const eTr = document.createElement('tr')
        Object.entries(row).forEach(function ([k,v]) {
            if(k != 'pk'){
                const eTd = document.createElement('td')

                if (k == 'Receipt') {
                    const viewBtn = document.createElement('button')
                    viewBtn.innerText = 'View'
                    viewBtn.classList = 'button'
                    viewBtn.style.margin = '1%'
                    viewBtn.onclick = function () { viewReceiptFromHistory(row.pk) }
                    eTd.append(viewBtn)
                }

                else if (k =='Updated On') {
                    if (v) {
                        eTd.innerText = new Date(v).toDateString();
                    } else {
                        eTd.innerText = '';
                    }
                }

                else{
                    eTd.innerHTML = v
                }
                eTr.append(eTd)
            eReceiptTable.children[1].append(eTr)
            }
        })
    })
}

function viewReceiptFromHistory(receipt_pk){
    const eButton = document.createElement('button')
    eButton.classList = 'button'
    eButton.innerHTML = 'View Receipt'

    fetch(`/ticket/receipt_view/${receipt_pk}`, {
        method   : 'POST',
        headers : { 'Content-Type' : 'application/json' },
        body : JSON.stringify({
            receipt_pk : receipt_pk,
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
