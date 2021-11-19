export default {
  // Collections
  allCollections: (state) => (collection: string) => state[collection],
  latestCollections: (state) => (collection: string, end: number = 10) =>
    state[collection].slice(0, end),
  firstCollection: (state) => (collection: string) => state[collection][0],
  collectionWatcher: (state) => state.collectionWatcher,
}
