export const getLocalSettings = () => localStorage.getItem("settings")

export const saveLocalSettings = (token: string) =>
  localStorage.setItem("settings", token)

export const removeLocalSettings = () => localStorage.removeItem("settings")
