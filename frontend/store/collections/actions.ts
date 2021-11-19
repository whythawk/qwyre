import { idb } from "@/api"
import {
  // IWorkMetadata,
  IWork,
  IAnthology,
  ISeries,
  IConversion,
} from "@/interfaces"
import { generateUUID } from "@/utilities"

/**
 * Collection actions effect state and IndexedDB, while Payload actions only
 * effect IndexedDB.
 * @param {string} collection - The state &/or objectStore effected.
 * @param {string | IWork | IAnthology | ISeries | IConversion | Blob} payload - The data object.
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
      payload: string | IWork | IAnthology | ISeries | IConversion | Blob
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
      payload: string | IWork | IAnthology | ISeries | IConversion | Blob
      key: string
    }
  ) {
    await dispatch("storePayload", { collection, payload, key })
    await commit("setCollection", { collection, key })
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
    await commit("setCollectionWatcher", `${collection}-${generateUUID()}`)
  },
  async restoreCollection(
    { commit, state },
    { collection }: { collection: string }
  ) {
    if (!state[collection].length) {
      const latestCollection = await idb.getLatestPayloads(collection)
      await commit("restoreCollection", {
        collection,
        keyList: latestCollection.map(({ key }) => key),
      })
    }
  },
}
