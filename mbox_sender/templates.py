# subject   = 'PostgreSQL Conference Nepal - Complete Registration'
# subject   = '[Speaker] Welcome to the 3rd PostgreSQL Conference Nepal 2025'
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


PAYMENT_FOLLOWUP_SUB = '[PgConf Nepal 2025] Payment Followup'
PAYMENT_FOLLOWUP = '''
Dear {name},

Thank you for registering for the 3rd PostgreSQL Conference Nepal 2025.
We look forward to your participation in this enriching and informative event.


Registration Details:
Status: {status}
Full Name: {name}
Email: {email}
Category: {category}
Conference Date: 5-6 May, 2025
Pre-Conference Training Date: 3-4 May, 2025 (SOLD OUT)

The selected talks, speakers and tentative schedules are available at
official website: https://pgconf.org.np/ [1]


Other Information:
Kindly confirm your participation by promptly updating your bio,
affiliation, and mobile number.
You may access your registration details,
ticket information, and upload the payment receipt
through the following link: https://pgconf.org.np/registered/{slug} [2]

If you have not yet completed the payment, HURRY UP! we are almost FULL.

If you have already completed the payment, kindly ignore this message.

We look forward to welcoming you to the conference!


Thank you,
Conference Organizing Team
Third PostgreSQL Conference Nepal
Visit Website [3]
Contact us at info@pgconf.org.np[4]
© 2025 PgConf Nepal. All rights reserved.

---
[1]  https://pgconf.org.np/
[2]  https://pgconf.org.np/registered/{slug}
[3]  https://pgconf.org.np
[4]  info@pgconf.org.np
'''


INTL_FINAL_CALL_SUB = '[final call] PostgreSQL Conference Nepal 2025'
INTL_FINAL_CALL = '''
Dear {name},

Greetings from the PostgreSQL Conference Nepal 2025 organizing team!

This is a final call for completing your registration payment for
the PostgreSQL Conference Nepal 2025, scheduled to be held in Nepal
during 5-6 May, 2025.

Due to essential logistic arrangements, we kindly request you
to complete your payments and confirm your participation
by April 26th, 2025. You can access your profile from the link below:
https://pgconf.org.np/registered/{slug}

Check the details:
Speakers: https://pgconf.org.np/programs/speakers
Tentative Program Schedule: https://pgconf.org.np/pages/schedule

Failure of payment may results in cancellation of your registration,
as we will be closing the international registration process after this date.

If you have already made the payment, please disregard this message
and share your travel details to Dr. Prakash Poudyal at prakash@ku.edu.np.
Otherwise, we request you to proceed at the earliest
and contact us if you need any assistance.

We appreciate your understanding and cooperation.

For any other information please contact any of our organizers:
- Mark Rivkin: m.rivkin@postgrespro.ru
- Prof. Dr. Bal Krishna Bal (bal@ku.edu.np)
- Dr. Prakash Poudyal (prakash@ku.edu.np)


Hope to see you in conference.

Thank you,
Conference Organizing Team
info@pgconf.org.np
Third PostgreSQL Conference Nepal
5-6 May, 2025
Visit Website
Contact us at info@pgconf.org.np
© 2025 PgConf Nepal. All rights reserved.

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
