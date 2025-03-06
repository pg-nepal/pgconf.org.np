export function checkPaymentReceipt(slug) {
    fetch(`/registered/payment_receipt_check/${slug}`).then(function (response) {
        if (response.status == 200) {
            document.getElementById('exising-receipt').innerHTML =
                "<div class='alert alert-info'>"+
                "Payment receipt file  &#11147;"+
                " <a href='/registered/payment_receipt_download/" + slug + "'>Download</a>"+
                "</div>"
            const btn = document.getElementById('submit-receiptFile')
            if(btn) btn.innerText = 'Update receipt'
        }
    })
}


export function getTicketDetails(slug) {
    fetch(`/registered/ticket/${slug}`).then(function (response) {
        if (200 == response.status) {
            return response.json()
        }
    }).then(function (json) {
        const eTable = document.getElementById('ticket-table')

        json.headers.forEach(function (h) {
            const eTh = document.createElement('th')
            eTh.innerHTML = h
            eTable.children[0].children[0].append(eTh)
        })

        let total = 0
        let currency = ''
        json.data.forEach(function (row) {
            const eTr = document.createElement('tr')
            row.forEach(function (cell, i) {
                const eTd = document.createElement('td')
                eTd.innerHTML = cell
                if (json.headers[i] == 'Currency') {
                    if (null !== cell) {
                        currency = cell
                    }
                }
                if (json.headers[i] == 'Amount') {
                    if (null !== cell) {
                        total += cell
                        eTd.innerHTML = cell.toLocaleString()
                    }
                }
                eTr.append(eTd)
            })
            eTable.children[1].append(eTr)
        })

        eTable.style.display = ''
        document.getElementById('total-amount').innerText = `${currency} ${total.toLocaleString()}`
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
