/* eslint-disable camelcase */
import { IWorkStateType, IMimeType, IContributorRoleType } from "./schema_types"
import { ISubject } from "./subject"
import {
  ICreatorSummary,
  ICreatorProfile,
  ICreatorMini,
  IContributorSummary,
} from "./creator"

export type IContributorRoles = "artist" | "editor" | "translator"
export type IOpinion = -1 | 0 | 1

export interface IDataSource {
  data: string
  name: string
}

export interface IContributorMetadata {
  role: IContributorRoles
  name: string
  terms: string
  year?: string
}

export interface IWorkMetadata {
  identifier?: string
  title: string
  language?: string
  rights?: string
  description?: string
  creator: string[]
  contributor?: IContributorMetadata[]
  isodate?: string
  subject?: string[]
  publisher?: string
  long_description?: string
  long_rights?: string[]
  work_uri?: string
  publisher_uri?: string
}

export interface IWorkContents {
  title: string
  href: string
}

export interface IWork {
  key: string
  metadata: IWorkMetadata
  date_created: Date
  currentCFI?: string
  contents?: IWorkContents[]
  bookmarks?: string[]
  locations?: string[]
  opinion?: IOpinion
}

export interface IWorkMetadataLineSummary {
  identifier: string
  uid: string
  creator: ICreatorMini[]
  title: string
  description?: string
  long_description?: string
  isodate?: string
  subject?: ISubject[]
  word_count?: number
}

export interface IWorkSearchSummary {
  identifier: string
  work: string
  creator: string[]
  title: string
  long_description?: string
  description?: string
  isodate?: string
  subject?: string[]
  word_count?: number
}

export interface IWorkLineSummary {
  identifier: string
  state: IWorkStateType
  metadata: IWorkMetadataLineSummary
  created: Date
}

export interface IWorkMetadataSummary {
  identifier: string
  uid: string
  title: string
  description?: string
  long_description?: string
  isodate?: string
  language?: string
  rights?: string
  creator: ICreatorSummary[]
  contributor?: IContributorSummary[]
  publisher?: string
  work_uri?: string
  publisher_uri?: string
  subject?: ISubject[]
  word_count?: number
}

export interface IWorkSummary {
  identifier: string
  state: IWorkStateType
  metadata: IWorkMetadataSummary
  created: Date
  dedication?: string[]
  price?: number
  spine?: string[]
  first500?: string
  start_page?: number
}
