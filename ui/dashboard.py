import streamlit as st
import requests
import pandas as pd

BACKEND_URL = "http://localhost:8000"

st.set_page_config(layout="wide")
st.title("💰 AI Receipt Ledger")

if "selected_ids" not in st.session_state:
    st.session_state.selected_ids = []

if "suggested" not in st.session_state:
    st.session_state.suggested = []

left, right = st.columns(2)

# ---------------- LEFT SIDE ----------------
with left:

    st.subheader("Process Receipt")

    uploaded_file = st.file_uploader("Upload Image", type=["jpg","png"])

    if st.button("Process") and uploaded_file:

        try:
            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type
                )
            }

            res = requests.post(f"{BACKEND_URL}/upload", files=files)

            st.session_state.suggested = res.json().get("suggested_items", [])

        except:
            st.error("Backend not reachable")

    if st.session_state.suggested:

        st.subheader("AI Suggestions")

        for item in st.session_state.suggested:

            name = item["name"]
            price = item["price"]

            if st.button(f"Add {name}"):

                requests.post(
                    f"{BACKEND_URL}/ledger/add",
                    json={"name": name, "price": price}
                )

                st.success(f"{name} added")
                st.rerun()

    # -------- Manual Add --------
    st.divider()
    st.subheader("Manual Add Item")

    m_name = st.text_input("Item name")
    m_price = st.number_input("Price", min_value=0.0, step=0.1)

    if st.button("Add Manually"):

        if m_name.strip() == "":
            st.warning("Item name required")
        else:

            requests.post(
                f"{BACKEND_URL}/ledger/add",
                json={"name": m_name, "price": m_price}
            )

            st.success("Item added")
            st.rerun()


# ---------------- RIGHT SIDE ----------------
with right:

    st.subheader("Manage Ledger")

    try:
        items = requests.get(f"{BACKEND_URL}/ledger").json().get("items", [])
    except:
        items = []
        st.error("Cannot connect to backend")

    # -------- Ledger Stats --------
    if items:

        total_spent = sum(item["price"] for item in items)
        item_count = len(items)
        most_expensive = max(items, key=lambda x: x["price"])

        stat1, stat2, stat3 = st.columns(3)

        stat1.metric("Total Spent", f"${total_spent:.2f}")
        stat2.metric("Items", item_count)
        stat3.metric(
            "Most Expensive",
            most_expensive["name"],
            f"${most_expensive['price']:.2f}"
        )

    st.divider()

    colA, colB, colC = st.columns(3)

    # Delete selected
    if colA.button("🗑 Delete Selected"):

        for sid in st.session_state.selected_ids:
            requests.delete(f"{BACKEND_URL}/ledger/delete/{sid}")

        st.session_state.selected_ids = []

        st.rerun()

    # Clear ledger
    if colB.button("Clear Ledger"):

        requests.delete(f"{BACKEND_URL}/ledger/clear")

        st.session_state.selected_ids = []

        st.rerun()

    # CSV Download
    if items:
        df = pd.DataFrame(items)

        if "id" in df.columns:
            df = df.drop(columns=["id"])

        csv = df.to_csv(index=False).encode("utf-8")

        colC.download_button(
            "Download CSV",
            csv,
            "ledger.csv",
            "text/csv"
        )

    st.divider()

    # -------- Ledger Items --------
    for item in items:

        iid = item["id"]

        col1, col2, col3, col4 = st.columns([0.5,3,1,1])

        selected = col1.checkbox("", key=f"check_{iid}")

        if selected and iid not in st.session_state.selected_ids:
            st.session_state.selected_ids.append(iid)

        elif not selected and iid in st.session_state.selected_ids:
            st.session_state.selected_ids.remove(iid)

        col2.write(item["name"])
        col3.write(f"${item['price']:.2f}")

        # -------- Edit Button --------
        if col4.button("Edit", key=f"edit_{iid}"):

            st.session_state[f"editing_{iid}"] = True

        if st.session_state.get(f"editing_{iid}"):

            new_name = st.text_input(
                "New name",
                value=item["name"],
                key=f"name_{iid}"
            )

            new_price = st.number_input(
                "New price",
                value=float(item["price"]),
                key=f"price_{iid}"
            )

            if st.button("Save", key=f"save_{iid}"):

                requests.put(
                    f"{BACKEND_URL}/ledger/update",
                    json={
                        "id": iid,
                        "name": new_name,
                        "price": new_price
                    }
                )

                st.session_state[f"editing_{iid}"] = False
                st.rerun()