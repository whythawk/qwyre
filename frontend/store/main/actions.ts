import { AxiosError } from "axios"
import { AppNotification } from "./state"
import { api } from "@/api"
import { tokenExpired, getLocalSettings, saveLocalSettings } from "@/utilities"
import { IUserOpenProfileCreate, IThemeState } from "@/interfaces"

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
        // await commit("setToken", token)
        await commit("setLoggedIn", true)
        await commit("setLogInError", false)
        await dispatch("getUserProfile")
        await dispatch("getCreatorProfile")
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
      maxAge: 60 * 30,
      // httpOnly: true,
      secure: true,
    })
    ;(this as any).$cookies.set("refresh", payload.refresh, {
      path: "/",
      maxAge: 60 * 60 * 24 * 30,
      // httpOnly: true,
      secure: true,
    })
    // if (process.client) {
    //   saveLocalToken(payload.token)
    //   saveRefreshToken(payload.refresh)
    // }
  },
  async refreshTokens({ commit, dispatch }) {
    try {
      let refresh = (this as any).$cookies.get("refresh")
      const response = await api.getRefreshedToken(refresh)
      const token = response.data.access_token
      refresh = response.data.refresh_token
      if (token && refresh) {
        dispatch("setAllTokens", { token, refresh })
        // await commit("setToken", token)
        await commit("setLoggedIn", true)
        await commit("setLogInError", false)
        // await dispatch("getUserProfile")
        // await dispatch("getCreatorProfile")
      } else {
        await dispatch("logOut")
      }
    } catch (error) {
      commit("setLogInError", true)
      await dispatch("logOut")
    }
  },
  async getUserProfile({ state, commit, dispatch }) {
    if (
      process.client &&
      (!state.userProfile ||
        Object.keys(state.userProfile).length === 0 ||
        Object.getPrototypeOf(state.userProfile) !== Object.prototype)
    ) {
      const token = (this as any).$cookies.get("token")
      if (token) {
        try {
          const response = await api.getOfficialMe(token)
          if (response.data) {
            await commit("setUserProfile", response.data)
          }
        } catch (error) {
          await dispatch("checkApiError", error)
        }
      }
    }
  },
  async getCreatorProfile({ state, commit, dispatch }) {
    if (
      process.client &&
      (!state.creatorProfile ||
        Object.keys(state.creatorProfile).length === 0 ||
        Object.getPrototypeOf(state.creatorProfile) !== Object.prototype)
    ) {
      const token = (this as any).$cookies.get("token")
      if (token) {
        try {
          const response = await api.getMe(token)
          if (response.data) {
            await commit("setCreatorProfile", response.data)
          }
        } catch (error) {
          await dispatch("checkApiError", error)
        }
      }
    }
  },
  async updateUserProfile({ commit, dispatch }, payload) {
    const token = (this as any).$cookies.get("token")
    if (token) {
      try {
        const loadingNotification = { content: "Saving...", showProgress: true }
        await commit("addNotification", loadingNotification)
        const response = await api.updateOfficialMe(token, payload)
        await commit("setUserProfile", response.data)
        await commit("removeNotification", loadingNotification)
        await commit("addNotification", {
          content: "Profile successfully updated",
          color: "success",
        })
      } catch (error) {
        await dispatch("checkApiError", error)
      }
    }
  },
  async updateCreatorProfile({ commit, dispatch }, payload) {
    const token = (this as any).$cookies.get("token")
    if (token) {
      try {
        const loadingNotification = { content: "Saving...", showProgress: true }
        await commit("addNotification", loadingNotification)
        const response = await api.updateMe(token, payload)
        await commit("setCreatorProfile", response.data)
        await commit("removeNotification", loadingNotification)
        await commit("addNotification", {
          content: "Profile successfully updated",
          color: "success",
        })
      } catch (error) {
        await dispatch("checkApiError", error)
      }
    }
  },
  async toggleCreatorPrivacy({ commit, dispatch }) {
    const token = (this as any).$cookies.get("token")
    if (token) {
      try {
        const loadingNotification = { content: "Saving...", showProgress: true }
        await commit("addNotification", loadingNotification)
        const response = await api.toggleCreatorPrivacy(token)
        await commit("setCreatorProfile", response.data)
        await commit("removeNotification", loadingNotification)
        await commit("addNotification", {
          content: "Profile successfully updated",
          color: "success",
        })
      } catch (error) {
        await dispatch("checkApiError", error)
      }
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
      await dispatch("checkApiError", error)
    }
  },
  async refreshLoggedProfile({ state, dispatch }) {
    /*
      1) If logged in and online, refresh data
    */
    if (state.isLoggedIn) {
      try {
        await dispatch("getUserProfile")
        await dispatch("getCreatorProfile")
      } catch (error) {
        await dispatch("checkApiError", error)
      }
    }
  },
  async refreshLoggedIn({ commit, dispatch }) {
    /*
      1) If token and token not expired, set logged in
      2) Else if refresh and refresh not expired, set logged in
    */
    const token = (this as any).$cookies.get("token")
    const hasExpired = token ? tokenExpired(token) : true
    if (!hasExpired) await commit("setLoggedIn", true)
    if (hasExpired) await dispatch("refreshTokens")
  },
  async refreshOffline({ state, commit, dispatch }) {
    /*
      1) If token and token not expired, set logged in
      2) Else if refresh and refresh not expired, set logged in
      3) If logged in and online, refresh data
    */
    let token = (this as any).$cookies.get("token")
    let hasExpired = token ? tokenExpired(token) : true
    if (!hasExpired) await commit("setLoggedIn", true)
    else {
      token = (this as any).$cookies.get("refresh")
      hasExpired = token ? tokenExpired(token) : true
      if (!hasExpired) await commit("setLoggedIn", true)
    }
  },
  async logOut({ commit }) {
    // removeLocalToken()
    // removeRefreshToken()
    // await commit("setToken", "")
    try {
      const refresh = (this as any).$cookies.get("refresh")
      if (refresh) await api.revokeRefreshedToken(refresh)
    } catch (e) {}
    await commit("setLoggedIn", false)
    await commit("setUserProfile", {})
    await commit("setCreatorProfile", {})
    ;(this as any).$cookies.remove("token")
    ;(this as any).$cookies.remove("refresh")
  },
  async checkApiError({ dispatch }, payload: AxiosError) {
    if ([400, 401, 403].includes(payload.response!.status)) {
      await dispatch("logOut")
    }
  },
  async addErrorNotification({ commit }, payload: AxiosError) {
    if (payload.response!.data.detail !== "Could not validate credentials") {
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
    }
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
  storeThemeState({ state }) {
    const theme: IThemeState = {
      theme: state.theme.theme,
      spacing: state.theme.spacing,
      font: state.theme.font,
      size: state.theme.size,
    }
    saveLocalSettings(JSON.stringify(theme))
  },
  async recoverThemeState({ commit, dispatch }) {
    const localSettings = getLocalSettings()
    if (localSettings) {
      await commit("setThemeState", JSON.parse(localSettings))
    } else {
      await dispatch("storeThemeState")
    }
  },
}
