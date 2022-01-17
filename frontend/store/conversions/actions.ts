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
    if ((this as any).$cookies.get("token")) {
      try {
        const response = await api.getWorkSummaries(
          (this as any).$cookies.get("token")
        )
        if (response.data) {
          await commit("setWorkSummaries", response.data)
        }
      } catch (error) {
        await dispatch("main/addErrorNotification", error, { root: true })
      }
    }
  },
  async getWorkToEdit({ commit, dispatch, rootState }, payload: string) {
    if ((this as any).$cookies.get("token")) {
      try {
        const response = await api.getWorkToEdit(
          (this as any).$cookies.get("token"),
          payload
        )
        if (response.data) {
          await commit("setWorkToEdit", response.data)
        }
      } catch (error) {
        await dispatch("main/addErrorNotification", error, { root: true })
      }
    }
  },
  async createWorkContract(
    { commit, dispatch, rootState },
    payload: { data: IContractCreate; workID: string }
  ) {
    if ((this as any).$cookies.get("token")) {
      try {
        const response = await api.createWorkContract(
          (this as any).$cookies.get("token"),
          payload.workID,
          payload.data
        )
        if (response.data) {
          await commit("setContractToEdit", response.data)
        }
      } catch (error) {
        await dispatch("main/addErrorNotification", error, { root: true })
      }
    }
  },
  async updateWorkContract(
    { commit, dispatch, rootState },
    payload: { data: IContractUpdate; contractID: string }
  ) {
    if ((this as any).$cookies.get("token")) {
      try {
        const response = await api.updateWorkContract(
          (this as any).$cookies.get("token"),
          payload.contractID,
          payload.data
        )
        if (response.data) {
          await commit("setContractToEdit", response.data)
        }
      } catch (error) {
        await dispatch("main/addErrorNotification", error, { root: true })
      }
    }
  },
  async publishWorkContract({ commit, dispatch, rootState }, payload: string) {
    if ((this as any).$cookies.get("token")) {
      try {
        const loadingNotification = {
          content: "Updating contract",
          showProgress: true,
        }
        await commit("main/addNotification", loadingNotification, {
          root: true,
        })
        const response = await api.publishWorkContract(
          (this as any).$cookies.get("token"),
          payload
        )
        if (response.data) {
          await commit("setWorkToEdit", response.data)
        }
      } catch (error) {
        await dispatch("main/addErrorNotification", error, { root: true })
      }
    }
  },
  async deleteWorkContract({ commit, dispatch, rootState }, payload: string) {
    if ((this as any).$cookies.get("token")) {
      try {
        const response = await api.deleteWorkContract(
          (this as any).$cookies.get("token"),
          payload
        )
        if (response.data) {
          await commit("setContractToEdit", {})
        }
      } catch (error) {
        await dispatch("main/addErrorNotification", error, { root: true })
      }
    }
  },
  async getContractToEdit(
    { getters, commit, dispatch, rootState },
    payload: string
  ) {
    if ((this as any).$cookies.get("token")) {
      try {
        let response
        if (
          getters.workEditCreatorIdentifiers.includes(
            rootState.main.creatorProfile.identifier
          )
        )
          response = await api.getWorkContractOffers(
            (this as any).$cookies.get("token"),
            payload
          )
        else
          response = await api.getWorkContract(
            (this as any).$cookies.get("token"),
            payload
          )
        if (response.data) {
          await commit("setContractToEdit", response.data)
        } else await commit("setContractToEdit", {})
      } catch (error) {
        await dispatch("main/addErrorNotification", error, { root: true })
      }
    }
  },
  async togglePartyContractAcceptance(
    { commit, dispatch, rootState },
    payload: string
  ) {
    if ((this as any).$cookies.get("token")) {
      try {
        const response = await api.togglePartyContractAcceptance(
          (this as any).$cookies.get("token"),
          payload
        )
        await commit("setContractToEdit", response.data)
        await commit("main/setChangeWatcher", generateUUID(), { root: true })
      } catch (error) {
        await dispatch("main/addErrorNotification", error, { root: true })
      }
    }
  },
  async togglePartyContractPublication(
    { commit, dispatch, rootState },
    payload: string
  ) {
    if ((this as any).$cookies.get("token")) {
      try {
        const response = await api.togglePartyContractPublication(
          (this as any).$cookies.get("token"),
          payload
        )
        await commit("setContractToEdit", response.data)
        await commit("main/setChangeWatcher", generateUUID(), { root: true })
      } catch (error) {
        await dispatch("main/addErrorNotification", error, { root: true })
      }
    }
  },
  async acceptContractOffer(
    { commit, dispatch, rootState },
    payload: { contractID: string; creatorID: string }
  ) {
    if ((this as any).$cookies.get("token")) {
      try {
        const response = await api.acceptContractOffer(
          (this as any).$cookies.get("token"),
          payload.contractID,
          payload.creatorID
        )
        await commit("setContractToEdit", response.data)
        await commit("main/setChangeWatcher", generateUUID(), { root: true })
      } catch (error) {
        await dispatch("main/addErrorNotification", error, { root: true })
      }
    }
  },
  async rejectContractOffer(
    { commit, dispatch, rootState },
    payload: { contractID: string; creatorID: string }
  ) {
    if ((this as any).$cookies.get("token")) {
      try {
        const response = await api.rejectContractOffer(
          (this as any).$cookies.get("token"),
          payload.contractID,
          payload.creatorID
        )
        await commit("setContractToEdit", response.data)
        await commit("main/setChangeWatcher", generateUUID(), { root: true })
      } catch (error) {
        await dispatch("main/addErrorNotification", error, { root: true })
      }
    }
  },
  async publishWork({ commit, dispatch, rootState }, payload: string) {
    if ((this as any).$cookies.get("token")) {
      try {
        const loadingNotification = {
          content: "Updating work",
          showProgress: true,
        }
        await commit("main/addNotification", loadingNotification, {
          root: true,
        })
        const response = await api.publishWork(
          (this as any).$cookies.get("token"),
          payload
        )
        if (response.data) {
          await commit("setWorkToEdit", response.data)
        }
      } catch (error) {
        await dispatch("main/addErrorNotification", error, { root: true })
      }
    }
  },
  async deleteWork({ commit, dispatch, rootState }, payload: string) {
    if ((this as any).$cookies.get("token")) {
      try {
        const response = await api.deleteWork(
          (this as any).$cookies.get("token"),
          payload
        )
        if (response.data) {
          await commit("setWorkToEdit", {})
        }
      } catch (error) {
        await dispatch("main/addErrorNotification", error, { root: true })
      }
    }
  },
}
