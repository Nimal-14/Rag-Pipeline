import os
from py_compile import main
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

def load_documents(docs_path="Docs"):
    """Load documents from the specified path."""
    print(f"Loading documents from path: {docs_path}")
    
    if not os.path.exists(docs_path):
        raise FileNotFoundError(f"The specified path '{docs_path}' does not exist.")
    
    loader = DirectoryLoader(
        docs_path
        ,glob="**/*.txt", #only look for .txt files
        loader_cls=TextLoader)
    
    documents = loader.load()
    
    if len(documents)==0:
        raise ValueError(f"No documents found in the specified path '{docs_path}'.")
    
    for i,doc in enumerate(documents[:2]):
        print(f"\nDocument {i+1}:")
        print(f"  Source: {doc.metadata['source']}")
        print(f"  Content length: {len(doc.page_content)} characters")
        print(f"  Content preview: {doc.page_content[:100]}...")
        print(f"  metadata: {doc.metadata}")
        
    return documents

def split_documents(documents, chunk_size=1000, chunk_overlap=0):
    """Split documents into smaller chunks."""
    print(f"Splitting documents into chunks of size {chunk_size} with overlap {chunk_overlap}.")
    
    text_splitter = CharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    
    chunks = text_splitter.split_documents(documents)
    
    if chunks:
        for i, chunk in enumerate(chunks[:5]):
            print(f"\n--- Chunk {i+1} ---")
            print(f"Source: {chunk.metadata['source']}")
            print(f"Content length: {len(chunk.page_content)} characters")
            print(f"Content:")
            print(chunk.page_content)
            print("-" * 50)
            
            if(len(chunks)>5):
                print(f"...and {len(chunks)-5} more chunks.")
    return chunks



def main():
    print("Starting the ingestion pipeline...")
    documents =load_documents(docs_path="Docs")
    
    chunks = split_documents(documents)

if __name__ == "__main__":
    main()