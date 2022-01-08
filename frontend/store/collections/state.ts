import { IContract, IWorkSearchSummary } from "@/interfaces"

export interface CollectionState {
  collectionWatcher: string
  libraryCollection: string
  library: string[]
  work: string[]
  anthology: string[]
  series: string[]
  conversion: string[]
  stream: string[]
  partyContributions: IContract[]
  offers: IContract[]
  offer: IContract
  search: IWorkSearchSummary[]
}

const defaultState: CollectionState = {
  collectionWatcher: "Nothing-nothing",
  libraryCollection: "",
  library: [],
  work: [],
  anthology: [],
  series: [],
  conversion: [],
  stream: [],
  partyContributions: [],
  offers: [],
  offer: {} as IContract,
  search: [],
}

export default () => defaultState
