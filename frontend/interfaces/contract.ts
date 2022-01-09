import { ICreatorProfile, ICreatorMini } from "./creator"
import { IWorkLineSummary } from "./works"

export interface IPartyCreate {
  identifier?: string
  proportion: number
  creator?: string
}

export interface IPartyUpdate extends IPartyCreate {
  identifier: string
}

export interface IParty {
  identifier: string
  created: Date
  proportion: number
  isApproved: boolean
  publicationApproved: boolean
  creator?: ICreatorProfile
}

export interface IContractCreate {
  description?: string
  work: string
  parties: IPartyCreate[]
}

export interface IContractUpdate {
  identifier: string
  description?: string
  work: string
  parties: IPartyUpdate[] | IPartyCreate[]
}

export interface IContract {
  identifier: string
  created: Date
  description?: string
  work: IWorkLineSummary
  parties: IParty[]
  offers: ICreatorMini[]
  isApproved: boolean
  publicationApproved: boolean
}
