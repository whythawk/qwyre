export default function ({ store }) {
  // plugins: "~/plugins/init.client.ts",
  // https://stackoverflow.com/a/58157422/295606
  store.dispatch("main/setLocalTokens")
}
