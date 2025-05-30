PARTICIPANTS_REG = '''
Dear {name},

Thank you for registering for the 3rd PostgreSQL Conference Nepal 2025.
We are excited to have you join us for this insightful event.

Registration Details:
Status: {status}
Full Name: {name}
Email: {email}
Category: {category}
Conference Date: 5-6 May, 2025
Pre-Conference Training Date: 3-4 May, 2025
More detail: visit official website  https://pgconf.org.np/ [1]

Other Information:
To confirm your participation, please complete your payment
by {deadline}. You can access your registration, ticket details
and process the payment via the link: https://pgconf.org.np/registered/{slug} [2]

Tickets are sold on a first-come, first-served basis, so payments
must be made promptly.

Note for International participants:
We only support wire transfer or onsite payment only.
For onsite payment related terms and conditions
contact us via email (info@pgconf.org.np) [4].

If you have already completed the payment, kindly ignore this message.

We look forward to welcoming you to the conference!

Best regards,
Conference Organizing Team
info@pgconf.org.np[4]
Third PostgreSQL Conference Nepal
Visit Website [3]
Contact us at info@pgconf.org.np[4]
© 2025 PgConf Nepal. All rights reserved.

---
[1]  https://pgconf.org.np/
[2]  https://pgconf.org.np/registered/{slug}
[3] https://pgconf.org.np
[4] info@pgconf.org.np
'''

PARTICIPANTS_PAYMENT_FOLLOWUP = '''
Dear {name},

Thank you for registering for the 3rd PostgreSQL Conference Nepal 2025.
We look forward to your participation in this enriching and informative event.


Registration Details:
Status: {status}
Full Name: {name}
Email: {email}
Category: {category}
Conference Date: 5-6 May, 2025
Pre-Conference Training Date: 3-4 May, 2025
More detail: visit official website  https://pgconf.org.np/ [1]


Other Information:
Kindly confirm your participation by promptly updating your bio,
affiliation, and mobile number.
If you have not yet completed the payment, please do so at your
earliest convenience. You may access your registration details,
ticket information, and upload the payment receipt
through the following link: https://pgconf.org.np/registered/{slug} [2]


Tickets are sold on a first-come, first-served basis, so payments
must be made promptly.

Note for International participants:
We only support wire transfer or onsite payment only.
For onsite payment related terms and conditions
contact us via email (info@pgconf.org.np) [4].

If you have already completed the payment, kindly ignore this message.

We look forward to welcoming you to the conference!


Thank you,
Conference Organizing Team
info@pgconf.org.np[4]
Third PostgreSQL Conference Nepal
Visit Website [3]
Contact us at info@pgconf.org.np[4]
© 2025 PgConf Nepal. All rights reserved.

---
[1]  https://pgconf.org.np/
[2]  https://pgconf.org.np/registered/{slug}
[3] https://pgconf.org.np
[4] info@pgconf.org.np
'''


def registration(slug, _type, name, email, status, category, deadline = '30 April, 2025'):
    return PARTICIPANTS_REG.format(
        slug = slug,
        category = category,
        name = name,
        status = status,
        email = email,
        deadline = deadline,
    )
