async function request(path, { method = 'GET', body } = {}) {
  const res = await fetch(path, {
    method,
    headers: body ? { 'Content-Type': 'application/json' } : undefined,
    body: body ? JSON.stringify(body) : undefined,
    credentials: 'include'
  })

  if (res.status === 204) return null

  const contentType = res.headers.get('content-type') || ''
  const data = contentType.includes('application/json') ? await res.json() : await res.text()

  if (!res.ok) {
    const err = new Error('Request failed')
    err.status = res.status
    err.data = data
    throw err
  }
  return data
}

export const api = {
  me: () => request('/api/auth/me'),
  login: (login, password) => request('/api/auth/login', { method: 'POST', body: { login, password } }),
  register: (login, password) => request('/api/auth/register', { method: 'POST', body: { login, password } }),
  logout: () => request('/api/auth/logout', { method: 'POST' }),

  getHits: () => request('/api/hits'),
  createHit: (x, y, r, fromGraph = false) => request('/api/hits', { method: 'POST', body: { x, y, r, fromGraph } }),
  clearHits: () => request('/api/hits', { method: 'DELETE' })
}
