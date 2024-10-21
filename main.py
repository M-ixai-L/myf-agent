from __future__ import annotations

import logging

from livekit.agents import (
    AutoSubscribe,
    JobContext,
    WorkerOptions,
    cli,
    llm,
)
from livekit.agents.multimodal import MultimodalAgent
from livekit.plugins import openai


logger = logging.getLogger("myagent")
logger.setLevel(logging.INFO)

async def entrypoint(ctx: JobContext):
    logger.info("starting entrypoint")

    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    participant = await ctx.wait_for_participant()

    model = openai.realtime.RealtimeModel(
        api_key="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",
        instructions="You are a helpful assistant",
        voice="shimmer",
        temperature=0.8,
        modalities=["audio", "text"],
    )
    assistant = MultimodalAgent(model=model)
    assistant.start(ctx.room)

    logger.info("starting agent")

    session = model.sessions[0]
    session.conversation.item.create(
      llm.ChatMessage(
        role="user",
        content="You are a voice assistant created by LiveKit. Your interface with users will be voice. "
                "You should use short and concise responses, and avoiding usage of unpronouncable punctuation."
                "Use the provided context to answer the user's question if needed.",
      )
    )
    session.response.create()

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, agent_name='Simple Agent'))
