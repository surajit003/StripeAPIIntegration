#Use case

An organization called Test Org comes to a property management company. The property management
investigates the property and determines a rate and sends the organization a quotation.
Upon agreement, the property management Co sends a payment link for the organization to make the
payment. The Organization makes the payment and a payment record is saved in the Database


#Endpoints

1. Charge Url - /stripe/organization/<int:org_id>/charge/

A unique url is generated by the business and is emailed to the organization.
The organization then clicks on the endpoint and proceeds to enter the card details

e.g /stripe/organization/PAM-1290/charge/


2. Payment secret - /stripe/payment/secret/

This endpoint is invoked by stripe to create a paymentIntent object that will
be used to complete the payment

3. Payment status - /stripe/payment/status/

This endpoint is the redirect url where stripe redirects after the payment is
completed. The payment details in the database in updated after fetching
more information from the payment intent and updated accordingly.

#Set Up:

To run the application follow the following steps
1. Log in /admin 
2. Create an organization record
3. Create a payment record for that organization with type ONBOARDING and
the correct amount
4. Save the payment record
5. Then navigate to the /stripe/organization/<your-organization-id/charge/
6. Use test card details as specified by stripe
     e.g. 
      Card Num - 4242424242424242
      
      Expiry - 12/34
      
      CVV - 010

Important note

Make sure to add your stripe Test Private Key in the following files
/stripe_app/base.html

e.g   const stripe = Stripe('pk_test..............');

Also update the return url for successful payment to redirect in 

/stripe_app/checkout.html

```javascript
  confirmParams: {
    return_url: 'PUT YOUR REDIRECT URL HERE'
}
```

#Run tests

python manage.py test