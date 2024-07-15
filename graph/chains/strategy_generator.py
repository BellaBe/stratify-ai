from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_groq import ChatGroq


class StrategyGeneratorChain:
    def __init__(self):
        self.llm = ChatGroq(model="llama3-8b-8192")
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system",
                 """
                    Role: You are an AI language model specialized in video content analysis and strategy extraction. Your task is to analyze the provided transcript of a YouTube video to determine if a strategy is described. If a strategy is detected, return it in the form of a list of actionable items. Otherwise, return that no strategy is detected.
                        
                    Target Audience:
                    - Businesses analyzing competitor strategies from YouTube videos
                    - Educators extracting teaching strategies from educational videos
                    - Individuals looking to implement strategies from tutorial videos

                    Instructions: Follow these step-by-step instructions to achieve the objective:
                    - Start with analyzing the provided transcript of the video.
                    - Identify any strategies described in the transcript.
                    - If a strategy is identified, list the actionable items.
                    - If no strategy is identified, respond with "No strategy detected.
                    
                    Return the strategy found or "No strategy detected": 
                """
                ),
                ("human",
                 "Transcript: {transcript}"
                 )
            ]
        )
        self.chain = self.prompt | self.llm | StrOutputParser()

    def invoke(self, input_data):
        return self.chain.invoke(input_data)
