export default {
  canUpdateWorkEdit: (state) => {
    return (
      state.workEdit &&
      Object.keys(state.workEdit).length !== 0 &&
      state.workEdit.state &&
      !["withdrawn", "suspended", "published"].includes(state.workEdit.state)
    )
  },
  canUpdateContractEdit: (state) => {
    return (
      state.contractEdit &&
      Object.keys(state.contractEdit).length !== 0 &&
      !state.contractEdit.isApproved
    )
  },
  workEditCreatorIdentifiers: (state) => {
    // https://stackoverflow.com/a/46694321/295606
    return state.workEdit &&
      Object.keys(state.workEdit).length !== 0 &&
      state.workEdit.metadata &&
      Object.keys(state.workEdit.metadata).length !== 0
      ? state.workEdit.metadata.creator.map(({ identifier }) => identifier)
      : []
  },
  conversionKey: (state) => state.key,
  currentStep: (state) => state.currentStep,
  workSummaries: (state) => state.workSummaries,
  workEdit: (state) => state.workEdit,
  contractEdit: (state) => state.contractEdit,
}
