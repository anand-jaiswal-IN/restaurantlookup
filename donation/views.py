from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import DonationForm
from django.contrib import messages
from utils.razorpay import create_order
from json import loads
from django.http import JsonResponse

def create_razorpay_order(req):
    if req.method != "POST":
        return JsonResponse({'error': 'only POST method is allowed'}, status=405)

    try:
        data = loads(req.body)
    except Exception as e:
        return JsonResponse({'error': f'invalid JSON data {e}' }, status=400)

    if 'amount' not in data:
        return JsonResponse({'error': 'amount field is required'}, status=400)

    try:
        amount = int(data['amount'])
        order_rzp = create_order(amount)
        return JsonResponse(order_rzp)
    except ValueError:
        return JsonResponse({'error': 'invalid amount'}, status=400)
    
def donation_page(req):

    # when payment is done, create Donation object
    if req.method == 'POST':
        try:
            data = loads(req.body)
        except Exception as e:
            return JsonResponse({'error': f'invalid JSON data {e}' }, status=400)
        
        form = DonationForm(data)

        if form.is_valid():
            donation = form.save(commit=False)
            donation.user = req.user
            donation.save()
            messages.success(req, 'Donation Successful')
            return JsonResponse({'status' : 'success', 'message' : 'Donation Successful'}, status=200)
        else:
            messages.error(req, form.errors)
            return redirect('/donation')

    context = {
        "title" : "Donation Page",
    }
    return render(req, 'donation/donation_page.html', context=context)
