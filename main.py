import streamlit as st
import sys
import os

# Fix the import issue - add this at the top
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    from app.models import Base, User, AdCampaign
    st.success("✅ Models imported successfully!")
except ImportError as e:
    st.error(f"❌ Import error: {e}")
    st.info("Checking project structure...")
    
    # Show current directory structure
    st.write("Current directory:", os.getcwd())
    if os.path.exists('app'):
        st.write("✅ app folder exists")
        if os.path.exists('app/__init__.py'):
            st.write("✅ app/__init__.py exists")
        else:
            st.write("❌ app/__init__.py missing")
        if os.path.exists('app/models.py'):
            st.write("✅ app/models.py exists")
        else:
            st.write("❌ app/models.py missing")
    else:
        st.write("❌ app folder doesn't exist")

# Your Streamlit app code
st.title("Meta Ad Bot Dashboard 🚀")
st.write("Welcome to your advertising dashboard!")

# Display sample data
st.subheader("Sample User Data")
st.write("""
- User ID: 1, Name: John Doe, Email: john@example.com
- User ID: 2, Name: Jane Smith, Email: jane@example.com
""")

st.subheader("Sample Campaign Data")
st.write("""
- Campaign: Summer Sale, Budget: $1000, Status: Active
- Campaign: Winter Promotion, Budget: $2000, Status: Planning
""")

# Add some interactive elements
if st.button("Click me!"):
    st.balloons()
    st.success("You clicked the button! 🎉")

# File upload example
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    st.write("File uploaded successfully!")
