import axios from "axios"

function authHeaders(token: string) {
  return {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  }
}

function contentHeaders(token: string) {
  return {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      Authorization: `Bearer ${token}`,
    },
  }
}

export const prxy = {
  async proxyGet(token: string, proxy: string) {
    return await axios.get(
      `${process.env.apiUrl}/api/v1/proxy/${proxy}`,
      authHeaders(token)
    )
  },
  async proxyGetBlob(token: string, proxy: string) {
    return await axios.get(
      `${process.env.apiUrl}/api/v1/proxy/${proxy}`,
      authHeaders(token)
    )
  },
  async proxyPost(token: string, proxy: string, data: object) {
    return await axios.post(
      `${process.env.apiUrl}/api/v1/proxy/${proxy}`,
      data,
      authHeaders(token)
    )
  },
}
