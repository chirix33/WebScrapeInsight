from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

model = OllamaLLM(model="llama3.2")

template = (
    "You are tasked with making this content more human readable: {content}. "
    "Do **not** add or edit any text whatsoever. "
) 

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