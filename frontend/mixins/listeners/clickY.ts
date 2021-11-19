/**
 * Thanks to Xyfir
 * https://github.com/Xyfir/xyfir-reader
 */

/**
 * Listen for clicks and convert them to actions based on the location of the
 * click on the page.
 * @param {HTMLElement} el - The HTML element to add event listeners to.
 * @param {Function} fn - The listener function.
 * @param {boolean} listen - Specify whether this adds or removes the listener. Default true.
 */

export default function clickYListener(
  el: HTMLElement,
  fn: Function,
  listen: boolean = true
) {
  function listenerAction(event: MouseEvent) {
    const cY = event.clientY
    console.log(cY)
    fn("menu")
  }
  if (listen) el.addEventListener("click", listenerAction, false)
  if (!listen) el.removeEventListener("click", listenerAction, false)
}
