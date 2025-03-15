from gpt_researcher import GPTResearcher
from gpt_researcher.utils.enum import ReportType, Tone, ReportSource
import asyncio
import os
import argparse
from logger import get_logger

SUPPORTED_REPORT_SOURCES = [ReportSource.Web.value, ReportSource.Local.value, ReportSource.Hybrid.value]

logger = get_logger()

async def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run deep research agent.')
    parser.add_argument('--report-source',
                       default='web',
                       choices=SUPPORTED_REPORT_SOURCES,
                       help='Specify data source for the report (local, web or hybrid)')
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
    if args.report_source == ReportSource.Hybrid.value or args.report_source == ReportSource.Local.value:
        doc_path = os.getenv("DOC_PATH")
        if doc_path is None:
            logger.error("DOC_PATH environment variable is not set.")
            return

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

if __name__ == "__main__":
    asyncio.run(main())
