from gpt_researcher import GPTResearcher
from gpt_researcher.utils.enum import ReportType, Tone, ReportSource
import asyncio
import os
import argparse
from logger import get_logger

def convert_to_report_source(source_str: str) -> ReportSource:
    """Convert string value to ReportSource enum."""
    return ReportSource(source_str.lower())

SUPPORTED_REPORT_SOURCES = [ReportSource.Web.value, ReportSource.Local.value, ReportSource.Hybrid.value]

logger = get_logger()

async def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run deep research agent.')
    parser.add_argument('--report-source',
                       default=ReportSource.Web.value,
                       choices=SUPPORTED_REPORT_SOURCES,
                       help='Specify data source for the report (local, web or hybrid).')
    args = parser.parse_args()

    # Convert string to enum
    try:
        report_source = convert_to_report_source(args.report_source)
    except ValueError:
        logger.error(f"Invalid report source: {args.report_source}")
        return

    # Read prompt from file
    try:
        with open('prompts.txt', 'r', encoding='utf-8') as file:
            prompt = file.read().strip()
    except FileNotFoundError:
        print("Error: prompts.txt file not found.")
        return
    except Exception as e:
        print(f"Error reading prompts.txt: {e}.")
        return

    logger.info(f"Starting deep research agent with report source: {report_source.value}.")

    document_urls = None
    if report_source in (ReportSource.Hybrid, ReportSource.Local):
        doc_path = os.getenv("DOC_PATH")
        if doc_path is None:
            logger.error("DOC_PATH environment variable is not set.")
            return

        if report_source == ReportSource.Hybrid:
            document_urls = os.getenv("DOCUMENT_URLS")
            if document_urls is not None:
                document_urls = document_urls.split(",")
                logger.info(f"Document URLs: {document_urls}")

    # Get retrievers from environment variable
    retrievers = os.getenv("RETRIEVERS")

    # Initialize researcher with deep research type
    researcher = GPTResearcher(
        query=prompt,
        report_type=ReportType.DeepResearch.value,
        tone=Tone.Formal,
        report_format="markdown",
        report_source=report_source.value,
        document_urls=document_urls,
        headers={
            "retrievers": retrievers
        }
    )

    # Run research
    await researcher.conduct_research()

    # Generate report
    report = await researcher.write_report()
    print(report)

if __name__ == "__main__":
    asyncio.run(main())
