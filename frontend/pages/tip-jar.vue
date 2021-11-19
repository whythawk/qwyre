<template>
  <div class="container min-h-screen mx-auto">
    <div
      class="relative max-w-3xl mx-auto py-6 sm:py-8 flex flex-col items-center text-center"
    >
      <p class="mb-4 text-xl text-ochre-900">
        <SvgIcon terms="h-20 w-20" icon="qwyreLogo" />
      </p>
      <h1
        class="inline-flex text-3xl font-extrabold text-ochre-900 lg:text-5xl"
      >
        Qwyre is an experiment.
      </h1>
      <p class="mt-4 text-2xl text-ochre-900">
        Our success depends on your support.
      </p>
    </div>
    <div class="flex justify-center px-4 sm:px-6 lg:px-8">
      <div class="max-w-md w-full space-y-8">
        <!-- Display a payment form -->
        <form id="payment-form" ref="payment-form">
          <div>
            <label class="block">
              <span class="text-ochre-600 text-xs ml-3">Tip jar</span>
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
              :class="`btn-woad-extended ${stripeDisabled ? 'opacity-50' : ''}`"
              :disabled="stripeDisabled"
            >
              <span id="spinner" ref="stripe-spinner" class="spinner hidden">
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
    <div
      class="relative max-w-3xl mx-auto py-6 px-6 flex flex-col items-center text-center sm:py-8 lg:px-0"
    >
      <p class="mt-8 text-lg text-ochre-900">
        <span class="font-semibold">Web Monetization</span> lets you stream
        micropayments to creators using <span class="font-semibold">Coil</span>,
        similar to how <span class="font-semibold">Stripe</span> processes our
        credit card payments. Learn more at the links below and we'd love for
        you to try streaming micropayments. If not, please support us with a
        small one-time donation.
      </p>
      <p class="inline-flex mt-8 text-xl text-ochre-900">
        <a href="https://www.grantfortheweb.org/"
          ><SvgIcon terms="h-10 w-36" icon="svgGrantForTheWeb"
        /></a>
        <a href="https://webmonetization.org/" class="ml-10"
          ><SvgIcon terms="h-9 w-9" icon="svgMonetizationStatic"
        /></a>
        <a href="https://coil.com/" class="ml-10"
          ><SvgIcon terms="h-8 w-16" icon="svgCoilLogo"
        /></a>
      </p>
    </div>
  </div>
</template>

<script lang="ts">
import { loadStripe } from "@stripe/stripe-js/pure"
import {
  Action,
  Component,
  Getter,
  Mutation,
  Ref,
  Vue,
} from "nuxt-property-decorator"
import { IStripeIntent } from "@/interfaces"

@Component({
  middleware: "anonymous",
  layout: "working",
})
export default class TipJar extends Vue {
  @Mutation("main/addNotification") addNotification
  @Getter("payments/stripeClientSecret") stripeClientSecret
  @Action("payments/getStripeIntent") getStripeIntent
  @Ref("currency-choice") readonly currencyChoice!: HTMLSelectElement
  @Ref("amount-choice") readonly amountChoice!: HTMLInputElement
  @Ref("stripe-button") readonly stripeButton!: HTMLButtonElement
  @Ref("stripe-button-text") readonly stripeButtonText!: HTMLSpanElement
  @Ref("payment-form") readonly stripePaymentForm!: HTMLFormElement
  @Ref("stripe-spinner") readonly stripeSpinner!: HTMLSpanElement
  public stripe: any = {}
  public payment: IStripeIntent = {} as IStripeIntent
  public stripeDisabled: boolean = false
  public denominations = { usd: "$", gbp: "£", eur: "€" }
  public placeholderAmount: number =
    ((process.env.stripeDefault as unknown) as number) / 100

  public stripeMinimumAmount: number =
    ((process.env.stripeMinimum as unknown) as number) / 100

  public stripeIntent: IStripeIntent = {
    amount: ((process.env.stripeDefault as unknown) as number) / 100,
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
  }
}
</script>
