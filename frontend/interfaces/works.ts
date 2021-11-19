/* eslint-disable camelcase */

export type IContributorRoles = "artist" | "editor" | "translator"
export type IOpinion = -1 | 0 | 1

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
