import { AppNotification } from "./state"
import {
  IUserProfile,
  ICreatorSummary,
  IPageTheme,
  IPageSpacing,
  IPageFont,
  IThemeState,
} from "@/interfaces"

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
  setCreatorProfile(state, payload: ICreatorSummary) {
    state.creatorProfile = payload
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
  setShowOptionsCall(state, payload: boolean) {
    state.showOptionsCall = payload
  },
  // Reader display options
  setThemeState(state, payload: IThemeState) {
    state.theme = payload
  },
  setTheme(state, payload: IPageTheme) {
    state.theme.theme = payload
  },
  setFont(state, payload: IPageFont) {
    state.theme.font = payload
  },
  setSpacing(state, payload: IPageSpacing) {
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
