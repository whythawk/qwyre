import { IUserProfile, ICreatorSummary, IThemeState } from "@/interfaces"

export interface AppNotification {
  content: string
  color?: string
  showProgress?: boolean
}

const defaultTheme: IThemeState = {
  theme: "light",
  spacing: "default",
  font: "serif",
  size: "100",
}

export interface MainState {
  isLoggedIn: boolean
  logInError: boolean
  creatorProfile: ICreatorSummary | {}
  userProfile: IUserProfile | {}
  notifications: AppNotification[]
  showOptions: boolean
  showOptionsCall: boolean
  watchReaderCFI: string
  theme: IThemeState
  work?: string
  changeWatcher: string
}

const defaultState: MainState = {
  isLoggedIn: false,
  logInError: false,
  creatorProfile: {},
  userProfile: {},
  notifications: [],
  showOptions: false,
  showOptionsCall: false,
  watchReaderCFI: "nothing",
  theme: defaultTheme,
  changeWatcher: "nowatch",
}

export default () => defaultState
