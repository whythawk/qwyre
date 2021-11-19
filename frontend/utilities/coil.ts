// Manage page redirect after processing the user's authorisation
export const getCoilRoute = () => localStorage.getItem("coilroute")
export const saveCoilRoute = (token: string) =>
  localStorage.setItem("coilroute", token)
export const removeCoilRoute = () => localStorage.removeItem("coilroute")
// Manage the user's coil access token
export const getCoilState = () => localStorage.getItem("coilstate")
export const saveCoilState = (token: string) =>
  localStorage.setItem("coilstate", token)
export const removeCoilState = () => localStorage.removeItem("coilstate")
// Manage the user's coil refresh token
export const getCoilRefresh = () => localStorage.getItem("coilrefresh")
export const saveCoilRefresh = (token: string) =>
  localStorage.setItem("coilrefresh", token)
export const removeCoilRefresh = () => localStorage.removeItem("coilrefresh")
