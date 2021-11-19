/**
 * Derived from Janglee123
 * https://github.com/Janglee123/eplee/
 */

/**
 * Listen for key press
 * @param {HTMLElement} el - The HTML element to add event listeners to.
 * @param {Function} fn - The listener function.
 * @param {boolean} listen - Specify whether this adds or removes the listener. Default true.
 */

export default function keyListener(
  el: HTMLElement,
  fn: Function,
  listen: boolean = true
) {
  function listenerAction(event: KeyboardEvent) {
    if (["ArrowRight", "ArrowUp"].includes(event.code)) fn("next")
    if (["ArrowLeft", "ArrowDown"].includes(event.code)) fn("prev")
    if (["Escape", "Backspace"].includes(event.code)) fn("menu")
  }
  if (listen) {
    el.addEventListener("keydown", listenerAction, false)
  }
  if (!listen) el.removeEventListener("keydown", listenerAction, false)
}
