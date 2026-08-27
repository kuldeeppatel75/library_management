from django.shortcuts import render, redirect
from .models import MemberRegistration

def home(request):
    return render(request, 'index.html')

def register_view(request):
    return render(request, 'register.html')


def register_view(request):
    if request.method == 'POST':
        # 1. Form ka saara data aur photo session me nahi, balki temporary request.FILES se pakad kar 
        # seedha database me 'Pending' (is_approved=False) save kar dete hain!
        
        plan = request.POST.get('membership_plan')
        amounts = {
            '4_hours': 500, 
            '8_hours': 800, 
            '12_hours': 1000, 
            'permanent': 1600
        }
        amount = amounts.get(plan, 500)
        
        # Database me turant entry kar do lekin abhi approved FALSE rahega
        new_reg = MemberRegistration.objects.create(
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            father_name=request.POST.get('father_name'),
            address=request.POST.get('address'),
            mobile=request.POST.get('mobile'),
            photo=request.FILES.get('photo'), # Photo yahan direct save ho jayegi (Pillow ki madad se)
            membership_plan=plan,
            amount=amount,
            utr_number="PENDING_UTR", # Abhi UTR nahi mila hai, baad me update hoga
            is_approved=False
        )
        
        # User ki ID ko session me save kar lo taaki payment page par pata chale kiski entry hai
        request.session['pending_reg_id'] = new_reg.id
        request.session['amount'] = amount
        
        return redirect('payment_page')

    return render(request, 'register.html')


def payment_view(request):
    amount = request.session.get('amount', 500)
    reg_id = request.session.get('pending_reg_id')
    
    if not reg_id:
        return redirect('register') # Agar session me ID nahi hai toh wapas register page bhej do
        
    if request.method == 'POST':
        utr = request.POST.get('utr_number')
        
        if utr:
            # UTR number mil gaya, ab database me us user ko dhoondh kar UTR update kar do
            try:
                registration = MemberRegistration.objects.get(id=reg_id)
                registration.utr_number = utr
                registration.save()
            except MemberRegistration.DoesNotExist:
                pass
            
            # Session saaf kar do
            if 'pending_reg_id' in request.session:
                del request.session['pending_reg_id']
            if 'amount' in request.session:
                del request.session['amount']
            
            return render(request, 'success_pending.html')
            
    return render(request, 'payment.html', {'amount': amount})
    amount = request.session.get('amount', 500)
    
    if request.method == 'POST':
        utr = request.POST.get('utr_number')
        reg_data = request.session.get('reg_data')
        
        if reg_data and utr:
            # Jab user UTR daal dega, tab database me Pending (is_approved=False) save hoga
            MemberRegistration.objects.create(
                first_name=reg_data['first_name'],
                last_name=reg_data['last_name'],
                father_name=reg_data['father_name'],
                address=reg_data['address'],
                mobile=reg_data['mobile'],
                membership_plan=reg_data['membership_plan'],
                amount=amount,
                utr_number=utr,
                is_approved=False # Admin jab tak approve nahi karega
            )
            
            # Session saaf kar do
            if 'reg_data' in request.session:
                del request.session['reg_data']
            if 'amount' in request.session:
                del request.session['amount']
            
            return render(request, 'success_pending.html')
            
    return render(request, 'payment.html', {'amount': amount})