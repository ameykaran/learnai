# Multi-Message Responses for Agent Tool Calls

## Overview

The onboarding agent now sends **multiple separate messages** for each tool call, providing real-time feedback as the assessment progresses.

## How It Works

### 1. WebSocket Callback System

Each tool in `OnboardingTools` can now send intermediate messages via WebSocket:

```python
class OnboardingTools:
    def __init__(self):
        self.websocket_callback = None  # Set by orchestrator
    
    def set_websocket_callback(self, callback):
        """Register a callback to send messages via WebSocket."""
        self.websocket_callback = callback
    
    def _send_websocket_message(self, message: str):
        """Send immediate message to user."""
        if self.websocket_callback:
            self.websocket_callback(message)
```

### 2. Tool-by-Tool Messages

Each tool sends its output immediately as a separate message:

#### **start_assessment**
Sends: Welcome greeting with assessment details
```
👋 Welcome to your Probability Knowledge Assessment!

I'm here to help determine your current understanding...
```

#### **get_next_question**
Sends: The formatted question
```
**Question 1 of 25** (Difficulty: easy)

What is the probability of getting heads in a fair coin flip?

A) 0.25
B) 0.5
C) 0.75
D) 1.0

Please select your answer (A, B, C, or D):
```

#### **submit_answer**
Sends: Immediate feedback
```
✅ **Correct!** Well done!
```
or
```
❌ **Incorrect.** The correct answer was **B (0.5)**.

💡 In a fair coin flip, each outcome has equal probability of 0.5.
```

#### **finalize_assessment**
Sends: Complete results and profile
```
🎓 **Assessment Complete!**

Here are your results:

Competence Level: Medium
Overall Accuracy: 68%
...
```

### 3. Message Flow Example

User starts assessment → Agent calls tools → User sees messages in real-time:

```
[User] "I'm ready to start"

[Agent Tool: start_assessment] 
👋 Welcome to your Probability Knowledge Assessment!
...

[Agent Tool: get_next_question]
**Question 1 of 25** ...

[User] "B"

[Agent Tool: submit_answer]
✅ **Correct!** Well done!

[Agent Tool: get_next_question]
**Question 2 of 25** ...

[User] "A"

[Agent Tool: submit_answer]
❌ **Incorrect.** The correct answer was **C**.
...

[After 25 questions]

[Agent Tool: finalize_assessment]
🎓 **Assessment Complete!**
Your results: ...
```

### 4. Frontend Handling

The frontend receives a new message type `tool_message`:

```tsx
case 'tool_message':
  // Display the tool output immediately
  addMessage(data.role, data.content, data.metadata)
  // Keep typing indicator for next tool
  setTimeout(() => setIsTyping(true), 100)
  break
```

## Benefits

✅ **Real-time feedback** - User sees results immediately after each answer
✅ **Better UX** - No waiting for all tools to complete
✅ **Progress visibility** - User knows what's happening at each step
✅ **Engagement** - Immediate reinforcement keeps users engaged
✅ **Natural conversation flow** - Feels like chatting, not filling a form

## Implementation Details

### Backend (`api_server/main.py`)

```python
async def handle_onboarding(..., websocket_manager=None):
    # Set up WebSocket callback for tool messages
    if websocket_manager:
        agent.tools_instance.set_websocket_callback(
            lambda msg: asyncio.create_task(
                websocket_manager.send_message(session_id, {
                    "type": "tool_message",
                    "role": "assistant",
                    "content": msg,
                    "metadata": {"source": "tool_output"}
                })
            )
        )
```

### Tools (`agents/onboarding/tools.py`)

Each tool calls `_send_websocket_message()` with formatted content:

```python
@tool
def submit_answer(self, session_id: str, question_id: int, user_answer: str):
    # ... process answer ...
    
    # Format and send feedback immediately
    feedback = get_feedback_prompt(is_correct, correct_answer, explanation)
    self._send_websocket_message(feedback)
    
    return response
```

### Frontend (`chat_frontend/src/components/ChatInterface.tsx`)

```tsx
const handleWebSocketMessage = (data: any) => {
  switch (data.type) {
    case 'tool_message':
      addMessage(data.role, data.content, data.metadata)
      setTimeout(() => setIsTyping(true), 100)
      break
    // ... other cases
  }
}
```

## Testing

1. Start the API server: `./start-api-server.sh`
2. Start the chat frontend: `./start-chat-frontend.sh`
3. Create an onboarding session
4. Answer questions - you'll see:
   - Each question appears immediately after submitting the previous answer
   - Feedback appears instantly
   - Progress messages throughout
   - Final results displayed step-by-step

## Configuration

To disable multi-message mode (send only final response):
```python
# Don't set the WebSocket callback
# The agent will only return the final response
```

## Future Enhancements

- **Progress bars** - Show completion percentage
- **Typing indicators** - Show "Agent is thinking..." between messages
- **Message grouping** - Group related tool messages
- **Timing control** - Add delays for better readability
- **Rich formatting** - Support images, charts in tool messages

## Notes

- WebSocket callback is optional - falls back to single response if not set
- Messages are sent asynchronously - non-blocking
- Frontend automatically scrolls to latest message
- Tool messages are stored in conversation history
- Works with both REST API and WebSocket endpoints
