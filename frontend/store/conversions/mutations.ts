export default {
  setConversionKey(state, payload: string) {
    state.key = payload
  },
  setCurrentStep(state, payload: string) {
    state.currentStep = payload
  },
}
