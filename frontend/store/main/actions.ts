import { api } from "@/api"
import {
  saveLocalToken,
  removeLocalToken,
  saveRefreshToken,
  removeRefreshToken,
  tokenExpired,
} from "@/utilities"
import { AxiosError } from "axios"
import { IUserOpenProfileCreate } from "@/interfaces"
import { AppNotification } from "./state"

export default {
  async logIn(
    { commit, dispatch },
    payload: { username: string; password: string }
  ) {
    try {
      const response = await api.logInGetToken(
        payload.username,
        payload.password
      )
      const token = response.data.access_token
      const refresh = response.data.refresh_token
      if (token && refresh) {
        dispatch("setAllTokens", { token, refresh })
        await commit("setToken", token)
        await commit("setLoggedIn", true)
        await commit("setLogInError", false)
        await dispatch("getUserProfile")
      } else {
        await dispatch("logOut")
      }
    } catch (error) {
      commit("setLogInError", true)
      await dispatch("logOut")
    }
  },
  setAllTokens({ state }, payload: { token: string; refresh: string }) {
    // https://stackoverflow.com/a/43620820/295606
    ;(this as any).$cookies.set("token", payload.token, {
      path: "/",
      maxAge: 60 * 60 * 24 * 8,
      // httpOnly: true,
      secure: true,
    })
    ;(this as any).$cookies.set("refresh", payload.refresh, {
      path: "/",
      maxAge: 60 * 60 * 24 * 90,
      // httpOnly: true,
      secure: true,
    })
    if (process.client) {
      saveLocalToken(payload.token)
      saveRefreshToken(payload.refresh)
    }
  },
  setLocalTokens() {
    if (process.client) {
      saveLocalToken((this as any).$cookies.get("token"))
      saveRefreshToken((this as any).$cookies.get("refresh"))
    }
  },
  async refreshTokens({ commit, dispatch }) {
    try {
      let refresh = (this as any).$cookies.get("refresh")
      const response = await api.getRefreshedToken(refresh)
      const token = response.data.access_token
      refresh = response.data.refresh_token
      if (token && refresh) {
        dispatch("setAllTokens", { token, refresh })
        await commit("setToken", token)
        await commit("setLoggedIn", true)
        await commit("setLogInError", false)
        await dispatch("getUserProfile")
      } else {
        await dispatch("logOut")
      }
    } catch (error) {
      commit("setLogInError", true)
      await dispatch("logOut")
    }
  },
  async getUserProfile({ commit, dispatch, state }) {
    try {
      const response = await api.getMe(state.token)
      if (response.data) {
        await commit("setUserProfile", response.data)
      }
    } catch (error) {
      await dispatch("checkApiError", error)
    }
  },
  async updateUserProfile({ commit, dispatch, state }, payload) {
    try {
      const loadingNotification = { content: "Saving...", showProgress: true }
      await commit("addNotification", loadingNotification)
      const response = await api.updateMe(state.token, payload)
      await commit("setUserProfile", response.data)
      await commit("removeNotification", loadingNotification)
      await commit("addNotification", {
        content: "Profile successfully updated",
        color: "success",
      })
    } catch (error) {
      await dispatch("checkApiError", error)
    }
  },
  async createUserProfile(
    { commit, dispatch },
    payload: IUserOpenProfileCreate
  ) {
    try {
      const loadingNotification = { content: "Creating...", showProgress: true }
      await commit("addNotification", loadingNotification)
      await api.createMe(payload)
      await commit("removeNotification", loadingNotification)
      await commit("addNotification", {
        content: "Account successfully created",
        color: "success",
      })
    } catch (error) {
      // console.log(error.response)
      await dispatch("checkApiError", error)
    }
  },
  async refreshLoggedIn({ commit, dispatch, state }) {
    let token = state.token
    if (!token) {
      token = (this as any).$cookies.get("token")
    }
    if (token) {
      const hasExpired = tokenExpired(token)
      if (hasExpired) {
        dispatch("refreshTokens")
      } else {
        await commit("setToken", token)
        try {
          await dispatch("getUserProfile")
          await commit("setLoggedIn", true)
        } catch (error) {
          await dispatch("checkApiError", error)
        }
      }
    } else {
      await dispatch("logOut")
    }
  },
  async logOut({ commit }) {
    removeLocalToken()
    removeRefreshToken()
    await commit("setToken", "")
    await commit("setLoggedIn", false)
    await commit("setUserProfile", null)
    ;(this as any).$cookies.remove("token")
    ;(this as any).$cookies.remove("refresh")
  },
  async checkApiError({ dispatch }, payload: AxiosError) {
    // console.log(payload.response)
    if ([400, 401, 403].includes(payload.response!.status)) {
      await dispatch("logOut")
    }
  },
  async addErrorNotification({ commit }, payload: AxiosError) {
    let content
    try {
      content = `${payload.response!.data.detail}`
    } catch {
      content = payload
    }
    await commit("addNotification", {
      content,
      color: "error",
    })
  },
  async removeNotification(
    { commit },
    payload: { notification: AppNotification; timeout: number }
  ) {
    return await new Promise((resolve) => {
      setTimeout(() => {
        commit("removeNotification", payload.notification)
        resolve(true)
      }, payload.timeout)
    })
  },
  async passwordRecovery({ commit, dispatch }, payload: { username: string }) {
    try {
      await Promise.all([
        api.passwordRecovery(payload.username),
        await new Promise<void>((resolve) => setTimeout(() => resolve(), 500)),
      ])
    } catch (error) {}
    // Refactored this ... shouldn't give user indication if their attempt was successful or not
    await dispatch("logOut")
    const loadingNotification = {
      content: "Sending password recovery email",
      showProgress: true,
    }
    await commit("addNotification", loadingNotification)
  },
  async resetPassword(
    { commit, dispatch },
    payload: { password: string; token: string }
  ) {
    const loadingNotification = {
      content: "Resetting password",
      showProgress: true,
    }
    try {
      await commit("addNotification", loadingNotification)
      await api.resetPassword(payload.password, payload.token)
      await commit("removeNotification", loadingNotification)
      await commit("addNotification", {
        content: "Password successfully reset",
        color: "success",
      })
      await dispatch("logOut")
    } catch (error) {
      await commit("removeNotification", loadingNotification)
      await commit("addNotification", {
        color: "error",
        content: "Error resetting password",
      })
    }
  },
}
