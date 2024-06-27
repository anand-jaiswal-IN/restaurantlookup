import razorpay
from os import environ

# auth = ("YOUR_ID", "YOUR_SECRET")
auth = (environ.get('RAZORPAY_ID'), environ.get('RAZORPAY_SECRET'))

def create_order(amount):
    auth = (environ.get('RAZORPAY_ID'), environ.get('RAZORPAY_SECRET'))

    client = razorpay.Client(auth=auth)
    data = { "amount": amount*100, "currency": "INR", "receipt": "order_rcptid_11" } # multiply by 100 in amount because amount in razorpay is taken in paise instead of rupee
    payment = client.order.create(data=data)
    return payment


# https://razorpay.me/@anandjaiswal9602