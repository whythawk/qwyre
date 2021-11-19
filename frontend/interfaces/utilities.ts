/* eslint-disable camelcase */

export interface SocketResponse {
  state: string
  data: {
    identifier: string
    work?: string
  }
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
