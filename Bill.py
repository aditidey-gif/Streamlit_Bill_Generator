import streamlit as st
import datetime
import textwrap

# Function to convert a number to words (Indian currency format)
def convert_amount_to_words(number):
    """
    Converts a number into words.
    Supports numbers up to 99,99,99,999 (99 Crore)
    """
    if not isinstance(number, (int, float)):
        return "Invalid input"

    def _convert_part(n):
        words = []
        if n == 0:
            return ""

        units = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
        teens = ["Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
        tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]

        if n >= 10000000:
            words.append(_convert_part(n // 10000000))
            words.append("Crore")
            n %= 10000000
        if n >= 100000:
            words.append(_convert_part(n // 100000))
            words.append("Lakh")
            n %= 100000
        if n >= 1000:
            words.append(_convert_part(n // 1000))
            words.append("Thousand")
            n %= 1000
        if n >= 100:
            words.append(units[n // 100])
            words.append("Hundred")
            n %= 100
        if n >= 20:
            words.append(tens[n // 10])
            n %= 10
        elif n >= 10:
            words.append(teens[n - 10])
            n = 0
        if n > 0:
            words.append(units[n])
        return " ".join(words)

    try:
        integer_part, decimal_part = str(f"{number:.2f}").split('.')
        integer_part = int(integer_part)
        decimal_part = int(decimal_part)
    except ValueError:
        return "Invalid number format"

    words = []
    if integer_part == 0 and decimal_part == 0:
        return "Zero Rupees Only"
    
    if integer_part > 0:
        words.append(_convert_part(integer_part))
        words.append("Rupees")
    
    if decimal_part > 0:
        if integer_part > 0:
            words.append("and")
        words.append(_convert_part(decimal_part))
        words.append("Paise")
    
    words.append("Only")
    
    return " ".join(words).strip()


def generate_bill_content(shop_details, customer_details, products):
    """
    Generates the bill content as a formatted string.
    """
    bill_date = customer_details['bill_date']
    customer_name = customer_details['customer_name']
    customer_phone = customer_details['customer_phone']
    customer_address = customer_details['customer_address']

    shop_name = shop_details['name']
    shop_address = shop_details['address']
    shop_phone = shop_details['phone']
    
    total_amount = sum(p['total_product_amount'] for p in products)
    amount_in_words = convert_amount_to_words(total_amount)
    wrapped_words = textwrap.fill(amount_in_words, width=80)
    
    bill_content = f"""
{shop_name.ljust(80)}
{shop_address.ljust(50)}
PHONE: {shop_phone.ljust(43)}

DATE : {bill_date.ljust(43)}

_______________________________BILL TO_________________________________
NAME   : {customer_name}
PHONE  : {customer_phone}
ADDRESS: {customer_address}

___________________________PRODUCT DETAILS_____________________________
{'PRODUCT NAME':<25} {'QTY':^5} {'PER UNIT AMT(₹)':>12} {'TOTAL AMT(₹)':>15}
_______________________________________________________________________
"""
    for product in products:
        bill_content += f"\n{product['name']:<25} {product['quantity']:^5} {product['unit_amount']:>12.2f} {product['total_product_amount']:>15.2f}"

    bill_content += f"""
_______________________________________________________________________
{'TOTAL:':<41} ₹{total_amount:>17.2f}
{'IN WORDS:':<5} {wrapped_words}
_______________________________________________________________________
"""
    return bill_content, total_amount

# --- Streamlit App UI ---
st.title("🧾BILL GENERATOR🧾")
st.markdown("---")

# 1. Shop Details
st.sidebar.header("Shop Details")
shop_name = st.sidebar.text_input("Shop Name")
shop_address = st.sidebar.text_area("Shop Address")
shop_phone = st.sidebar.text_input("Shop Phone Number")

# 2. Customer and Bill Details
st.header("Customer Details")
col1, col2 = st.columns(2)
with col1:
    customer_name = st.text_input("Customer Name", key="customer_name")
    customer_phone = st.text_input("Customer Phone Number", key="customer_phone")
with col2:
    today = datetime.date.today()
    bill_date = st.date_input("Bill Date", value=today, key="bill_date").strftime("%d-%m-%Y")
    customer_address = st.text_area("Customer Address", key="customer_address")

st.markdown("---")

# 3. Product Details (using session state)
st.header("Product Details")

if 'products' not in st.session_state:
    st.session_state.products = []

with st.form("product_form", clear_on_submit=True):
    col3, col4, col5 = st.columns([3, 1, 2])
    with col3:
        product_name = st.text_input("Product Name", key="product_name_input")
    with col4:
        quantity = st.number_input("Quantity", min_value=1, value=1, step=1, key="quantity_input")
    with col5:
        unit_amount = st.number_input("Unit Amount (₹)", min_value=0.0, value=0.0, key="unit_amount_input")
    
    add_button = st.form_submit_button("Add Product")

    if add_button:
        if product_name and quantity > 0 and unit_amount >= 0:
            product_total_amount = quantity * unit_amount
            st.session_state.products.append({
                "name": product_name.upper(),
                "quantity": quantity,
                "unit_amount": unit_amount,
                "total_product_amount": product_total_amount
            })
            st.success(f"Added {product_name} to the bill.")
        else:
            st.error("Please fill in all product details correctly.")

# Display a table of added products
if st.session_state.products:
    st.markdown("### Added Products")
    st.table(st.session_state.products)
    
st.markdown("---")

# 4. Generate Bill and Download
if st.button("Generate & Display Bill"):
    # Create the shop_details dictionary dynamically from user input
    shop_details = {
        "name": shop_name,
        "address": shop_address,
        "phone": shop_phone
    }
    
    customer_details = {
        "customer_name": customer_name if customer_name else "N/A",
        "customer_phone": customer_phone if customer_phone else "N/A",
        "customer_address": customer_address if customer_address else "N/A",
        "bill_date": bill_date
    }
    
    if st.session_state.products:
        bill_content, total_amount = generate_bill_content(shop_details, customer_details, st.session_state.products)
        
        st.subheader("Final Bill Preview")
        st.code(bill_content, language='text')

        # Download button
        st.download_button(
            label="Download Bill",
            data=bill_content,
            file_name=f"bill_{customer_name.replace(' ', '')}_{bill_date}.txt",
            mime="text/plain"
        )
    else:
        st.warning("Please add at least one product before generating the bill.")
