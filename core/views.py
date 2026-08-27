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

from django.contrib.auth.hashers import make_password, check_password

def login_view(request):
    if request.method == 'POST':
        mobile = request.POST.get('mobile')
        password = request.POST.get('password')
        
        try:
            member = MemberRegistration.objects.get(mobile=mobile)
            
            # Check karo ki admin ne approve kiya hai ya nahi
            if not member.is_approved:
                return render(request, 'login.html', {'error': 'Aapka registration abhi pending hai, admin approval ka wait karein.'})
            
            # Agar pehli baar login kar raha hai (password set nahi hai)
            if not member.password:
                request.session['setup_mobile'] = mobile
                return redirect('setup_password')
            
            # Agar password pehle se hai toh match karo
            if member.password and check_password(password, member.password):
                request.session['member_id'] = member.id
                return redirect('student_dashboard')
            else:
                return render(request, 'login.html', {'error': 'Galat mobile number ya password hai.'})
                
        except MemberRegistration.DoesNotExist:
            return render(request, 'login.html', {'error': 'Yeh mobile number registered nahi hai.'})
            
    return render(request, 'login.html')

def setup_password_view(request):
    mobile = request.session.get('setup_mobile')
    if not mobile:
        return redirect('login')
        
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password == confirm_password:
            member = MemberRegistration.objects.get(mobile=mobile)
            member.password = make_password(new_password)
            member.save()
            
            if 'setup_mobile' in request.session:
                del request.session['setup_mobile']
            request.session['member_id'] = member.id
            
            return redirect('student_dashboard')
        else:
            return render(request, 'setup_password.html', {'error': 'Dono passwords match nahi ho rahe hain.'})
            
    return render(request, 'setup_password.html') # 👈 Yahan par '_view' hata dena hai # Note: file ka naam check kar lena niche diye steps ke hisab se

def student_dashboard_view(request):
    member_id = request.session.get('member_id')
    if not member_id:
        return redirect('login')
        
    member = MemberRegistration.objects.get(id=member_id)
    return render(request, 'student_dashboard.html', {'member': member})