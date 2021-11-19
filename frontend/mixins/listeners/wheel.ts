/**
 * Derived from Janglee123
 * https://github.com/Janglee123/eplee/
 */

/**
 * Listen for scroll wheel and convert them to next or prev action based on direction.
 * @param {HTMLElement} el - The HTML element to add event listeners to.
 * @param {Function} fn - The listener function.
 * @param {boolean} listen - Specify whether this adds or removes the listener. Default true.
 */

export default function wheelListener(
  el: HTMLElement,
  fn: Function,
  listen: boolean = true
) {
  // Required min distance traveled to be considered swipe
  const threshold = 350
  // Maximum time allowed to travel that distance
  const allowedTime = 50
  let dist = 0
  let isScrolling
  // core listener action
  function listenerAction(event: WheelEvent) {
    clearTimeout(isScrolling)
    dist += event.deltaY
    isScrolling = setTimeout(() => {
      if (Math.abs(dist) >= threshold) {
        // If wheel scrolled down it indicates left
        const direction = Math.sign(dist) > 0 ? "next" : "prev"
        fn(direction)
        dist = 0
      }
      dist = 0
    }, allowedTime)
  }
  if (listen) el.addEventListener("wheel", listenerAction, false)
  if (!listen) el.removeEventListener("wheel", listenerAction, false)
}
