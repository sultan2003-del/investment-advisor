import streamlit as st
import os
from crewai import Agent, Task, Crew
from langchain_groq import ChatGroq
from langchain.agents import tool

# Setup Groq API Key from Streamlit secrets
os.environ["GROQ_API_KEY"] = st.secrets["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"]

# Create Groq LLM
llm = ChatGroq(api_key=os.environ["GROQ_API_KEY"], model_name="mixtral-8x7b-32768")

# Define agents
risk_agent = Agent(
    role="Risk Assessor",
    goal="Evaluate investment risk based on user's age and capital",
    backstory="Expert in financial planning and retirement investment strategies",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# Define task
def recommend_strategy(age: int, capital: float) -> str:
    task = Task(
        description=f"Recommend an investment strategy for a user aged {age} with a capital of ${capital}",
        expected_output="Clear, beginner-friendly investment recommendation with risk profile",
        agent=risk_agent
    )
    crew = Crew(agents=[risk_agent], tasks=[task], verbose=True)
    result = crew.kickoff()
    return result

# Streamlit UI
st.title("💸 Investment Advisor")
age = st.number_input("Enter your age", min_value=18, max_value=100, value=30)
capital = st.number_input("Enter your investment capital ($)", min_value=100.0, value=10000.0)

if st.button("Get Investment Advice"):
    with st.spinner("Thinking..."):
        recommendation = recommend_strategy(age, capital)
        st.success("Here's your personalized investment advice:")
        st.write(recommendation)
