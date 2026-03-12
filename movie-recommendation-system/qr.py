import qrcode
import os
import uuid
import time
import requests

# Function to generate the QR code (no changes here)
def generate_qr_code(data, save_dir='assets/qr'):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    filename = f"qr_{uuid.uuid4().hex[:8]}.png"
    full_path = os.path.join(save_dir, filename)
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=8,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(full_path)
    
    return full_path

# Function to initiate payment and check payment status
def initiate_payment_and_verify(bill_data, order_id):
    qr_data = f"upi://pay?pa=paytmqr5lwrim@ptys&pn=RAJDIP%20CHANDRAKANT%20PATIL&am={bill_data['amount']}&tr={order_id}&tn=taxi%20bill"
    
    # Generate the QR code and save it
    qr_image_path = generate_qr_code(qr_data)
    print(f"QR Code saved at: {qr_image_path}")
    
    # Now wait for the payment to be completed
    print("Waiting for payment confirmation...")
    time.sleep(5)  # Allow some time for the user to complete the payment
    
    # Check payment status
    response = check_payment_status(order_id)
    
    if response:
        print("Payment successful! You can now watch the movie.")
        # Here you can trigger the movie playback (or UI update with green checkmark)
    else:
        print("Payment not successful or still pending. Please try again.")
        
# Example usage:
bill_data = {'amount': 100}  # Amount for the movie
order_id = "1745054673"  # Order ID (it should be dynamically generated in your real application)
initiate_payment_and_verify(bill_data, order_id)
