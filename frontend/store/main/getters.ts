export default {
  hasAdminAccess: (state) => {
    return (
      state.userProfile &&
      state.userProfile.is_superuser &&
      state.userProfile.is_active
    )
  },
  canMakeCreativeOffers: (state) => {
    return (
      state.creatorProfile &&
      state.creatorProfile.isActive &&
      !state.creatorProfile.isBanned &&
      !state.creatorProfile.isPrivate &&
      state.userProfile &&
      state.userProfile.email_validated &&
      state.userProfile.is_active
    )
  },
  loginError: (state) => state.logInError,
  creatorProfile: (state) => state.creatorProfile,
  userProfile: (state) => state.userProfile,
  isLoggedIn: (state) => state.isLoggedIn,
  firstNotification: (state) =>
    state.notifications.length > 0 && state.notifications[0],
  showOptions: (state) => state.showOptions,
  showOptionsCall: (state) => state.showOptionsCall,
  pageTheme: (state) => state.theme.theme,
  pageFont: (state) => state.theme.font,
  pageSpacing: (state) => state.theme.spacing,
  pageSize: (state) => state.theme.size,
  watchReaderCFI: (state) => state.watchReaderCFI,
  changeWatcher: (state) => state.changeWatcher,
}
