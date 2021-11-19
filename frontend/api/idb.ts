// Derived from https://www.raymondcamden.com/2019/10/16/using-indexeddb-with-vuejs
// and https://github.com/cfjedimaster/vue-demos/blob/master/idb/src/api/idb.js

import { IWork, IAnthology, ISeries, IConversion } from "@/interfaces"

const IDB_NAME: string = String(process.env.idbName)
const IDB_VERSION: number = Number(process.env.idbVersion)
const IDB_OBJECT_STORES: [string, boolean][] = [
  ["epub", false],
  ["docx", false],
  ["cover", false],
  ["work", true],
  ["anthology", true],
  ["series", true],
  ["conversion", true],
]
let IDB: IDBDatabase

export const idb = {
  getDB() {
    return new Promise<IDBDatabase>((resolve, reject) => {
      if (IDB) {
        return resolve(IDB)
      }
      const request = window.indexedDB.open(IDB_NAME, IDB_VERSION)
      request.onerror = (event) => {
        console.log("Error opening db", event)
        reject(new Error("Failed to open IndexedDB."))
      }
      request.onsuccess = (event: any) => {
        // Needs to be recast,
        // cf: https://github.com/microsoft/TypeScript/issues/30669
        IDB = event.target.result
        resolve(IDB)
      }
      request.onupgradeneeded = (event: any) => {
        // Create object stores for: epub files, works, anthologies and series
        const db: IDBDatabase = event.target.result
        IDB_OBJECT_STORES.forEach(([objectStore, key]) => {
          if (key)
            db.createObjectStore(objectStore, {
              keyPath: "key",
            })
          else {
            db.createObjectStore(objectStore)
          }
        })
      }
    })
  },
  // Set, Get, GetAll and Remove functions for each Payload type
  async setPayload(
    objectStore: string,
    payload: string | IWork | IAnthology | ISeries | IConversion | Blob,
    key: string | null = null
  ) {
    const db = await this.getDB()
    return new Promise<void>((resolve) => {
      const transaction = db.transaction([objectStore], "readwrite")
      transaction.oncomplete = () => {
        resolve()
      }
      const store = transaction.objectStore(objectStore)
      if (key) {
        try {
          store.put(payload, key)
        } catch (error) {
          store.add(payload, key)
        }
      } else
        try {
          store.put(payload)
        } catch (error) {
          store.add(payload)
        }
    })
  },
  async getPayload(objectStore: string, key: string) {
    const db = await this.getDB()
    return new Promise<
      string | IWork | IAnthology | ISeries | IConversion | Blob
    >((resolve) => {
      const payload = db
        .transaction([objectStore], "readonly")
        .objectStore(objectStore)
        .get(key)
      payload.onsuccess = (event: any) => resolve(event.target.result)
    })
  },
  async getAllPayloads(objectStore: string) {
    const db = await this.getDB()
    const payloads: IWork[] | IAnthology[] | ISeries[] | IConversion[] = []
    return new Promise<IWork[] | IAnthology[] | ISeries[] | IConversion[]>(
      (resolve) => {
        const payloadStore = db
          .transaction([objectStore], "readonly")
          .objectStore(objectStore)
          .getAll()
        payloadStore.onsuccess = (event: any) => {
          let cursor = event.target.result
          cursor = resolve(cursor)
          if (cursor) {
            payloads.push(cursor.value)
            cursor.continue()
          }
        }
      }
    )
  },
  async getLatestPayloads(objectStore: string, items: number = 10) {
    // won't work for string or blob stores
    let payloads = (await this.getAllPayloads(objectStore)) as
      | IWork[]
      | IAnthology[]
      | ISeries[]
      | IConversion[]
    payloads = payloads.sort((a, b) => b.date_created - a.date_created)
    return payloads.slice(0, items)
  },
  async removePayload(objectStore: string, key: string) {
    const db = await this.getDB()
    return new Promise((resolve) => {
      const transaction = db.transaction([objectStore], "readwrite")
      transaction.oncomplete = () => {
        resolve(objectStore)
      }
      const store = transaction.objectStore(objectStore)
      store.delete(key)
    })
  },
  async replaceKey(objectStore: string, keyOld: string, keyNew: string) {
    // Arises when a temporary key is created prior to
    // completion of a conversion.
    const payload:
      | string
      | IWork
      | IAnthology
      | ISeries
      | IConversion
      | Blob = await this.getPayload(objectStore, keyOld)
    await this.removePayload(objectStore, keyOld)
    if (Object.prototype.hasOwnProperty.call(payload, "key"))
      // @ts-ignore
      payload.key = keyNew
    return await this.setPayload(objectStore, payload, keyNew)
  },
  async hasKey(objectStore: string, key: string) {
    // https://stackoverflow.com/a/37076976/295606
    const db = await this.getDB()
    return new Promise<number>((resolve) => {
      const payload = db
        .transaction([objectStore], "readonly")
        .objectStore(objectStore)
        .count(key)
      payload.onsuccess = (event: any) => resolve(event.target.result)
    })
  },
}
