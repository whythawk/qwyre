import axios from "axios"
import WebSocketAsPromised from "websocket-as-promised"
import {
  IDataSource,
  IWorkMetadata,
  IWorkLineSummary,
  IWorkSearchSummary,
  IContract,
  IContractCreate,
  IContractUpdate,
  IUserProfile,
  IUserProfileUpdate,
  IUserProfileCreate,
  ICreatorSummary,
  IUserOpenProfileCreate,
  IStripeIntent,
  ISendEmail,
  IMsg,
} from "@/interfaces"

// const DEBUG = process.env.appEnv === "development"

// axios.interceptors.request.use(
//   (config) => {
//     /** In dev, intercepts request and logs it into console for dev */
//     if (DEBUG) {
//       console.info("✉️ ", config)
//     }
//     return config
//   },
//   (error) => {
//     if (DEBUG) {
//       console.error("✉️ ", error)
//     }
//     return Promise.reject(error)
//   }
// )

function authHeaders(token: string) {
  return {
    headers: {
      "Cache-Control": "no-cache",
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
  async revokeRefreshedToken(token: string) {
    return await axios.post(
      `${process.env.apiUrl}/api/v1/login/revoke-token`,
      {},
      authHeaders(token)
    )
  },
  async createMe(data: IUserOpenProfileCreate) {
    return await axios.post(`${process.env.apiUrl}/api/v1/users/`, data)
  },
  async getMe(token: string) {
    return await axios.get<ICreatorSummary>(
      `${process.env.apiUrl}/api/v1/creators/`,
      authHeaders(token)
    )
  },
  async getOfficialMe(token: string) {
    return await axios.get<IUserProfile>(
      `${process.env.apiUrl}/api/v1/users/`,
      authHeaders(token)
    )
  },
  async updateMe(token: string, data: ICreatorSummary) {
    return await axios.put<ICreatorSummary>(
      `${process.env.apiUrl}/api/v1/creators/`,
      data,
      authHeaders(token)
    )
  },
  async updateOfficialMe(token: string, data: IUserProfileUpdate) {
    return await axios.put<IUserProfile>(
      `${process.env.apiUrl}/api/v1/users/`,
      data,
      authHeaders(token)
    )
  },
  async toggleCreatorPrivacy(token: string) {
    return await axios.put<IUserProfile>(
      `${process.env.apiUrl}/api/v1/creators/toggle-privacy`,
      {},
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
  async requestValidationEmail(token: string) {
    return await axios.post(
      `${process.env.apiUrl}/api/v1/users/send-validation-email`,
      {},
      authHeaders(token)
    )
  },
  async validateEmail(token: string, validation: string) {
    return await axios.post(
      `${process.env.apiUrl}/api/v1/users/validate-email`,
      { validation },
      authHeaders(token)
    )
  },
  // CREATORS
  async getCreator(creatorID: string) {
    return await axios.get<ICreatorSummary>(
      `${process.env.apiUrl}/api/v1/creators/summary/${creatorID}`
    )
  },
  async getCreators() {
    return await axios.get<ICreatorSummary[]>(
      `${process.env.apiUrl}/api/v1/creators/summaries`
    )
  },
  async getCreatorAsAdmin(token: string, creatorID: string) {
    return await axios.get<ICreatorSummary>(
      `${process.env.apiUrl}/api/v1/creators/${creatorID}`,
      authHeaders(token)
    )
  },
  // Chapisha API works management
  async buildWork(
    token: string,
    data: { [key: string]: IWorkMetadata | string | null }
  ) {
    return await axios.post(
      `${process.env.apiUrl}/api/v1/works/create`,
      data,
      authHeaders(token)
    )
  },
  async deleteWork(token: string, workID: string) {
    return await axios.delete<IWorkLineSummary>(
      `${process.env.apiUrl}/api/v1/works/${workID}`,
      authHeaders(token)
    )
  },
  // Workshop tools
  async getWorkSummaries(token: string) {
    return await axios.get<IWorkLineSummary[]>(
      `${process.env.apiUrl}/api/v1/creators/works`,
      authHeaders(token)
    )
  },
  async getWorkToEdit(token: string, workID: string) {
    return await axios.get<IWorkLineSummary>(
      `${process.env.apiUrl}/api/v1/works/${workID}/auth`,
      authHeaders(token)
    )
  },
  async getWorkContractOffers(token: string, workID: string) {
    return await axios.get<IContract>(
      `${process.env.apiUrl}/api/v1/works/contract/${workID}/offers`,
      authHeaders(token)
    )
  },
  async getWorkContract(token: string, workID: string) {
    return await axios.get<IContract>(
      `${process.env.apiUrl}/api/v1/works/contract/${workID}`,
      authHeaders(token)
    )
  },
  async createWorkContract(
    token: string,
    workID: string,
    payload: IContractCreate
  ) {
    return await axios.post<IContract>(
      `${process.env.apiUrl}/api/v1/works/contract/${workID}`,
      payload,
      authHeaders(token)
    )
  },
  async updateWorkContract(
    token: string,
    contractID: string,
    payload: IContractUpdate
  ) {
    return await axios.put<IContract>(
      `${process.env.apiUrl}/api/v1/contracts/${contractID}`,
      payload,
      authHeaders(token)
    )
  },
  async deleteWorkContract(token: string, contractID: string) {
    return await axios.delete<IContract>(
      `${process.env.apiUrl}/api/v1/contracts/${contractID}`,
      authHeaders(token)
    )
  },
  async publishWorkContract(token: string, workID: string) {
    return await axios.put<IWorkLineSummary>(
      `${process.env.apiUrl}/api/v1/works/contract/${workID}/publish`,
      {},
      authHeaders(token)
    )
  },
  async publishWork(token: string, workID: string) {
    return await axios.put<IWorkLineSummary>(
      `${process.env.apiUrl}/api/v1/works/${workID}/publish`,
      {},
      authHeaders(token)
    )
  },
  async expressContractInterest(token: string, contractID: string) {
    return await axios.post<IMsg>(
      `${process.env.apiUrl}/api/v1/contracts/offers/${contractID}/express-interest`,
      {},
      authHeaders(token)
    )
  },
  async acceptContractOffer(
    token: string,
    contractID: string,
    creatorID: string
  ) {
    return await axios.post<IContract>(
      `${process.env.apiUrl}/api/v1/contracts/offers/${contractID}/editor/${creatorID}/accept`,
      {},
      authHeaders(token)
    )
  },
  async rejectContractOffer(
    token: string,
    contractID: string,
    creatorID: string
  ) {
    return await axios.post<IContract>(
      `${process.env.apiUrl}/api/v1/contracts/offers/${contractID}/editor/${creatorID}/reject`,
      {},
      authHeaders(token)
    )
  },
  async togglePartyContractAcceptance(token: string, contractID: string) {
    return await axios.post<IContract>(
      `${process.env.apiUrl}/api/v1/contracts/${contractID}/approve`,
      {},
      authHeaders(token)
    )
  },
  async togglePartyContractPublication(token: string, contractID: string) {
    return await axios.post<IContract>(
      `${process.env.apiUrl}/api/v1/contracts/${contractID}/publish`,
      {},
      authHeaders(token)
    )
  },
  async getOffers() {
    return await axios.get<IContract[]>(
      `${process.env.apiUrl}/api/v1/contracts/offers`
    )
  },
  async getOffer(contractID: string) {
    return await axios.get<IContract>(
      `${process.env.apiUrl}/api/v1/contracts/offers/${contractID}`
    )
  },
  async getPartyContributions(token: string) {
    return await axios.get<IContract[]>(
      `${process.env.apiUrl}/api/v1/contracts/contributions`,
      authHeaders(token)
    )
  },
  // Data sources
  async getCoverPublic(coverID: string, coverType: string) {
    return await axios.get<IDataSource>(
      `${process.env.apiUrl}/api/v1/sources/${coverType}/${coverID}`
    )
  },
  async getCoverAuthenticated(
    token: string,
    coverID: string,
    coverType: string
  ) {
    return await axios.get<IDataSource>(
      `${process.env.apiUrl}/api/v1/sources/authenticated/${coverType}/${coverID}`,
      authHeaders(token)
    )
  },
  async getSearch(terms: string) {
    return await axios.get<IWorkSearchSummary[]>(
      `${process.env.apiUrl}/api/v1/search/?q=${encodeURIComponent(terms)}`
    )
  },
  async getSearchSuggestions(terms: string) {
    return await axios.get<string[]>(
      `${process.env.apiUrl}/api/v1/search/suggestions/?q=${encodeURIComponent(
        terms
      )}`
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
  // WEBSOCKETS
  socketCreateWork() {
    return new WebSocketAsPromised(`${process.env.apiWS}/api/v1/works/create`, {
      packMessage: (data) => JSON.stringify(data),
      unpackMessage: (data) => JSON.parse(data as string),
    })
  },
  socketImportWork() {
    return new WebSocketAsPromised(`${process.env.apiWS}/api/v1/works/import`, {
      packMessage: (data) => JSON.stringify(data),
      unpackMessage: (data) => JSON.parse(data as string),
    })
  },
  socketUpdateWork(workID: string) {
    return new WebSocketAsPromised(
      `${process.env.apiWS}/api/v1/works/import/${workID}`,
      {
        packMessage: (data) => JSON.stringify(data),
        unpackMessage: (data) => JSON.parse(data as string),
      }
    )
  },
  socketStreamWork(workID: string) {
    return new WebSocketAsPromised(
      `${process.env.apiWS}/api/v1/stream/${workID}`,
      {
        packMessage: (data) => JSON.stringify(data),
        unpackMessage: (data) => JSON.parse(data as string),
      }
    )
  },
}
