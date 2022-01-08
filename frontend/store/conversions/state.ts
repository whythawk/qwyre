import { IWorkLineSummary, IWorkSummary, IContract } from "@/interfaces"

export interface ConversionState {
  key: string | null
  currentStep: string
  workSummaries: IWorkLineSummary[]
  workEdit: IWorkSummary
  contractEdit: IContract
}

const defaultState: ConversionState = {
  key: null,
  currentStep: "description",
  workSummaries: [],
  workEdit: {} as IWorkSummary,
  contractEdit: {} as IContract,
}

export default () => defaultState
