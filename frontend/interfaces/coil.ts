/* eslint-disable camelcase */

export interface ICoilUserResourceRequest {
  response_type: string
  scope: string
  client_id: string
  state: string
  redirect_uri: string
  prompt: string
}

export interface ICoilUserResourceResponse {
  code: string
  state: string
  scope: string
}

export interface ICoilUserTokenRequest {
  code: string
  grant_type: string
  redirect_uri: string
}

export interface ICoilUserTokenResponse {
  access_token: string
  expires_in: number
  id_token: string
  refresh_token: string
  scope: string
  token_type: string
}

export interface ICoilUserTokenRefreshRequest {
  refresh_token: string
  grant_type: string
  scope: string
}

export interface ICoilUserTokenRevokeRequest {
  token: string
}

export interface ICoilUserInfo {
  email?: string
  sub: string
}

export interface ICoilUserBTP {
  btpToken: string
}
