from models.simulation.result_kind import ResultKind

# Each event outcome maps to the Statistics field (attribute name) that counts it.
RESULT_KIND_COUNTERS = {
    ResultKind.ALLOCATED: "allocated",
    ResultKind.FREED: "freed",
    ResultKind.FREED_MISSING: "freed_missing",
    ResultKind.FAIL_EXTERNAL_FRAGMENTATION: "external_fragmentation_failures",
    ResultKind.FAIL_NO_SPACE: "no_space_failures",
}
