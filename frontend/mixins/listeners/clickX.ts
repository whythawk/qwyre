/**
 * Thanks to Xyfir
 * https://github.com/Xyfir/xyfir-reader
 */

/**
 * Listen for clicks and convert them to actions based on the location of the
 * click on the page.
 * @param {HTMLElement} el - The HTML element to add event listeners to.
 * @param {Function} fn - The listener function.
 * @param {number} pw - The page width in pixels, versus the viewport width.
 * @param {boolean} listen - Specify whether this adds or removes the listener. Default true.
 */

export default function clickXListener(
  el: HTMLElement,
  fn: Function,
  pw: number,
  listen: boolean = true
) {
  function listenerAction(event: MouseEvent) {
    // Standard listener event for add and remove
    // Get click location
    const cX = event.clientX
    // Get view-port size, and leave middle 50% of page width to select options.
    const wX = el.clientWidth / 2 - pw * 0.25
    // Click was in left 30% of page
    if (cX < wX) fn("prev")
    // Click was in right 30% of page
    else if (cX > el.clientWidth - wX) fn("next")
    else fn("menu")
  }
  if (listen) el.addEventListener("click", listenerAction, false)
  if (!listen) el.removeEventListener("click", listenerAction, false)
}
