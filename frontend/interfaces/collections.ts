/* eslint-disable camelcase */

import { IOpinion, IWorkMetadata } from "@/interfaces"

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
}

export interface IConversionState {
  description: boolean
  upload: boolean
  dedication: boolean
  conversion: boolean
}

export interface IConversion {
  key: string
  date_created: Date
  metadata: IWorkMetadata
  dedication: string
  conversionState: IConversionState
}
