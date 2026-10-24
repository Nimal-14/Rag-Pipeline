import os
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

def load_documents(docs_path="docs"):
    """Load documents from the specified path."""
    printf("Loading documents from path:", docs_path)
    
    if not os.path.exists(docs_path):
        raise FileNotFoundError(f"The specified path '{docs_path}' does not exist.")
    
    loader = DirectoryLoader(
        docs_path
        ,glob="**/*.txt",
        loader_cls=TextLoader)
    
    documents = loader.load()
    
    if lem(documents)==0:
        raise ValueError(f"No documents found in the specified path '{docs_path}'.")
    
    for i,doc in enumerate(documents):
        print(f"\nDocument {i+1}:")
        print(f"  Source: {doc.metadata['source']}")
        print(f"  Content length: {len(doc.page_content)} characters")
        print(f"  Content preview: {doc.page_content[:100]}...")
        print(f"  metadata: {doc.metadata}")
        
    return documents