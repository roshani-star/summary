import streamlit as st

from auth import register_user, login_user

from summarizer import (
    generate_summary,
    extract_text_from_pdf,
    extract_text_from_url,
    generate_viva_questions,
    generate_study_notes
)
# ---------------- SESSION ----------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""
    
if "last_content" not in st.session_state:
    st.session_state.last_content = ""
if "trial_count" not in st.session_state:
    st.session_state.trial_count = 3
 
if "summary_count" not in st.session_state:
    st.session_state.summary_count = 0

if "notes_count" not in st.session_state:
    st.session_state.notes_count = 0

if "viva_count" not in st.session_state:
    st.session_state.viva_count = 0    

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="BriefIQ",
    page_icon="🧠",
    layout="wide"
)

# ---------------- CSS ----------------

st.markdown("""
<style>

[data-testid="stAppViewContainer"]{
    background: linear-gradient(
        135deg,
        #050816,
        #0b1026,
        #11162e
    );
    color:white;
}

header{
    background: transparent !important;
}

html, body, [class*="css"]{
    color:white;
}

section[data-testid="stSidebar"]{
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(20px);
}

.stTextInput input{
    background: rgba(255,255,255,0.08);
    color:white !important;
    border-radius:12px;
}

textarea{
    background: rgba(255,255,255,0.08) !important;
    color:white !important;
    border-radius:15px !important;
}

.stButton button{
    background: linear-gradient(
        90deg,
        #ff4fd8,
        #6c63ff
    );
    color:white;
    border:none;
    border-radius:15px;
    padding:12px 25px;
    font-weight:bold;
}

.feature-card{
    background: rgba(255,255,255,0.05);
    padding:20px;
    border-radius:20px;
    text-align:center;
}

.big-title{
    font-size:60px;
    font-weight:800;
}

.gradient{
    background: linear-gradient(
        90deg,
        #ff4fd8,
        #6c63ff
    );

    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------

st.sidebar.title("🧠 BriefIQ")

if st.session_state.logged_in:

    st.sidebar.success(
        f"Logged in as {st.session_state.username}"
    )

    st.sidebar.info(
        f"🎁 Free Trials Left: {st.session_state.trial_count}"
    )

    if st.sidebar.button("Logout"):

        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.trial_count = 3

        st.rerun()
    if st.session_state.logged_in:

     st.sidebar.success(
        f"👋 Welcome, {st.session_state.username}"
    )

    st.sidebar.markdown("## 📊 Dashboard")

    st.sidebar.info(
        f"""
📝 Summaries: {st.session_state.summary_count}

📚 Notes: {st.session_state.notes_count}

🎓 Viva Questions: {st.session_state.viva_count}
"""
    )
# ---------------- MENU ----------------

menu = ["Login", "Signup"]

choice = st.sidebar.radio(
    "Navigation",
    menu
)

# ---------------- SIGNUP ----------------

if choice == "Signup":

    st.markdown("""
    <h1 class='big-title'>
    Create your
    <span class='gradient'>BriefIQ</span>
    ✨
    </h1>
    """, unsafe_allow_html=True)

    new_user = st.text_input("Username")

    new_pass = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Create Account"):

        if new_user and new_pass:

            register_user(
                new_user,
                new_pass
            )

            st.success(
                "✅ Account Created Successfully!"
            )

            st.balloons()

        else:

            st.warning(
                "Please fill all fields."
            )

# ---------------- LOGIN ----------------

elif choice == "Login":

    st.markdown("""
    <h1 class='big-title'>
    Welcome to
    <span class='gradient'>BriefIQ</span>
    ✨
    </h1>
    """, unsafe_allow_html=True)

    st.write(
        "### Summarize smarter, not harder."
    )

    # ---------- LOGIN FORM ----------

    if not st.session_state.logged_in:

        username = st.text_input("Username")

        password = st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            user = login_user(
                username,
                password
            )

            if user:

                st.session_state.logged_in = True
                st.session_state.username = username

                st.rerun()

            else:

                st.error(
                    "Invalid Credentials"
                )

    # ---------- DASHBOARD ----------

    if st.session_state.logged_in:

        st.success(
            f"Welcome back, {st.session_state.username} 🚀"
        )

        st.markdown("---")

        # ---------- CARDS ----------

        col1, col2, col3 = st.columns(3)

        with col1:

            st.markdown("""
            <div class="feature-card">
            <h2>📰</h2>
            <h3>Article/Text</h3>
            <p>Summarize articles instantly.</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:

            st.markdown("""
            <div class="feature-card">
            <h2>📄</h2>
            <h3>PDF Upload</h3>
            <p>Upload PDFs for summaries.</p>
            </div>
            """, unsafe_allow_html=True)

        with col3:

            st.markdown("""
            <div class="feature-card">
            <h2>🔗</h2>
            <h3>Website Link</h3>
            <p>Summarize blogs & articles.</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ---------- TABS ----------

        tab1, tab2, tab3 = st.tabs([
            "📰 Article/Text",
            "📄 PDF Upload",
            "🔗 Website Link"
        ])

        # ---------- ARTICLE ----------

        text_input = ""

        with tab1:

            text_input = st.text_area(
                "Paste your article/text here...",
                height=250
            )

        # ---------- PDF ----------

        pdf_text = ""

        with tab2:

            uploaded_file = st.file_uploader(
                "Upload PDF",
                type=["pdf"]
            )

            if uploaded_file:

                pdf_text = extract_text_from_pdf(
                    uploaded_file
                )

                st.success(
                    "PDF Uploaded Successfully ✅"
                )

                st.text_area(
                    "Extracted PDF Text",
                    pdf_text[:1000],
                    height=200
                )

        # ---------- LINK ----------

        link_input = ""

        with tab3:

            link_input = st.text_input(
                "Paste Website Link"
            )

        # ---------- LANGUAGE ----------

        language = st.selectbox(
            "Select Summary Language",
            ["English", "Hindi"]
        )

        # ---------- LENGTH ----------

        length = st.radio(
            "Summary Length",
            ["Short", "Medium", "Detailed"]
        )

        # ---------- GENERATE BUTTON ----------

        if st.button("✨ Generate Summary"):

            # ---------- TRIAL CHECK ----------

            if st.session_state.trial_count <= 0:

                st.error(
                    "🚫 Free Trial Ended!"
                )

                st.markdown("""
                ## 👑 BriefIQ Premium

                Unlock:
                - Unlimited summaries
                - PDF downloads
                - Hindi translation
                - Faster AI generation
                - No ads
                """)

                st.button("💎 Upgrade Now")

            else:

                st.session_state.trial_count -= 1

                # ---------- ARTICLE SUMMARY ----------

                if text_input:

                    with st.spinner(
                        "Generating AI Summary..."
                    ):

                        summary = generate_summary(
                            text_input,
                            length,
                            language
                        )
                        st.session_state.summary_count += 1
                        st.session_state.last_content = text_input
                    

                    st.markdown(
                        "## 📌 Article Summary"
                    )

                    st.success(summary)

                # ---------- WEBSITE SUMMARY ----------

                elif link_input:

                    with st.spinner(
                        "Extracting Website Content..."
                    ):

                        article_text = extract_text_from_url(
                            link_input
                        )

                        summary = generate_summary(
                            article_text,
                            length,
                            language
                        )
                        st.session_state.summary_count += 1
                        st.session_state.last_content = article_text

                    st.markdown(
                        "## 🔗 Website Summary"
                    )

                    st.success(summary)
                    

                # ---------- PDF SUMMARY ----------

                elif pdf_text:

                    with st.spinner(
                        "Generating PDF Summary..."
                    ):

                        pdf_summary = generate_summary(
                            pdf_text,
                            length,
                            language
                        )
                        st.session_state.summary_count += 1
                        st.session_state.last_content = pdf_text

                    st.markdown(
                        "## 📄 PDF Summary"
                    )

                    st.success(pdf_summary)

                else:

                    st.warning(
                        "Please enter text, upload PDF, or add website link."
                    )
                    # ---------- STUDY NOTES ----------

if st.session_state.last_content:

    st.divider()

    if st.button("📚 Generate Study Notes"):

        with st.spinner("Generating Study Notes..."):

            notes = generate_study_notes(
                st.session_state.last_content,
                language
            )
            st.session_state.notes_count += 1

        st.markdown("## 📚 AI Study Notes")

        st.write(notes)
if st.button("🎓 Generate Viva Questions"):

        with st.spinner("Generating Viva Questions..."):

            viva = generate_viva_questions(
                st.session_state.last_content,
                language
            )
            st.session_state.viva_count += 1

        st.markdown("## 🎓 Viva Questions")

        st.write(viva)