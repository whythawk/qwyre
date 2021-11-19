export default {
  stripeClientSecret: (state) =>
    state.stripe != null && state.stripe.clientSecret,
}
