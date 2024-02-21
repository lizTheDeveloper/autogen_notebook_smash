from langchain_tools import ssh, make_request
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
import os 


template = """Visit the following article and write a quick summary of the content:

{url}"""
prompt = ChatPromptTemplate.from_template(template)

model = ChatOpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
)

chain = prompt | model | StrOutputParser() | make_request

chain.invoke({"url": "https://www.polygon.com/24075023/princess-peach-showtime-nintendo-switch-impressions"})

