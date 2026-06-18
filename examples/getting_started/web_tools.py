# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Example demonstrating web tools using Google Antigravity SDK.

To run:
  python web_tools.py
"""

import asyncio

from google.antigravity import Agent
from google.antigravity import CapabilitiesConfig
from google.antigravity import LocalAgentConfig
from google.antigravity import types


async def main() -> None:
  """Runs the web tools example.

  This function initializes an agent with web search capabilities,
  sends a query about the world population, and prints the agent's response.
  """
  # Configure the agent to use the web search tool.
  config = LocalAgentConfig(
      capabilities=CapabilitiesConfig(
          enabled_tools=[
              types.BuiltinTools.SEARCH_WEB,
          ]
      ),
  )

  async with Agent(config) as my_agent:
    prompt = (
        "What is the current weather and temperature in New York City right"
        " now? Please provide the source."
    )
    print(f"User: {prompt}\n")

    print("Agent is thinking and searching...")
    response = await my_agent.chat(prompt)

    # Await the full aggregated text response.
    response_text = await response.text()
    print(f"\nAgent Response:\n{response_text}")


if __name__ == "__main__":
  asyncio.run(main())
