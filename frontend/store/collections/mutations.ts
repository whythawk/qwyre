export default {
  setCollection(
    state,
    {
      collection,
      key,
    }: {
      collection: string
      key: string
    }
  ) {
    // Keep a history of the last 10 collections in activity order
    state[collection] = state[collection].filter((k: string) => k !== key)
    state[collection].unshift(key)
    state[collection] = state[collection].slice(0, 10)
  },
  removeCollection(
    state,
    {
      collection,
      key,
    }: {
      collection: string
      key: string
    }
  ) {
    state[collection] = state[collection].filter((k: string) => k !== key)
  },
  setCollectionWatcher(state, payload: string) {
    state.collectionWatcher = payload
  },
  restoreCollection(
    state,
    { collection, keyList }: { collection: string; keyList: string[] }
  ) {
    state[collection] = keyList.slice(0)
  },
}
