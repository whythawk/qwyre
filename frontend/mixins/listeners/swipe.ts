/**
 * Thanks to Xyfir
 * https://github.com/Xyfir/xyfir-reader
 */

/**
 * Listen for swipes convert them to actions.
 * @param {HTMLElement} el - The HTML element to add event listeners to.
 * @param {Function} fn - The listener function.
 * @param {boolean} listen - Specify whether this adds or removes the listener. Default true.
 */
export default function swipeListener(
  el: HTMLElement,
  fn: Function,
  listen: boolean = true
) {
  // Defaults: 100, 350, 100
  // Required min distance traveled to be considered a swipe
  const threshold = 50
  // Maximum time allowed to travel that distance
  const allowedTime = 500
  // Maximum distance allowed at the same time in perpendicular direction
  const restraint = 200
  let startX
  let startY
  let startTime
  function startListenerAction(event: TouchEvent) {
    startX = event.changedTouches[0].pageX
    startY = event.changedTouches[0].pageY
    startTime = Date.now()
  }
  function endListenerAction(event: TouchEvent) {
    // Get distance traveled by finger while in contact with surface
    const distX = event.changedTouches[0].pageX - startX
    const distY = event.changedTouches[0].pageY - startY
    // Time elapsed since touchstart
    const elapsedTime = Date.now() - startTime
    if (elapsedTime <= allowedTime) {
      // Horizontal swipe
      if (Math.abs(distX) >= threshold && Math.abs(distY) <= restraint)
        // If dist traveled is negative, it indicates left swipe
        fn(distX < 0 ? "next" : "prev")
      // Vertical swipe
      else if (Math.abs(distY) >= threshold && Math.abs(distX) <= restraint)
        // Up / down swipe
        fn("menu")
    }
  }
  if (listen) {
    el.addEventListener("touchstart", startListenerAction, false)
    el.addEventListener("touchend", endListenerAction, false)
  }
  if (!listen) {
    el.removeEventListener("touchstart", startListenerAction, false)
    el.removeEventListener("touchend", endListenerAction, false)
  }
}
