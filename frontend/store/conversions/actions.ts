import { idb } from "@/api"
import { IConversion } from "@/interfaces"

export default {
  async updateConversionState(
    { dispatch },
    {
      conversionKey,
      conversionStep,
    }: { conversionKey: string; conversionStep: string }
  ) {
    const conversion = ((await idb.getPayload(
      "conversion",
      conversionKey
    )) as unknown) as IConversion
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
}
