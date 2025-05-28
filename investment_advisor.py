import os
import streamlit as st
from crewai import Agent, Task, Crew
from langchain_groq import ChatGroq

# Set your Groq API key
os.environ["GROQ_API_KEY"] = st.secrets["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"]

# Initialize LLM
llm = ChatGroq(
    api_key=os.environ["GROQ_API_KEY"],
    model_name="llama3-70b-8192",
    temperature=0.5
)

# Streamlit UI
st.title("💸 AI Investment Advisor")
st.write("Get smart investment recommendations based on your age and budget.")

age = st.number_input("Enter your age", min_value=18, max_value=100, value=30)
investment = st.number_input("Enter investment amount (INR)", min_value=10000, step=1000, value=500000)

if st.button("Get Investment Recommendation"):
    # Step 1: Define agents
    risk_assessor = Agent(
        role="Risk Assessor",
        goal="Evaluate user's age and investment amount to determine risk tolerance",
        backstory="An expert in investment strategy and age-based financial planning.",
        allow_delegation=False,
        verbose=False,
        llm=llm
    )

    recommendation_expert = Agent(
        role="Recommendation Engine",
        goal="Give suitable investment options based on user's risk profile",
        backstory="A financial advisor with deep knowledge of mutual funds, stocks, and bonds.",
        allow_delegation=False,
        verbose=False,
        llm=llm
    )

    # Step 2: Define tasks
    task1 = Task(
        description=f"Analyze a user aged {age} with an investment budget of ₹{investment}. Determine their risk category (e.g. high, medium, low).",
        expected_output="A risk profile summary with reasoning.",
        agent=risk_assessor
    )

    task2 = Task(
        description="Based on the risk profile from Task 1, recommend 2–3 suitable investment products (mutual funds, stocks, bonds). Justify each.",
        expected_output="List of investment options with risk-aligned justifications.",
        agent=recommendation_expert
    )

    # Step 3: Run Crew
    crew = Crew(
        agents=[risk_assessor, recommendation_expert],
        tasks=[task1, task2],
        verbose=True
    )

    with st.spinner("🤖 Thinking..."):
        result = crew.kickoff()

    st.subheader("📊 Investment Advice")
    st.write(result)
