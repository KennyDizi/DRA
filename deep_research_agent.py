from gpt_researcher import GPTResearcher
from gpt_researcher.utils.enum import ReportType, Tone
import asyncio

async def main():
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

    # Initialize researcher with deep research type
    researcher = GPTResearcher(
        query=prompt,  # Use the prompt from file
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
