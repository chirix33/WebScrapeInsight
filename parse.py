from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

model = OllamaLLM(model="llama3.2")

template = (
    "You are tasked with making the following text content readable and robust: {content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Organize Text:** Only organize the information into a robust and readable format. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Original Response:** If there is no way to organize the information, leave it as it is and include it."
    "4. **Direct Data Only:** Your output should contain only the text that is given, with no other text."
) 

# template = (
#     "You are tasked with making the following text content readable and robust: {content}. "
#     "Please follow these instructions carefully: \n\n"
#     "1. **Organize Text:** Only organize the information into a robust and readable format. "
#     "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
#     "3. **Original Response:** If there is no way to organize the information, leave it as it is and include it."
#     "4. **Direct Data Only:** Your output should contain only the text that is given, with no other text."
#     "5. **No Summarization:** Do not summarize the text, only organize it. Use the exact the text given. "
# ) 

def parse_with_ollama(chunks):
    prompt = ChatPromptTemplate([template])
    chain = prompt | model

    parsed_results = []

    for i, chunk in enumerate(chunks, start=1):
        result = chain.invoke(
            {"content": chunk}
            )
        print(f"Chunk {i} of {len(chunks)} done!")
        parsed_results.append(result)
    return "\n".join(parsed_results)