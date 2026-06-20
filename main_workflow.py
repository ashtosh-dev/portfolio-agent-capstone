import asyncio
import os
import sys
from google.adk import Workflow

# Import agents
from agents.context_agent import context_agent
from agents.quant_agent import quant_agent
from agents.strategist_agent import strategist_agent

from google.adk.runners import InMemoryRunner
from google.genai.types import Content, Part


from google.adk.workflow import node
from google.adk import Context
from typing import Any

@node(name="portfolio_orchestrator", rerun_on_resume=True)
async def portfolio_orchestrator(ctx: Context, node_input: Any) -> str:
    # Extract prompt text
    request_text = node_input
    if hasattr(node_input, "parts") and node_input.parts:
        request_text = "".join([p.text for p in node_input.parts if hasattr(p, "text") and p.text])
        
    # 1. Context Agent fetches live Yahoo Finance data
    context_output = await ctx.run_node(context_agent, node_input=request_text)
    
    # 2. Quant Agent computes weighted returns and expense ratios
    quant_output = await ctx.run_node(quant_agent, node_input=context_output)
    
    # 3. Strategist Agent receives Context and Quant data explicitly
    combined_prompt = f"""Please synthesize the following data into the final client report:
    
User request:
{request_text}

Live Market Data from Context Agent:
{context_output}

Quantitative calculations from Quant Agent:
{quant_output}
"""
    final_report = await ctx.run_node(strategist_agent, node_input=combined_prompt)
    return final_report

def main():
    # Prompt the user for input or use a default investment request
    default_prompt = (
        "Create an investment portfolio with 60% VOO (equity) and 40% AGG (bonds). "
        "Calculate the 1-year and 5-year annualized returns, the weighted expense ratio, "
        "and present a client-ready report."
    )
    
    user_prompt = sys.argv[1] if len(sys.argv) > 1 else default_prompt
    
    print("=" * 80)
    print("Starting Portfolio Strategist Workflow...")
    print(f"Request: {user_prompt}")
    print("=" * 80)
    
    # Check for GEMINI_API_KEY or Vertex AI credentials
    if not os.environ.get("GEMINI_API_KEY") and not os.environ.get("GOOGLE_API_KEY"):
        print("\n[WARNING] Neither GEMINI_API_KEY nor GOOGLE_API_KEY environment variables are set.")
        print("The workflow execution might fail if credentials are required by the ADK runtime.")
        print("Please export your API key before running: export GEMINI_API_KEY='your-api-key'\n")
        
    try:
        # Initialize InMemoryRunner with the workflow graph
        runner = InMemoryRunner(node=portfolio_orchestrator)
        runner.auto_create_session = True
        
        print("\nExecuting workflow steps...")
        # Wrap the user's raw string request into a proper Content object
        wrapped_message = Content(
            role="user",
            parts=[Part(text=user_prompt)]
        )
        
        # Execute the workflow using the runner
        events = runner.run(
            user_id="default_user",
            session_id="default_session",
            new_message=wrapped_message
        )
        
        from rich.console import Console
        from rich.markdown import Markdown
        
        console = Console()
        
        # Suppress intermediate console output and collect/render final report
        with console.status("[bold green]Executing Portfolio Strategist Workflow...") as status:
            final_report = ""
            current_agent = None
            
            for event in events:
                # Update status based on who is authoring the event
                if event.author and event.author != current_agent and event.author != "user":
                    current_agent = event.author
                    if current_agent == "context_agent":
                        status.update("[bold blue]Researcher (Context Agent) is pulling market data...")
                    elif current_agent == "quant_agent":
                        status.update("[bold cyan]Number Cruncher (Quant Agent) is executing calculations...")
                    elif current_agent == "strategist_agent":
                        status.update("[bold magenta]Orchestrator (Strategist Agent) is synthesizing final report...")
                
                # Accumulate the strategist report text
                if event.author == "strategist_agent":
                    if hasattr(event, "content") and event.content:
                        if hasattr(event.content, "parts") and event.content.parts:
                            for part in event.content.parts:
                                if hasattr(part, "text") and part.text:
                                    final_report += part.text
                        else:
                            final_report += str(event.content)
                    elif hasattr(event, "text") and event.text:
                        final_report += event.text
                        
        console.print("\n[bold green]Workflow Completed Successfully.[/bold green]\n")
        console.print("[bold magenta]FINAL SYNTHESIZED PORTFOLIO REPORT:[/bold magenta]\n")
        console.print("=" * 80)
        if final_report.strip():
            console.print(Markdown(final_report))
        else:
            console.print("[bold red]No report output was generated by the Strategist Agent.[/bold red]")
        console.print("=" * 80)
        
    except Exception as e:
        print(f"\nExecution failed: {str(e)}")
        print("\nIf this is a dependency/API key issue, you can inspect the agent/tool files in:")
        print("  - agents/context_agent.py (Researcher)")
        print("  - agents/quant_agent.py (Number Cruncher)")
        print("  - agents/strategist_agent.py (Orchestrator)")
        print("  - tools/mcp_client.py (Data Client)")
        print("  - tools/python_executor.py (Sandbox Executor)")

if __name__ == "__main__":
    main()
