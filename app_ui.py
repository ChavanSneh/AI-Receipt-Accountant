import streamlit as st
import requests
import pandas as pd
from database import get_all_items, delete_item, update_item

st.title("🛒 AI Receipt Accountant (Database-Synced)")

uploaded_file = st.file_uploader("Upload receipt...", type=["jpg", "png"])

if uploaded_file:
    st.image(uploaded_file, caption='Receipt', use_container_width=True)
    if st.button("Analyze Receipt"):
        with st.spinner("Processing..."):
            files = {"file": uploaded_file.getvalue()}
            response = requests.post("http://localhost:8000/upload", files=files)
            if response.status_code == 200:
                st.session_state.data = response.json()
                st.success("Analysis Complete!")

# --- UI FOR LEDGER (Syncs with Docker) ---
st.subheader("Manual Item Ledger")
col1, col2 = st.columns(2)
with col1:
    item_name = st.text_input("Item Name")
with col2:
    item_price = st.number_input("Price", min_value=0.0, format="%.2f")

# ADD ITEM
if st.button("Add to Ledger"):
    requests.post("http://localhost:8000/ledger/add", params={"name": item_name, "price": item_price})
    st.rerun() # Refresh to show new data

    # Fetch the list of items from your database
items = get_all_items()

# Loop through each individual item dictionary
for item in items:
    # Now 'item' is defined and has keys: 'id', 'name', 'price'
    st.write(f"Item: {item['name']} | Price: {item['price']}")
    
    # Now your buttons will work because 'item['id']' exists

# Assuming 'item' is an object from your database (id, name, price)
with st.expander(f"{item['name']} - {item['price']}"):
    
# --- DELETE SECTION ---
# We use a button that triggers a confirmation
 if st.button("Delete this item", key=f"del_{item['id']}"):
        st.warning(f"Are you sure you want to delete {item['name']}?")
        col1, col2 = st.columns(2)
if col1.button("Yes", key=f"yes_del_{item['id']}"):
            delete_item(item['id']) # Call your database function
            st.rerun()
if col2.button("No", key=f"no_del_{item['id']}"):
            st.info("Delete cancelled.")
            
    # --- EDIT SECTION ---
if st.button("Edit this item", key=f"edit_{item['id']}"):
        # Open a form to get new data
        with st.form(key=f"form_{item['id']}"):
            new_name = st.text_input("New Name", value=item['name'])
            new_price = st.number_input("New Price", value=item['price'])
            submit = st.form_submit_button("Confirm Edit?")
            
if submit:
                update_item(item['id'], new_name, new_price)
                st.rerun()

# FETCH AND DISPLAY DATA
response = requests.get("http://localhost:8000/ledger")
if response.status_code == 200:
    ledger_data = response.json().get("items", [])
    
    if ledger_data:
        df = pd.DataFrame(ledger_data)
        st.table(df)
        
        total_sum = sum(item['price'] for item in ledger_data)
        st.metric("Total Ledger Balance", f"${total_sum:.2f}")
        
        # DOWNLOAD
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download CSV", csv_data, 'ledger.csv', 'text/csv')

    # CLEAR
    if st.button("Clear Ledger"):
        requests.post("http://localhost:8000/ledger/clear")
        st.rerun()