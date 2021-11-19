function getPageNumberNavigation(
  totalPages: number,
  currentPage: number
): (string | number)[] {
  // format: 1 - 1 2 3 ... 8 9 10
  if (totalPages === 1) return []
  let navArray: (number | string)[] = []
  if (totalPages <= 6) {
    navArray = [...Array(totalPages + 1).keys()]
    navArray.shift()
    return navArray
  }
  if (currentPage <= 3)
    return [1, 2, 3, "...", totalPages - 2, totalPages - 1, totalPages]
  if (currentPage > 3 && currentPage < totalPages - 2) {
    navArray = [
      1,
      "...",
      currentPage - 1,
      currentPage,
      currentPage + 1,
      "...",
      totalPages,
    ]
    return navArray
  }
  return [1, "...", totalPages - 2, totalPages - 1, totalPages]
}

export { getPageNumberNavigation }
