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
