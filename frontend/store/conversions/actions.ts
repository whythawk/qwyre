import { idb, api } from "@/api"
import { IContractCreate, IContractUpdate, IConversion } from "@/interfaces"
import { generateUUID } from "@/utilities"

export default {
  async updateConversionState(
    { dispatch },
    {
      conversionKey,
      conversionStep,
    }: { conversionKey: string; conversionStep: string }
  ) {
    const conversion = (await idb.getPayload(
      "conversion",
      conversionKey
    )) as unknown as IConversion
    conversion.conversionState[conversionStep] = true
    // And can now save the conversion
    await dispatch(
      "collections/storeCollectionPayload",
      {
        collection: "conversion",
        payload: conversion,
        key: conversionKey,
      },
      { root: true }
    )
  },
  async getWorkSummaries({ commit, dispatch, rootState }) {
    try {
      const response = await api.getWorkSummaries(rootState.main.token)
      if (response.data) {
        await commit("setWorkSummaries", response.data)
      }
    } catch (error) {
      await dispatch("main/addErrorNotification", error, { root: true })
    }
  },
  async getWorkToEdit({ commit, dispatch, rootState }, payload: string) {
    try {
      const response = await api.getWorkToEdit(rootState.main.token, payload)
      if (response.data) {
        await commit("setWorkToEdit", response.data)
      }
    } catch (error) {
      await dispatch("main/addErrorNotification", error, { root: true })
    }
  },
  async createWorkContract(
    { commit, dispatch, rootState },
    payload: { data: IContractCreate; workID: string }
  ) {
    try {
      const response = await api.createWorkContract(
        rootState.main.token,
        payload.workID,
        payload.data
      )
      if (response.data) {
        await commit("setContractToEdit", response.data)
      }
    } catch (error) {
      await dispatch("main/addErrorNotification", error, { root: true })
    }
  },
  async updateWorkContract(
    { commit, dispatch, rootState },
    payload: { data: IContractUpdate; contractID: string }
  ) {
    try {
      const response = await api.updateWorkContract(
        rootState.main.token,
        payload.contractID,
        payload.data
      )
      if (response.data) {
        await commit("setContractToEdit", response.data)
      }
    } catch (error) {
      await dispatch("main/addErrorNotification", error, { root: true })
    }
  },
  async publishWorkContract({ commit, dispatch, rootState }, payload: string) {
    try {
      const loadingNotification = {
        content: "Updating contract",
        showProgress: true,
      }
      await commit("main/addNotification", loadingNotification, { root: true })
      const response = await api.publishWorkContract(
        rootState.main.token,
        payload
      )
      if (response.data) {
        await commit("setWorkToEdit", response.data)
      }
    } catch (error) {
      await dispatch("main/addErrorNotification", error, { root: true })
    }
  },
  async deleteWorkContract({ commit, dispatch, rootState }, payload: string) {
    try {
      const response = await api.deleteWorkContract(
        rootState.main.token,
        payload
      )
      if (response.data) {
        await commit("setContractToEdit", {})
      }
    } catch (error) {
      await dispatch("main/addErrorNotification", error, { root: true })
    }
  },
  async getContractToEdit(
    { getters, commit, dispatch, rootState },
    payload: string
  ) {
    try {
      let response
      if (
        getters.workEditCreatorIdentifiers.includes(
          rootState.main.creatorProfile.identifier
        )
      )
        response = await api.getWorkContractOffers(
          rootState.main.token,
          payload
        )
      else response = await api.getWorkContract(rootState.main.token, payload)
      if (response.data) {
        await commit("setContractToEdit", response.data)
      } else await commit("setContractToEdit", {})
    } catch (error) {
      await dispatch("main/addErrorNotification", error, { root: true })
    }
  },
  async togglePartyContractAcceptance(
    { commit, dispatch, rootState },
    payload: string
  ) {
    try {
      const response = await api.togglePartyContractAcceptance(
        rootState.main.token,
        payload
      )
      await commit("setContractToEdit", response.data)
      await commit("main/setChangeWatcher", generateUUID(), { root: true })
    } catch (error) {
      await dispatch("main/addErrorNotification", error, { root: true })
    }
  },
  async togglePartyContractPublication(
    { commit, dispatch, rootState },
    payload: string
  ) {
    try {
      const response = await api.togglePartyContractPublication(
        rootState.main.token,
        payload
      )
      await commit("setContractToEdit", response.data)
      await commit("main/setChangeWatcher", generateUUID(), { root: true })
    } catch (error) {
      await dispatch("main/addErrorNotification", error, { root: true })
    }
  },
  async acceptContractOffer(
    { commit, dispatch, rootState },
    payload: { contractID: string; creatorID: string }
  ) {
    try {
      const response = await api.acceptContractOffer(
        rootState.main.token,
        payload.contractID,
        payload.creatorID
      )
      await commit("setContractToEdit", response.data)
      await commit("main/setChangeWatcher", generateUUID(), { root: true })
    } catch (error) {
      await dispatch("main/addErrorNotification", error, { root: true })
    }
  },
  async rejectContractOffer(
    { commit, dispatch, rootState },
    payload: { contractID: string; creatorID: string }
  ) {
    try {
      const response = await api.rejectContractOffer(
        rootState.main.token,
        payload.contractID,
        payload.creatorID
      )
      await commit("setContractToEdit", response.data)
      await commit("main/setChangeWatcher", generateUUID(), { root: true })
    } catch (error) {
      await dispatch("main/addErrorNotification", error, { root: true })
    }
  },
  async publishWork({ commit, dispatch, rootState }, payload: string) {
    try {
      const loadingNotification = {
        content: "Updating work",
        showProgress: true,
      }
      await commit("main/addNotification", loadingNotification, { root: true })
      const response = await api.publishWork(rootState.main.token, payload)
      if (response.data) {
        await commit("setWorkToEdit", response.data)
      }
    } catch (error) {
      await dispatch("main/addErrorNotification", error, { root: true })
    }
  },
  async deleteWork({ commit, dispatch, rootState }, payload: string) {
    try {
      const response = await api.deleteWork(rootState.main.token, payload)
      if (response.data) {
        await commit("setWorkToEdit", {})
      }
    } catch (error) {
      await dispatch("main/addErrorNotification", error, { root: true })
    }
  },
}
