import { api } from "@/api"
import { IUserProfileCreate, IUserProfileUpdate } from "@/interfaces"
// Review global namespacing https://vuex.vuejs.org/guide/modules.html

export default {
  async getUsers({ commit, dispatch, rootState }) {
    if ((this as any).$cookies.get("token")) {
      try {
        const response = await api.getUsers((this as any).$cookies.get("token"))
        if (response) {
          await commit("setUsers", response.data)
        }
      } catch (error) {
        await dispatch("main/checkApiError", error, { root: true })
      }
    }
  },
  async updateUser(
    { commit, dispatch, rootState },
    payload: { id: number; user: IUserProfileUpdate }
  ) {
    if ((this as any).$cookies.get("token")) {
      try {
        const loadingNotification = {
          content: "Saving...",
          showProgress: true,
        }
        await commit("main/addNotification", loadingNotification, {
          root: true,
        })
        const response = (
          await Promise.all([
            api.updateUser(
              (this as any).$cookies.get("token"),
              payload.id,
              payload.user
            ),
            // eslint-disable-next-line @typescript-eslint/no-unused-vars
            await new Promise<void>((resolve) =>
              setTimeout(() => resolve(), 500)
            ),
          ])
        )[0]
        await commit("setUser", response.data)
        await commit("main/removeNotification", loadingNotification, {
          root: true,
        })
        await commit(
          "main/addNotification",
          {
            content: "User successfully updated",
            color: "success",
          },
          { root: true }
        )
      } catch (error) {
        await dispatch("main/checkApiError", error, { root: true })
      }
    }
  },
  async createUser(
    { commit, dispatch, rootState },
    payload: IUserProfileCreate
  ) {
    if ((this as any).$cookies.get("token")) {
      try {
        const loadingNotification = { content: "Saving...", showProgress: true }
        await commit("main/addNotification", loadingNotification, {
          root: true,
        })
        const response = (
          await Promise.all([
            api.createUser((this as any).$cookies.get("token"), payload),
            await new Promise<void>((resolve) =>
              setTimeout(() => resolve(), 500)
            ),
          ])
        )[0]
        await commit("setUser", response.data)
        await commit("main/removeNotification", loadingNotification, {
          root: true,
        })
        await commit(
          "main/addNotification",
          {
            content: "User successfully created",
            color: "success",
          },
          { root: true }
        )
      } catch (error) {
        await dispatch("main/checkApiError", error, { root: true })
      }
    }
  },
}
