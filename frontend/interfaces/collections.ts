/* eslint-disable camelcase */

import { IOpinion, IWorkMetadata, IWorkMetadataSummary } from "@/interfaces"

export interface IAnthology {
  key: string
  name: string | null
  description?: string
  date_created: Date
  opinion?: IOpinion
  works?: string[]
}

export interface ISeries {
  key: string
  name: string
  description?: string
  date_created: Date
  opinion?: IOpinion
  anthologies?: string[]
  works?: string[]
}

export interface IConversionState {
  describe: boolean
  upload: boolean
  dedication: boolean
  conversion: boolean
}

export interface IConversion {
  key: string
  date_created: Date
  metadata: IWorkMetadata
  dedication: string
  conversionState: string[]
}

export interface IStream {
  key: string
  date_created?: Date
  metadata: IWorkMetadataSummary
  price?: number
  spine?: string[]
  first500: string
  stream: string[][]
  start_page: number
  page: number
  position: number
  currentPage?: number
  currentPosition?: number
}

export interface IStreamIn {
  stream: string[][]
  page: number
  position: number
}

export interface ILibrary {
  key: string
  date_created: Date
  collection: "work" | "stream"
}
