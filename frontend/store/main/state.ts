import { IUserProfile } from "@/interfaces"

export type PageTheme = "light" | "dark"
export type PageSpacing = "tight" | "default" | "double" | "source"
export type PageFont = "serif" | "sans_serif" | "source"

export interface AppNotification {
  content: string
  color?: string
  showProgress?: boolean
}

export interface ThemeState {
  theme: PageTheme
  spacing: PageSpacing
  font: PageFont
  size: string
}

const defaultTheme: ThemeState = {
  theme: "light",
  spacing: "default",
  font: "serif",
  size: "100",
}

export interface MainState {
  token: string
  isLoggedIn: boolean | null
  logInError: boolean
  userProfile: IUserProfile | null
  notifications: AppNotification[]
  showOptions: boolean
  watchReaderCFI: string
  theme: ThemeState
  work?: string
  changeWatcher: string
}

const defaultState: MainState = {
  isLoggedIn: null,
  token: "",
  logInError: false,
  userProfile: null,
  notifications: [],
  showOptions: false,
  watchReaderCFI: "nothing",
  theme: defaultTheme,
  changeWatcher: "nowatch",
}

export default () => defaultState
