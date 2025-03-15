from gpt_researcher import GPTResearcher
from gpt_researcher.utils.enum import ReportType, Tone, ReportSource
import asyncio
import os
import argparse
from logger import get_logger
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_unstructured import UnstructuredLoader

SUPPORTED_REPORT_SOURCES = [ReportSource.Web.value, ReportSource.Hybrid.value]

logger = get_logger()

async def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run deep research agent.')
    parser.add_argument('--report-source',
                       default='web',
                       choices=SUPPORTED_REPORT_SOURCES,
                       help='Specify data source for the report (web or hybrid)')
    parser.add_argument('--collection-name',
                       default='generic-knowledge-base',
                       help='Specify the collection name for the vector store')
    args = parser.parse_args()

    # Read prompt from file
    try:
        with open('prompts.txt', 'r', encoding='utf-8') as file:
            prompt = file.read().strip()
    except FileNotFoundError:
        print("Error: prompts.txt file not found")
        return
    except Exception as e:
        print(f"Error reading prompts.txt: {e}")
        return

    logger.info(f"Starting deep research agent with report source: {args.report_source}.")

    vector_store = None
    if args.report_source == ReportSource.Hybrid.value:
        # Initialize vector store
        embeddings = OpenAIEmbeddings(model="text-embedding-3-large", dimensions=1536)
        FAISS_INDEX_NAME = os.path.join("openworkspace-o1-vecs", f"faiss_index_{args.collection_name}")

        # Check if the index already exists
        if os.path.exists(FAISS_INDEX_NAME):
            logger.info(f"Loading existing FAISS index from {FAISS_INDEX_NAME}.")
            # Load the existing FAISS index
            vector_store = FAISS.load_local(FAISS_INDEX_NAME, embeddings, allow_dangerous_deserialization=True)
        else:
            logger.info(f"Creating a new FAISS index.")

            loader = UnstructuredLoader(file_path=f"openworkspace-o1-docs/introduction.txt")
            docs = loader.load()
            # Create a FAISS index from the text documents
            vector_store = FAISS.from_documents(docs, embeddings)

    # Initialize researcher with deep research type
    researcher = GPTResearcher(
        query=prompt,
        report_type=ReportType.DeepResearch,
        tone=Tone.Formal,
        report_format="markdown",
        report_source=args.report_source,
        vector_store=vector_store
    )

    # Run research
    await researcher.conduct_research()

    # Generate report
    report = await researcher.write_report()
    print(report)

    # Save the FAISS index to disk
    FAISS.save_local(vector_store, FAISS_INDEX_NAME)

if __name__ == "__main__":
    asyncio.run(main())
