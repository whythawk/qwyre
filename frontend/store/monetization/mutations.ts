export default {
  setCoilRoute(state, payload: string) {
    state.coilRoute = payload
  },
  setCoilState(state, payload: string) {
    state.coilState = payload
  },
  setCoilToken(state, payload: string) {
    state.coilToken = payload
  },
  setCoilPointer(state, payload: string) {
    state.coilPointer = payload
  },
  setIsStreaming(state, payload: boolean) {
    state.isStreaming = payload
  },
  setRequestError(state, payload: boolean) {
    state.requestError = payload
  },
  setCoilSub(state, payload: string) {
    state.coilSub = payload
  },
  setBtpToken(state, payload: string) {
    state.btpToken = payload
  },
}
