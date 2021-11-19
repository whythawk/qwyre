import { coil } from "@/api"
import {
  generateUUID,
  getCoilRoute,
  saveCoilRoute,
  getCoilState,
  saveCoilState,
  getCoilRefresh,
  saveCoilRefresh,
  removeCoilRefresh,
} from "@/utilities"
import { AxiosError, AxiosResponse } from "axios"
import {
  ICoilUserResourceResponse,
  ICoilUserTokenResponse,
  ICoilUserInfo,
  ICoilUserBTP,
} from "@/interfaces"

export default {
  // STORE and RECOVER resource auth state
  async storeCoilResourceState(
    { commit },
    { coilRoute }: { coilRoute: string }
  ) {
    if (!getCoilState()) saveCoilState(generateUUID())
    await commit("setCoilState", getCoilState())
    saveCoilRoute(coilRoute)
  },
  async recoverCoilResourceState({ commit, dispatch }) {
    await commit("setCoilState", getCoilState())
    await commit("setCoilRoute", getCoilRoute())
    if (getCoilRefresh()) await dispatch("refreshUserBTP")
  },
  // START web monetization
  async startMonetizationStream({ commit, dispatch, state }) {
    await dispatch("refreshUserBTP")
    if (!state.requestError) {
      await commit("setIsStreaming", true)
      await commit("setCoilPointer", process.env.coilPointer as string)
      await commit(
        "main/addNotification",
        {
          content: "You have started web monetization.",
          color: "success",
        },
        { root: true }
      )
    }
  },
  // STOP web monetization
  async stopMonetizationStream({ commit }) {
    await commit("setIsStreaming", false)
    await commit("setCoilPointer", "")
    await commit(
      "main/addNotification",
      {
        content: "You have stopped web monetization.",
        color: "success",
      },
      { root: true }
    )
  },
  // REVOKE web monetization
  async revokeMonetization({ commit, dispatch, state }) {
    await dispatch("stopMonetizationStream")
    await commit("setCoilSub", "")
    if (state.coilToken) {
      await coil.revokeUserResource(state.coilToken)
      await commit("setCoilToken", "")
    } else if (getCoilRefresh()) {
      // Counterintuitively, we need a new user_token to request the revoke
      try {
        const response: AxiosResponse = await coil.getUserRefresh(
          getCoilRefresh() as string
        )
        const data: ICoilUserTokenResponse = response.data
        if (
          data &&
          Object.keys(data).length !== 0 &&
          data.constructor === Object
        )
          await coil.revokeUserResource(data.access_token)
      } catch (error) {
        await dispatch("checkCoilError", error)
      }
    }
    if (getCoilRefresh()) removeCoilRefresh()
    await commit(
      "main/addNotification",
      {
        content: "You have successfully revoked web monetization.",
        color: "success",
      },
      { root: true }
    )
  },
  // INITIALISE and REFRESH main calls
  async initialiseUserBTP(
    { dispatch, commit, state },
    payload: ICoilUserResourceResponse
  ) {
    await dispatch("getUserToken", payload)
    if (!state.requestError) {
      await dispatch("getUserInfo")
      await dispatch("getUserBTP")
      await commit("setRequestError", false)
    }
  },
  async refreshUserBTP({ commit, dispatch, state }) {
    if (getCoilRefresh()) {
      try {
        const response: AxiosResponse = await coil.getUserRefresh(
          getCoilRefresh() as string
        )
        const data: ICoilUserTokenResponse = response.data
        // https://stackoverflow.com/a/32108184/295606
        if (
          data &&
          Object.keys(data).length !== 0 &&
          data.constructor === Object
        ) {
          await commit("setCoilToken", data.access_token)
          saveCoilRefresh(data.refresh_token)
          if (!state.coilSub) await dispatch("getUserInfo")
          if (!state.requestError) {
            await dispatch("getUserBTP")
            await commit("setRequestError", false)
          }
        } else {
          await commit("setRequestError", true)
        }
      } catch (error) {
        await dispatch("checkCoilError", error)
      }
    } else {
      await commit("setRequestError", true)
      await commit(
        "main/addNotification",
        {
          content: "Error authorising web monetization.",
          color: "error",
        },
        { root: true }
      )
    }
  },
  // GET Coil user user_token, info and BTP
  async getUserToken({ commit, dispatch }, payload: ICoilUserResourceResponse) {
    if (getCoilState() !== payload.state) {
      await commit("setRequestError", true)
    } else {
      try {
        try {
          const response: AxiosResponse = await coil.getUserToken(payload.code)
          const data: ICoilUserTokenResponse = response.data
          await commit("setCoilToken", data.access_token)
          saveCoilRefresh(data.refresh_token)
        } catch (error) {
          await dispatch("checkCoilError", error)
        }
      } catch (error) {
        await dispatch("checkCoilError", error)
      }
    }
  },
  async getUserInfo({ commit, dispatch, state }) {
    try {
      const response: AxiosResponse = await coil.getUserInfo(state.coilToken)
      const data: ICoilUserInfo = response.data
      await commit("setCoilSub", data.sub)
    } catch (error) {
      await dispatch("checkCoilError", error)
    }
  },
  async getUserBTP({ commit, dispatch, state }) {
    try {
      const response: AxiosResponse = await coil.getUserBTP(state.coilToken)
      const data: ICoilUserBTP = response.data
      await commit("setBtpToken", data.btpToken)
    } catch (error) {
      await dispatch("checkCoilError", error)
    }
  },
  // CHECK ERRORS
  async checkCoilError({ commit, dispatch, state }, payload: AxiosError) {
    if (
      state.coilSub &&
      Object.prototype.hasOwnProperty.call(payload, "response") &&
      payload.response!.status === 403
    ) {
      await dispatch("stopStreamMonetization")
    } else {
      await commit("setRequestError", true)
    }
    await commit(
      "main/addNotification",
      {
        content: "Error authorising web monetization.",
        color: "error",
      },
      { root: true }
    )
  },
}
