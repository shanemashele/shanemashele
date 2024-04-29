from urllib import request
from django.shortcuts import  render, redirect,get_object_or_404
from django.http.response import HttpResponse
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Cloth, Cart, CartItem, Customer,Order
from django.core.files.storage import FileSystemStorage 
from django.db.models import Sum, F,DecimalField
from .models import Measurement
from django.contrib.auth.decorators import login_required
from .models import UploadedImage,OrderItem,Payment
import json
import random
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt





def homep(request):
    return render(request,'homepage.html')


def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get("username")
        email = request.POST.get("email")
        name = request.POST.get("name")
        surname = request.POST.get("surname")
        password = request.POST.get("password")
        conformpassword = request.POST.get("password2")
        
        
       

        # Check if passwords match
        if password != conformpassword:
            messages.warning(request, 'Passwords do not match')
            return redirect('/signup')
        
        if get_user_model().objects.filter(username=uname).exists():
            messages.warning(request, 'Username already exists. Please choose a different username.')
            return redirect('/signup')
            
        if get_user_model().objects.filter(email=email).exists():
            messages.warning(request, 'Email already exists. Please choose a different email.')
            return redirect('/signup')
        
        # Get the User model
        User = get_user_model()

        # Create the user
        myuser = User.objects.create_user(username=uname, email=email, password=password, first_name=name, last_name=surname)
        
        # Create the associated Customer profile if it doesn't already exist
        try:
            Customer = myuser.customer
        except Customer.DoesNotExist:
            Customer = Customer.objects.create(user=myuser, first_name=name, last_name=surname, email=email)
        
        messages.success(request, "Sign up Success! Please login.")
        return redirect('/login')

    return render(request, "SignUp.html")
def loginpage(request):
    if request.method == 'POST':
        uname = request.POST.get("username")
        password= request.POST.get("password")
        myuser =authenticate(username=uname,password=password)
        
        if myuser is not None:
            login(request, myuser)
            messages.success(request,"Login Successfully")
            return redirect("/Category")
        else:
            messages.error(request,"Invalid Credantials")
            return redirect("/login")
           
         
    
    return render(request, 'Loginpage.html')

def logoutnow(request):
    logout(request)
    messages.info(request,"Logout Success")
    return redirect("/login")



def homepage(request):
    
    allPosts=Cloth.objects.all()[:12]

    context = {'allPosts':allPosts}
    print(allPosts)

    return render(request, 'Category.html',context)


def woman(request):
    # Filter Cloth objects by the woman category
    womanPosts = Cloth.objects.filter(category__name='woman')
    con = {'womanPosts': womanPosts}
    print(womanPosts)

    return render(request, 'woman.html', con)


def man(request):
    # Filter Cloth objects by the woman category
    manPosts = Cloth.objects.filter(category__name='man')
    conn = {'manPosts': manPosts}
    print(manPosts)

    return render(request, 'man.html', conn)
from .models import CustomerAddress

@login_required
def add_address(request):
    address = request.user.customeraddress if hasattr(request.user, 'customeraddress') else None

    if request.method == 'POST':
        # Process form submission
        address_type = request.POST.get('address_type')
        street_address = request.POST.get('street_address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
        country = request.POST.get('country')
        default = request.POST.get('default') == 'on'  # Checkbox value
        is_active = request.POST.get('is_active') == 'on'  # Checkbox value

        # Update existing address or create a new one
        if address:
            address.address_type = address_type
            address.street_address = street_address
            address.city = city
            address.state = state
            address.postal_code = postal_code
            address.country = country
            address.default = default
            address.is_active = is_active
        else:
            address = CustomerAddress(
                user_id=request.user,
                address_type=address_type,
                street_address=street_address,
                city=city,
                state=state,
                postal_code=postal_code,
                country=country,
                default=default,
                is_active=is_active
            )
        address.save()
        return redirect('listaddress')  # Redirect to the profile page
    else:
        # Pass the existing address to the template for editing
        return render(request, 'address.html', {'address': address})
def address_list(request):
    addresses = CustomerAddress.objects.all()
    return render(request, 'addresslist.html', {'addresses': addresses})  

def children(request):
    childrenPosts = Cloth.objects.filter(category__name='children')
    child = {'childrenPosts': childrenPosts}
    print(childrenPosts)

    return render(request, "Childrens.html",child)


def Desired(request):
    if request.method == 'POST':
        image = request.FILES['image']
        uploaded_image = UploadedImage.objects.create(user=request.user, image=image)
        # Handle image upload and redirect to a success page
        return redirect('upload_success')
    return render(request, 'Desired.html')
def add_cart(request, image_id):
    image = UploadedImage.objects.get(pk=image_id)
    cart_item = CartItem.objects.create(user=request.user, image=image)
    # Add logic to handle adding to cart and redirect to cart page
    return redirect('cart')

     
def Couples(request):
    couplesPosts = Cloth.objects.filter(category__name='couples')
    context = {'couplesPosts': couplesPosts}
    print(couplesPosts)
    return render(request, "Couples.html", context)



def cloth_detail(request, cloth_id):
    cloth = get_object_or_404(Cloth, pk=cloth_id)
     
    return render(request, 'cloth_detail.html', {'cloth': cloth})


def add_to_cart(request, cloth_id):
    # Retrieve the Cloth object with the given cloth_id or return 404 if not found
    cloth = get_object_or_404(Cloth, pk=cloth_id)
    
    # Create a new CartItem object with the cloth details and save it
    cart_item, created = CartItem.objects.get_or_create(user=request.user, cloth=cloth)
  

    
    # If the cart item already exists, increase its quantity by 1
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    # Redirect the user to the cloth detail page
    return redirect("cloth_detail", cloth_id=cloth_id)


def remove_from_cart(request, cloth_id):
    # Retrieve the cart item to remove
    cart_item = get_object_or_404(CartItem, user=request.user, cloth_id=cloth_id)
    # Delete the cart item
    cart_item.delete()
    # Redirect back to the cart page
    return redirect('cart')
def increment_quantity(request, cloth_id):
    # Retrieve the cart item to increment quantity
    cart_item = get_object_or_404(CartItem, user=request.user, cloth_id=cloth_id)
    # Increment the quantity
    cart_item.quantity += 1
    cart_item.save()
    
    # Update session variable for total items count
    update_total_items_count(request)
    
    return redirect('/cart')

def decrement_quantity(request, cloth_id):
    # Retrieve the cart item to decrement quantity
    cart_item = get_object_or_404(CartItem, user=request.user, cloth_id=cloth_id)
    # Decrement the quantity if greater than 1
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    
    # Update session variable for total items count
    update_total_items_count(request)
    
    return redirect('/cart')

def update_total_items_count(request):
    # Get the cart items for the current user
    cart_items = CartItem.objects.filter(user=request.user)
    # Calculate the total quantity of all items in the cart
    total_items = sum(item.quantity for item in cart_items)
   
    request.session['total_items'] = total_items
 
    
def view_cart(request):
    # Get the cart items for the current user
    cart_items = CartItem.objects.filter(user=request.user)
    

    # Retrieve total items count from session if available

    # Calculate the total price of all items in the cart
    total_items = sum(item.quantity for item in cart_items)
    
    total_price = cart_items.aggregate(
        total_price=Sum(F('cloth__price') * F('quantity'), output_field=DecimalField())
    )['total_price']

    return render(request, 'cart.html', {'cart_items': cart_items,'total_items':total_items ,'total_price': total_price})

def Size(request):
    # Your view logic here
    return render(request, 'Size.html')

def Enter(request):
     if request.method == 'POST':
        # Retrieve form data from POST request
        crown = request.POST.get('crown')
        shoulder = request.POST.get('shoulder')
        chest = request.POST.get('chest')
        waist = request.POST.get('waist')
        hips = request.POST.get('hips')
        inseam = request.POST.get('inseam')
        floor = request.POST.get('floor')

        # Convert all measurements to float to handle possible conversion errors
        try:
            crown = float(crown)
            shoulder = float(shoulder)
            chest = float(chest)
            waist = float(waist)
            hips = float(hips)
            inseam = float(inseam)
            floor = float(floor)
        except ValueError:
            # Display an error message if any measurement is not a valid number
            messages.error(request, 'enter measurements as valid numbers.')
            return redirect('enter')

        # Check if any measurement is outside the valid range (0 to 300 cm)
        if any(measurement < 0 or measurement > 300 for measurement in [crown, shoulder, chest, waist, hips, inseam, floor]):
            messages.error(request, 'Please ensure all measurements are enter in the range < o and >300')
            return redirect('enter')

        # Handle file upload
        icon = request.FILES.get('icon')
        existing_measurement = Measurement.objects.filter(user=request.user).first()

        if existing_measurement:
            # Update existing measurement
            existing_measurement.crown = crown
            existing_measurement.shoulder = shoulder
            existing_measurement.chest = chest
            existing_measurement.waist = waist
            existing_measurement.hips = hips
            existing_measurement.inseam = inseam
            existing_measurement.floor = floor
            existing_measurement.icon = icon
            existing_measurement.save()
            messages.success(request, 'Size successfully updated.')
        else:
            # Create new measurement object
            measurement = Measurement.objects.create(
                user=request.user,
                crown=crown,
                shoulder=shoulder,
                chest=chest,
                waist=waist,
                hips=hips,
                inseam=inseam,
                floor=floor,
                icon=icon
            )
            messages.success(request, 'Size successfully uploaded.')

        # Redirect to success page
        return redirect('size')
     else:
        return render(request, 'EnterSize.html')
    
def receive_measurements(request):
    user = request.user
    
    if request.method == 'POST':
        measurements_data = json.loads(request.body)
        crown = measurements_data.get('crown')
        shoulder = measurements_data.get('shoulder')
        chest = measurements_data.get('chest')
        waist = measurements_data.get('waist')
        hips = measurements_data.get('hips')
        inseam = measurements_data.get('inseam')
        floor = measurements_data.get('floor')

        if any(measurement is None for measurement in [crown, shoulder, chest, waist, hips, inseam, floor]):
            return JsonResponse({'success': False, 'message': 'Incomplete measurements data'})

        try:
            measurement = Measurement.objects.create(
                user=user,
                crown=crown,
                shoulder=shoulder,
                chest=chest,
                waist=waist,
                hips=hips,
                inseam=inseam,
                floor=floor
            )
            # Return JSON response for successful measurement creation
            return JsonResponse({'success': True, 'message': 'Measurements saved successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error: {e}'})

    else:
        # If request method is not POST, retrieve existing measurements for the user
        measurements = Measurement.objects.filter(user=user)
        # Return rendered template with existing measurements
        return render(request, 'scan.html', {'measurements': measurements})
    
def measurement_list(request):
    measurements = Measurement.objects.filter(user=request.user)
    
    return render(request, 'measurement_list.html', {'measurements': measurements})


def customer_profile(request):
    if request.user.is_authenticated:
        try:
            customer = Customer.objects.get(user=request.user)
            # Fetch associated address of the customer if it exists
            address = CustomerAddress.objects.filter(user_id=request.user).first()
            return render(request, 'profile.html', {'customer': customer, 'address': address})
        except Customer.DoesNotExist:
            # Handle the case where the customer profile does not exist
            return render(request, 'profile.html', {'customer': None, 'address': None})
    else:
        # Handle the case where the user is not authenticated
        return render(request, 'profile.html', {'customer': None, 'address': None})
import uuid
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.utils import timezone
import uuid
from paypal.standard.forms import PayPalPaymentsForm
from django.urls import reverse
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

def generate_order_number():
    # Use current timestamp as prefix
    timestamp_prefix = timezone.now().strftime('%Y%m%d%H%M%S')
    # Generate a random UUID to ensure uniqueness
    unique_id = uuid.uuid4().hex[:6].upper()  # Use the first 6 characters of the UUID
    # Combine prefix and unique ID to create the order number
    order_number = f'ORD-{timestamp_prefix}-{unique_id}'
    return order_number
def checkout(request):
    # Get cart items for the current user
    cart_items = CartItem.objects.filter(user=request.user)

    # Get user information
    user_info = {
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
    }

    # Calculate total items count
    total_items = sum(item.quantity for item in cart_items)
    
    # Calculate the total price of all items in the cart
    total_price = cart_items.aggregate(
        total_price=Sum(F('cloth__price') * F('quantity'), output_field=DecimalField())
    )['total_price']

    # Generate order number (you may use your existing method here)
    order_number = generate_order_number()

    # Save the order to the database
    order = Order.objects.create(
        user=request.user,
        order_number=order_number,
        total_price=total_price,
        quantities=total_items,  # Provide value for quantities field
        status='Pending',
    )

    # Generate PayPal checkout form
    host = request.get_host()
    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': total_price,
        'item_name': 'Items from your cart',
        'invoice': uuid.uuid4(),
        'currency_code': 'USD',
        'notify_url': f"http://{host}{reverse('paypal-ipn')}",
        'return_url': f"http://{host}{reverse('payment-success')}",
       
    }
    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)

    # Pass relevant data to the template
    context = {
        'cart_items': cart_items,
        'total_items': total_items,
        'total_price': total_price,
        'order_number': order_number,
        'user_info': user_info,
        'paypal': paypal_payment,
    }

    return render(request, 'checkout.html', context)
from django.core.exceptions import ObjectDoesNotExist
@csrf_exempt
def paypal_ipn(request):
    if request.method == 'POST':
        # Process PayPal IPN data
        ipn_data = request.POST.copy()
        
        # Extract relevant data from IPN
        transaction_id = ipn_data.get('txn_id')
        payment_status = ipn_data.get('payment_status')
        custom_data = ipn_data.get('custom')  # Order number
        
        # Find the corresponding order in your database using custom_data
        try:
            order = Order.objects.get(order_number=custom_data)
        except Order.DoesNotExist:
            return HttpResponse(status=404)
        
        # Create payment record in your database
        Payment.objects.create(
            order=order,
            transaction_id=transaction_id,
            status=payment_status,
            amount=order.total_price,
            # Add more fields as necessary
        )
        
        # Additional logic based on payment status (e.g., update order status)
        
        # Return a success response to PayPal
        return HttpResponse(status=200)
    
    # Handle other HTTP methods gracefully
    return HttpResponse(status=405)

def PaymentSuccessful(request):
    # Redirect to the view_orders view
    return redirect('view_orders')
def shopnow(request):
    # Redirect to the view_orders view
    return render(request,'shopnow.html')
def payment_complete(request):
    # Logic for payment completion
    
    # Clear the cart after payment
    cart_id = request.session.get('cart_id')
    if cart_id:
        Cart.objects.filter(id=cart_id).delete()
        del request.session['cart_id']  # Remove cart_id from session
    
    # Redirect to a different URL or render a template
    return render(request, 'payment.html')
def order_success(request, order_number, total_price):
    return render(request, 'order_success.html', {'order_number': order_number, 'total_price': total_price})
def view_orders(request):
    # Retrieve orders associated with the current user
    orders = Order.objects.filter(user=request.user)
    address = CustomerAddress.objects.filter(user_id=request.user).first()
    # Create a list to store order details for each order
    order_details = []

    # Iterate through each order to retrieve order details
    for order in orders:
        # Create a dictionary to store order details
        order_detail = {
            'order': order.order_number,
            'cloth_images': [cloth.image.url for cloth in order.cloth.all()],
            'total_price': order.total_price,
            'status': order.status
        }

        # Append order details to the main list
        order_details.append(order_detail)

    return render(request, 'view_orders.html', {'order_details': order_details,'address':address})

   
def track_order(request):
    if request.method == 'POST':
        # Get the order number from the POST data
        order_number = request.POST.get('order_number')
        
        # Filter orders by the current user
        orders = Order.objects.filter(user=request.user)
        address = CustomerAddress.objects.filter(user_id=request.user).first()
        # Attempt to retrieve the order with the given order number
        try:
            order = Order.objects.get(order_number=order_number, user=request.user)
            return render(request, 'track_order_result.html', {'order': order, 'orders': orders,'address':address})
        except Order.DoesNotExist:
            return render(request, 'track_order_result.html', {'error_message': 'Order not found'})
    
    # If the request method is not POST, render the track_order.html template
    return render(request, 'track_order.html')

def track_order_result(request):
    # If the request method is POST, process the form data
    if request.method == 'POST':
        # Get the order number from the POST data
        order_number = request.POST.get('order_number')
        
        # Filter orders by the current user
        orders = Order.objects.filter(user=request.user)
        address = CustomerAddress.objects.filter(user_id=request.user).first()
        # Attempt to retrieve the order with the given order number
        try:
            order = Order.objects.get(order_number=order_number, user=request.user)
            return render(request, 'track_order_result.html', {'order': order, 'orders': orders,'address':address })
        except Order.DoesNotExist:
            return render(request, 'track_order_result.html', {'error_message': 'Order not found'})
    
    # If the request method is not POST, render the track_order.html template
    return render(request, 'track_order.html')
def about_us(request):
    # Render the About Us page template with the context data
    return render(request, 'aboutus.html')
def terms(request):
    # Render the About Us page template with the context data
    return render(request, 'terms.html')
