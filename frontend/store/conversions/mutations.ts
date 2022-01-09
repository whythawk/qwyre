import { IWorkLineSummary, IWorkSummary, IContract } from "@/interfaces"

export default {
  setConversionKey(state, payload: string) {
    state.key = payload
  },
  setCurrentStep(state, payload: string) {
    state.currentStep = payload
  },
  setWorkSummaries(state, payload: IWorkLineSummary[]) {
    state.workSummaries = payload
  },
  setWorkToEdit(state, payload: IWorkSummary) {
    state.workEdit = payload
  },
  setContractToEdit(state, payload: IContract) {
    state.contractEdit = payload
  },
}
