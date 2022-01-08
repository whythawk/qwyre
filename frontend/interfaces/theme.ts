export type IPageTheme = "light" | "dark"
export type IPageSpacing = "tight" | "default" | "double" | "source"
export type IPageFont = "serif" | "sans_serif" | "source"

export interface IThemeState {
  theme: IPageTheme
  spacing: IPageSpacing
  font: IPageFont
  size: string
}
