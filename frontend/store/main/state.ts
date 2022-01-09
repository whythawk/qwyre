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
  token: string
  isLoggedIn: boolean | null
  logInError: boolean
  creatorProfile: ICreatorSummary | null
  userProfile: IUserProfile | null
  notifications: AppNotification[]
  showOptions: boolean
  showOptionsCall: boolean
  watchReaderCFI: string
  theme: IThemeState
  work?: string
  changeWatcher: string
}

const defaultState: MainState = {
  isLoggedIn: null,
  token: "",
  logInError: false,
  creatorProfile: null,
  userProfile: null,
  notifications: [],
  showOptions: false,
  showOptionsCall: false,
  watchReaderCFI: "nothing",
  theme: defaultTheme,
  changeWatcher: "nowatch",
}

export default () => defaultState
