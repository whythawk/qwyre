import { ISubject } from "./subject"
import { IContributorRoleType } from "./schema_types"

export interface ICreatorSummary {
  identifier: string
  created: Date
  creator: string
  description?: string
  wallet?: string
  website?: string
  subject?: ISubject[]
  isActive: boolean
  isPrivate: boolean
  isBanned: boolean
}

export interface ICreatorProfile {
  identifier: string
  creator: string
  description?: string
  wallet?: string
  website?: string
  subject?: ISubject[]
}

export interface ICreatorMini {
  identifier: string
  creator: string
}

export interface IContributorSummary {
  identifier: string
  creator?: ICreatorSummary
  role: IContributorRoleType
  name?: string
  terms?: string
}
