import { StripeIntentResponse } from "./state"

export default {
  setStripeIntentResponse(state, payload: StripeIntentResponse) {
    state.stripe = payload
  },
}
