export default {
  hasAdminAccess: (state) => {
    return (
      state.userProfile &&
      state.userProfile.is_superuser &&
      state.userProfile.is_active
    )
  },
  loginError: (state) => state.logInError,
  userProfile: (state) => state.userProfile,
  token: (state) => state.token,
  isLoggedIn: (state) => state.isLoggedIn,
  firstNotification: (state) =>
    state.notifications.length > 0 && state.notifications[0],
  showOptions: (state) => state.showOptions,
  pageTheme: (state) => state.theme.theme,
  pageFont: (state) => state.theme.font,
  pageSpacing: (state) => state.theme.spacing,
  pageSize: (state) => state.theme.size,
  watchReaderCFI: (state) => state.watchReaderCFI,
  changeWatcher: (state) => state.changeWatcher,
}
