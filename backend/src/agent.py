import logging
import json
import random
from datetime import datetime
from pathlib import Path
from typing import Annotated

from dotenv import load_dotenv
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    JobProcess,
    MetricsCollectedEvent,
    RoomInputOptions,
    WorkerOptions,
    cli,
    metrics,
    tokenize,
    function_tool,
    RunContext
)
from livekit.plugins import murf, silero, google, deepgram, noise_cancellation
from livekit.plugins.turn_detector.multilingual import MultilingualModel

logger = logging.getLogger("agent")

load_dotenv(".env.local")

# Load tutor content
CONTENT_FILE = Path("../shared-data/day4_tutor_content.json")
tutor_content = []
if CONTENT_FILE.exists():
    with open(CONTENT_FILE, "r") as f:
        tutor_content = json.load(f)
        logger.info(f"Loaded {len(tutor_content)} concepts from {CONTENT_FILE}")
else:
    logger.warning(f"Content file not found: {CONTENT_FILE}")

# Session state
current_mode = None  # 'learn', 'quiz', or 'teach_back'
current_concept = None
current_room = None


# Greeter Agent - Initial agent that routes to learning modes
class GreeterAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are a friendly tutor greeter. Your job is to welcome students and help them choose a learning mode.
            
            You have three learning modes available:
            1. LEARN mode - Where I explain programming concepts to you
            2. QUIZ mode - Where I ask you questions to test your knowledge
            3. TEACH BACK mode - Where you explain concepts back to me
            
            Available concepts:
            - Variables
            - Loops
            - Functions
            - Conditional Statements
            - Arrays and Lists
            
            Ask the user which mode they'd like to start with, or if they want to hear more about each mode.
            Once they choose, use the switch_mode tool to connect them to the appropriate learning agent.
            
            Keep your responses friendly, encouraging, and concise.""",
        )
    
    @function_tool
    async def switch_mode(self, context: RunContext, mode: Annotated[str, "The learning mode: 'learn', 'quiz', or 'teach_back'"]):
        """Switch to a specific learning mode.
        
        Args:
            mode: The learning mode to switch to ('learn', 'quiz', or 'teach_back')
        """
        global current_mode
        mode = mode.lower().strip()
        
        if mode not in ['learn', 'quiz', 'teach_back']:
            return f"Sorry, '{mode}' is not a valid mode. Please choose 'learn', 'quiz', or 'teach back'."
        
        current_mode = mode
        logger.info(f"Switching to mode: {mode}")
        
        # Trigger agent handoff
        if mode == 'learn':
            await context.start_agent(LearnAgent())
            return "Switching you to Learn mode with Matthew..."
        elif mode == 'quiz':
            await context.start_agent(QuizAgent())
            return "Switching you to Quiz mode with Alicia..."
        else:  # teach_back
            await context.start_agent(TeachBackAgent())
            return "Switching you to Teach Back mode with Ken..."


# Learn Mode Agent - Explains concepts (Voice: Matthew)
class LearnAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are Matthew, a patient and clear programming tutor in LEARN mode.
            
            Your role is to explain programming concepts from the content file in a clear, beginner-friendly way.
            Use analogies and examples to make concepts easy to understand.
            
            After explaining a concept, ask if the student has questions or if they'd like to:
            - Learn another concept
            - Switch to Quiz mode to test themselves
            - Switch to Teach Back mode to explain it themselves
            
            Keep explanations concise but thorough. Use the get_concept tool to retrieve concept information.
            
            Your voice is warm, encouraging, and supportive.""",
        )
    
    @function_tool
    async def get_concept(self, context: RunContext, concept_id: Annotated[str, "The concept ID: 'variables', 'loops', 'functions', 'conditionals', or 'arrays'"]):
        """Get a concept to explain.
        
        Args:
            concept_id: The ID of the concept to retrieve
        """
        global current_concept
        
        concept = next((c for c in tutor_content if c['id'] == concept_id.lower()), None)
        if not concept:
            return f"I don't have information about '{concept_id}'. Available concepts are: variables, loops, functions, conditionals, and arrays."
        
        current_concept = concept
        logger.info(f"Explaining concept: {concept['title']}")
        
        return f"Let me explain {concept['title']}. {concept['summary']} Do you have any questions about this?"
    
    @function_tool
    async def switch_to_quiz(self, context: RunContext):
        """Switch to Quiz mode."""
        global current_mode
        current_mode = 'quiz'
        await context.start_agent(QuizAgent())
        return "Switching to Quiz mode with Alicia..."
    
    @function_tool
    async def switch_to_teach_back(self, context: RunContext):
        """Switch to Teach Back mode."""
        global current_mode
        current_mode = 'teach_back'
        await context.start_agent(TeachBackAgent())
        return "Switching to Teach Back mode with Ken..."


# Quiz Mode Agent - Asks questions (Voice: Alicia)
class QuizAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are Alicia, an enthusiastic quiz master in QUIZ mode.
            
            Your role is to test the student's knowledge by asking them questions about programming concepts.
            Use the sample questions from the content file, or create variations.
            
            After they answer:
            - Give positive, encouraging feedback
            - Gently correct any misconceptions
            - Offer to quiz them on another topic or switch modes
            
            Available concepts to quiz on:
            - Variables
            - Loops
            - Functions  
            - Conditional Statements
            - Arrays and Lists
            
            Keep the atmosphere fun and low-pressure. Learning is about progress, not perfection!
            
            Your voice is energetic, supportive, and motivating.""",
        )
    
    @function_tool
    async def ask_question(self, context: RunContext, concept_id: Annotated[str, "The concept to quiz on"]):
        """Ask a quiz question about a concept.
        
        Args:
            concept_id: The concept ID to quiz on
        """
        global current_concept
        
        concept = next((c for c in tutor_content if c['id'] == concept_id.lower()), None)
        if not concept:
            return f"I don't have questions about '{concept_id}'. Let's try: variables, loops, functions, conditionals, or arrays."
        
        current_concept = concept
        logger.info(f"Quizzing on concept: {concept['title']}")
        
        return f"Here's your question about {concept['title']}: {concept['sample_question']}"
    
    @function_tool
    async def switch_to_learn(self, context: RunContext):
        """Switch to Learn mode."""
        global current_mode
        current_mode = 'learn'
        await context.start_agent(LearnAgent())
        return "Switching to Learn mode with Matthew..."
    
    @function_tool
    async def switch_to_teach_back(self, context: RunContext):
        """Switch to Teach Back mode."""
        global current_mode
        current_mode = 'teach_back'
        await context.start_agent(TeachBackAgent())
        return "Switching to Teach Back mode with Ken..."


# Teach Back Mode Agent - Student explains concepts (Voice: Ken)
class TeachBackAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are Ken, a supportive coach in TEACH BACK mode.
            
            Your role is to ask the student to explain programming concepts back to you, as if they were teaching.
            This is the most effective way to learn - by teaching!
            
            When a student explains a concept:
            - Listen actively and encourage them
            - Ask follow-up questions if they miss key points
            - Give qualitative feedback: "Great job!", "You got the main idea!", "Let me add one thing..."
            - Don't be overly critical - focus on what they got right
            
            After they teach you:
            - Offer to let them teach another concept
            - Suggest switching to Learn mode if they struggled
            - Suggest Quiz mode to reinforce learning
            
            Your voice is calm, patient, and genuinely interested in their explanation.""",
        )
    
    @function_tool
    async def prompt_teaching(self, context: RunContext, concept_id: Annotated[str, "The concept for student to teach"]):
        """Prompt the student to teach a concept.
        
        Args:
            concept_id: The concept the student should explain
        """
        global current_concept
        
        concept = next((c for c in tutor_content if c['id'] == concept_id.lower()), None)
        if not concept:
            return f"I don't have that concept. Try: variables, loops, functions, conditionals, or arrays."
        
        current_concept = concept
        logger.info(f"Student teaching concept: {concept['title']}")
        
        return f"Okay, I'm ready to learn! Please explain {concept['title']} to me as if I've never heard of it before. Take your time and use examples if you'd like."
    
    @function_tool
    async def give_feedback(self, context: RunContext, feedback_type: Annotated[str, "Type of feedback: 'excellent', 'good', or 'needs_work'"]):
        """Give feedback on the student's explanation.
        
        Args:
            feedback_type: The quality of the explanation
        """
        feedback_messages = {
            'excellent': "Excellent explanation! You really understand this concept. You explained it clearly and included good examples. Well done!",
            'good': "Good job! You got the main idea across. Let me just add a couple of points to make it even stronger...",
            'needs_work': "I can see you're on the right track. Let me help clarify a few points, and then maybe you'd like to try again or switch to Learn mode for a refresher?"
        }
        
        return feedback_messages.get(feedback_type.lower(), feedback_messages['good'])
    
    @function_tool
    async def switch_to_learn(self, context: RunContext):
        """Switch to Learn mode."""
        global current_mode
        current_mode = 'learn'
        await context.start_agent(LearnAgent())
        return "Switching to Learn mode with Matthew..."
    
    @function_tool
    async def switch_to_quiz(self, context: RunContext):
        """Switch to Quiz mode."""
        global current_mode
        current_mode = 'quiz'
        await context.start_agent(QuizAgent())
        return "Switching to Quiz mode with Alicia..."


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


async def entrypoint(ctx: JobContext):
    global current_room, current_mode, current_concept
    current_room = ctx.room
    
    # Reset session state when starting
    current_mode = None
    current_concept = None
    
    # Logging setup
    ctx.log_context_fields = {
        "room": ctx.room.name,
    }

    # Create session factory that can be reused for different agents
    def create_session(agent_type: str):
        # Choose voice based on agent type
        voice_map = {
            'greeter': 'en-US-matthew',  # Greeter uses Matthew
            'learn': 'en-US-matthew',     # Learn mode uses Matthew
            'quiz': 'en-US-alicia',       # Quiz mode uses Alicia
            'teach_back': 'en-US-ken'     # Teach back mode uses Ken
        }
        
        voice = voice_map.get(agent_type, 'en-US-matthew')
        logger.info(f"Creating session for {agent_type} with voice {voice}")
        
        return AgentSession(
            stt=deepgram.STT(model="nova-3"),
            llm=google.LLM(model="gemini-2.5-flash"),
            tts=murf.TTS(
                voice=voice,
                style="Conversation",
                tokenizer=tokenize.basic.SentenceTokenizer(min_sentence_len=2),
                text_pacing=True
            ),
            turn_detection=MultilingualModel(),
            vad=ctx.proc.userdata["vad"],
            preemptive_generation=True,
        )

    # Start with Greeter agent (Matthew voice)
    session = create_session('greeter')

    # Metrics collection
    usage_collector = metrics.UsageCollector()

    @session.on("metrics_collected")
    def _on_metrics_collected(ev: MetricsCollectedEvent):
        metrics.log_metrics(ev.metrics)
        usage_collector.collect(ev.metrics)

    async def log_usage():
        summary = usage_collector.get_summary()
        logger.info(f"Usage: {summary}")

    ctx.add_shutdown_callback(log_usage)

    # Start the session with Greeter agent
    greeter = GreeterAgent()
    
    await session.start(
        agent=greeter,
        room=ctx.room,
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    # Join the room and connect to the user
    await ctx.connect()


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))
