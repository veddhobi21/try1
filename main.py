

import streamlit as st
with st.sidebar:
        st.markdown("""
                <div class='header-container'>
                    <h2>💬Welcome to the Chatbot World! 
                            🤗💬 LLM Chat App🤖</h2>
                </div>
            """, unsafe_allow_html=True)

st.markdown("""
    <style>
    .main-container {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    }
    .sidebar-container {
        background-color: #2c3e50;
        color: black;
        padding: 20px;
        border-radius: 8px;
    }
    .header-container {
        background: linear-gradient(90deg, #4CAF50, #34a5dd);
        padding: 20px;
        color: black;
        text-align: center;
        border-radius: 8px;
    }
    .response-box {
        background-color: ;
        border: 1px solid #4caf50;
        padding: 10px;
        border-radius: 5px;
        margin-top: 10px;
    }
    .chat-input {
        margin-top: 20px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)
import hashlib
from dotenv import load_dotenv
import os
import sqlite3
import streamlit as st
# Load environment variables
load_dotenv()

# Initialize session states
if "login_status" not in st.session_state:
    st.session_state["login_status"] = False
if "current_user" not in st.session_state:
    st.session_state["current_user"] = None


# Database Setup
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()
def register_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password_hash))
        conn.commit()
        conn.close()
        return "Registration successful!"
    except sqlite3.IntegrityError:
        return "Username already exists. Please choose a different one."

def login_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password_hash))
    user = c.fetchone()
    conn.close()
    return user is not None

# --- Session State Initialization ---
if "login_status" not in st.session_state:
    st.session_state["login_status"] = False

if "current_user" not in st.session_state:
    st.session_state["current_user"] = None

# --- Registration Page ---
def registration_page():
    st.title("🔐 Register")
    with st.form("register_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Register")
        if submitted:
            result = register_user(username, password)
            if "successful" in result:
                st.success(result)
            else:
                st.error(result)

# --- Login Page ---
def login_page():
    st.title("🔓 Login")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            if login_user(username, password):
                st.session_state["login_status"] = True
                st.session_state["current_user"] = username
                st.success(f"Welcome, {username}!")
            else:
                st.error("Invalid username or password.")
# Define Page Functions
def home_page():
    st.markdown("""
            <div class='header-container'>
                <h1>Welcome to the Modern Chatbot 🤖</h1>
                <p>Chat with AI, extract PDF insights, and generate reports.</p>
            </div>
        """, unsafe_allow_html=True)
    # # # st.title("Home Page")
    # # st.markdown("""
    # #     Welcome to the Chatbot Application! 🌟
    # #     Use the sidebar to navigate through the app and explore its features.
    # """)
    # st.title("Welcome to Chatbot App! 🌟")
    user = st.session_state.get("current_user", "Guest")

    # Set page configuration
    # st.set_page_config(
    #     page_title="Chatbot Homepage",
    #     page_icon="🤖",
    #     layout="wide",
    #     initial_sidebar_state="expanded"
    #  )

    # Custom CSS for styling
    st.markdown("""
        <style>
        /* General Page Styling */
        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(to right, #2c3e50, #34495e);
            color: #ecf0f1;
        }
        .main-header {
            text-align: center;
            color: #ecf0f1;
            font-size: 48px;
            font-weight: 800;
            margin-top: 20px;
            margin-bottom: 10px;
            text-shadow: 2px 2px 5px rgba(0,0,0,0.7);
        }
        .sub-header {
            text-align: center;
            color: #bdc3c7;
            font-size: 24px;
            margin-bottom: 50px;
        }

        /* Sidebar Styling */
        .stSidebar {
            background-color: #34495e;
            border-right: 2px solid #2ecc71;
            color: #ecf0f1;
        }

        /* Cards */
        .card {
            background: #2c3e50;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.5);
            padding: 20px;
            text-align: center;
        }
        .card h3 {
            font-size: 22px;
            color: #ecf0f1;
        }
        .card p {
            font-size: 16px;
            color: #bdc3c7;
        }

        /* Button */
        .cta-button {
            background: linear-gradient(90deg, #27ae60, #2ecc71);
            color: #ecf0f1;
            border: none;
            border-radius: 8px;
            padding: 15px 30px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            text-align: center;
            margin: 20px auto;
            display: block;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
            transition: transform 0.2s ease-in-out;
        }
        .cta-button:hover {
            transform: scale(1.05);
        }

        /* Footer */
        .footer {
            text-align: center;
            margin-top: 50px;
            font-size: 14px;
            color: #bdc3c7;
        }
        .footer a {
            color: #2ecc71;
            text-decoration: none;
            font-weight: 600;
        }
        </style>
    """, unsafe_allow_html=True)

    # Main Header
    # st.markdown('<div class="main-header">Welcome to the Modern Chatbot 🤖</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">Engage, assist, and simplify your interactions with AI-powered conversations.</div>',
        unsafe_allow_html=True)

    # Main Content Area
    st.write("### Key Features")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="card">
            <h3>Advanced AI</h3>
            <p>Experience cutting-edge technology that understands and responds intelligently.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="card">
            <h3>Seamless Integration</h3>
            <p>Effortlessly integrate the chatbot into your workflows and applications.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="card">
            <h3>Natural Conversations</h3>
            <p>Engage in lifelike, meaningful dialogues tailored to your needs.</p>
        </div>
        """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
        <div class="footer">
            © 2024 Modern Chatbot | 
            <a href="https://twitter.com">Twitter</a> | 
            <a href="https://linkedin.com">LinkedIn</a> | 
            <a href="https://github.com">GitHub</a>
        </div>
    """, unsafe_allow_html=True)

    # Welcome Message
    st.markdown(f"### Hi, {user}! 👋")
    st.write("We're excited to have you here. Explore the features below to make the most of the app.")

    # Quick Start Guide
    st.subheader("Quick Start Guide")
    st.markdown("""
        1. **Ask the Chatbot**: Interact with our intelligent assistant for instant answers. 🤖  
        2. **Upload PDFs**: Extract insights from your documents. 📄  
        3. **Generate Reports**: Create professional PDFs in a few clicks. 📊  
        """)

    # Recent Updates
    st.subheader("Recent Updates")
    st.markdown("""
        - 🆕 **New Model Added**: Experience the power of Llama3-70b-8192.  
        - 🌟 **PDF Summarization**: Quickly generate concise summaries of lengthy documents.  
        - 🔧 **Improved Interface**: Enhanced user experience with a sleek new look.  
        """)


    # Inspiring Quote
    st.subheader("Inspiration for Today")
    st.markdown("> “The best way to predict the future is to invent it.” – Alan Kay")

    # Fun Fact
    st.subheader("Did You Know?")
    st.info("The first chatbot, ELIZA, was created in 1966 by Joseph Weizenbaum!")

    # Feedback Section
    st.subheader("We Value Your Feedback")
    feedback = st.text_area("Share your thoughts about the app:")
    if st.button("Submit Feedback"):
        st.success("Thank you for your feedback!")



home_page_css = """
    <style>
        .main-container {
            font-family: 'Roboto', sans-serif;
            background-color: #f0f4f8;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }
        .welcome-banner {
            background: linear-gradient(to right, #4CAF50, #34a5dd);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            margin-bottom: 20px;
        }
    </style>
    """
st.markdown(home_page_css, unsafe_allow_html=True)


def about_page():
    import streamlit as st

    st.markdown("""
        <style>
        /* General Page Styling */
        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(to right, #2c3e50, #34495e);
            color: #2c3e50;  /* New plain color */
        }
        .main-header {
            text-align: center;
            color: #2c3e50;
            font-size: 48px;
            font-weight: 800;
            margin-top: 20px;
            margin-bottom: 10px;
            text-shadow: 2px 2px 5px rgba(0,0,0,0.7);
        }
        .sub-header {
            text-align: center;
            color: #ecf0f1;  /* New plain color */
            font-size: 24px;
            margin-bottom: 50px;
        }

        /* Sidebar Styling */
        .stSidebar {
            background-color: #34495e;
            border-right: 2px solid #2ecc71;
            color: #2c3e50;
        }

        /* Cards */
        .card {
            background: #2c3e50;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.5);
            padding: 20px;
            text-align: center;
        }
        .card h3 {
            font-size: 22px;
            color: #2c3e50;
        }
        .card p {
            font-size: 16px;
            color: #ecf0f1;  /* New plain color */
        }

        /* Button */
        .cta-button {
            background: linear-gradient(90deg, #27ae60, #2ecc71);
            color: #2c3e50;
            border: none;
            border-radius: 8px;
            padding: 15px 30px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            text-align: center;
            margin: 20px auto;
            display: block;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
            transition: transform 0.2s ease-in-out;
        }
        .cta-button:hover {
            transform: scale(1.05);
        }

        /* Footer */
        .footer {
            text-align: center;
            margin-top: 50px;
            font-size: 14px;
            color: #2c3e50;
        }
        .footer a {
            color: #34495e;  /* New color */
            text-decoration: none;
            font-weight: 600;
        }
        </style>
    """, unsafe_allow_html=True)

    # st.markdown("""
    #         <div class='header-container'>
    #             <h1>🤖 About page</h1>
    #             <p>Chat with AI, extract PDF insights, and generate reports.</p>
    #         </div>
    #     """, unsafe_allow_html=True)
    import streamlit as st

    # Set page configuration
    # st.set_page_config(
    #     page_title="About - Chatbot",
    #     page_icon="🤖",
    #     layout="wide",
    #     initial_sidebar_state="expanded"
    # )
    # st.title("About")
    st.markdown('''
                ## About
                This app is an LLM-powered chatbot built using:
                - [Streamlit](https://streamlit.io/)
                - [LangChain](https://python.langchain.com/)
                - [OpenAI](https://platform.openai.com/docs/models) LLM model
                 ''')
    st.write('Made with ❤️ by [Mr. DHOBI VED JAYESHBHAI](https://youtube.com/@engineerprompt)')
    st.title("About the Chatbot App")

    # App Overview
    st.subheader("What is this app?")
    st.markdown("""
            This app is your ultimate tool for:
            - 🤖 Chatting with a powerful AI chatbot.
            - 📄 Extracting insights from uploaded PDFs.
            - 📊 Generating professional PDF reports.
            - 🌟 And much more!
        """)

    # Technology Stack
    st.subheader("Powered By")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("https://upload.wikimedia.org/wikipedia/commons/4/4f/Streamlit_logo.svg", width=100)
        st.caption("Streamlit")
    with col2:
        st.image("https://upload.wikimedia.org/wikipedia/commons/6/6e/OpenAI_Logo.svg", width=100)
        st.caption("OpenAI")
    with col3:
        st.image("https://upload.wikimedia.org/wikipedia/commons/3/38/SQLite370.svg", width=100)
        st.caption("SQLite")

    # FAQs
    st.subheader("FAQs")
    with st.expander("What is the purpose of this app?"):
        st.write("This app is designed to make AI interaction and document analysis accessible to everyone.")
    with st.expander("How does the chatbot work?"):
        st.write("The chatbot uses state-of-the-art AI models to understand and respond to your queries.")
    with st.expander("Can I use this app for free?"):
        st.write("Yes! The app is free to use, but some advanced features may require an API key.")

    # Links and Contact
    st.subheader("Learn More")
    st.markdown("""
            - 📚 [User Guide](https://example.com/user-guide)  
            - 💻 [GitHub Repository](https://github.com/example/chatbot-app)  
            - ✉️ [Contact Us](mailto:support@example.com)
        """)

    # Development Journey
    st.subheader("Our Journey")
    st.write("""
            This app was started in 2023 with the goal of simplifying AI-powered tools. 
            We've come a long way and are excited to bring you even more features in the future!
        """)
    # Custom CSS for styling
    st.markdown("""
        <style>
        /* Hero Section */
        .hero {
            background: linear-gradient(to right, #4facfe, #00f2fe);
            padding: 50px;
            text-align: center;
            color: white;
            font-family: 'Poppins', sans-serif;
        }
        .hero h1 {
            font-size: 48px;
            font-weight: 800;
            margin-bottom: 10px;
            text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);
        }
        .hero p {
            font-size: 18px;
            font-weight: 300;
        }

        /* Features Section */
        .features {
            margin: 50px 0;
            font-family: 'Roboto', sans-serif;
        }
        .features h2 {
            text-align: center;
            font-size: 36px;
            margin-bottom: 20px;
        }
        .features .feature {
            text-align: center;
            padding: 20px;
        }
        .features img {
            width: 80px;
            margin-bottom: 10px;
        }
        .features p {
            font-size: 16px;
            color: #555;
        }

        /* Team Section */
        .team {
            margin: 50px 0;
            font-family: 'Roboto', sans-serif;
        }
        .team h2 {
            text-align: center;
            font-size: 36px;
            margin-bottom: 20px;
        }
        .team .member {
            text-align: center;
            margin: 20px;
            transition: transform 0.3s ease;
        }
        .team .member:hover {
            transform: scale(1.05);
        }
        .team img {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            margin-bottom: 10px;
        }
        .team h3 {
            font-size: 20px;
            margin-bottom: 5px;
        }
        .team p {
            font-size: 14px;
            color: #777;
        }

        /* Testimonial Section */
        .testimonials {
            background: #f9f9f9;
            padding: 50px 0;
            font-family: 'Roboto', sans-serif;
        }
        .testimonials h2 {
            text-align: center;
            font-size: 36px;
            margin-bottom: 20px;
        }
        .testimonials .testimonial {
            text-align: center;
            padding: 20px;
        }
        .testimonials .testimonial p {
            font-size: 16px;
            font-style: italic;
            color: #555;
        }
        .testimonials .testimonial h3 {
            font-size: 18px;
            margin-top: 10px;
            color: #333;
        }
        </style>
    """, unsafe_allow_html=True)

    # Hero Section
    # st.markdown("""
    #     <div class="hero">
    #         <h1>About Our Chatbot</h1>
    #         <p>Discover the future of AI-powered conversations. Our chatbot is designed to assist, engage, and simplify your interactions.</p>
    #     </div>
    # """, unsafe_allow_html=True)

    # Features Section
    st.markdown("""
        <div class="features">
            <h2>Key Features</h2>
            <div class="stColumns">
                <div class="feature">
                    <img src="https://img.icons8.com/color/96/000000/chat--v3.png" alt="Natural Conversations">
                    <h3>Natural Conversations</h3>
                    <p>Engage in lifelike, meaningful dialogues.</p>
                </div>
                <div class="feature">
                    <img src="https://img.icons8.com/color/96/000000/artificial-intelligence.png" alt="Advanced AI">
                    <h3>Advanced AI</h3>
                    <p>Leverages state-of-the-art algorithms to deliver intelligent responses.</p>
                </div>
                <div class="feature">
                    <img src="https://img.icons8.com/color/96/000000/cloud-sync.png" alt="Seamless Integration">
                    <h3>Seamless Integration</h3>
                    <p>Easily integrates into your workflow and applications.</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)




def settings_page():
    st.markdown('<div class="header">Settings</div>', unsafe_allow_html=True)
    # st.title("⚙️ Settings")
    # st.write("Customize your preferences below:")
    st.title('hey! choose the model as per your need')
    option = st.selectbox("Select an option:", ["exact or accurate word", "with detailed", "mix or combine"])
    if option == "exact or accurate word":
        model = st.selectbox(
            'model', ['Llama3-8b-8192']
        )
    elif option == "with detailed":
        model = st.selectbox(
            'model', ['Llama3-70b-8192']
        )
    else:
        model = st.selectbox(
            'model', ['Mixtral-8x7b-32768']
        )

        # model = st.selectbox(
        #     'Choose a model', ['Llama3-8b-8192', 'Llama3-70b-8192', 'Mixtral-8x7b-32768']
        # )

        # Profile Management
    st.subheader("Profile")
    name = st.text_input("Name", value=st.session_state.get("current_user", ""))
    if st.button("Save Profile"):
        st.success("Profile updated successfully!")
    # Account Management
    st.subheader("Account")

    if st.button("Delete Account"):
        st.warning("This feature is under construction.")

    # Custom CSS for styling
    st.markdown("""
        <style>
        /* General Page Styling */
        body {
            font-family: 'Roboto', sans-serif;
        }
        .header {
            text-align: center;
            color: #2c3e50;
            font-size: 36px;
            font-weight: 800;
            margin-top: 20px;
            margin-bottom: 10px;
        }
        .sub-header {
            text-align: center;
            color: #7f8c8d;
            font-size: 18px;
            margin-bottom: 30px;
        }

        /* Tabs Navigation */
        .stTabs {
            margin-bottom: 20px;
        }

        /* Cards Styling */
        .card {
            background: #ffffff;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            padding: 20px;
            margin-bottom: 20px;
        }
        .card h3 {
            font-size: 20px;
            color: #2c3e50;
        }
        .card p {
            font-size: 14px;
            color: #555;
        }
        .card .stButton > button {
            background-color: #4caf50;
            color: white;
            border-radius: 8px;
            padding: 10px;
            font-weight: bold;
        }

        /* Save Changes Button */
        .save-button {
            text-align: center;
            margin-top: 30px;
        }
        .save-button .stButton > button {
            background: linear-gradient(90deg, #4caf50, #43a047);
            color: white;
            font-size: 18px;
            font-weight: 600;
            border-radius: 8px;
            padding: 15px 30px;
        }
        </style>
    """, unsafe_allow_html=True)
    if st.button("Logout"):
        st.session_state["login_status"] = False
        st.session_state["current_user"] = None
        st.success("You have been logged out.")

# --- Chatbot Page ---
def chatbot_page1():
    global st
    import os
    # Load environment variables
    google_api = os.getenv('google_api')
    # Sidebar
    st.markdown("""
        <div class='header-container'>
            <h1>🤖 Searching Chatbot</h1>
            <p>Chat with AI, extract PDF insights, and generate reports.</p>
        </div>
    """, unsafe_allow_html=True)
    # # Sidebar - Enhanced
    # with st.sidebar:
    #     st.markdown("""
    #             <div class='header-container'>
    #                 <h2>💬Welcome to the Chatbot World!
    #                         🤗💬 LLM Chat App🤖</h2>
    #             </div>
    #         """, unsafe_allow_html=True)

    # with st.sidebar:
    #     st.sidebar.title("💬Welcome To The Chatbot World!")



    # Sidebar - User Profile

    # user_avatar = Image.open("legend.jpeg")
    # st.sidebar.image(user_avatar, width=100)

    # Sidebar contents
    # with st.sidebar:
    #     st.title('🤗💬 LLM Chat App')
    #     st.markdown('''
    #     ## About
    #     This app is an LLM-powered chatbot built using:
    #     - [Streamlit](https://streamlit.io/)
    #     - [LangChain](https://python.langchain.com/)
    #     - [OpenAI](https://platform.openai.com/docs/models) LLM model
    #      ''')
    #     st.write('Made with ❤️ by [Prompt Engineer](https://youtube.com/@engineerprompt)')

    load_dotenv()
    import os
    google_api = os.getenv("AIzaSyB9ds5LORzcW6I2PCPlajCVGU7E9Cy-LrY")
    # print(groq_api_key)
    # with st.sidebar:
    #     st.markdown("""
    #             <div class='header-container'>
    #                 <h2>🤖Personalization</h2>
    #             </div>
    #         """, unsafe_allow_html=True)
    # st.sidebar.title("Personalization")
    # prompt = st.sidebar.title("system prompt :")
    model = st.sidebar.selectbox(
        'Choose a model',['Llama3-8b-8192','Llama3-70b-8192','Mixtral-8x7b-32768']
    )
    from groq import Groq
    #groq client
    client = Groq(api_key=google_api)

    #streamlit interface
    # st.title("💬Chat with Groqs llm." "")
    st.title("🤖How Can i Help You Today?" "")

    #initialize session state for history
    if "history" not in st.session_state:
        st.session_state.history = []

    user_input = st.text_input("Enter your query:","")
    if st.button("submit"):
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role" : "user",
                    "content" : user_input,
                }
            ],
            model = model,
        )
    #store the query and response in history
        response = chat_completion.choices[0].message.content
        st.session_state.history.append({"query": user_input,"response":response})

    #Display the response
        st.markdown(f'<div class="response-box">{response}</div>',unsafe_allow_html=True)

    #Display history
        st.sidebar.title("History")
        for i,entry in enumerate(st.session_state.history):
            if st.sidebar.button(f'query {i+1}:{entry["query"]}'):
                st.markdown(f'<div class="response-box">{entry["response"]}</div>',unsafe_allow_html=True)

def chatbot_page2():
    st.markdown("""
            <div class='header-container'>
                <h1>🤖Advance PDF Q-A Chatbot</h1>
                <p>Chat with AI, extract PDF insights, and generate reports.</p>
            </div>
        """, unsafe_allow_html=True)
    # import pdfplumber
    # def extract_text_from_pdf(pdf_file):
    #     pdf_text = ""
    #     with pdfplumber.open(pdf_file) as pdf:
    #         for page in pdf.pages:
    #             pdf_text += page.extract_text()
    #     return pdf_text
    #
    # def answer_question(text, question):
    #     # Simple keyword-based search
    #     sentences = text.split('. ')
    #     sentences = [s.strip() for s in sentences if s]
    #     best_sentence = max(sentences, key=lambda s: s.lower().count(question.lower()),
    #                         default="No relevant answer found.")
    #     return best_sentence
    #
    # st.title("PDF Chatbot")
    #
    # # File uploader
    # pdf_file = st.file_uploader("Upload a PDF", type="pdf")
    #
    # if pdf_file:
    #     # Extract text from PDF
    #     pdf_text = extract_text_from_pdf(pdf_file)
    #     st.write("PDF text extracted successfully.")
    #
    #     # Display extracted text (for debugging or confirmation)
    #     st.text_area("Extracted PDF Text", pdf_text, height=300)
    #
    #     # Question input
    #     question = st.text_input("Ask a question about the PDF content:")
    #
    #     if question:
    #         # Get answer
    #         answer = answer_question(pdf_text, question)
    #         st.write("Answer:", answer)
    from PyPDF2 import PdfReader
    from transformers import pipeline
    from sentence_transformers import SentenceTransformer
    import faiss
    import numpy as np
    from nltk import sent_tokenize
    import nltk
    nltk.download('punkt_tab')
    import nltk
    print(nltk.data.path)


    # Load Models
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    qa_model = pipeline("question-answering", model="deepset/roberta-base-squad2")

    # Initialize FAISS Index
    dimension = 384  # Embedding size for the model
    index = faiss.IndexFlatL2(dimension)
    text_data = []  # Store text chunks for reference

    # Function to Extract Text from PDF
    def extract_text_from_pdf(pdf_file):
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

    # Function to Split Text into Logical Chunks
    def split_text_to_chunks(text, max_length=500):
        sentences = sent_tokenize(text)
        chunks = []
        current_chunk = ""
        for sentence in sentences:
            if len(current_chunk) + len(sentence) <= max_length:
                current_chunk += sentence + " "
            else:
                chunks.append(current_chunk.strip())
                current_chunk = sentence + " "
        if current_chunk:
            chunks.append(current_chunk.strip())
        return chunks

    # Streamlit App
    # st.title("Advanced PDF Q&A Chatbot")

    uploaded_pdf = st.file_uploader("Upload a PDF", type="pdf")
    if uploaded_pdf:
        with st.spinner("Processing the PDF..."):
            raw_text = extract_text_from_pdf(uploaded_pdf)
            chunks = split_text_to_chunks(raw_text)

            # Embed chunks and build FAISS index
            embeddings = embedding_model.encode(chunks, convert_to_tensor=False)
            embeddings = np.array(embeddings)
            index.add(embeddings)
            text_data.extend(chunks)

        st.success("PDF uploaded and indexed!")

    query = st.text_input("Ask a question:")
    if query:
        # Embed the query and find relevant chunks
        query_embedding = embedding_model.encode([query], convert_to_tensor=False)
        distances, indices = index.search(np.array(query_embedding), k=3)  # Retrieve top 3 chunks

        # Refine the answer with extractive Q&A
        candidate_answers = []
        for idx in indices[0]:
            chunk = text_data[idx]
            result = qa_model(question=query, context=chunk)
            candidate_answers.append((result['answer'], result['score'], chunk))

        # Sort by confidence and display the best answer
        best_answer = max(candidate_answers, key=lambda x: x[1])
        st.write(f"**Answer:** {best_answer[0]}")
        st.write(f"**Confidence:** {best_answer[1]:.2f}")
        st.write(f"**Relevant Context:** {best_answer[2]}")

        # Log the top 3 answers for transparency
        with st.expander("See other possible answers"):
            for ans, score, context in candidate_answers:
                st.write(f"- **Answer:** {ans}\n  **Confidence:** {score:.2f}\n  **Context:** {context[:200]}...")

    # Summarization for Quick Overview
    if st.checkbox("Summarize PDF Content"):
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        summary = summarizer(raw_text, max_length=150, min_length=30, do_sample=False)
        st.write("**Summary:**")
        st.write(summary[0]['summary_text'])


def chatbot_page3():
    import streamlit as st
    st.markdown("""
            <div class='header-container'>
                <h1>🤖 Chatbot with PDF Make </h1>
                <p>Chat with AI, extract PDF insights, and generate reports.</p>
            </div>
        """, unsafe_allow_html=True)
    import os
    from fpdf import FPDF
    from PIL import Image
    import streamlit as st

    # Function to create PDF
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, 'Generated PDF', align='C', ln=1)
            self.ln(10)

    def create_pdf(content, images=None, file_name="output.pdf"):
        pdf = PDF()
        pdf.set_auto_page_break(auto=True, margin=15)

        pdf.set_font("Arial", size=12)

        # Add text content if available
        if content:
            pdf.add_page()
            for line in content:
                pdf.multi_cell(0, 10, line)

        # Add each image on a new page
        if images:
            for img_path in images:
                pdf.add_page()
                pdf.image(img_path, x=10, y=10, w=190)  # Adjust size and position if needed

        pdf.output(file_name)

    # Streamlit UI
    # st.title("Chatbot with PDF Maker")
    with st.sidebar:
        st.markdown("""
                <div class='header-container'>
                    <h2>PDF Setting Here...</h2>
                </div>
            """, unsafe_allow_html=True)

    uploaded_files = st.file_uploader("Upload Images (Optional)", type=["png", "jpg", "jpeg"],
                                      accept_multiple_files=True)
    text_content = st.text_area("Enter your content here:", placeholder="Type text for your PDF...")
    file_name = st.sidebar.text_input("File Name", value="output.pdf")

    # Ensure 'temp' directory exists
    if not os.path.exists("temp"):
        os.makedirs("temp")

    # PDF generation
    if st.button("Generate PDF"):
        if not text_content.strip() and not uploaded_files:
            st.error("Please provide text or upload at least one image to generate a PDF.")
        else:
            # Process text and images
            text_lines = text_content.split('\n') if text_content.strip() else []
            image_paths = []

            if uploaded_files:
                for uploaded_file in uploaded_files:
                    try:
                        img = Image.open(uploaded_file)
                        img_path = os.path.join("temp", uploaded_file.name)
                        img.save(img_path)
                        image_paths.append(img_path)
                    except Exception as e:
                        st.error(f"Error processing image: {e}")

            # Generate PDF
            try:
                create_pdf(text_lines, images=image_paths, file_name=file_name)
                st.success(f"PDF '{file_name}' has been generated.")
                with open(file_name, "rb") as pdf_file:
                    st.download_button(label="Download PDF", data=pdf_file, file_name=file_name, mime="application/pdf")
            except Exception as e:
                st.error(f"Error generating PDF: {e}")

            # Clean up temporary files
            for img_path in image_paths:
                if os.path.exists(img_path):
                    os.remove(img_path)


def chatbot_page4():
    from PIL import Image, ImageOps, ImageFilter
    st.markdown("""
                        <div class='header-container'>
                            <h2>Image Processing & OCR.</h2>
                        </div>
                    """, unsafe_allow_html=True)

    def image_processing():
        import pytesseract
        """Image Processing and OCR Functionality."""
        # st.header("Image Processing & OCR")
        uploaded_image = st.file_uploader("Upload an image (png, jpg, jpeg):", type=["png", "jpg", "jpeg"])

        if uploaded_image is not None:
            image = Image.open(uploaded_image)
            st.image(image, caption="Uploaded Image", use_column_width=True)

            # Sidebar: Image Manipulation Options
            st.sidebar.header("Image Manipulation Options")
            action = st.sidebar.radio("Choose an action:", ["None", "Resize", "Crop", "Filter"])

            if action == "Resize":
                width = st.sidebar.number_input("Width", min_value=50, max_value=2000, value=300)
                height = st.sidebar.number_input("Height", min_value=50, max_value=2000, value=300)
                resized_image = image.resize((int(width), int(height)))
                st.image(resized_image, caption="Resized Image", use_column_width=True)

            elif action == "Crop":
                left = st.sidebar.slider("Left", 0, image.width, 0)
                top = st.sidebar.slider("Top", 0, image.height, 0)
                right = st.sidebar.slider("Right", 0, image.width, image.width)
                bottom = st.sidebar.slider("Bottom", 0, image.height, image.height)
                cropped_image = image.crop((left, top, right, bottom))
                st.image(cropped_image, caption="Cropped Image", use_column_width=True)

            elif action == "Filter":
                filter_type = st.sidebar.radio("Select Filter", ["Grayscale", "Blur", "Edge Detection"])
                if filter_type == "Grayscale":
                    filtered_image = ImageOps.grayscale(image)
                elif filter_type == "Blur":
                    filtered_image = image.filter(ImageFilter.BLUR)
                elif filter_type == "Edge Detection":
                    filtered_image = image.filter(ImageFilter.FIND_EDGES)
                st.image(filtered_image, caption=f"{filter_type} Image", use_column_width=True)

            # OCR Functionality
            if st.sidebar.button("Extract Text (OCR)"):
                with st.spinner("Extracting text..."):
                    extracted_text = pytesseract.image_to_string(image)
                    st.text_area("Extracted Text", extracted_text, height=250)
        else:
            st.info("Please upload an image to proceed.")

    if __name__ == "__main__":
        image_processing()


def chatbot_page5():
    import streamlit as st
    import pandas as pd
    def process_excel(excel_file):
        """Display and process Excel file."""
        # st.subheader("Excel File Preview")
        data = pd.read_excel(excel_file)
        st.dataframe(data)

        # Summarize the data (row and column counts)
        st.subheader("Data Summary")
        st.write(f"Number of Rows: {data.shape[0]}")
        st.write(f"Number of Columns: {data.shape[1]}")

    st.markdown("""
                                            <div class='header-container'>
                                                <h2>Automated Workflows in Chatbot</h2>
                                            </div>
                                """, unsafe_allow_html=True)

    def automated_workflow():
        """Run the automated workflow."""
        # st.title("Automated Workflows in Chatbot")

        # File Upload
        uploaded_file = st.file_uploader(
            "Upload a file (Excel):", type=["xlsx"]
        )

        if uploaded_file is not None:
            file_name = uploaded_file.name

            if file_name.endswith(".xlsx"):
                st.info("Excel File Detected")
                process_excel(uploaded_file)
        else:
            st.warning("Please upload a valid file to proceed.")

        # Workflow Chaining Example
        st.subheader("Automated Workflow Chaining")
        action = st.radio("Choose an automated task:", ["Excel Summary"])

        if action == "Excel Summary" and uploaded_file and file_name.endswith(".xlsx"):
            process_excel(uploaded_file)

    if __name__ == "__main__":
        automated_workflow()
def chatbot_page6():
    import streamlit as st

    st.markdown("""
                <div class='header-container'>
                    <h1>🤖Advanced Text Summarization</h1>
                    <p>Chat with AI, extract PDF insights, and generate reports.</p>
                </div>
            """, unsafe_allow_html=True)
    import streamlit as st
    from transformers import pipeline

    # Title and description
    # st.title("Advanced Text Summarization with Streamlit")
    st.write("Enter a long text, and this application will summarize it for you using advanced NLP models.")

    # Sidebar for model selection
    st.sidebar.title("Summarization Options")
    model_name = st.sidebar.selectbox(
        "Choose a pre-trained model:",
        ("facebook/bart-large-cnn", "t5-small", "t5-base", "t5-large")
    )

    # Load summarization pipeline
    @st.cache_resource
    def load_summarization_model(model_name):
        return pipeline("summarization", model=model_name)

    summarizer = load_summarization_model(model_name)

    # Input text
    st.subheader("Input Text")
    text = st.text_area("Paste your text here for summarization:", height=200)

    # Summarization parameters
    st.sidebar.subheader("Parameters")
    max_length = st.sidebar.slider("Maximum length of summary:", 30, 300, 130)
    min_length = st.sidebar.slider("Minimum length of summary:", 10, 100, 30)
    do_sample = st.sidebar.checkbox("Use sampling for summarization", value=False)

    # Generate summary
    if st.button("Summarize"):
        if text.strip():
            st.write("Summarizing...")
            try:
                summary = summarizer(
                    text,
                    max_length=max_length,
                    min_length=min_length,
                    do_sample=do_sample,
                )[0]['summary_text']
                st.subheader("Summary")
                st.write(summary)
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please enter some text to summarize.")


def chatbot_page7():
    # Footer
    import streamlit as st

    st.sidebar.info("Powered by Hugging Face Transformers and Streamlit")
    st.markdown("""
                <div class='header-container'>
                    <h1>🤖Advanced Image Enhancement</h1>
                    <p>Chat with AI, extract PDF insights, and generate reports.</p>
                </div>
            """, unsafe_allow_html=True)
    import streamlit as st
    import cv2
    from PIL import Image
    import numpy as np

    # Title and description
    # st.title("Advanced Image Enhancement with Streamlit")
    st.write(
        "Upload an image and apply various enhancement techniques such as brightness, contrast, sharpening, denoising, and edge detection.")

    # Sidebar for image upload
    st.sidebar.title("Upload Options")
    uploaded_file = st.sidebar.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    # Sidebar enhancement options
    st.sidebar.title("Enhancement Options")
    enhancement = st.sidebar.selectbox(
        "Select Enhancement Type:",
        ("Original", "Brightness & Contrast", "Sharpening", "Denoising", "Edge Detection")
    )

    # Brightness and contrast sliders
    if enhancement == "Brightness & Contrast":
        brightness = st.sidebar.slider("Brightness", -100, 100, 0)
        contrast = st.sidebar.slider("Contrast", -100, 100, 0)

    # Sharpening slider
    if enhancement == "Sharpening":
        sharpness_level = st.sidebar.slider("Sharpening Intensity", 1, 5, 3)

    # Denoising slider
    if enhancement == "Denoising":
        denoise_strength = st.sidebar.slider("Denoising Strength", 1, 30, 10)

    # Edge Detection slider
    if enhancement == "Edge Detection":
        edge_threshold1 = st.sidebar.slider("Threshold 1", 50, 200, 100)
        edge_threshold2 = st.sidebar.slider("Threshold 2", 50, 200, 150)

    # Function to apply enhancements
    def enhance_image(image, enhancement_type):
        if enhancement_type == "Brightness & Contrast":
            enhanced_image = cv2.convertScaleAbs(image, alpha=1 + contrast / 100, beta=brightness)
        elif enhancement_type == "Sharpening":
            kernel = np.array([[0, -1, 0], [-1, sharpness_level + 4, -1], [0, -1, 0]])
            enhanced_image = cv2.filter2D(image, -1, kernel)
        elif enhancement_type == "Denoising":
            enhanced_image = cv2.fastNlMeansDenoisingColored(image, None, denoise_strength, denoise_strength, 7, 21)
        elif enhancement_type == "Edge Detection":
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            enhanced_image = cv2.Canny(gray_image, edge_threshold1, edge_threshold2)
        else:
            enhanced_image = image
        return enhanced_image

    # Process the uploaded image
    if uploaded_file is not None:
        # Load image
        image = Image.open(uploaded_file)
        image_array = np.array(image)

        # Apply enhancement
        enhanced_image = enhance_image(image_array, enhancement)

        # Display images
        st.subheader("Original Image")
        st.image(image, use_column_width=True)

        st.subheader(f"Enhanced Image - {enhancement}")
        if enhancement == "Edge Detection":
            st.image(enhanced_image, channels="GRAY", use_column_width=True)
        else:
            st.image(enhanced_image, use_column_width=True)
    else:
        st.write("Please upload an image to start enhancement.")

    # Footer
    st.sidebar.info("Powered by OpenCV and Streamlit")

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import docx
import pdfplumber
import nltk

def chatbot_page8():
    # Download NLTK resources
    nltk.download('punkt')
    nltk.download('stopwords')

    # Helper Functions
    def preprocess_text(text):
        tokens = word_tokenize(text.lower())
        tokens = [word for word in tokens if word.isalnum()]
        stop_words = set(stopwords.words('english'))
        tokens = [word for word in tokens if word not in stop_words]
        return tokens

    def calculate_similarity(text1, text2):
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([text1, text2])
        score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return round(score * 100, 2)

    def find_overlapping_keywords(tokens1, tokens2):
        counter1 = Counter(tokens1)
        counter2 = Counter(tokens2)
        common_words = set(tokens1).intersection(set(tokens2))
        common_counts = {word: min(counter1[word], counter2[word]) for word in common_words}
        return common_counts

    def read_file(file):
        if file.type == "text/plain":  # TXT file
            return file.read().decode('utf-8')
        elif file.type == "application/pdf":  # PDF file
            text = ""
            try:
                with pdfplumber.open(file) as pdf:
                    for page in pdf.pages:
                        text += page.extract_text()
            except:
                st.error("Error reading PDF file.")
            return text
        elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":  # DOCX file
            doc = docx.Document(file)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        else:
            st.error("Unsupported file type!")
            return ""

    # Streamlit App
    st.title("📄 Document Comparison App")
    st.write("Easily compare the content and similarity of two documents in an elegant layout.")

    # File Upload
    col1, col2 = st.columns(2)
    with col1:
        file1 = st.file_uploader("Upload First Document", type=["txt", "pdf", "docx"])
    with col2:
        file2 = st.file_uploader("Upload Second Document", type=["txt", "pdf", "docx"])

    if file1 and file2:
        # Read files
        text1 = read_file(file1)
        text2 = read_file(file2)

        if text1 and text2:
            # Preprocess text
            tokens1 = preprocess_text(text1)
            tokens2 = preprocess_text(text2)

            # Calculate similarity
            similarity_score = calculate_similarity(text1, text2)

            # Find overlapping keywords
            overlapping_keywords = find_overlapping_keywords(tokens1, tokens2)

            # Display Results
            st.subheader("📊 Results Summary")
            st.metric("Similarity Score", f"{similarity_score}%", delta="High" if similarity_score > 80 else "Low")

            st.subheader("🔑 Overlapping Keywords")
            if overlapping_keywords:
                st.write("The following keywords are common in both documents:")
                st.write(
                    ", ".join([f"**{word}** ({count} occurrences)" for word, count in overlapping_keywords.items()])
                )
            else:
                st.write("No overlapping keywords found.")

            # Side-by-Side View
            st.subheader("📜 Document Comparison")
            col1, col2 = st.columns(2)
            with col1:
                st.text_area("Document 1", text1, height=300, key="doc1", disabled=True)
            with col2:
                st.text_area("Document 2", text2, height=300, key="doc2", disabled=True)

            # Decorative Divider
            st.markdown("---")
            st.success("Comparison Completed Successfully! 🎉")

import streamlit as st
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
from transformers import BlipForConditionalGeneration


def chatbot_page9():

    # Load the BLIP model and processor
    @st.cache_resource
    def load_model():
        processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
        model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
        return processor, model

    processor, model = load_model()

    # Caption generation function
    def generate_caption(image):
        inputs = processor(images=image, return_tensors="pt").to("cpu")
        outputs = model.generate(**inputs)
        caption = processor.decode(outputs[0], skip_special_tokens=True)
        return caption

    # Streamlit App
    st.title("🖼️ Text-to-Image Caption Generator")
    st.write("Upload an image, and the app will generate a caption for it.")

    # Upload image
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Generate caption
        with st.spinner("Generating caption..."):
            caption = generate_caption(image)

        st.subheader("Generated Caption")
        st.write(f"**{caption}**")

        # Option to refine the caption
        st.subheader("Refine Caption")
        refined_caption = st.text_input("Modify the generated caption:", value=caption)

        if refined_caption:
            st.success("Caption updated successfully!")
            st.write(f"**Refined Caption:** {refined_caption}")


# Main Application Logic
def main():
    init_db()
    st.sidebar.title("Navigation")
    if not st.session_state["login_status"]:
        page = st.sidebar.selectbox("Choose a page", ["Login", "Register"])
        if page == "Login":
            login_page()
        elif page == "Register":
            registration_page()
    else:
        menu = st.sidebar.radio("Navigate to", ["Home", "Searching Chatbot", "PDF Q-A Chatbot","Image to PDF","ocr","Auto","text summ","Image Enhancement","Document comparison","Text-to-Image caption generator","About", "Settings"])
        if menu == "Home":
            home_page()
        elif menu == "Searching Chatbot":
            chatbot_page1()
        elif menu == "PDF Q-A Chatbot":
            chatbot_page2()
        elif menu == "Image to PDF":
            chatbot_page3()
        elif menu == "ocr":
            chatbot_page4()
        elif menu == "Auto":
            chatbot_page5()
        elif menu == "text summ":
            chatbot_page6()
        elif menu == "Image Enhancement":
            chatbot_page7()
        elif menu == "Document comparison":
            chatbot_page8()
        elif menu == "Text-to-Image caption generator":
            chatbot_page9()
        elif menu == "About":
            about_page()
        elif menu == "Settings":
            settings_page()

if __name__ == "__main__":
    main()
