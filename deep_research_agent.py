from gpt_researcher import GPTResearcher
from gpt_researcher.utils.enum import ReportType, Tone
import asyncio

async def main():
    # Initialize researcher with deep research type
    researcher = GPTResearcher(
        query="I gonna sell my apartment in with 46 square meters, one bed room and one bathroom in the next 6 months. The apartment is in Glory Heights, Vinhomes Grand Park, Thu Duc City, Ho Chi Minh City, Vietnam. What is the best time to sell it?",
        report_type=ReportType.DeepResearch,  # This triggers deep research modd
        tone=Tone.Formal,
        report_format="markdown"
    )

    # Run research
    await researcher.conduct_research()

    # Generate report
    report = await researcher.write_report()
    print(report)

if __name__ == "__main__":
    asyncio.run(main())
