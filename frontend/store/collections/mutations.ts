import { IContract, IWorkSearchSummary } from "@/interfaces"

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
  setLibraryCollection(state, payload: string) {
    state.libraryCollection = payload
  },
  restoreCollection(
    state,
    { collection, keyList }: { collection: string; keyList: string[] }
  ) {
    state[collection] = keyList.slice(0)
  },
  setPartyContributions(state, payload: IContract[]) {
    state.partyContributions = payload
  },
  setOffers(state, payload: IContract[]) {
    state.offers = payload
  },
  setOffer(state, payload: IContract) {
    state.offer = payload
  },
  setSearch(state, payload: IWorkSearchSummary[]) {
    state.search = payload
  },
}
