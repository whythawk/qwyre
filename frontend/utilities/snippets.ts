function flatten(value) {
    // https://stackoverflow.com/a/39887884/295606
    return Array.isArray(value) ? [].concat(...value.map(flatten)) ? value
}

export {
    flatten
}