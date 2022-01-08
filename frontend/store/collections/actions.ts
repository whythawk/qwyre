import { api, idb } from "@/api"
import {
  // IWorkMetadata,
  IWork,
  IAnthology,
  ISeries,
  IConversion,
  IStream,
  ILibrary,
} from "@/interfaces"
import { generateUUID } from "@/utilities"

/**
 * Collection actions effect state and IndexedDB, while Payload actions only
 * effect IndexedDB.
 * @param {string} collection - The state &/or objectStore effected.
 * @param {string | IWork | IAnthology | ISeries | IConversion | IStream | Blob} payload - The data object.
 * @param {string} key - Unique reference identity, usually derived from the epub, or a UUID.
 */

export default {
  async storePayload(
    { _commit },
    {
      collection,
      payload,
      key,
    }: {
      collection: string
      payload:
        | string
        | IWork
        | IAnthology
        | ISeries
        | IConversion
        | IStream
        | Blob
      key: string
    }
  ) {
    if (Object.prototype.hasOwnProperty.call(payload, "date_created"))
      // @ts-ignore
      payload.date_created = new Date()
    // Store the payload in IDB
    if (Object.prototype.hasOwnProperty.call(payload, "key"))
      await idb.setPayload(collection, payload)
    else await idb.setPayload(collection, payload, key)
  },
  async storeCollectionPayload(
    { commit, dispatch },
    {
      collection,
      payload,
      key,
    }: {
      collection: string
      payload:
        | string
        | IWork
        | IAnthology
        | ISeries
        | IConversion
        | IStream
        | Blob
      key: string
    }
  ) {
    if (collection === "stream") (payload as IStream).key = key
    await dispatch("storePayload", { collection, payload, key })
    await commit("setCollection", { collection, key })
    if (["stream", "work"].includes(collection)) {
      const library: ILibrary = {
        key,
        date_created: new Date(),
        collection: collection as "stream" | "work",
      }
      collection = "library"
      await dispatch("storePayload", {
        collection,
        payload: library,
        key,
      })
      await commit("setCollection", { collection, key })
    }
    await commit("setCollectionWatcher", `${collection}-${generateUUID()}`)
  },
  async removePayload(
    { _commit },
    {
      collection,
      key,
    }: {
      collection: string
      key: string
    }
  ) {
    await idb.removePayload(collection, key)
  },
  async removeCollectionPayload(
    { commit, dispatch },
    {
      collection,
      key,
    }: {
      collection: string
      key: string
    }
  ) {
    await dispatch("removePayload", { collection, key })
    await commit("removeCollection", { collection, key })
    if (["stream", "work"].includes(collection)) {
      collection = "library"
      await dispatch("removePayload", { collection, key })
      await dispatch("removePayload", { collection: "cover", key })
      await commit("removeCollection", { collection, key })
    }
    await commit("setCollectionWatcher", `${collection}-${generateUUID()}`)
  },
  async replaceCollectionKey(
    { commit },
    {
      collection,
      keyOld,
      keyNew,
    }: { collection: string; keyOld: string; keyNew: string }
  ) {
    await idb.replaceKey(collection, keyOld, keyNew)
    await commit("removeCollection", { collection, keyOld })
    await commit("setCollection", { collection, keyNew })
    if (["stream", "work"].includes(collection)) {
      collection = "library"
      await idb.replaceKey(collection, keyOld, keyNew)
      await commit("removeCollection", { collection, keyOld })
      await commit("setCollection", { collection, keyNew })
    }
    await commit("setCollectionWatcher", `${collection}-${generateUUID()}`)
  },
  async restoreCollection(
    { commit, state },
    { collection }: { collection: string }
  ) {
    if (!state[collection].length) {
      const latestCollection = await idb.getLatestPayloads(collection)
      const firstCollection = latestCollection.length
        ? latestCollection[0].key
        : null
      await commit("restoreCollection", {
        collection,
        keyList: latestCollection.map(({ key }) => key),
      })
      if (["stream", "work"].includes(collection)) {
        collection = "library"
        const latestCollection = await idb.getLatestPayloads(collection)
        await commit("restoreCollection", {
          collection,
          keyList: latestCollection.map(({ key }) => key),
        })
        if (firstCollection)
          await commit("setCollection", {
            collection,
            key: firstCollection,
          })
      } else if (collection === "library") {
        for (const c of ["stream", "work"]) {
          const latestCollection = await idb.getLatestPayloads(c)
          await commit("restoreCollection", {
            collection: c,
            keyList: latestCollection.map(({ key }) => key),
          })
          if (latestCollection.length)
            await commit("setCollection", {
              collection: c,
              key: latestCollection[0].key,
            })
        }
      }
    }
  },
  async getOffers({ commit, dispatch }) {
    try {
      const response = await api.getOffers()
      if (response.data) {
        await commit("setOffers", response.data)
      }
    } catch (error) {
      await dispatch("main/addErrorNotification", error, { root: true })
    }
  },
  async getOffer({ commit, dispatch }, payload: string) {
    try {
      const response = await api.getOffer(payload)
      if (response.data) {
        await commit("setOffer", response.data)
      }
    } catch (error) {
      await dispatch("main/addErrorNotification", error, { root: true })
    }
  },
  async getPartyContributions({ commit, dispatch, rootState }) {
    try {
      const response = await api.getPartyContributions(rootState.main.token)
      if (response.data) {
        await commit("setPartyContributions", response.data)
      }
    } catch (error) {
      await dispatch("main/addErrorNotification", error, { root: true })
    }
  },
  async getSearch({ commit }, payload: string) {
    try {
      const response = await api.getSearch(payload)
      if (response.data) {
        await commit("setSearch", response.data)
      } else {
        await commit("setSearch", [])
      }
    } catch (error) {}
  },
}
