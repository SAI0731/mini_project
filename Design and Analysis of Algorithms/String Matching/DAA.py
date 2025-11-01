import streamlit as st
import time

# ------------------------------------------
# Naive String Matching Algorithm
# ------------------------------------------
def naive_search(text, pattern):
    n = len(text)
    m = len(pattern)
    positions = []

    for i in range(n - m + 1):
        j = 0
        while j < m and text[i + j] == pattern[j]:
            j += 1
        if j == m:
            positions.append(i)
    return positions


# ------------------------------------------
# Rabin-Karp Algorithm
# ------------------------------------------
def rabin_karp_search(text, pattern, q=101):
    d = 256
    n = len(text)
    m = len(pattern)
    p = 0
    t = 0
    h = 1
    positions = []

    for i in range(m - 1):
        h = (h * d) % q

    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    for i in range(n - m + 1):
        if p == t:
            if text[i:i + m] == pattern:
                positions.append(i)
        if i < n - m:
            t = (d * (t - ord(text[i]) * h) + ord(text[i + m])) % q
            if t < 0:
                t += q
    return positions


# ------------------------------------------
# Streamlit UI
# ------------------------------------------
st.set_page_config(page_title="String Matching Algorithms", page_icon="🔍", layout="centered")

st.title("🔍 String Matching Algorithm Comparison")
st.write("Compare **Naive String Matching** and **Rabin-Karp Algorithm** performance for the same input text.")

st.divider()

# User Inputs
text = st.text_area("Enter the main text:", "ABABDABACDABABCABAB")
pattern = st.text_input("Enter the pattern to search:", "ABABCABAB")

if st.button("🔎 Run Comparison"):
    if not text or not pattern:
        st.warning("Please enter both text and pattern.")
    else:
        st.divider()
        st.subheader("⚙️ Algorithm Execution")

        # --- Naive ---
        start_naive = time.time()
        naive_result = naive_search(text, pattern)
        end_naive = time.time()

        # --- Rabin-Karp ---
        start_rk = time.time()
        rk_result = rabin_karp_search(text, pattern)
        end_rk = time.time()

        # --- Results ---
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🧩 Naive Algorithm")
            st.write(f"**Positions:** {naive_result if naive_result else 'No Match Found'}")
            st.write(f"**Time Taken:** {end_naive - start_naive:.8f} seconds")

        with col2:
            st.markdown("### ⚡ Rabin-Karp Algorithm")
            st.write(f"**Positions:** {rk_result if rk_result else 'No Match Found'}")
            st.write(f"**Time Taken:** {end_rk - start_rk:.8f} seconds")

        st.divider()
        st.subheader("📊 Comparison Summary")

        st.info(f"""
        **Observation:**
        - Naive algorithm compares each substring character by character.
        - Rabin-Karp uses hashing to skip unnecessary comparisons.
        - For large texts, **Rabin-Karp** is usually faster, especially when multiple pattern matches are needed.
        """)

        # Efficiency note
        st.success("✅ Both algorithms give the same result, but differ in efficiency and approach.")

st.divider()
st.markdown("**Developed for DAA Mini Project: String Matching Algorithms (Naive vs Rabin-Karp)**")
