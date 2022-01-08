export interface CoilState {
  coilRoute: string
  coilState: string
  coilToken: string
  coilPointer: string
  coilReceipt: string
  isStreaming: boolean
  requestError: boolean
  coilSub: string
  btpToken: string
  monetizationWatcher: boolean
}

const defaultState: CoilState = {
  coilRoute: "",
  coilState: "",
  coilToken: "",
  coilReceipt: "",
  coilPointer: process.env.coilPointer as string,
  isStreaming: false,
  requestError: false,
  coilSub: "",
  btpToken: "",
  monetizationWatcher: false,
}

export default () => defaultState
