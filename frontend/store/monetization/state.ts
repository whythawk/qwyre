export interface CoilState {
  coilRoute: string
  coilState: string
  coilToken: string
  coilPointer: string
  isStreaming: boolean
  requestError: boolean
  coilSub: string
  btpToken: string
}

const defaultState: CoilState = {
  coilRoute: "",
  coilState: "",
  coilToken: "",
  coilPointer: process.env.coilPointer as string,
  isStreaming: false,
  requestError: false,
  coilSub: "",
  btpToken: "",
}

export default () => defaultState
