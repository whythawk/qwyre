export default async function ({ store, redirect }) {
  await store.dispatch("main/refreshLoggedIn")
  if (
    !(await store.getters["main/hasAdminAccess"]) &&
    !(await store.getters["main/isLoggedIn"])
  ) {
    return redirect("/")
  }
}
