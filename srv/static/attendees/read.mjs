export function checkPaymentReceipt(slug) {
    fetch(
        `/registered/payment_receipt_check/${slug}`
    ).then(function (response) {
        if(response.status == 200) {
            document.getElementById('exising-receipt').innerHTML =
                "<div class='alert alert-info'>"+
                "Payment receipt file  &#11147;"+
                " <a href='/registered/payment_receipt_download/" + slug + "'>Download</a>"+
                "</div>"
            const btn = document.getElementById('submit-receiptFile')
            if(btn) btn.innerText = "Update receipt"
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
