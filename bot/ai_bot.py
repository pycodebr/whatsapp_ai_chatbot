import os

from decouple import config

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq


os.environ['GROQ_API_KEY'] = config('GROQ_API_KEY')


class AIBot:

    def __init__(self):
        self.__chat = ChatGroq(model='llama-3.1-70b-versatile')

    def __get_messages(self, history_messages, question):
        messages = []
        for message in history_messages:
            message_class = HumanMessage if message.get('fromMe') else AIMessage
            messages.append(message_class(content=message.get('body')))
        messages.append(HumanMessage(content=question))
        return messages

    def invoke(self, history_messages, question):
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    'system',
                    'Você é um assistente especializado em tirar dúvidas sobre raças de cães. '
                    'Responda sempre em formato markdown de WhatsApp, com emojis e em português brasileiro.',
                ),
                MessagesPlaceholder(variable_name='messages'),
            ]
        )
        chain = prompt | self.__chat | StrOutputParser()
        response = chain.invoke({'messages': self.__get_messages(history_messages, question)})
        return response
