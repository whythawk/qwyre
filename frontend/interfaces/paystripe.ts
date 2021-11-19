/* eslint-disable camelcase */
export type ICurrencyTypes = "usd" | "gbp" | "eur"

export interface IStripeIntent {
  amount: number
  currency: ICurrencyTypes
}
