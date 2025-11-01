# ---------------------------------------
# Blockchain-Based Certificate Verification System
# ---------------------------------------
# Fixed version with unique Streamlit keys
# ---------------------------------------

import streamlit as st
import hashlib
import pandas as pd
import datetime

# --------------------------------------------------------
# Blockchain Class Implementation
# --------------------------------------------------------
class CertificateBlockchain:
    def __init__(self):
        self.chain = []  # Blockchain ledger

    def generate_hash(self, certificate_data):
        """
        Generate SHA-256 hash of certificate data.
        """
        hash_input = (certificate_data['name'] + certificate_data['course'] +
                      certificate_data['date'] + certificate_data['issuer'])
        return hashlib.sha256(hash_input.encode()).hexdigest()

    def add_certificate(self, name, course, date, issuer):
        """
        Add a new certificate to the blockchain ledger.
        """
        certificate_data = {
            'name': name,
            'course': course,
            'date': date,
            'issuer': issuer
        }
        certificate_hash = self.generate_hash(certificate_data)
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'certificate': certificate_data,
            'hash': certificate_hash
        }
        self.chain.append(block)
        return block

    def verify_certificate(self, name, course, date, issuer, given_hash):
        """
        Verify certificate authenticity by recalculating hash.
        """
        certificate_data = {
            'name': name,
            'course': course,
            'date': date,
            'issuer': issuer
        }
        calculated_hash = self.generate_hash(certificate_data)
        return calculated_hash == given_hash


# --------------------------------------------------------
# Streamlit Web App
# --------------------------------------------------------
st.set_page_config(page_title="Blockchain Certificate Verification System", layout="wide")

st.title("🎓 Blockchain-Based Certificate Verification System")
st.write("""
This project securely generates and verifies certificates using **Blockchain Hashing (SHA-256)**.  
Each certificate acts as a block in a digital blockchain ledger.
""")

# Initialize Blockchain
blockchain = CertificateBlockchain()

# Tabs
tab1, tab2 = st.tabs(["🪪 Generate Certificate", "✅ Verify Certificate"])

# --------------------------------------------------------
# Generate Certificate Tab
# --------------------------------------------------------
with tab1:
    st.subheader("🧾 Generate Certificate")

    # Input fields with unique keys
    name = st.text_input("Student Name", key="gen_name")
    course = st.text_input("Course Name", key="gen_course")
    date = st.date_input("Date of Issue", key="gen_date")
    issuer = st.text_input("Issuer / Organization Name", key="gen_issuer")

    if st.button("Generate Certificate", key="generate_btn"):
        if name and course and issuer:
            block = blockchain.add_certificate(name, course, str(date), issuer)
            st.success("✅ Certificate Generated Successfully!")

            st.markdown("### 📋 Certificate Details")
            st.json(block['certificate'])

            st.markdown("### 🔐 Blockchain Hash (Unique ID)")
            st.code(block['hash'])

            st.info("Share this hash with the student. It can be used later for verification.")
        else:
            st.error("⚠️ Please fill all fields before generating the certificate.")

# --------------------------------------------------------
# Verify Certificate Tab
# --------------------------------------------------------
with tab2:
    st.subheader("🔍 Verify Certificate Authenticity")

    # Input fields with unique keys
    name_v = st.text_input("Student Name (for verification)", key="ver_name")
    course_v = st.text_input("Course Name", key="ver_course")
    date_v = st.date_input("Date of Issue (Verification)", key="ver_date")
    issuer_v = st.text_input("Issuer / Organization Name", key="ver_issuer")
    hash_v = st.text_area("Enter Certificate Hash (for verification)", key="ver_hash")

    if st.button("Verify Certificate", key="verify_btn"):
        if name_v and course_v and issuer_v and hash_v:
            valid = blockchain.verify_certificate(name_v, course_v, str(date_v), issuer_v, hash_v)
            if valid:
                st.success("🎉 Certificate is Authentic and Verified on Blockchain.")
                st.balloons()
            else:
                st.error("🚫 Invalid Certificate! Details or Hash do not match.")
        else:
            st.warning("⚠️ Please fill all fields to verify the certificate.")

# --------------------------------------------------------
# Blockchain Ledger Section
# --------------------------------------------------------
st.markdown("---")
st.subheader("🧩 Blockchain Ledger (Session Data)")

if blockchain.chain:
    df = pd.DataFrame(blockchain.chain)
    st.dataframe(df[['index', 'timestamp', 'hash']])
else:
    st.info("No certificates generated yet. Generate one to see it in the blockchain ledger.")

# Footer
st.markdown("---")
st.caption("© 2025 Blockchain-Based Certificate Verification System | Built using Python & Streamlit")
