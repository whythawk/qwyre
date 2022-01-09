import axios from "axios"
import {
  ICoilUserResourceRequest,
  ICoilUserTokenRequest,
  ICoilUserTokenResponse,
  ICoilUserTokenRefreshRequest,
  ICoilUserTokenRevokeRequest,
  ICoilUserInfo,
  ICoilUserBTP,
} from "@/interfaces"

function requestHeaders() {
  const token = btoa(`${process.env.coilID}:${process.env.coilSecret}`)
  return {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      Authorization: `Basic ${token}`,
    },
  }
}

function requestUserHeaders(accessToken: string) {
  return {
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      Authorization: `Bearer ${accessToken}`,
    },
  }
}

export const coil = {
  getUserResource(coilState: string): string {
    // https://help.coil.com/docs/dev/get-oauth-auth#request-parameters
    // NOTE: currently the 'signup' prompt doesn't work
    // https://www.valentinog.com/blog/url/
    const getResourceURL = new URL(`${process.env.coilUrl}/oauth/auth`)
    const data: ICoilUserResourceRequest = {
      response_type: "code",
      scope: "simple_wm openid",
      client_id: process.env.coilID as unknown as string,
      state: coilState,
      redirect_uri: `${process.env.baseUrl}/support-us`,
      prompt: "login",
    }
    // const params = new URLSearchParams()
    for (const [key, value] of Object.entries(data)) {
      // params.append(key, value)
      getResourceURL.searchParams.append(key, value)
    }
    // return await axios.get(`${process.env.apiUrl}/api/v1/coil/proxy/oauth/auth`, { params })
    return getResourceURL.href
  },
  async getUserToken(coilCode: string) {
    // https://help.coil.com/docs/dev/post-oauth-token/index.html#request-an-access-token-for-an-authenticated-user
    const data: ICoilUserTokenRequest = {
      code: coilCode,
      grant_type: "authorization_code",
      redirect_uri: `${process.env.baseUrl}/support-us`,
    }
    return await axios.post<ICoilUserTokenResponse>(
      `${process.env.apiUrl}/api/v1/coil/proxy/oauth/token`,
      data,
      requestHeaders()
    )
  },
  async getUserRefresh(refreshToken: string) {
    const data: ICoilUserTokenRefreshRequest = {
      refresh_token: refreshToken,
      grant_type: "refresh_token",
      scope: "simple_wm openid",
    }
    return await axios.post<ICoilUserTokenResponse>(
      `${process.env.apiUrl}/api/v1/coil/proxy/oauth/token`,
      data,
      requestHeaders()
    )
  },
  async revokeUserResource(token: string) {
    const data: ICoilUserTokenRevokeRequest = {
      token,
    }
    return await axios.post(
      `${process.env.apiUrl}/api/v1/coil/proxy/oauth/token/revocation`,
      data,
      requestHeaders()
    )
  },
  async getUserInfo(accessToken: string) {
    return await axios.get<ICoilUserInfo>(
      `${process.env.apiUrl}/api/v1/coil/proxy/user/info`,
      requestUserHeaders(accessToken)
    )
  },
  async getUserBTP(accessToken: string) {
    return await axios.post<ICoilUserBTP>(
      `${process.env.apiUrl}/api/v1/coil/proxy/user/btp`,
      {},
      requestUserHeaders(accessToken)
    )
  },
}
