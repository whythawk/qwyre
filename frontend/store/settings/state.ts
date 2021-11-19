export interface HelperState {
  headingTitle: string | null
  currentStep: string | null
}

const defaultState: HelperState = {
  headingTitle: null,
  currentStep: null,
}

export default () => defaultState
