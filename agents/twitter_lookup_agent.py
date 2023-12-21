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

    template = """Given the full name {name_of_person}, I want you to find a link to their Twitter profile page, and extract their username from it. \
    Your answer should only give me the person's username."""

    tools_for_the_agent = [
        Tool(
            name="Crawl Google for Twitter profile page",
            func=get_profile_url,
            description="This is useful for you when you get the Twitter Page URL",
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

    Twitter_username = agent.run(prompt_template.format_prompt(name_of_person=name))

    return Twitter_username
