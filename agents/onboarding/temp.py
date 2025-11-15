from strands import Agent
from strands.models import BedrockModel
from strands.models.gemini import GeminiModel
from botocore.config import Config as BotocoreConfig
import os

print(os.getenv("AWS_SESSION_TOKEN"))


# Create a boto client config with custom settings
boto_config = BotocoreConfig(
    retries={"max_attempts": 3, "mode": "standard"},
    connect_timeout=5,
    read_timeout=60
)

# Create a configured Bedrock model
model = BedrockModel(
    model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
    temperature=0.3,
    top_p=0.8,
    stop_sequences=["###", "END"],
    boto_client_config=boto_config,
)


# model = GeminiModel(
#     client_args={
#         "api_key": os.getenv("GEMINI_API_KEY")
#     },
#     model_id="gemini-2.5-flash-lite",
# )

# Create an agent with the configured model
agent = Agent(model=model)

# Use the agent
response = agent("Write a short story about an AI assistant.")