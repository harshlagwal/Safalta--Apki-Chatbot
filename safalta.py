import streamlit as st
import sqlite3
import openai  # Corrected Import

# DeepSeek API settings
DEEPSEEK_API_KEY = "sk - xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # Replace with your API key
DEEPSEEK_API_URL = "https://openrouter.ai/api/v1"

# Configure OpenAI with DeepSeek API
openai.api_key = DEEPSEEK_API_KEY
openai.base_url = DEEPSEEK_API_URL

# Function to generate a career roadmap
def generate_roadmap(goals):
    goals = goals.lower()
    if "data scientist" in goals:
        return """
        Here’s your roadmap to become a Data Scientist:
        1. Learn Python and Statistics.
        2. Take online courses in Data Science.
        3. Work on real-world projects.
        4. Build a portfolio and apply for internships.
        """
    elif "software engineer" in goals:
        return """
        Here’s your roadmap to become a Software Engineer:
        1. Learn Programming (Python, Java, etc.).
        2. Study Data Structures and Algorithms.
        3. Build projects and contribute to open source.
        4. Prepare for technical interviews.
        """
    elif "graphic designer" in goals:
        return """
        Here’s your roadmap to become a Graphic Designer:
        1. Learn design tools like Adobe Photoshop and Illustrator.
        2. Study color theory and typography.
        3. Build a portfolio with sample projects.
        4. Apply for internships or freelance work.
        """
    elif "data analyst" in goals:
        return """
        Here’s your roadmap to become a Data Analyst:
        1. Learn Excel, SQL, and Python.
        2. Take courses in data visualization (e.g., Tableau, Power BI).
        3. Work on real-world datasets.
        4. Apply for entry-level data analyst roles.
        """
    else:
        return "I’m still learning about this career. Let me find more information for you!"

# Function to save user information in a database
def save_user_info(name, age, education, interests, skills, goals):
    conn = sqlite3.connect("career_bot.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            name TEXT,
            age TEXT,
            education TEXT,
            interests TEXT,
            skills TEXT,
            goals TEXT
        )
    """)
    cursor.execute("""
        INSERT INTO users (name, age, education, interests, skills, goals)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, age, education, interests, skills, goals))
    conn.commit()
    conn.close()

# Function to ask DeepSeek for career advice
def ask_deepseek(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="deepseek/deepseek-r1:free",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as err:
        st.error(f"Error: {err}")
        return "Sorry, I couldn't process your request. Please try again."

# Streamlit App
def main():
    # Set page title and icon
    st.set_page_config(page_title="Safalta Apki", page_icon="🚀")

    # Add a cool header
    st.markdown(
        """
        <style>
        .header {
            font-size: 40px;
            font-weight: bold;
            color: #4CAF50;
            text-align: center;
            padding: 20px;
        }
        </style>
        <div class="header">Safalta Apki 🚀</div>
        """,
        unsafe_allow_html=True
    )

    st.write("Welcome to your personalized career guidance chatbot! Yeh app aapko apne career goals achieve karne mein madad karega.")

    # Use columns for better layout
    col1, col2 = st.columns(2)

    with col1:
        st.header("User Information")
        name = st.text_input("What's your name?")
        age = st.text_input("How old are you?")
        education = st.text_input("What's your current education level?")

    with col2:
        st.header("Career Details")
        interests = st.text_input("What are your interests?")
        skills = st.text_input("What skills do you have?")
        career_options = [
            "Software Engineer",
            "Data Scientist",
            "Graphic Designer",
            "Data Analyst",
            "Other"
        ]
        goals = st.selectbox("Select your career goal:", career_options)

    if st.button("Submit"):
        # Save user information to the database
        save_user_info(name, age, education, interests, skills, goals)
        st.success("Information saved successfully!")

        # Generate and display the roadmap
        st.header("Your Career Roadmap")
        roadmap = generate_roadmap(goals)
        st.write(roadmap)

    # Chat interface
    st.header("Chat with Safalta Apki")
    user_input = st.text_input("Ask me anything about your career:")
    if user_input:
        response = ask_deepseek(user_input)
        st.write(f"Safalta Apki: {response}")

# Run the Streamlit app
if __name__ == "__main__":
    main()
