export interface ConversionState {
  key: string | null
  currentStep: string
}

const defaultState: ConversionState = {
  key: null,
  currentStep: "description",
}

export default () => defaultState
