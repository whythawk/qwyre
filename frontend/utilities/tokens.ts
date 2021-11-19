export const getLocalToken = () => localStorage.getItem("token")

export const saveLocalToken = (token: string) =>
  localStorage.setItem("token", token)

export const removeLocalToken = () => localStorage.removeItem("token")

export const getRefreshToken = () => localStorage.getItem("refresh")

export const saveRefreshToken = (token: string) =>
  localStorage.setItem("refresh", token)

export const removeRefreshToken = () => localStorage.removeItem("refresh")
