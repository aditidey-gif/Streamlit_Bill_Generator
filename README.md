<img width="450" height="604" alt="image" src="https://github.com/user-attachments/assets/880b762c-2533-4c2f-89d3-6fc1e233ad8e" />
<img width="376" height="429" alt="image" src="https://github.com/user-attachments/assets/3221ab26-06a1-4f14-9563-d3c795940d1d" />



# Streamlit_Bill_Generator

A simple yet effective web application built with Streamlit and Python to generate professional-looking bills and invoices. This tool is designed to be easy to use, allowing for quick creation of bills with automatic calculations and a clean, readable format.

✨**FEATURES**✨

**User-Friendly Interface:** A clear and intuitive Streamlit app layout for entering customer and product details.

**Dynamic Product Listing:** Add multiple products with quantities and unit amounts to build a comprehensive bill.

**Automatic Calculations:** Calculates the total amount for each product and the grand total for the entire bill.

**Indian Currency Conversion:** The total amount is automatically converted into words, following the Indian numbering system (Lakhs and Crores).

**Bill Preview:** See a real-time preview of the bill before generating the final document.

**Downloadable Bills:** Generate and download the bill as a .txt file for easy sharing or printing.



🚀 **HOW TO RUN**🚀

**Clone the repository:**
https://github.com/aditidey-gif/Streamlit_Bill_Generator/blob/main/Bill.py

**Install the required libraries:**
pip install streamlit

**Run the App: Open your terminal and type this command:**
streamlit run Bill.py



📖 **CODE STRUCTURE**📖

**convert_amount_to_words(number):** A helper function that converts a numerical value into words, specifically for the Indian currency system.

**generate_bill_content(shop_details, customer_details, products):** This function formats all the bill data into a clean, well-aligned string ready for display and download.

**Streamlit UI:** The main part of the script that handles the user interface, including input fields, forms, and the final bill display using st.title, st.header, st.columns, and st.button.

**Session State:** The app uses st.session_state to store and manage the list of products added by the user.



🤝 **CONTRIBUTION**🤝

Contributions, issues, and feature requests are welcome! Feel free to open a pull request or submit an issue on this repository.



📜 **LICENSE**📜

This project is licensed under the MIT License.
