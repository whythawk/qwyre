export interface StripeIntentResponse {
  clientSecret: string
}

export interface PaymentState {
  stripe: StripeIntentResponse | null
}

const defaultState: PaymentState = {
  stripe: null,
}

export default () => defaultState
