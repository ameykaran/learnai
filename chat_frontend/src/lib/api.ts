/**
 * API Client for Learning Management System
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
const WS_BASE_URL = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:8000'

export interface Message {
  role: 'user' | 'assistant'
  content: string
  timestamp: string
  metadata?: any
}

export interface SessionInfo {
  session_id: string
  user_id: string
  mode: 'orchestrator' | 'onboarding'
  current_agent?: string
  message_count: number
  has_profile: boolean
}

export interface CreateSessionResponse {
  session_id: string
  user_id: string
  mode: string
  message: string
}

export interface ChatResponse {
  session_id: string
  response: string
  agent?: string
  mode: string
  metadata?: any
}

export interface UserProfile {
  user_id: string
  has_profile: boolean
  profile?: any
  message?: string
}

/**
 * Create a new chat session
 */
export async function createSession(
  userId: string,
  mode: 'orchestrator' | 'onboarding' = 'orchestrator'
): Promise<CreateSessionResponse> {
  const response = await fetch(`${API_BASE_URL}/api/sessions`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ user_id: userId, mode }),
  })

  if (!response.ok) {
    throw new Error(`Failed to create session: ${response.statusText}`)
  }

  return response.json()
}

/**
 * Get session information
 */
export async function getSessionInfo(sessionId: string): Promise<SessionInfo> {
  const response = await fetch(`${API_BASE_URL}/api/sessions/${sessionId}`)

  if (!response.ok) {
    throw new Error(`Failed to get session info: ${response.statusText}`)
  }

  return response.json()
}

/**
 * Send a chat message (REST)
 */
export async function sendMessage(
  sessionId: string,
  message: string,
  context?: any
): Promise<ChatResponse> {
  const response = await fetch(`${API_BASE_URL}/api/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      session_id: sessionId,
      message,
      context,
    }),
  })

  if (!response.ok) {
    throw new Error(`Failed to send message: ${response.statusText}`)
  }

  return response.json()
}

/**
 * Get conversation history
 */
export async function getConversationHistory(sessionId: string): Promise<{
  session_id: string
  history: Message[]
}> {
  const response = await fetch(
    `${API_BASE_URL}/api/sessions/${sessionId}/history`
  )

  if (!response.ok) {
    throw new Error(`Failed to get history: ${response.statusText}`)
  }

  return response.json()
}

/**
 * Get user profile
 */
export async function getUserProfile(userId: string): Promise<UserProfile> {
  const response = await fetch(`${API_BASE_URL}/api/users/${userId}/profile`)

  if (!response.ok) {
    throw new Error(`Failed to get user profile: ${response.statusText}`)
  }

  return response.json()
}

/**
 * Create WebSocket connection
 */
export function createWebSocket(
  sessionId: string,
  onMessage: (data: any) => void,
  onError?: (error: Event) => void,
  onClose?: () => void
): WebSocket {
  const ws = new WebSocket(`${WS_BASE_URL}/ws/${sessionId}`)

  ws.onopen = () => {
    console.log('WebSocket connected')
  }

  ws.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data)
      onMessage(data)
    } catch (error) {
      console.error('Failed to parse WebSocket message:', error)
    }
  }

  ws.onerror = (error) => {
    console.error('WebSocket error:', error)
    onError?.(error)
  }

  ws.onclose = () => {
    console.log('WebSocket disconnected')
    onClose?.()
  }

  return ws
}

/**
 * Send message via WebSocket
 */
export function sendWebSocketMessage(ws: WebSocket, message: string) {
  if (ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({ message }))
  } else {
    throw new Error('WebSocket is not connected')
  }
}
