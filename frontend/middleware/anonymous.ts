export default async function ({ store, redirect }) {
  if (await store.getters["main/isLoggedIn"]) {
    return redirect("/")
  }
}
