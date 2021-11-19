import Vue from "vue"
import { ValidationObserver, ValidationProvider, extend } from "vee-validate"
import { required, confirmed, email, mimes } from "vee-validate/dist/rules"

extend("required", {
  ...required,
  message: "This field is required.",
})

extend("confirmed", {
  ...confirmed,
  message: "These fields must be identical.",
})

extend("email", {
  ...email,
  message: "Please use a valid email address.",
})

extend("url", {
  // https://stackoverflow.com/a/62972724/295606
  validate(value: string | null | undefined): boolean {
    if (value) {
      return /^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([-.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$/.test(
        value
      )
    }

    return false
  },
  message: "This value must be a valid URL",
})

extend("mimes", {
  ...mimes,
  message: "Please upload a valid file-type.",
})

// Register it globally
Vue.component("ValidationProvider", ValidationProvider)
Vue.component("ValidationObserver", ValidationObserver)
