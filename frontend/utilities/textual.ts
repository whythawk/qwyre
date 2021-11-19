function convertCSVtoJSON(
  csv: string,
  headers: string,
  constants: { [x: string]: string } = {}
): { [x: string]: string }[] {
  const rows = csv.replace(/\r/g, "").split(/\n/)
  const keys = headers.split(",")
  let response: { [x: string]: string }[] = []
  for (const row of rows) {
    // https://stackoverflow.com/a/39128144/295606
    const values = row.split(",")
    let rowObj = keys.reduce((o, k, i) => ({ ...o, [k]: values[i].trim() }), {})
    rowObj = Object.assign({}, rowObj, constants)
    response.push(rowObj)
  }
  // Remove duplicates
  // https://stackoverflow.com/a/53543030/295606
  response = response.filter(
    (
      (s) => (o) =>
        ((k) => !s.has(k) && s.add(k))(keys.map((k) => o[k]).join("|"))
    )(new Set())
  )
  return response
}

function convertBlobToBase64(blob: File): Promise<string | ArrayBuffer | null> {
  // https://stackoverflow.com/a/18650249/295606
  // User like:
  //  let b64 = (await this.convertBlobToBase64(blob)) as string
  //  b64 = b64.substring(b64.indexOf(",") + 1) to get rid of ';base64,'
  return new Promise((resolve) => {
    const reader = new FileReader()
    reader.onloadend = () => resolve(reader.result)
    reader.readAsDataURL(blob)
  })
}

function readableDate(term: Date | string, showYear: boolean = true) {
  // https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/toLocaleDateString
  // https://stackoverflow.com/a/66590756/295606
  // https://stackoverflow.com/a/67196206/295606
  const readable = term instanceof Date ? term : new Date(term)
  const day = readable.toLocaleDateString("en-UK", { day: "numeric" })
  const month = readable.toLocaleDateString("en-UK", { month: "short" })
  if (showYear) {
    const year = readable.toLocaleDateString("en-UK", { year: "numeric" })
    return `${day} ${month} ${year}`
  }
  return `${day} ${month}`
}

function capitalizeFirst(text: string): string {
  return text.charAt(0).toUpperCase() + text.slice(1)
}

function splitWordify(text: string): string {
  return text
    .split("_")
    .map((x) => capitalizeFirst(x))
    .join(" ")
}

function snakeWordify(text: string): string {
  return text.toLowerCase().split(" ").join("_")
}

export {
  convertCSVtoJSON,
  convertBlobToBase64,
  readableDate,
  capitalizeFirst,
  splitWordify,
  snakeWordify,
}
