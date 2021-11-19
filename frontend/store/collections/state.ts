export interface CollectionState {
  collectionWatcher: string
  work: string[]
  anthology: string[]
  series: string[]
  conversion: string[]
}

const defaultState: CollectionState = {
  collectionWatcher: "Nothing-nothing",
  work: [],
  anthology: [],
  series: [],
  conversion: [],
}

export default () => defaultState
