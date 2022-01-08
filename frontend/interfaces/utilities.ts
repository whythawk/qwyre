/* eslint-disable camelcase */
import { IStream, IStreamIn } from "./collections"

export interface ISocketDataStream {
  stream: IStream | IStreamIn
  pointer: string
}

export interface ISocketResponse {
  state: string
  data?: ISocketDataStream
  error?: string | null
}

export interface readerIframeView {
  iframe: HTMLIFrameElement
  document: Document
  id: string
}

export interface ISendEmail {
  email: string
  subject: string
  content: string
}

export interface IMsg {
  msg: string
}
