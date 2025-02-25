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
        if (response.status == 200) {
            const tableBody = document.getElementById('table-body')
            const template = document.getElementById('row-template')
            response.json().then(function (json){
                json.data.forEach(function (ticket) {
                    const row = template.content.cloneNode(true)
                    row.querySelector('.ticket').textContent = ticket[0]
                    row.querySelector('.rate').textContent   = ticket[1]
                    row.querySelector('.status').textContent = ticket[2]
                    tableBody.appendChild(row)
                })
                document.getElementById('ticket-table').style = ''
            })
        } else {
            document.getElementById('ticket-table').style.display = 'none'
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
