import requests
import time

def get_successful_response(url, max_retries=20, delay=2):
    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            data = response.json()  # Parse JSON response
            
            # Check if the 'code' field is 200 (indicating success)
            if data.get('code') == 200:
                print(f"Success on attempt {attempt + 1}")
                return data  # Return the successful data
            else:
                print(f"Attempt {attempt + 1}: code = {data.get('code')}, message = {data.get('message')}")
        except Exception as e:
            print(f"Attempt {attempt + 1} failed with exception: {e}")
        
        time.sleep(delay)
    
    print("Max retries reached without success.")
    return None

def check_payment_status(order_id):
    # Construct the API URL for payment verification
    url = f"https://your-payment-api.com/verify?order_id={order_id}"
    return get_successful_response(url)

# Usage Example:
# Once the payment is made, call this function to verify the payment status
order_id = "1745054673"
response = check_payment_status(order_id)

if response:
    # If payment is successful, trigger movie playback (or update UI)
    print("Payment successful! You can now watch the movie.")
    # Unlock the movie playback or show a green checkmark
else:
    print("Payment verification failed or not successful yet.")
