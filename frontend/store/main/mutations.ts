import { AppNotification, PageSpacing, PageTheme, PageFont } from "./state"
import { IUserProfile } from "@/interfaces"

export default {
  setToken(state, payload: string) {
    state.token = payload
  },
  setLoggedIn(state, payload: boolean) {
    state.isLoggedIn = payload
  },
  setLogInError(state, payload: boolean) {
    state.logInError = payload
  },
  setUserProfile(state, payload: IUserProfile) {
    state.userProfile = payload
  },
  // Notifications
  addNotification(state, payload: AppNotification) {
    state.notifications.push(payload)
  },
  removeNotification(state, payload: AppNotification) {
    state.notifications = state.notifications.filter(
      (notification) => notification !== payload
    )
  },
  // Menu panels
  setShowOptions(state, payload: boolean) {
    state.showOptions = payload
  },
  // Reader display options
  setTheme(state, payload: PageTheme) {
    state.theme.theme = payload
  },
  setFont(state, payload: PageFont) {
    state.theme.font = payload
  },
  setSpacing(state, payload: PageSpacing) {
    state.theme.spacing = payload
  },
  setSize(state, payload: number) {
    state.theme.size = payload
  },
  // Current work
  setWork(state, payload: string) {
    state.work = payload
  },
  // changeReaderCFI
  setWatchReaderCFI(state, payload: string) {
    state.watchReaderCFI = payload
  },
  setChangeWatcher(state, payload: string) {
    state.changeWatcher = payload
  },
}
