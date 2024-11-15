#import library
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import random
import time #For time
import os
from fpdf import FPDF  #Import FPDF for PDF generation
from PIL import Image
import base64
import ast
import altair as alt


#-----------------------------Global Variable-------------------------------
#voucer codes
voucher_codes = {
    "DISCOUNT10": 0.10,  # 10% discount
    "DISCOUNT20": 0.20,  # 20% discount
}

#menu & price
menu = {
        "Americano": 6.00,
        "Cappuccino": 7.50,
        "Latte": 7.00,
        "Chocolate Latte": 8.50,
        "Matcha Latte": 9.00
}

#images 1
menu_images_1 = {
    "Americano": "https://th.bing.com/th/id/OIP.cArocB5W0PQPokOzkvNT4wHaHa?rs=1&pid=ImgDetMain",
    "Cappuccino": "https://th.bing.com/th/id/OIP.GQKWmWnRu5y4Bc3lfTz1fQHaLI?pid=ImgDet&w=203&h=305&c=7",
    "Latte": "https://th.bing.com/th/id/OIP.ueTivOeGgF3bLL1FjZLOnAHaJP?rs=1&pid=ImgDetMain",
    "Chocolate Latte": "https://www.livveganstrong.com/wp-content/uploads/2022/02/Toasted-Coconut-Mocha-Latte-2-full-scaled.jpg",
    "Matcha Latte": "https://th.bing.com/th/id/OIP.XXmmjBgzFWiB1YZDSbJu5AHaLH?rs=1&pid=ImgDetMain"
}

#images 2
menu_images_2 = {
    "Americano": "https://th.bing.com/th/id/OIP.Qdjl2UnflKurS06cphm_JAHaHa?w=172&h=180&c=7&r=0&o=5&pid=1.7",
    "Cappuccino": "https://th.bing.com/th/id/OIP.2m86YwVZYHm4kb2zXVO19AHaKy?w=203&h=295&c=7&r=0&o=5&pid=1.7",
    "Latte": "https://th.bing.com/th/id/OIP.L-V9QgDo_g3jJ1DjU5rswwHaJQ?pid=ImgDet&w=203&h=253&c=7",
    "Chocolate Latte": "https://th.bing.com/th/id/OIP.v0HW1MplFD1BTEiTzgMK_gHaLH?w=203&h=304&c=7&r=0&o=5&pid=1.7",
    "Matcha Latte": "https://th.bing.com/th/id/OIP.RA1kD1sCbrXacgakn6C28AHaLH?w=203&h=304&c=7&r=0&o=5&pid=1.7"
}

#coffee description
description = {
    "Americano": "A smooth and bold classic. Our Americano is crafted by blending rich, freshly brewed espresso with hot water, delivering a strong yet balanced flavor profile. It’s perfect for those who love a full-bodied coffee experience with a touch of elegance in every sip.",
    "Cappuccino": "Indulge in the perfect harmony of flavors. Our Cappuccino features a velvety layer of steamed milk topped with a thick, luxurious foam, all over a rich shot of espresso. The bold espresso flavor blends beautifully with the creamy milk, creating a warm and comforting drink that’s perfect anytime.",
    "Latte": "Savor the creamy richness of our Latte. This delightful blend of smooth espresso and perfectly steamed milk is topped with a light layer of foam for a delicate, silky finish. It’s the perfect choice for those seeking a subtle, balanced coffee with a rich, comforting texture.",
    "Chocolate Latte": "For the ultimate indulgence, try our Chocolate Latte. This decadent drink combines our smooth espresso with creamy steamed milk and rich, velvety chocolate syrup, finished with a touch of whipped cream. It’s a delicious treat that satisfies both your coffee and chocolate cravings.",
    "Matcha Latte": "Experience a vibrant and refreshing twist on a classic. Our Matcha Latte blends premium ceremonial-grade matcha green tea with perfectly steamed milk for a creamy, slightly sweet drink packed with antioxidants. It’s an energizing and flavorful choice for those who love a healthy yet indulgent beverage."
}

#their add ons & price
preference = {"Hot": 0, "Cold": 1.0}
sizes = {"Small": 0, "Medium": 0.5, "Large": 1.0}
addons = {"Extra Sugar": 0.25, "Extra Espresso": 1.00, "Extra Milk": 0.50, "Whipped Cream": 0.75}

# Sample inventory data with individual thresholds
initial_inventory = {
    'Matcha': 4,      # in packs
    'Chocolate': 5,    #in packs
    'Coffee Beans': 5,  # in packs
    'Milk': 7,          # in packs
    'Sugar': 5,          # in packs
    'Small Cups': 42,     # unit count
    'Medium Cups': 25,     # unit count
    'Large Cups': 20,     # unit count
    'Ice': 7,     # unit count(bags)
    'Whipped Cream': 4   # in bottle
}

# Threshold levels
threshold = {
    'Matcha': 2,
    'Chocolate': 2,
    'Coffee Beans': 2,   
    'Milk': 3,          
    'Sugar': 2,          
    'Small Cups': 40,     
    'Medium Cups': 40,     
    'Large Cups': 40,     
    'Ice': 3,
    'Whipped Cream': 1   
}

# Sample inventory cost data
product_costs = {
    'Matcha': 35.00,        # cost per pack in RM
    'Chocolate': 25.00,      # cost per pack in RM
    'Coffee Beans': 50.00,   # cost per pack in RM
    'Milk': 4.50,            # cost per pack in RM
    'Sugar': 2.00,           # cost per pack in RM
    'Small Cups': 0.50,      # cost per unit in RM
    'Medium Cups': 0.60,     # cost per unit in RM
    'Large Cups': 0.80,        # cost per unit in RM
    'Ice': 5.00,              # cost per bag in RM
    'Whipped Cream': 10.00   # cost per bottle in RM
}

ingredient_mapping = {
    'Matcha Latte': {'Matcha': 0.2, 'Coffee Beans': 0.1, 'Milk': 0.1},
    'Chocolate Latte': {'Chocolate': 0.2, 'Coffee Beans': 0.1, 'Milk': 0.1, 'Sugar': 0.1},
    'Americano': {'Coffee Beans': 0.2},
    'Cappuccino': {'Coffee Beans': 0.2, 'Milk': 0.1},
    'Latte': {'Coffee Beans': 0.2, 'Milk': 0.1}
}

addon_mapping = {
    'Extra Sugar': {'Sugar': 0.1},
    'Extra Espresso': {'Coffee Beans': 0.1},
    'Extra Milk': {'Milk': 0.1},
    'Whipped Cream': {'Whipped Cream': 0.1}
}



#-----------------------------User Pages-------------------------------
   
def about():
    st.image("about.jpg", use_column_width=True)
    st.markdown("<h1 style='text-align: center;'>KOPILALA</h1>", unsafe_allow_html=True)
    st.markdown("""
    ### Welcome to KOPILALA - More Than Just Coffee

    KOPILALA is more than just a place to grab a quick cup of coffee; its an experience. Founded with a passion for quality coffee, we create a space where coffee enthusiasts and casual drinkers alike can come together to savor something truly special. We believe that every cup of coffee tells a story—of the farmers who cultivate it, the process that refines it, and the people who enjoy it. At KOPILALA, we strive to tell that story with every sip.

    ---

    ### Our Story

    KOPILALA began with a simple vision: to craft a space where people feel a genuine connection—to coffee, to each other, and to the world around them. Inspired by both traditional coffee houses and modern café culture, we blend warmth, creativity, and a dedication to the art of coffee-making. 

    We source our beans from ethically grown farms around the globe, focusing on sustainability and fair-trade practices. With every cup, we aim to contribute to a better world, one coffee at a time.

    The name “KOPILALA” is derived from the Malay word "kopi," meaning coffee, and "lala," evoking a sense of relaxation and joy. Its a name that reflects the welcoming atmosphere we've created—a space where you can unwind, pause, and immerse yourself in life's simple pleasures. Whether you're meeting friends, working on a project, or simply taking a break, KOPILALA is designed to feel like home.

    ---

    ### Our Commitment

    At KOPILALA, we're passionate about three things: **quality**, **community**, and **sustainability**.

    - **Quality**: Our skilled baristas craft each cup with care, using high-quality beans and artisanal techniques to bring out the best in every roast. We believe that coffee isn't just about taste—it's about the experience. That's why our menu is both innovative and inclusive, offering options for every taste and dietary preference.

    - **Community**: We aim to build a community that values sustainability and positive impact. From our eco-friendly packaging to our partnerships with local suppliers, we're committed to reducing our environmental footprint and supporting the communities we serve. KOPILALA isn't just a coffee shop; it's a hub for like-minded people who care about the world their coffee comes from—and the difference they can make.

    - **Sustainability**: We're committed to making choices that have a lasting, positive impact. Whether it's the beans we source or the way we operate, sustainability is at the core of everything we do.

    ---

    ### Why KOPILALA?

    Because we believe that coffee should be more than just a drink—it should be an experience that uplifts, connects, and inspires. From the first aroma to the last sip, every moment at KOPILALA is crafted to be memorable. Whether you're a devoted coffee lover or a curious first-timer, we invite you to explore the world of coffee with us.

    Visit us at KOPILALA—where coffee and community come together. We can't wait to serve you!
    """)

def team():
    st.markdown("<h1 style='text-align: center;'>-- TEAM MEMBER -- </h1>", unsafe_allow_html=True)
    
    student = {
        "Name": ["Alexander Yoong Li Xhing", "Alif Putra Nazmi Bin Azmi", "Muhammad Haziq Fawwaz bin Muhammad Firdaus"],
        "ID": ["20000967", "20001496", "20001350"],
        "Course": ["IT", "IT", "IT"]
    }

    # Create DataFrame
    df = pd.DataFrame(student)
    
    # Reset the index (if needed) and remove the index column
    df = df.reset_index(drop=True)
    
    # Using st.dataframe() with style
    st.dataframe(df,hide_index=True, use_container_width=True)

def save_payment_to_excel(name, card, expiry, cvc):
    df = pd.DataFrame({
        "Name": [name],
        "Card Number": [card],
        "Expiry Date": [expiry],
        "CVC": [cvc]
    })
    filename = "order_data.xlsx"
    if os.path.exists(filename):
        existing_df = pd.read_excel(filename)
        df = pd.concat([existing_df, df], ignore_index=True)
    df.to_excel(filename, index=False)

def generate_invoice(total_price, order_details):
    """Function to generate an invoice PDF with a logo and formatted as a coffee shop receipt."""
    # Load and encode logo
    logo_path = "logo.png"  # Update with your logo path
    with open(logo_path, "rb") as image_file:
        logo_base64 = base64.b64encode(image_file.read()).decode()

    pdf = FPDF()
    pdf.add_page()

    # Add Logo at the top center
    pdf.set_xy(10, 10)
    pdf.image(logo_path, x=85, w=40)  # Adjust 'x' for centering and 'w' for width as needed

    # Coffee shop name and tagline
    pdf.set_font("Arial", "B", size=16)
    pdf.cell(200, 10, txt="KOPI LALA COFFEE SHOP", ln=True, align='C')
    pdf.set_font("Arial", "I", size=12)
    pdf.cell(200, 10, txt="Where Every Cup is Crafted with Love", ln=True, align='C')

    pdf.ln(10)  # Add some space

    # Date and Order Number
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d')}", ln=True, align='R')
    pdf.cell(200, 10, txt="Order Details", ln=True, align='L')
    pdf.ln(5)

    # Table Header
    pdf.set_font("Arial", "B", size=10)
    pdf.cell(20, 10, "Qty", border=1)
    pdf.cell(60, 10, "Item", border=1)
    pdf.cell(30, 10, "Size", border=1)
    pdf.cell(50, 10, "Add-ons", border=1)
    pdf.cell(30, 10, "Price (RM)", border=1, ln=True)

    # Order Details
    pdf.set_font("Arial", size=10)
    for order in order_details:
        addons = ', '.join(order['addons']) if order['addons'] else "None"
        
        # Calculate maximum row height based on content
        line_height = pdf.font_size * 1.5
        addons_lines = pdf.get_string_width(addons) / 50  # Divide by width of Add-ons cell to estimate lines
        max_height = max(line_height, line_height * (addons_lines // 1 + 1))  # Ensure height for all content

        # Print the first three cells in the row (Qty, Item, Size)
        pdf.cell(20, max_height, str(order['quantity']), border=1)
        pdf.cell(60, max_height, f"{order['coffee']} ({order['preference']})", border=1)
        pdf.cell(30, max_height, order['size'], border=1)
        
        # Save current position for Add-ons multi-cell handling
        x, y = pdf.get_x(), pdf.get_y()
        pdf.multi_cell(50, line_height, addons, border=1)
        
        # Ensure alignment of the rest of the row after multi-cell
        pdf.set_xy(x + 50, y)  # Move to the start of the Price column
        pdf.cell(30, max_height, f"{order['price']:.2f}", border=1, ln=True)

    # Total
    pdf.ln(10)
    pdf.set_font("Arial", "B", size=12)
    pdf.cell(200, 10, txt=f"Total Price: RM{total_price:.2f}", ln=True, align='R')

    # Save PDF
    invoice_path = f'invoice_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
    pdf.output(invoice_path)

    # Download link for the invoice
    with open(invoice_path, "rb") as f:
        st.download_button(
            label="Download Invoice",
            data=f,
            file_name=invoice_path,
            mime='application/pdf'
        )   
    
def save_order_to_excel(name, total_price, order_details, booking_number):
    """Save the order to an Excel file."""
    df = pd.DataFrame({
        "Name": [name],
        "Order ID": [booking_number],
        "Total Price": [total_price],
        "Order Details": [str(order_details)],  # Convert order details to string for storage
        "Date": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "Status": ["Processing"]
    })
    filename = "order_history.xlsx"
    
    # If the file exists, load the existing data and append the new order
    if os.path.exists(filename):
        existing_df = pd.read_excel(filename)
        df = pd.concat([existing_df, df], ignore_index=True)
    
    # Save the updated order history to Excel
    df.to_excel(filename, index=False)

def menu_page():
    st.write("---")
    st.markdown("<h1 style='text-align: center;'> -- MENU --</h1>", unsafe_allow_html=True)
    st.write("---")
    for coffee, price in menu.items():
        st.write(f"**{coffee}**: RM{price:.2f}")
        st.caption(description.get(coffee))
        col1, col2 = st.columns(2)
        with col1:
            st.image(menu_images_1.get(coffee), use_column_width=True)
        with col2:
            st.image(menu_images_2.get(coffee), use_column_width=True)
        st.write("---")
   
def customer_order():
    st.markdown("<h1 style='text-align: center;'> -- PLACE YOUR ORDER --</h1>", unsafe_allow_html=True)
    st.write("---")
    selected_coffee = st.selectbox("Choose your coffee", list(menu.keys()))
    selected_quantity = st.number_input("Select quantity", min_value=1, max_value=20, value=1)
    selected_preference = st.selectbox("Choose your preference", list(preference.keys()))
    selected_size = st.selectbox("Choose size", list(sizes.keys()))
    selected_addons = st.multiselect("Choose add-ons", list(addons.keys()))
    base_price = menu[selected_coffee]
    preference_price = preference[selected_preference]
    size_price = sizes[selected_size]
    addons_price = sum([addons[addon] for addon in selected_addons])
    price = base_price + preference_price + size_price + addons_price
    total_price = price * selected_quantity
    st.write(f"Total Price: RM{price:.2f}")

    if st.button("Add to Cart"):
        st.session_state.order_list.append({
            "coffee": selected_coffee,
            "preference": selected_preference,
            "size": selected_size,
            "addons": selected_addons,
            "quantity": selected_quantity,
            "price": total_price
        })
        st.success(f"{selected_coffee} added to your order!")

    if st.session_state.order_list:
        st.subheader("Your Current Order")
        for idx, order in enumerate(st.session_state.order_list):
            st.write(f"**Coffee {idx + 1}:** {order['quantity']}x {order['coffee']} ({order['preference']}), {order['size']}, Add-ons: {', '.join(order['addons'])}, Price: RM{order['price']:.2f}")

        #Voucher code input section
        voucher = st.text_input("Enter Voucher Code:")
        discount = 0.0
        if voucher in voucher_codes:
            discount = voucher_codes[voucher]
            st.success(f"Voucher code applied! Discount: {int(discount * 100)}%")
        else:
            if voucher:
                st.error("Invalid voucher code.")

        total_order_price = sum([order['price'] for order in st.session_state.order_list])
        discounted_price = total_order_price * (1 - discount)
        st.write(f"Total Order Price: RM{total_order_price:.2f}")
        st.write(f"Discounted Price: RM{discounted_price:.2f}")

        if st.button("Place Full Order"):
            st.session_state['total_order_price'] = discounted_price
            st.session_state['order_details'] = st.session_state.order_list.copy()
            st.session_state.order_list = []
            st.session_state['show_payment_page'] = True
            st.session_state['page'] = 'payment'
            st.rerun()

def payment_page(): 
    if 'show_payment_page' in st.session_state and st.session_state['show_payment_page']:
        # Back button at the top left
        back_clicked = st.button("⬅ Back", key="back_button")
        if back_clicked:
            st.session_state['page'] = 'menu'  # Navigate to the menu page
            st.rerun()
            return  # Exit the function after navigating back

        st.markdown("<h1 style='text-align: center;'> -- PAYMENT --</h1>", unsafe_allow_html=True)
        st.write("---")

        # Payment input fields
        payment_name = st.text_input("Name on Card")
        payment_card = st.text_input("Card Number", type="password", max_chars=16)
        payment_expiry = st.text_input("Expiry Date (MM/YY)", max_chars=5, help="Format: MM/YY")
        payment_cvc = st.text_input("CVC", type="password", max_chars=3)

        # Retrieve total price and order details from session state
        total_price = st.session_state.get('total_order_price', 0)
        order_details = st.session_state.get('order_details', [])

        # "Submit Payment" button
        if st.button("Submit Payment"):
            if payment_name and payment_card and payment_expiry and payment_cvc:
                # Validate card number
                if len(payment_card) != 16 or not payment_card.isdigit():
                    st.error("Card number must be exactly 16 digits.")
                # Validate CVC
                elif len(payment_cvc) != 3 or not payment_cvc.isdigit():
                    st.error("CVC must be exactly 3 digits.")
                # Validate expiry date format
                elif len(payment_expiry) != 5 or payment_expiry[2] != '/' or not (payment_expiry[:2].isdigit() and payment_expiry[3:].isdigit()):
                    st.error("Expiry date must be in MM/YY format, e.g., 10/24.")
                else:
                    # Generate booking number and preparation time
                    booking_number = f"{random.randint(1000, 9999)}-{int(time.time())}"
                    prep_time = random.randint(5, 15)  # Preparation time (e.g., 5 to 15 minutes)

                    # Process payment and save details
                    save_payment_to_excel(payment_name, payment_card, payment_expiry, payment_cvc)
                    save_order_to_excel(st.session_state['username'], total_price, order_details, booking_number)
                    st.success("Payment successful! Your order is being processed.")

                    # Add order to order history
                    st.session_state['order_history'].append({
                        "booking_number": booking_number,
                        "total_price": total_price,
                        "order_list": order_details,
                        "prep_time": prep_time,
                        "order_timestamp": time.time()
                    })

                    # Generate and provide invoice
                    generate_invoice(total_price, order_details)

                    # Reset order details in session state
                    st.session_state['show_payment_page'] = False
                    st.session_state['order_details'] = []
                    st.session_state['total_order_price'] = 0

                    # Redirect to history or another page after payment
                    st.session_state['page'] = 'menu'
            else:
                st.error("Please complete all payment fields.")
    else:
        # If it's not the payment page, display an error message
        st.warning("Page not found.")

def load_order_history(username):
    """Load the order history for the logged-in user."""
    filename = "order_history.xlsx"
    
    if os.path.exists(filename):
        df = pd.read_excel(filename)
        
        # Filter orders by the username
        user_orders = df[df['Name'] == username]
        return user_orders
    else:
        return pd.DataFrame()  # Return an empty DataFrame if no history exists

def order_history():
    st.markdown("<h1 style='text-align: center;'> -- ORDER HISTORY -- </h1>", unsafe_allow_html=True)
    st.write('---')

    # Load orders for the logged-in user
    filename = "order_history.xlsx"
    if os.path.exists(filename):
        df = pd.read_excel(filename)
        
        # Filter orders by the username
        user_orders = df[df['Name'] == st.session_state['username']]

        if not user_orders.empty:
            for i, order in user_orders.iterrows():
                st.markdown(f"<h4>Order ID ---- {order['Order ID']} ---- {order['Date']} ", unsafe_allow_html=True)
                st.write(f"**Total Price ---** RM{order['Total Price']:.2f}")
                order_details = eval(order['Order Details'])  # Convert string back to list of dicts
                for detail in order_details:
                    st.write(f"{detail['coffee']} **---** {detail['preference']} **---** {', '.join(detail['addons']) if detail['addons'] else 'None'} **---** {detail['size']} **---** {detail['quantity']} **-------------------** RM{detail['price']:.2f}")
                if order['Status'] == 'Completed':
                    st.success(f"Your order is ready for pickup! Enjoy Your Drink!!!")
                elif order['Status'] == 'Cancelled':
                    st.error(f"Your order has been cancelled. We are deeply sorry for this matter")
                else:
                    st.warning(f"Your order is still being processed. Do be patient for the best coffee in the town!")

                st.write("---")
        else:
            st.write("No order history available.")
    else:
        st.write("No order history found.")

def customer_feedback():
    st.markdown("<h1 style='text-align: center;'> -- CUSTOMER FEEDBACK --</h1>", unsafe_allow_html=True)
    st.write("---")

    coffee_rating = st.slider("Rate your coffee (1-5)", 1, 5)
    service_rating = st.slider("Rate our service (1-5)", 1, 5)
    feedback_comments = st.text_area("Additional Comments")

    if st.button("Submit Feedback"):
        # Check if feedback_comments is not empty
        if feedback_comments.strip():  # Ensure it's not just whitespace
            feedback_entry = {
                "coffee_rating": coffee_rating,
                "service_rating": service_rating,
                "comments": feedback_comments,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            # Append the feedback entry to session state
            st.session_state.feedback_list.append(feedback_entry)
            st.success("Thank you for your feedback!")

            # Save the updated feedback list to an Excel file
            df = pd.DataFrame(st.session_state.feedback_list)
            df.to_excel("customer_feedback.xlsx", index=False)
        else:
            st.error("Feedback comments cannot be empty.")
    
def user_page():
    
    if 'order_list' not in st.session_state:
        st.session_state.order_list = []
    if 'order_history' not in st.session_state:
        st.session_state.order_history = []

    # Add your logo to the sidebar with HTML for centering
    logo_path = "logo.png"  # Update with the path to your logo image

    # Center the logo using HTML
    st.sidebar.markdown(
        f"""
        <div style="text-align: center;">
            <img src="data:image/png;base64,{base64.b64encode(open(logo_path, 'rb').read()).decode()}" width="100">
        </div>
        """,
        unsafe_allow_html=True)

    page = st.sidebar.selectbox("Go to", ["Menu", "Order", "Order History & Pickup Notification", "Customer Feedback","About Us", "Team"], index=0)

    if st.sidebar.button("Logout"):
        logout()
        st.rerun()

    if page == "Menu":
        menu_page()
    elif page == "Order":
        customer_order()
    elif page == "Order History & Pickup Notification":
        order_history()
    elif page == "About Us":
        about()
    elif page == "Team":
        team()
    elif page == "Customer Feedback":
        customer_feedback()



#------------------------------------Admin Pages------------------------------

def handle_order():
    st.markdown("<h1 style='text-align: center;'> -- CURRENT ORDERS --</h1>", unsafe_allow_html=True)
    st.write("---")
    filename = "order_history.xlsx"

    # Check if the file exists and load the dataframe into session state
    if filename not in st.session_state:
        if os.path.exists(filename):
            df = pd.read_excel(filename)
            st.session_state.df = df
        else:
            st.write("No orders found.")
            st.stop()  # Stops execution if the file doesn't exist

    # Retrieve the dataframe from session state
    df = st.session_state.df

    # Filter orders with 'Processing' status
    processing_orders = df[df['Status'] == 'Processing']

    # Display orders to admin
    for idx, order in processing_orders.iterrows():
        st.markdown(f"### Order {order['Name']} - {order['Date']}")
        st.write(f"**Total Price:** RM{order['Total Price']:.2f}")
        
        order_details = eval(order['Order Details'])  # Convert string representation of list/dict back to a list of dicts
        for detail in order_details:
            st.write(f"{detail['coffee']} **---** {detail['preference']} **---** {', '.join(detail['addons']) if detail['addons'] else 'None'} **---** {detail['size']} **---** {detail['quantity']} **-------------------** RM{detail['price']:.2f}")
        
        # Buttons to process the order
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"Mark as Completed", key=f"complete_{idx}"):
                # Update status to 'Completed'
                df.at[idx, 'Status'] = 'Completed'
                reduce_inventory(order_details)
                # Save the updated dataframe in session state
                st.session_state.df = df
                # Save changes to the Excel file
                df.to_excel(filename, index=False)
                st.success(f"Order {order['Name']} marked as completed!")
                st.rerun()

        with col2:
            if st.button(f"Mark as Cancelled", key=f"cancel_{idx}"):
                # Update status to 'Cancelled'
                df.at[idx, 'Status'] = 'Cancelled'
                # Save the updated dataframe in session state
                st.session_state.df = df
                # Save changes to the Excel file
                df.to_excel(filename, index=False)
                st.error(f"Order {order['Name']} marked as cancelled!")
                st.rerun()

    # If there are no 'Processing' orders, display a message
    if len(processing_orders) == 0:
        st.write("No processing orders found.")


def load_order_data():
    return pd.read_excel('order_history.xlsx')

# Inventory management function
def inventorymanagement():
    if 'inventory' not in st.session_state:
        st.session_state.inventory = initial_inventory.copy()

    if 'threshold' not in st.session_state:
        st.session_state.threshold = threshold

    # Display inventory
    st.subheader("Inventory Monitoring")
    display_inventory()

    # Alert for low stock items
    st.subheader("Low Inventory Alerts")
    display_low_inventory_alerts()

    st.subheader("Suggested Restock List")
    display_restock_list()

    # Manual Inventory Stocking
    st.subheader("Manual Inventory Stocking")
    restock_amounts = {item: st.number_input(f"{item} Restock Amount", min_value=0, max_value=1000, step=1, key=item) for item in st.session_state.inventory.keys()}

    # Restock Button
    if st.button("Restock Inventory"):
        for item, amount in restock_amounts.items():
            st.session_state.inventory[item] += amount
        st.success("Inventory restocked successfully!")
        st.rerun()  # Refresh page to update tables

# Display inventory table
def display_inventory():
    inventory_df = pd.DataFrame({
        "Product": list(st.session_state.inventory.keys()),
        "Current Quantity": list(st.session_state.inventory.values()),
        "Threshold": [st.session_state.threshold[item] for item in st.session_state.inventory.keys()]
    })
    # Reset the index (if needed) and remove the index column
    inventory_df = inventory_df.reset_index(drop=True)
    
    # Using st.dataframe() with style
    st.dataframe(inventory_df,hide_index=True)

# Low inventory alert function
def display_low_inventory_alerts():
    for item, stock in st.session_state.inventory.items():
        if stock < st.session_state.threshold[item]:
            st.warning(f"{item} is below threshold ({stock} units). Please restock!")

def reduce_inventory(order_details):
    for item in order_details:
        coffee = item['coffee']
        quantity = item['quantity']
        size = item['size'].lower()  # Converting size to lowercase for easier matching
        preference = item['preference'].lower()  # Converting preference to lowercase
        addons = item['addons']

        # Reduce coffee ingredients based on coffee type
        if coffee in ingredient_mapping:
            for ingredient, amount_per_unit in ingredient_mapping[coffee].items():
                st.session_state.inventory[ingredient] -= amount_per_unit * quantity
                st.session_state.inventory[ingredient] = max(0, st.session_state.inventory[ingredient])

        # Reduce cup inventory based on the size of the drink
        cup_key = f"{size.capitalize()} Cups"  # Match keys like "Small Cups", "Medium Cups", etc.
        if cup_key in st.session_state.inventory:
            st.session_state.inventory[cup_key] -= quantity
            st.session_state.inventory[cup_key] = max(0, st.session_state.inventory[cup_key])

        # Reduce inventory for any add-ons
        for addon in addons:
            if addon in addon_mapping:
                for ingredient, amount_per_addon in addon_mapping[addon].items():
                    st.session_state.inventory[ingredient] -= amount_per_addon * quantity
                    st.session_state.inventory[ingredient] = max(0, st.session_state.inventory[ingredient])

        # Reduce ice inventory if the preference is "cold"
        if preference == "cold" and 'Ice' in st.session_state.inventory:
            st.session_state.inventory['Ice'] -= 0.1 * quantity  # Adjust ice amount per drink as needed
            st.session_state.inventory['Ice'] = max(0, st.session_state.inventory['Ice'])

# Display Auto-Generated Restock List
def display_restock_list():
    restock_list_data = [
        {"Product": item, "Quantity to Restock": int(st.session_state.threshold[item] - st.session_state.inventory[item])}
        for item in st.session_state.inventory.keys() if st.session_state.inventory[item] < st.session_state.threshold[item]
    ]
    if restock_list_data:
        restock_list_df = pd.DataFrame(restock_list_data)
        restock_list_df = restock_list_df.reset_index(drop=True)
        # Using st.dataframe() with style
        st.dataframe(restock_list_df,hide_index=True)
    else:
        st.write("All items are sufficiently stocked.")

# Load and prepare the sales data
def loadorderhistory_admin():
    df = pd.read_excel("order_history.xlsx")
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')  # Convert to datetime
    df['Total Price'] = df['Total Price'].astype(float)  # Ensure prices are floats
    return df

# Initialize sales data
sales_df = loadorderhistory_admin()

# Function to extract coffee names from order details
def get_coffee_names(order_details):
    try:
        order_list = ast.literal_eval(order_details)
        coffee_names = [item['coffee'] for item in order_list if isinstance(item, dict) and 'coffee' in item]
        return coffee_names
    except (ValueError, SyntaxError):
        return []

def salesreport(sales_df):
    st.markdown("<h1 style='text-align: center;'> -- SALES REPORT --</h1>", unsafe_allow_html=True)
    st.write("---")

    # Select report type
    st.subheader("Select Report Type")
    report_type = st.selectbox("Display by", ["Daily", "Weekly", "Monthly"])

    st.subheader("Display Format")
    display_format = st.radio("Choose display format", ["Table", "Chart"])

    # Extract only the date part for daily reports
    sales_df['DateOnly'] = sales_df['Date'].dt.date

    # Group data based on report type
    if report_type == "Daily":
        grouped_sales = sales_df.groupby('DateOnly').agg({'Total Price': 'sum'}).reset_index()
        grouped_sales = grouped_sales.rename(columns={'DateOnly': 'Date'})  # Rename column to "Date"
        grouped_sales = grouped_sales.rename(columns={'Total Price': 'Total Sales'})  # Rename column to "Total Sales"
    elif report_type == "Weekly":
        grouped_sales = sales_df.resample('W-Mon', on='Date').agg({'Total Price': 'sum'}).reset_index()
        grouped_sales['Date'] = grouped_sales['Date'].dt.date  # Remove time component for weekly
        grouped_sales = grouped_sales.rename(columns={'Total Price': 'Total Sales'})  # Rename column to "Total Sales"
    else:
        grouped_sales = sales_df.resample('M', on='Date').agg({'Total Price': 'sum'}).reset_index()
        grouped_sales['Date'] = grouped_sales['Date'].dt.date  # Remove time component for monthly
        grouped_sales = grouped_sales.rename(columns={'Total Price': 'Total Sales'})  # Rename column to "Total Sales"

    # Display the selected format
    st.subheader(f"{report_type} Sales Report")
    if display_format == "Table":
        grouped_sales= grouped_sales.reset_index(drop=True)
        # Using st.dataframe() with style
        st.dataframe(grouped_sales,hide_index=True)
    elif not grouped_sales.empty:
        st.line_chart(grouped_sales.set_index('Date')['Total Sales'])
    else:
        st.write("No data available for the selected period.")

    # Extract coffee names from Order Details and filter out invalid entries
    sales_df['Coffee Names'] = sales_df['Order Details'].apply(get_coffee_names)

    # Expand to handle each coffee item individually, removing invalid entries
    valid_coffee_sales = sales_df.explode('Coffee Names').dropna(subset=['Coffee Names'])

    # Calculate counts for each coffee type and filter out extraneous data
    coffee_counts = valid_coffee_sales['Coffee Names'].value_counts().reset_index()
    coffee_counts.columns = ['coffee_type', 'Total Sales']
    coffee_counts = coffee_counts[coffee_counts['coffee_type'].isin(valid_coffee_sales['Coffee Names'].unique())]

    # Plot Best and Worst Sellers
    st.subheader("Best and Worst Sellers")
    if not coffee_counts.empty:
        chart = alt.Chart(coffee_counts).mark_bar().encode(
            x='Total Sales',
            y=alt.Y('coffee_type', sort='-x'),
            color=alt.Color('coffee_type', legend=None)
        ).properties(width=600, height=300)
        st.altair_chart(chart, use_container_width=True)
    else:
        st.write("No coffee sales data available.")

    # Best and worst sellers
    if not coffee_counts.empty:
        best_seller = coffee_counts.loc[coffee_counts['Total Sales'].idxmax(), 'coffee_type']
        worst_seller = coffee_counts.loc[coffee_counts['Total Sales'].idxmin(), 'coffee_type']
    else:
        best_seller = "No data available"
        worst_seller = "No data available"

    st.write(f"Best Seller: {best_seller}")
    st.write(f"Worst Seller: {worst_seller}")

    # Calculate total cost by multiplying each product's price with quantity in session state inventory
    total_cost = sum(product_costs[product] * quantity for product, quantity in st.session_state.inventory.items())

    # Total sales and profit calculation
    total_sales = grouped_sales['Total Sales'].sum()
    total_profit = total_sales - total_cost

    st.write(f"Total Sales: RM{total_sales:.2f}")
    st.write(f"Total Costs: RM{total_cost:.2f}")
    st.write(f"Total Profit: RM{total_profit:.2f}")

  
    # Initialize FPDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Logo positioning (centered at the top)
    logo_width = 35  # Adjust the width of the logo
    pdf.image("logo.png", x=(220 - logo_width) / 2, y=10, w=logo_width)  # Centered horizontally

    # Set title and styles
    pdf.set_font('Arial', 'B', 16)
    pdf.ln(40)  # Add some space below the logo
    pdf.cell(200, 10, txt="Sales Report - " + report_type, ln=True, align='C')

    # Add total profit
    pdf.ln(10)  # Line break
    pdf.set_font('Arial', '', 12)
    pdf.cell(200, 10, txt=f"Total Profit: RM{total_profit:.2f}", ln=True, align='C')


    # Add sales data table (centered)
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)

    # Define column widths
    col_widths = [80, 40]  # Adjust widths as necessary for 'Date' and 'Total Price'

    # Calculate the start x position to center the table
    table_width = sum(col_widths)
    start_x = (210 - table_width) / 2  # Center the table horizontally

    # Table headers
    pdf.set_x(start_x)
    pdf.cell(col_widths[0], 10, 'Date', border=1, align='C')
    pdf.cell(col_widths[1], 10, 'Total Sales', border=1, align='C')
    pdf.ln()

    # Table rows
    pdf.set_font('Arial', '', 12)
    for index, row in grouped_sales.iterrows():
        pdf.set_x(start_x)  # Reset x position for each row to keep it centered
        pdf.cell(col_widths[0], 10, str(row['Date']), border=1, align='C')
        pdf.cell(col_widths[1], 10, f"RM {row['Total Sales']:.2f}", border=1, align='C')
        pdf.ln()

    # Add Best and Worst Sellers
    pdf.ln(10)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(200, 10, txt="Best and Worst Sellers", ln=True, align='C')

    pdf.set_font('Arial', '', 12)
    pdf.cell(200, 10, txt=f"Best Seller: {best_seller}", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Worst Seller: {worst_seller}", ln=True, align='C')


    # Add report generation date
    report_date = datetime.now().strftime("%B %d, %Y")  # Format date as "Month Day, Year"
    pdf.ln(10)  # Line break
    pdf.cell(200, 10, txt=f"Report Generated On: {report_date}", ln=True, align='C')

    # Output the PDF and allow the user to download it
    pdf_output = pdf.output(dest='S')

    # Display the download button
    st.download_button(label="Download PDF", data=pdf_output, file_name="sales_report.pdf", mime="application/pdf")

def analytics_dashboard():
    st.markdown("<h1 style='text-align: center;'> -- ANALYTICS DASHBOARD --</h1>", unsafe_allow_html=True)
    st.write("---")

    # Calculate total orders and sales based on loaded sales data
    total_orders = len(sales_df)
    total_sales = sales_df['Total Price'].sum()  # Assuming Total Price is the revenue per order

    # Displaying total orders, total sales, and inventory items
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Orders", total_orders)
    col2.metric("Total Sales", f"RM{total_sales:.2f}")
    col3.metric("Inventory Items", len(st.session_state.inventory))

    # Real-Time Inventory Monitoring
    st.subheader("Real-Time Inventory Monitoring")

    # Create a DataFrame for inventory and thresholds
    inventory_df = pd.DataFrame({
        "Product": list(st.session_state.inventory.keys()),
        "Stock Level": list(st.session_state.inventory.values()),
        "Threshold Level": [st.session_state.threshold[item] for item in st.session_state.inventory.keys()]
    })

    # Inventory bar chart with threshold line
    bars = alt.Chart(inventory_df).mark_bar().encode(
        x=alt.X("Product", sort="-y"),
        y="Stock Level",
        color=alt.Color("Product", legend=None)
    )
    threshold_line = alt.Chart(inventory_df).mark_rule(color="red").encode(
        x="Product",
        y="Threshold Level", 
        tooltip=["Product", "Threshold Level"]
    )
    chart = (bars + threshold_line).properties(width=700, height=400)
    st.altair_chart(chart, use_container_width=True)

    # Inventory Health Check Section
    st.subheader("Inventory Health Check")
    with st.container():
    # Check for low inventory items in st.session_state.inventory
        low_inventory_items = {
            item: stock for item, stock in st.session_state.inventory.items()
            if stock < st.session_state.threshold[item]
        }

        # Display warnings for low inventory items
        if low_inventory_items:
            for item, stock in low_inventory_items.items():
                st.warning(f"{item} is running low ({stock} in stock). Restock recommended.")
        else:
            st.write("All items are sufficiently stocked.")

# Function to load customer feedback from the Excel file
def load_customer_feedback():
    # Load the Excel file
    feedback_df = pd.read_excel("customer_feedback.xlsx")
    
    # Rename columns to desired names
    feedback_df = feedback_df.rename(columns={
        'coffee_rating': 'Coffee Rating',
        'service_rating': 'Service Rating',
        'comments': 'Comments',
        'timestamp': 'Date'
    })

    # Convert 'Date' column to datetime format
    feedback_df['Date'] = pd.to_datetime(feedback_df['Date'], errors='coerce')
    
    return feedback_df

# Customer Feedback Page
def customer_feedback_admin():
    # Title for the page
    st.markdown("<h1 style='text-align: center;'> -- CUSTOMER FEEDBACK --</h1>", unsafe_allow_html=True)
    st.write("---")

    # Load the latest customer feedback data
    feedback_df = load_customer_feedback()

    # Show the table with the customer feedback data
    st.subheader("Customer Feedback Data")
    
    # Display the dataframe in Streamlit
    feedback_df= feedback_df.reset_index(drop=True)
    # Using st.dataframe() with style
    st.dataframe(feedback_df,hide_index=True)

    # Display bar charts for Coffee Rating and Service Rating
    st.subheader("Coffee Rating Distribution")
    
    # Count occurrences of each rating (1-5), ensuring all ratings are included
    coffee_rating_counts = feedback_df['Coffee Rating'].value_counts().reindex(range(1, 6), fill_value=0).reset_index()
    coffee_rating_counts.columns = ['Rating', 'Coffee Rating Count']
    
    coffee_rating_chart = alt.Chart(coffee_rating_counts).mark_bar().encode(
        x=alt.X('Rating:O', title='Rating', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('Coffee Rating Count:Q', title='Count of Ratings'),
        color='Rating:N'
    ).properties(width=600, height=400)
    
    st.altair_chart(coffee_rating_chart, use_container_width=True)

    st.subheader("Service Rating Distribution")
    
    # Count occurrences of each rating (1-5), ensuring all ratings are included
    service_rating_counts = feedback_df['Service Rating'].value_counts().reindex(range(1, 6), fill_value=0).reset_index()
    service_rating_counts.columns = ['Rating', 'Service Rating Count']
    
    service_rating_chart = alt.Chart(service_rating_counts).mark_bar().encode(
        x=alt.X('Rating:O', title='Rating', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('Service Rating Count:Q', title='Count of Ratings'),
        color='Rating:N'
    ).properties(width=600, height=400)
    
    st.altair_chart(service_rating_chart, use_container_width=True)

def admin_page():
    ####Side Button Configuration
    # Add your logo to the sidebar with HTML for centering
    logo_path = "logo.png"  # Update with the path to your logo image

    # Center the logo using HTML
    st.sidebar.markdown(
        f"""
        <div style="text-align: center;">
            <img src="data:image/png;base64,{base64.b64encode(open(logo_path, 'rb').read()).decode()}" width="100">
        </div>
        """, unsafe_allow_html=True
    )

    page = st.sidebar.selectbox("Go to", ["Handle Order", "Inventory Management", "Sales Report", "Analytics Dashboard", "Customer Feedback"], index=0)

    if st.sidebar.button("Logout"):
        logout()
        st.rerun()

    #Initialize inventory in session state if not set
    if 'inventory' not in st.session_state:
        st.session_state.inventory = initial_inventory.copy()

    if page == "Handle Order":
        handle_order()
    elif page == "Inventory Management":
        inventorymanagement()

    elif page == "Sales Report":
        salesreport(sales_df)

    elif page == "Analytics Dashboard":
        analytics_dashboard()

    elif page == "Customer Feedback":
        customer_feedback_admin()

#------------------------------------Global Pages-------------------------------
def login_page():
    
    # Load your image and encode it to base64
    image_path = "logo.png"  # Change this to your image path
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode()

    # Use st.markdown with HTML to center the image
    st.markdown(
        f"""
        <div style="text-align: center;">
            <img src="data:image/jpeg;base64,{encoded_image}" width="150">
        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown("<h1 style='text-align: center;'>WELCOME TO KOPILALA</h1>", unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login", key="login_button"):
        if authenticate(username, password):
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.session_state['page'] = 'menu'  # Redirect to the menu page
            st.success(f"Welcome, {username}!")
            st.rerun()
        else:
            st.error("Invalid username or password")
    st.write("___________________________________________________________________________")
    st.markdown("<h5 style='text-align: center;'>Havent Register?</h1>", unsafe_allow_html=True)
    st.caption("Join our community today—register now to unlock exclusive features and start your journey with us!")

    if st.button("Register", key="register_button"):
        # Navigate to registration page
        st.session_state['page'] = 'register'
        st.rerun()
        registration()        

def registration():
    back_clicked = st.button("⬅ Back", key="back_button")
    if back_clicked:
        st.session_state['page'] = 'login'  # Navigate to the login page
        st.rerun()
        return  # Exit the function after navigating back
    st.markdown("<h1 style='text-align: center;'> -- REGISTRATION --</h1>", unsafe_allow_html=True)
    st.write("---")

    # User input fields for username and password
    new_username = st.text_input("Choose a Username")
    new_password = st.text_input("Choose a Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if new_password != confirm_password:
            st.error("Passwords do not match.")
        elif register_user(new_username, new_password):
            st.success("Registration successful! You can now log in.")
            st.session_state['page'] = 'login' #go to login after register
            st.rerun()
        else:
            st.error("Username already exists. Please choose another one.")

def register_user(username, password):
    # Load the existing users from the Excel file
    users_df = load_users()
    
    # Check if username already exists
    if username in users_df['Username'].values:
        return False  # User already exists
    
    # Add the new user to the dataframe
    new_user = pd.DataFrame({"Username": [username], "Password": [password]})
    users_df = pd.concat([users_df, new_user], ignore_index=True)
    
    # Save the updated users data back to the Excel file
    users_df.to_excel("users.xlsx", index=False)
    
    return True

def load_users():
    if os.path.exists("users.xlsx"):
        users_df = pd.read_excel("users.xlsx")
    else:
        # If no file exists, create a new one
        users_df = pd.DataFrame(columns=["Username", "Password"])
        users_df.to_excel("users.xlsx", index=False)
    
    return users_df

def authenticate(username, password):
    try:
    # Load users data from the Excel file
        users_df = pd.read_excel("users.xlsx")

        # Check if the username exists in the dataframe
        user_row = users_df[users_df["Username"] == username]
        
        if not user_row.empty:
            # Compare the entered password with the stored password
            stored_password = user_row.iloc[0]["Password"]
            if stored_password == password:
                return True
        return False
    except Exception as e:
        st.error(f"Error loading users file: {e}")
        return False

def logout():
    st.session_state['logged_in'] = False
    st.session_state['username'] = ''
    st.session_state['page'] = 'login'
    st.success("You have logged out.")

def main():
    #Add session state to track user login
    #Initialize session state for pages and login
    if 'page' not in st.session_state:
        st.session_state['page'] = 'login'
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['username'] = ''
    if 'show_payment_page' not in st.session_state:
        st.session_state['show_payment_page'] = False
    if 'feedback_list' not in st.session_state:
        st.session_state['feedback_list'] = []

    # Render different pages based on the value of session state 'page'
    if st.session_state['page'] == 'login':
        login_page()
    elif st.session_state['page'] == 'order':
        customer_order()
    elif st.session_state['page'] == 'register':
        registration()
    elif st.session_state['page'] == 'payment':
        payment_page()
    elif st.session_state['page'] == 'history':
        order_history()
    elif st.session_state['page'] == 'about':
        about()
    elif st.session_state['page'] == 'team':
        team()
    elif st.session_state['page'] == 'menu' and st.session_state['logged_in']:
        #st.write("You are logged in! Go to the menu.")
        if st.session_state['username'] == 'admin':
            admin_page()
        else:
            user_page()
        
if __name__ == "__main__":
    main()
