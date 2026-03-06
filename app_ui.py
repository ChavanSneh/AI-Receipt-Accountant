import streamlit as st
import requests
import pandas as pd

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