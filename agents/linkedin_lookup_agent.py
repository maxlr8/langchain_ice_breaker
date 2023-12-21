# pylint: disable-all

import os

from dotenv import load_dotenv
from tools.tools import get_profile_url

from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.agents import initialize_agent, Tool, AgentType

def lookup(name: str) -> str:

    load_dotenv()

    llm = ChatOpenAI(
        temperature=0,
        model_name="gpt-3.5-turbo",
        openai_api_key=os.environ["OPENAI_KEY"],
    )

    template = """Given the full name {name_of_person}, I want you to get me the link of their LinkedIn profile. \
    Your answer should only contain the URL of the profile"""

    tools_for_the_agent = [
        Tool(
            name="Crawl Google for LinkedIn profile page",
            func=get_profile_url,
            description="This is useful for you when you get the LinkedIn Page URL",
        )
    ]

    agent = initialize_agent(
        tools=tools_for_the_agent,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    prompt_template = PromptTemplate(
        template=template, 
        input_variables=["name_of_person"]
    )

    linkedin_username = agent.run(prompt_template.format_prompt(name_of_person=name))

    return linkedin_username
