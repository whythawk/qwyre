<template>
  <div class="flex flex-col">
    <div
      class="container relative max-w-full md:max-w-2xl mx-auto py-8 lg:py-16 text-center bg-ochre-900 md:bg-opacity-0 z-0"
    >
      <div
        class="mx-auto mt-12 py-8 px-6 sm:py-12 lg:px-0 flex flex-col items-center text-center"
      >
        <span class="mb-4 text-xl text-ochre-10">
          <SvgIcon terms="h-20 w-20" icon="qwyreLogo" />
        </span>
        <h1
          class="inline-flex text-4xl font-extrabold text-ochre-10 lg:text-6xl"
        >
          Qwyre is an experiment.
        </h1>
        <p class="mt-4 text-2xl text-ochre-10">
          Our success depends on your support.
        </p>
      </div>
    </div>
    <div class="container relative mx-auto max-w-6xl">
      <div class="mx-0 md:mx-6">
        <!--Lead Card-->
        <div
          class="bg-ochre-10 rounded bg-opacity-90 overflow-hidden shadow-lg"
        >
          <!--- WEB MONETIZATION --->
          <MonetizationSupportUs
            v-if="!showAuthenticating && !coilSub"
            :uri="coilRequestURI"
          />
          <MonetizationAuthenticating v-if="showAuthenticating" />
          <MonetizationAuthComplete v-if="!showAuthenticating && coilSub" />
          <!--- STRIPE --->
          <div class="flex justify-center px-4 sm:px-6 lg:px-8 mb-10">
            <div class="max-w-md w-full space-y-8">
              <p class="text-xl text-ochre-800">
                <span class="font-semibold">If</span> you prefer a one-time
                donation over streaming micropayments, please
                <span class="font-semibold">buy us a coffee...</span>
              </p>
              <!-- Display a payment form -->
              <form id="payment-form" ref="payment-form">
                <div>
                  <label class="block">
                    <span class="text-ochre-700 text-md ml-3">Tip jar</span>
                    <span class="inpt-span">
                      <select
                        id="currency"
                        ref="currency-choice"
                        v-model="stripeIntent.currency"
                        name="currency"
                        class="inpt-text rounded-r-none rounded-l-full w-1/5"
                      >
                        <option
                          v-for="(symbol, currency, i) in denominations"
                          :key="`currency-${i}`"
                          :value="currency"
                        >
                          {{ symbol }}
                        </option>
                      </select>
                      <input
                        id="donation"
                        ref="amount-choice"
                        v-model="stripeIntent.amount"
                        name="donation"
                        type="text"
                        :class="`inpt-text ${
                          stripeIntent.amount < stripeMinimumAmount
                            ? 'text-sinopia-500'
                            : ''
                        }`"
                        :placeholder="placeholderAmount"
                      />
                    </span>
                  </label>
                </div>
                <div class="inpt-span mt-4">
                  <span id="card-element" class="inpt-text h-9 rounded-l-full">
                    <!--Stripe.js injects the Card Element-->
                  </span>
                </div>
                <div class="mt-4 max-w-2xl mx-auto flex justify-center">
                  <button
                    id="submit"
                    ref="stripe-button"
                    :class="`btn-woad-extended ${
                      stripeDisabled ? 'opacity-50' : ''
                    }`"
                    :disabled="stripeDisabled"
                  >
                    <span
                      id="spinner"
                      ref="stripe-spinner"
                      class="spinner hidden"
                    >
                      <SvgIcon terms="w-8 h-8" icon="svgRingsSpinner" />
                    </span>
                    <span id="button-text" ref="stripe-button-text"
                      >Buy us a coffee</span
                    >
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { loadStripe } from "@stripe/stripe-js/pure"
import {
  Component,
  Getter,
  Action,
  Mutation,
  Ref,
  Vue,
} from "nuxt-property-decorator"
import { ICoilUserResourceResponse, IStripeIntent } from "@/interfaces"
import { coil } from "@/api"

@Component({
  middleware: "refresh-authentication",
  layout: "support",
})
export default class AuthoriseUserWebMonetization extends Vue {
  @Getter("monetization/coilRoute") coilRoute
  @Getter("monetization/coilToken") coilToken
  @Getter("monetization/coilState") coilState
  @Getter("monetization/coilSub") coilSub
  @Mutation("main/addNotification") addNotification
  @Getter("payments/stripeClientSecret") stripeClientSecret
  @Action("payments/getStripeIntent") getStripeIntent
  @Action("monetization/recoverCoilResourceState") recoverCoilResourceState
  @Action("monetization/storeCoilResourceState") storeCoilResourceState
  @Action("monetization/initialiseUserBTP") initialiseUserBTP
  @Ref("currency-choice") readonly currencyChoice!: HTMLSelectElement
  @Ref("amount-choice") readonly amountChoice!: HTMLInputElement
  @Ref("stripe-button") readonly stripeButton!: HTMLButtonElement
  @Ref("stripe-button-text") readonly stripeButtonText!: HTMLSpanElement
  @Ref("payment-form") readonly stripePaymentForm!: HTMLFormElement
  @Ref("stripe-spinner") readonly stripeSpinner!: HTMLSpanElement
  public showAuthenticating: boolean = false
  public coilRequestURI: string = ""
  public stripe: any = {}
  public payment: IStripeIntent = {} as IStripeIntent
  public stripeDisabled: boolean = false
  public denominations = { usd: "$", gbp: "£", eur: "€" }
  public placeholderAmount: number =
    (process.env.stripeDefault as unknown as number) / 100

  public stripeMinimumAmount: number =
    (process.env.stripeMinimum as unknown as number) / 100

  public stripeIntent: IStripeIntent = {
    amount: (process.env.stripeDefault as unknown as number) / 100,
    currency: "usd",
  }

  public showStripeError() {
    this.showStripeLoading(false)
    this.stripeDisabled = false
  }

  public showStripeOrderComplete() {
    this.showStripeLoading(false)
    this.stripeDisabled = true
  }

  public showStripeLoading(isLoading) {
    if (isLoading) {
      this.stripeDisabled = true
      this.stripeSpinner.classList.remove("hidden")
      this.stripeButtonText.classList.add("hidden")
    } else {
      this.stripeDisabled = false
      this.stripeSpinner.classList.add("hidden")
      this.stripeButtonText.classList.remove("hidden")
    }
  }

  async payWithCard(card) {
    this.showStripeLoading(true)
    if (this.stripeIntent.amount < this.stripeMinimumAmount) {
      this.showStripeError()
      this.addNotification({
        content: `The minimum amount Stripe permits for payment is ${
          this.denominations[this.stripeIntent.currency]
        }0.${this.stripeMinimumAmount * 100}.`,
        color: "error",
      })
    } else {
      const stripeCardIntent = {
        amount: Math.round(this.stripeIntent.amount * 100),
        currency: this.stripeIntent.currency,
      }
      await this.getStripeIntent(stripeCardIntent)
      const result = await this.stripe.confirmCardPayment(
        this.stripeClientSecret,
        {
          payment_method: {
            card,
          },
        }
      )
      if (result.error) {
        this.showStripeError()
        this.addNotification({
          content: result.error.message,
          color: "error",
        })
      } else {
        this.showStripeOrderComplete()
        this.addNotification({
          content: "Thank you for supporting",
          color: "success",
        })
      }
    }
  }

  async created(): Promise<void> {
    if (process.client) {
      // <--- STRIPE SETUP --->
      this.stripe = await loadStripe(process.env.stripeKey as string)
      const elements = this.stripe.elements()
      const style = {
        base: {
          color: "#635246",
          fontFamily: "PTSerifRegular",
          fontSmoothing: "antialiased",
          fontSize: "16px",
          "::placeholder": {
            color: "#635246",
          },
        },
        invalid: {
          fontFamily: "PTSerifRegular",
          color: "#da4000",
          iconColor: "#da4000",
        },
      }
      const card = elements.create("card", { style })
      // Stripe injects an iframe into the DOM
      card.mount("#card-element")
      card.on("change", (event) => {
        // Disable the Pay button if there are no card details in the Element
        this.stripeButton.disabled = event.empty
        if (event.error)
          this.addNotification({
            content: event.error.message,
            color: "error",
          })
      })
      this.stripePaymentForm.addEventListener("submit", (event) => {
        event.preventDefault()
        this.payWithCard(card)
      })
      // <--- WEB MONETIZATION SETUP --->
      if (!this.coilSub) this.recoverCoilResourceState()
      // if not, and there are route query terms, process auth 'n auth
      if (
        !this.coilSub &&
        this.$route.query.code &&
        this.$route.query.state &&
        this.$route.query.scope
      ) {
        this.showAuthenticating = true
        const payload: ICoilUserResourceResponse = {
          code: this.$route.query.code as string,
          state: this.$route.query.state as string,
          scope: this.$route.query.scope as string,
        }
        await this.initialiseUserBTP(payload)
        if (this.coilSub) this.showAuthenticating = false
      }
      if (!this.coilSub) {
        const lastPage: string = this.$nuxt.context.from
          ? this.$nuxt.context.from.path
          : "/"
        await this.storeCoilResourceState({ coilRoute: lastPage })
        this.coilRequestURI = coil.getUserResource(this.coilState)
      }
    }
  }
}
</script>
