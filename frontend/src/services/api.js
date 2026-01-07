const DEFAULT_BACKEND_URL = 'http://localhost:8000'
const PRODUCTION_BACKEND_URL = 'https://aayushbotv3.onrender.com'

function getBackendBaseUrl() {
    // Priority: 1. Environment variable, 2. Production URL (if deployed), 3. Localhost
    const fromEnv = import.meta?.env?.VITE_BACKEND_URL
    if (fromEnv && String(fromEnv).trim()) {
        return String(fromEnv).trim()
    }

    // Auto-detect if running in production (Vercel)
    const isProduction = import.meta?.env?.PROD || window.location.hostname !== 'localhost'
    return isProduction ? PRODUCTION_BACKEND_URL : DEFAULT_BACKEND_URL
}

export async function login({ username, password }) {
    const baseUrl = getBackendBaseUrl().replace(/\/+$/, '')
    // Backend expects OAuth2PasswordRequestForm (x-www-form-urlencoded) at POST /admin
    const body = new URLSearchParams()
    body.set('username', username)
    body.set('password', password)
    const res = await fetch(`${baseUrl}/admin`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        credentials: 'include',
        body,
    })

    if (!res.ok) {
        let message = `Login failed (${res.status})`
        try {
            const data = await res.json()
            if (typeof data?.detail === 'string') message = data.detail
            if (typeof data?.message === 'string') message = data.message
        } catch {
            // ignore
        }
        throw new Error(message)
    }

    // Allow any response shape (token/json/text). Backend can be implemented later.
    try {
        return await res.json()
    } catch {
        return await res.text()
    }
}

export async function verifyAdmin() {
    const baseUrl = getBackendBaseUrl().replace(/\/+$/, '')
    const res = await fetch(`${baseUrl}/admin`, {
        method: 'GET',
        credentials: 'include',
    })

    if (!res.ok) {
        let message = `Not authenticated (${res.status})`
        try {
            const data = await res.json()
            if (typeof data?.detail === 'string') message = data.detail
        } catch {
            // ignore
        }
        throw new Error(message)
    }

    return await res.json()
}

export async function uploadAdminPdf(file) {
    const baseUrl = getBackendBaseUrl().replace(/\/+$/, '')
    const form = new FormData()
    form.append('pdf', file)

    const res = await fetch(`${baseUrl}/admin/upload`, {
        method: 'POST',
        credentials: 'include',
        body: form,
    })

    if (!res.ok) {
        let message = `Upload failed (${res.status})`
        try {
            const data = await res.json()
            if (typeof data?.detail === 'string') message = data.detail
        } catch {
            // ignore
        }
        throw new Error(message)
    }

    return await res.json()
}

export async function logout() {
    const baseUrl = getBackendBaseUrl().replace(/\/+$/, '')
    const res = await fetch(`${baseUrl}/logout`, {
        method: 'POST',
        credentials: 'include',
    })

    if (!res.ok) {
        let message = `Logout failed (${res.status})`
        try {
            const data = await res.json()
            if (typeof data?.detail === 'string') message = data.detail
        } catch {
            // ignore
        }
        throw new Error(message)
    }

    try {
        return await res.json()
    } catch {
        return await res.text()
    }
}

export async function sendChatMessage(messages, threadId = 'default-thread') {
    const baseUrl = getBackendBaseUrl().replace(/\/+$/, '')
    const res = await fetch(`${baseUrl}/chat`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({
            messages,
            thread_id: threadId,
        }),
    })

    if (!res.ok) {
        let message = `Chat failed (${res.status})`
        try {
            const data = await res.json()
            if (typeof data?.detail === 'string') message = data.detail
        } catch {
            // ignore
        }
        throw new Error(message)
    }

    return await res.json()
}

