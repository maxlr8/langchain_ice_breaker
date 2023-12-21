# pylint: disable-all

from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI

from output_parser import summary_parser, ice_breaker_parser, topics_of_interest_parser

llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
llm_creative = ChatOpenAI(temperature=1, model_name="gpt-3.5-turbo")

def get_summary_chain() -> LLMChain:

    summary_template = """
        Given the profile LinkedIn information {information} and Twitter information {twitter_posts} about a person from which I want to create:
        1) A short summary.
        2) 2 interesting facts about them.
        3) A topic that may interest them.
        4) 2 creative ice-breakers to open a conversation with them 
        \n{format_instructions}.
    """

    summary_prompt_template = PromptTemplate(
        input_variables=["information", "twitter_posts"],
        template=summary_template,
        partial_variables={
            "format_instructions": summary_parser.get_format_instructions()
        },
    )

    return LLMChain(llm=llm, prompt=summary_prompt_template)


def get_interests_chain() -> LLMChain:
    interesting_facts_template = """
        Given the profile LinkedIn information {information} and Twitter information {twitter_posts}, 
        I want you to get the top 3 topics that might interest them to instigate a conversation.
        \n{format_instructions}
    """

    interesting_facts_prompt_template = PromptTemplate(
        input_variables=["information", "twitter_posts"],
        template=interesting_facts_template,
        partial_variables={
            "format_instructions": topics_of_interest_parser.get_format_instructions()
        },
    )

    return LLMChain(llm=llm, prompt=interesting_facts_prompt_template)


def get_ice_breaker_chain() -> LLMChain:

    ice_breaker_template = """
        Given the profile LinkedIn information {information} and Twitter information {twitter_posts}, 
        2 creative Ice breakers with them that are derived from their activity on Linkedin and Twitter, preferably on the latest latest tweets.
        \n{format_instructions}
    """

    ice_breaker_prompt_template = PromptTemplate(
        input_variables=["information", "twitter_posts"],
        template=ice_breaker_template,
        partial_variables={
            "format_instructions": ice_breaker_parser.get_format_instructions()
        },
    )

    return LLMChain(llm=llm_creative, prompt=ice_breaker_prompt_template)