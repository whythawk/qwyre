import axios from "axios"
import {
  IWorkMetadata,
  IUserProfile,
  IUserProfileUpdate,
  IUserProfileCreate,
  IUserOpenProfileCreate,
  IStripeIntent,
  ISendEmail,
} from "@/interfaces"

function authHeaders(token: string) {
  return {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  }
}

export const api = {
  // MEMBER AUTH N AUTH
  async logInGetToken(username: string, password: string) {
    const params = new URLSearchParams()
    params.append("username", username)
    params.append("password", password)
    return await axios.post(
      `${process.env.apiUrl}/api/v1/login/access-token`,
      params
    )
  },
  async getRefreshedToken(token: string) {
    return await axios.post(
      `${process.env.apiUrl}/api/v1/login/refresh-token`,
      {},
      authHeaders(token)
    )
  },
  async createMe(data: IUserOpenProfileCreate) {
    return await axios.post(`${process.env.apiUrl}/api/v1/users/open`, data)
  },
  async getMe(token: string) {
    return await axios.get<IUserProfile>(
      `${process.env.apiUrl}/api/v1/users/me`,
      authHeaders(token)
    )
  },
  async updateMe(token: string, data: IUserProfileUpdate) {
    return await axios.put<IUserProfile>(
      `${process.env.apiUrl}/api/v1/users/me`,
      data,
      authHeaders(token)
    )
  },
  async getUsers(token: string) {
    return await axios.get<IUserProfile[]>(
      `${process.env.apiUrl}/api/v1/users/`,
      authHeaders(token)
    )
  },
  async updateUser(token: string, userId: number, data: IUserProfileUpdate) {
    return await axios.put(
      `${process.env.apiUrl}/api/v1/users/${userId}`,
      data,
      authHeaders(token)
    )
  },
  async createUser(token: string, data: IUserProfileCreate) {
    return await axios.post(
      `${process.env.apiUrl}/api/v1/users/`,
      data,
      authHeaders(token)
    )
  },
  async passwordRecovery(email: string) {
    return await axios.post(
      `${process.env.apiUrl}/api/v1/password-recovery/${email}`
    )
  },
  async resetPassword(password: string, token: string) {
    return await axios.post(`${process.env.apiUrl}/api/v1/reset-password/`, {
      new_password: password,
      token,
    })
  },
  // Chapisha API works management
  async buildWork(
    token: string,
    data: { [key: string]: IWorkMetadata | string | null }
  ) {
    return await axios.post(
      `${process.env.apiUrl}/api/v1/chapisha/build`,
      data,
      authHeaders(token)
    )
  },
  async getWork(token: string, identifier: string) {
    return await axios.get<IWorkMetadata>(
      `${process.env.apiUrl}/api/v1/chapisha/${identifier}`,
      authHeaders(token)
    )
  },
  // Email contact us
  async postEmailContact(data: ISendEmail) {
    return await axios.post(
      `${process.env.apiUrl}/api/v1/utils/contact-us`,
      data
    )
  },
  // Stripe payments intents
  async getStripeIntent(data: IStripeIntent) {
    return await axios.post(`${process.env.apiUrl}/api/v1/stripe/`, data)
  },
}
