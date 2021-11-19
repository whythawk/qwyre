import Vue from "vue"

const socket = new WebSocket("ws://localhost/api/v1/epub/ws")

const emitter = new Vue({
  methods: {
    send(message) {
      if (socket.readyState === 1) socket.send(message)
    },
  },
})

socket.onmessage = (msg) => {
  emitter.$emit("message", msg.data)
}
socket.onerror = (err) => {
  emitter.$emit("error", err)
}

export default emitter
