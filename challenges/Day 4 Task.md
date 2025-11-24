# Day 4 – Teach-the-Tutor: Active Recall Coach

## Primary Goal (Required)

Build a "Teach-the-Tutor" experience with three learning modes using agent handoffs and different voices.

### Core Requirements

1. **Three learning modes**
   - `learn` – the agent explains a concept (Voice: Matthew)
   - `quiz` – the agent asks you questions (Voice: Alicia)
   - `teach_back` – the agent asks you to explain concepts back (Voice: Ken)

2. **Small course content file**
   - JSON file with programming concepts:
     - Variables
     - Loops
     - Functions
     - Conditional Statements
     - Arrays and Lists

3. **Agent handoffs**
   - Initial greeter agent routes to learning modes
   - Seamless transitions between modes
   - Context preservation during switches
   - User can switch modes at any time

## Implementation Status: ✅ COMPLETE

### What Was Built:

#### Backend (`backend/src/agent.py`)
- ✅ **Greeter Agent** - Initial routing agent (Voice: Matthew)
  - Welcomes students and explains available modes
  - Routes to appropriate mode using `switch_mode` tool
  
- ✅ **Learn Mode Agent** - Explains concepts (Voice: Matthew)
  - Retrieves concepts from JSON content file
  - Explains programming concepts clearly with analogies
  - Offers mode switching to quiz or teach back
  
- ✅ **Quiz Mode Agent** - Tests knowledge (Voice: Alicia)
  - Asks questions from content file
  - Provides encouraging feedback
  - Corrects misconceptions gently
  - Fun, low-pressure atmosphere
  
- ✅ **Teach Back Mode Agent** - Student teaches (Voice: Ken)
  - Prompts student to explain concepts
  - Active listening and follow-up questions
  - Qualitative feedback system
  - Focus on what student got right

#### Content System (`shared-data/day4_tutor_content.json`)
- ✅ 5 programming concepts with detailed summaries
- ✅ Sample questions for each concept
- ✅ Shared across all learning modes

#### Agent Handoff Features
- ✅ Seamless transitions between modes
- ✅ Different Murf Falcon voices per mode:
  - Matthew (Greeter & Learn)
  - Alicia (Quiz)
  - Ken (Teach Back)
- ✅ Context preservation during switches
- ✅ User-initiated mode changes

### Conversation Flow

1. **Greeter Agent** - Matthew welcomes student and explains modes
2. **Mode Selection** - Student chooses learn, quiz, or teach_back
3. **Learn Mode** - Matthew explains concepts from content file
4. **Quiz Mode** - Alicia asks questions and provides feedback
5. **Teach Back Mode** - Ken asks student to explain concepts
6. **Mode Switching** - Student can switch modes at any time

### Content Structure

```json
[
  {
    "id": "variables",
    "title": "Variables",
    "summary": "Variables are like labeled containers that store values...",
    "sample_question": "What is a variable and why is it useful in programming?"
  },
  // ... 4 more concepts
]
```

## Advanced Goals (Optional)

### Advanced Goal 1: Richer Concept Mastery Model
- Track scores and averages per concept
- Store mastery data in session state
- Example structure:
```python
session_state["tutor"]["mastery"]["loops"] = {
    "times_explained": 3,
    "times_quizzed": 4,
    "times_taught_back": 2,
    "last_score": 72,
    "avg_score": 65.3
}
```

### Advanced Goal 2: Teach-back Evaluator Tool
- Helper function to score explanations
- Compare user explanation to concept summary
- Update mastery scores and give targeted feedback

### Advanced Goal 3: Richer Content & Flows
- More concepts and learning paths
- Lightweight learning paths (beginner → intermediate → advanced)
- Practice plans based on weakest concepts

## Resources

- LiveKit Agent Handoffs: https://docs.livekit.io/agents/build/agents-handoffs/
- Context Preservation: https://docs.livekit.io/agents/build/agents-handoffs/#context-preservation
- Example Code: https://github.com/livekit-examples/python-agents-examples/blob/main/complex-agents/medical_office_triage/triage.py
