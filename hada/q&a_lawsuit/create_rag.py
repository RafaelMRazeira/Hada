import torch
import transformers
from langchain.chains import RetrievalQA
from langchain.vectorstores import DeepLake
from langchain.llms import HuggingFacePipeline
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter

text = """ Google opens up its AI language model PaLM to challenge
OpenAI and GPT-3 Google offers developers access to one of its most
advanced AI language models: PaLM. The search giant is launching an
API for PaLM alongside a number of AI enterprise tools it says will
help businesses "generate text, images, code, videos, audio, and
more from simple natural language prompts."
PaLM is a large language model, or LLM, similar to the GPT series
created by OpenAI or Meta's LLaMA family of models. Google first
announced PaLM in April 2022. Like other LLMs, PaLM is a flexible
system that can potentially carry out all sorts of text generation
and editing tasks. You could train PaLM to be a conversational
chatbot like ChatGPT, for example, or you could use it for tasks
like summarizing text or even writing code. (It's similar to
features Google also announced today for its Workspace apps like
Google Docs and Gmail.)
"""
# write text to local file
with open("my_file.txt", "w") as file:
    file.write(text)
# use TextLoader to load text from local file
loader = TextLoader("my_file.txt")
docs_from_file = loader.load()
print(len(docs_from_file))
# 1

# create a text splitter
text_splitter = CharacterTextSplitter(chunk_size=50, chunk_overlap=20)
# split documents into chunks
docs = text_splitter.split_documents(docs_from_file)
print(len(docs))
# 2

model_name = "sentence-transformers/all-mpnet-base-v2"
model_kwargs = {"device": "cpu"}
encode_kwargs = {"normalize_embeddings": False}
embeddings = HuggingFaceEmbeddings(
    model_name=model_name, model_kwargs=model_kwargs, encode_kwargs=encode_kwargs
)

db = DeepLake(embedding_function=embeddings)

db.add_documents(docs)

# create retriever from db
retriever = db.as_retriever()

model_id = "meta-llama/Meta-Llama-3.1-8B-Instruct"
pipeline = transformers.pipeline(
    "text-generation",
    model=model_id,
    model_kwargs={"torch_dtype": torch.bfloat16},
    device_map="auto",
    # max_length=256,
    max_new_tokens=256,
)

llm = HuggingFacePipeline(pipeline=pipeline)
# create a retrieval chain
qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

query = "How Google plans to challenge OpenAI?"
response = qa_chain.run(query)
print(response)

breakpoint()
