import { api } from "@/api"
import { IStripeIntent } from "@/interfaces"

export default {
  async getStripeIntent({ commit }, payload: IStripeIntent) {
    try {
      const response = await api.getStripeIntent(payload)
      if (response) {
        await commit("setStripeIntentResponse", response.data)
      }
    } catch (error) {
      await commit(
        "main/addNotification",
        {
          content: error,
          color: "error",
        },
        { root: true }
      )
    }
  },
}
