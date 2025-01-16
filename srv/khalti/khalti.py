import json

import flask

from srv import app

KHALTI_API_KEY = app.config.get('KHALTI_KEY', 'default_key')
url = app.config.get('KHALTI_URL', 'https://dev.khalti.com/api/v2/epayment/initiate/')
print('Payment URL', url)


@app.post('/start-payment')
def start_payment():
    data = flask.request.get_json()

    data = json.dumps({
        'amount'              : data.get('amount'),  # Amount to be paid
        'return_url'          : data.get('return_url'),
        'website_url'         : data.get('website_url'),
        'purchase_order_id'   : data.get('purchase_order_id'),
        'purchase_order_name' : data.get('purchase_order_name'),
        'customer_info'       : {
            'name'  : data.get('customer_info', {}).get('name'),
            'email' : data.get('customer_info', {}).get('email'),
            'phone' : data.get('customer_info', {}).get('phone')
        }
    })

    headers = {
        'Authorization' : KHALTI_API_KEY,
        'content-type'  : 'application/json'
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        response_data = response.json()
        payment_url = response_data.get('payment_url')
        print('payment_url: ', payment_url)

        return flask.jsonify({
            'payment_url' : payment_url
        })

    return flask.jsonify({
        'error'   : 'Failed to initiate payment',
        'details' : response.text
    }), 500


@app.route('/payment-success')
def payment_success():
    payment_status = flask.request.args.get('status')
    transaction_id = flask.request.args.get('transaction_id')

    if payment_status == 'success':
        return f'Payment successful: Transaction ID: {transaction_id}'

    return f'Payment failed: Transaction ID: {transaction_id}'
