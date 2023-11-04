from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from app.helpers.decorators import user_must_be_registered
from app.models import Member
from app.helpers.utils import send_otp
from datetime import datetime
import pyotp

def login(request):
    if request.method == 'GET':
        return render(request, 'member/auth/login.html')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if email and password:
            member = Member.objects.filter(email=email).first()

            if member:
                if check_password(password, member.password):
                    request.session['customer_id'] = member.uuid_str()
                    request.session['user_type'] = 'member'
                    return redirect('app.member:member_dashboard_activity')
                else:
                    messages.error(request, 'Ups, Password salah!')
                    return redirect('app.member:login')

            else:
                messages.error(request, 'Email belum terdaftar di SkillUpKids!')
                return redirect('app.member:login')

def register(request):
    if request.method == 'GET':        
        return render(request, 'member/auth/register.html')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        number = request.POST.get('num_wa')
        password = request.POST.get('password')
        
        if name and email and number and password:            
            if Member.objects.filter(email=email).exists():
                messages.error(request, 'Email sudah terdaftar!')
                return redirect('app.member:register')
                        
            if Member.objects.filter(number=number).exists():
                messages.error(request, 'Nomor whatsapp sudah terdaftar!')
                return redirect('app.member:register')
            
            request.session.flush()
            import uuid
            unique_code = str(uuid.uuid4())
            request.session['unique_code'] = unique_code 
            
            request.session['name'] = name
            request.session['email'] = email
            request.session['number'] = number
            request.session['password'] = password
            request.session.set_expiry(300)

            send_otp(request, email)          
            messages.success(request, 'Kode berhasil dikirim ke email anda!')

            return redirect('app.member:verify')
        else:
            return redirect('app.member:register')
    
@user_must_be_registered
def verify(request):
    
    if request.method == 'GET':
        return render(request, 'member/auth/verify.html')

    if request.method == 'POST':
        user_otp = request.POST.get('digit-1') + request.POST.get('digit-2') + request.POST.get('digit-3') + request.POST.get('digit-4')
        otp_secret_key = request.session['otp_secret_key']
        otp_valid_until = request.session['otp_valid_until']

        if otp_secret_key and otp_valid_until is not None:
            valid_until = datetime.fromisoformat(otp_valid_until)

            if valid_until > datetime.now():
                totp = pyotp.TOTP(otp_secret_key, digits=4, interval=60)

                if totp.verify(user_otp):
                    name = request.session['name']
                    email = request.session['email']
                    number = request.session['number']
                    password = request.session['password']

                    customer = Member(name=name, email=email, number=number, password=password, is_verified=True)
                    customer.save()

                    request.session.clear()
                    request.session['customer_id'] = customer.uuid_str()
                    request.session['user_type'] = 'member'
                    return redirect('app.member:member_dashboard_activity')
                
                else:
                    messages.error(request, 'Kode OTP salah!')
                    return redirect('app.member:verify')
            
            else:
                messages.error(request, 'Kode OTP sudah kadaluarsa!')
                return redirect('app.member:verify')

        else:
            messages.error(request, 'Ups...terjadi kesalahan, silahkan coba lagi!')
            return redirect('app.member:verify')