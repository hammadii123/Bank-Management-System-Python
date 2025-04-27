import streamlit as st
from datetime import datetime

# Initialize session state
if 'users' not in st.session_state:
    st.session_state.users = {}

if 'current_user' not in st.session_state:
    st.session_state.current_user = None

if 'page' not in st.session_state:
    st.session_state.page = 'main'

def create_account():
    with st.form("Create Account"):
        st.subheader("Create New Account")
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1, max_value=100, step=1)
        salary = st.number_input("Salary", min_value=0, step=100)
        pin = st.text_input("PIN (4 digits)", max_chars=4, type="password")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            if st.form_submit_button("Create Account"):
                if len(pin) != 4 or not pin.isdigit():
                    st.error("PIN must be a 4-digit number!")
                    return
                if name.strip() == "":
                    st.error("Name is required!")
                    return
                if pin in st.session_state.users:
                    st.error("PIN already exists!")
                    return
                
                st.session_state.users[pin] = {
                    'name': name,
                    'age': age,
                    'salary': salary,
                    'balance': 0,
                    'transactions': [],
                    'pin': pin
                }
                st.success("Account created successfully!")
                st.session_state.page = 'main'
                st.rerun()
        
        with col2:
            if st.form_submit_button("Back to Login"):
                st.session_state.page = 'main'
                st.rerun()

def login():
    with st.form("Login"):
        st.subheader("Login")
        name = st.text_input("Name")
        pin = st.text_input("PIN", type="password", max_chars=4)
        
        if st.form_submit_button("Login"):
            user = st.session_state.users.get(pin)
            if user and user['name'] == name:
                st.session_state.current_user = pin
                st.session_state.page = 'user_details'
                st.rerun()
            else:
                st.error("Invalid Name or PIN")

def user_details():
    user = st.session_state.users[st.session_state.current_user]
    
    st.title("Bank Management System")
    st.subheader(f"Welcome, {user['name']}!")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Age", user['age'])
    col2.metric("Salary", f"${user['salary']}")
    col3.metric("Current Balance", f"${user['balance']}")
    
    # Deposit and Withdraw forms
    col1, col2 = st.columns(2)
    
    with col1:
        with st.form("Deposit"):
            st.subheader("Deposit")
            amount = st.number_input("Amount", min_value=1, step=100, key="deposit_amount")
            if st.form_submit_button("Deposit"):
                user['balance'] += amount
                user['transactions'].append({
                    'type': 'deposit',
                    'amount': amount,
                    'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'balance': user['balance']
                })
                st.rerun()
    
    with col2:
        with st.form("Withdraw"):
            st.subheader("Withdraw")
            amount = st.number_input("Amount", min_value=1, step=100, key="withdraw_amount")
            if st.form_submit_button("Withdraw"):
                if amount > user['balance']:
                    st.error("Insufficient balance!")
                else:
                    user['balance'] -= amount
                    user['transactions'].append({
                        'type': 'withdraw',
                        'amount': amount,
                        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'balance': user['balance']
                    })
                    st.rerun()
    
    # Transaction History
    st.subheader("Transaction History")
    if user['transactions']:
        for t in reversed(user['transactions']):
            color = "green" if t['type'] == 'deposit' else "red"
            st.markdown(f"""
            <div style="padding: 10px; border-radius: 5px; margin: 5px 0; 
                        border-left: 5px solid {color}; background-color: #f0f0f0">
                <strong>{t['type'].title()}</strong><br>
                Amount: ${t['amount']}<br>
                Date: {t['date']}<br>
                Balance: ${t['balance']}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No transactions yet")
    
    if st.button("Logout"):
        st.session_state.current_user = None
        st.session_state.page = 'main'
        st.rerun()

def main_page():
    st.title("Bank Management System")
    
    if st.session_state.page == 'create_account':
        create_account()
    elif st.session_state.page == 'user_details':
        user_details()
    else:
        login()
        st.write("---")
        if st.button("Create New Account"):
            st.session_state.page = 'create_account'
            st.rerun()

if __name__ == "__main__":
    main_page()