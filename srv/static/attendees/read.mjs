export function checkPaymentReceipt(slug) {
    fetch(
        `/registered/payment_receipt_check/${slug}`
    ).then(function (response) {
        if(response.status == 200) {
            // console.log("Found")
            document.getElementById('exising-receipt').innerHTML = 
                "<div class='alert alert-info'>"+
                "You have already uploaded a document. &#11147;"+
                " <a href='/registered/payment_receipt_download/" + slug + "'>Download</a>"+
                "</div>"
            document.getElementById('submit-receiptFile').innerText = "Update receipt"
        }
    })
}
