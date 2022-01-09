export default {
  // Collections
  allCollections: (state) => (collection: string) => state[collection],
  latestCollections:
    (state) =>
    (collection: string, end: number = 10) =>
      state[collection].slice(0, end),
  firstCollection: (state) => (collection: string) => state[collection][0],
  collectionWatcher: (state) => state.collectionWatcher,
  libraryCollection: (state) => state.libraryCollection,
  partyContributions: (state) => state.partyContributions,
  offers: (state) => state.offers,
  offer: (state) => state.offer,
  search: (state) => state.search,
}
