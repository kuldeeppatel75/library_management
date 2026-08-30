from django.shortcuts import render, redirect
from .models import MemberRegistration
from .models import ContactMessage
from django.contrib.auth import authenticate, login


def home(request):
    # Database se sirf wahi members gin rahe hain jinka is_approved True (approved) hai
    approved_count = MemberRegistration.objects.filter(is_approved=True).count()
    
    context = {
        'approved_count': approved_count,
    }
    return render(request, 'index.html', context)
    

def register_view(request):
    return render(request, 'register.html')


def register_view(request):
    if request.method == 'POST':
        # 1. Form ka saara data aur photo session me nahi, balki temporary request.FILES se pakad kar 
        # seedha database me 'Pending' (is_approved=False) save kar dete hain!
        mobile_input = request.POST.get('mobile')
        if MemberRegistration.objects.filter(mobile=mobile_input).exists():
            return render(request, 'register.html', {'error': 'Mobile Number already registered!'})
        
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

            # 1. Pehle check karo ki admin ne approve kiya hai ya nahi
            if not member.is_approved:
                return render(request, 'login.html', {'error': 'Your registration is pending Please wait for admin approve .'})

            # 2. Agar user ka password abhi tak database me set nahi hua hai
            if not member.password:
                request.session['setup_mobile'] = mobile
                return redirect('setup_password')

            # 3. Agar password field khali chhod di hai
            if not password:
                return render(request, 'login.html', {'error': 'Please Fill the password'})

            # 4. Agar password match ho jata hai
            if check_password(password, member.password):
                request.session['member_id'] = member.id
                return redirect('student_dashboard')
            else:
                return render(request, 'login.html', {'error': 'Wrong Password try again!'})

        except MemberRegistration.DoesNotExist:
            return render(request, 'login.html', {'error': 'This Phone Number not registerd .'})

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
            return render(request, 'setup_password.html', {'error': 'Password does not match.'})
            
    return render(request, 'setup_password.html') # 👈 Yahan par '_view' hata dena hai # Note: file ka naam check kar lena niche diye steps ke hisab se

def student_dashboard_view(request):
    member_id = request.session.get('member_id')
    if not member_id:
        return redirect('login')
        
    member = MemberRegistration.objects.get(id=member_id)
    return render(request, 'student_dashboard.html', {'member': member})
def role_selection_view(request):
    return render(request, 'role_selection.html')

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def admin_login_view(request):
    if request.method == 'POST':
        username_input = request.POST.get('username')
        password_input = request.POST.get('password')
        
        # User authenticate karein
        user = authenticate(request, username=username_input, password=password_input)
        
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('/admin/')  # Login ke baad kahan jana hai
        else:
            return render(request, 'admin_login.html', {'error': 'Wrong Username or Password!'})
            
    return render(request, 'admin_login.html')


def logout_view(request):
    if 'member_id' in request.session:
        del request.session['member_id']
    return redirect('login_page')

from django.shortcuts import render
from .models import ContactMessage

from django.core.mail import send_mail
from django.conf import settings

def contact_view(request):
    success_message = None
    if request.method == 'POST':
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        category = request.POST.get('category')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Database me save karna
        ContactMessage.objects.create(
            name=name,
            mobile=mobile,
            email=email,
            category=category,
            subject=subject,
            message=message
        )

        # Email notification bhejne ka code
        email_subject = f"Naya Message/Complaint: {subject} ({category})"
        email_message = f"""
        Library website par ek naya contact/query aaya hai:
        
        Naam: {name}
        Mobile: {mobile}
        Email: {email if email else 'N/A'}
        Category: {category}
        Subject: {subject}
        
        Message Details:
        {message}
        """
        
        try:
            send_mail(
                email_subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],  # Yeh email aapke apne inbox mein aayega
                fail_silently=False,
            )
        except Exception as e:
            print("Email bhejne mein error aaya:", e)

        success_message = "Your Message submited successfull. we will contact you soon!"

    return render(request, 'contact.html', {'success_message': success_message})


def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        category = request.POST.get('category')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Database me save karna
        ContactMessage.objects.create(
            name=name, mobile=mobile, email=email,
            category=category, subject=subject, message=message
        )

        # Email notification bhejne ka code
        email_subject = f"Naya Message/Complaint: {subject} ({category})"
        email_message = f"""
        Library website par ek naya contact/query aaya hai:
        
        Naam: {name}
        Mobile: {mobile}
        Email: {email if email else 'N/A'}
        Category: {category}
        Subject: {subject}
        
        Message Details:
        {message}
        """
        
        try:
            send_mail(
                email_subject,
                email_message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
        except Exception as e:
            print("Email bhejne mein error aaya:", e)

        # Success hone ke baad naye page par redirect karna
        return redirect('contact_success')

    return render(request, 'contact.html')

# Naya view success page ke liye
def contact_success_view(request):
    return render(request, 'contact_success.html')


from django.shortcuts import redirect

def custom_logout(request):
    # Session se user ka data hata rahe hain
    if 'pending_reg_id' in request.session:
        del request.session['pending_reg_id']
    # Agar Django auth use kiya hai toh logout() bhi kar sakte hain
    from django.contrib.auth import logout
    logout(request)
    return redirect('home')


from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required(login_url='admin_login')
def admin_dashboard_view(request):
    approved_count = MemberRegistration.objects.filter(is_approved=True).count()
    pending_count = MemberRegistration.objects.filter(is_approved=False).count()
    context = {
        'approved_count': approved_count,
        'pending_count': pending_count,
    }
    return render(request, 'admin_dashboard.html', context)

@staff_member_required(login_url='admin_login')
def admin_approved_view(request):
    approved_members = MemberRegistration.objects.filter(is_approved=True)
    return render(request, 'admin_approved.html', {'members': approved_members})

@staff_member_required(login_url='admin_login')
def admin_pending_view(request):
    pending_members = MemberRegistration.objects.filter(is_approved=False)
    return render(request, 'admin_pending.html', {'members': pending_members})

@staff_member_required(login_url='admin_login')
def admin_action_view(request, member_id, action):
    try:
        member = MemberRegistration.objects.get(id=member_id)
        if action == 'approve':
            member.is_approved = True
            member.save()
        elif action == 'delete':
            member.delete()
    except MemberRegistration.DoesNotExist:
        pass
    
    if action == 'approve':
        return redirect('admin_pending')
    return redirect('admin_approved')

def custom_admin_login_view(request):
    if request.method == 'POST':
        username_input = request.POST.get('username')
        password_input = request.POST.get('password')
        user = authenticate(request, username=username_input, password=password_input)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        else:
            return render(request, 'custom_admin_login.html', {'error': 'Wrong Username or Password / Not Staff'})
    return render(request, 'custom_admin_login.html')