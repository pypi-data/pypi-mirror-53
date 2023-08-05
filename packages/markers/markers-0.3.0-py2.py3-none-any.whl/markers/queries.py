LABELS_FOR_PROJECT_QUERY = """
query LabelsForProject (
    $projectId: UUID!,
    $labelFilter: LabelFilter
) {
    projectById (id: $projectId) {
        categories {
            nodes {
                id
                name
                properties
            }
        }
        labels (
            filter: $labelFilter,
            orderBy: CREATED_AT_ASC
        ) {
            nodes {
                id
                cycleId
                document {
                    externalId
                }
                contents
                source
                reviewResult
            }
        }
    }
}
"""

PROJECT_QUERY = """
query ProjectQuery ($projectId: UUID!) {
    projectById (id: $projectId) {
        id
        name
    }
}
"""

ASSIGN_DOCUMENTS_MUTATION = """
mutation AssignDocuments(
    $projectId: UUID!
    $cycleId: String
    $externalDocumentIds: [String]
    $labelIds: [UUID]
    $toSelf: Boolean
    $toRole: String
) {
    assignDocuments(
        input: {
            projectId: $projectId
            cycleId: $cycleId
            externalDocumentIds: $externalDocumentIds
            labelIds: $labelIds
            toSelf: $toSelf
            toRole: $toRole
        }
    ) {
        createdTasks {
            id
        }
    }
}
"""

CREATE_CYCLE_MUTATION = """
mutation CreateCycle ($projectId: UUID!) {
    createCycle(
        input: {
            cycle: {
                projectId: $projectId
            }
        }
    ) {
        cycle {
            id
            creatorId
            projectId
        }
    }
}
"""

PROJECT_CYCLES_QUERY = """
query ProjectCyclesQuery ($projectId: UUID!) {
  projectById (id: $projectId) {
    cycles (orderBy: CREATED_AT_ASC) {
      totalCount
      nodes {
        id
        createdAt
        documentCount
        labelCount
        tasks {
          totalCount
        }
      }
    }
  }
}
"""

CREATE_EXTERNAL_LABEL_MUTATION = """
mutation CreateExternalLabel (
    $projectId: UUID!
    $cycleId: String
    $documentId: UUID
    $externalDocumentId: String
    $contents: JSON!
    $metadata: JSON
) {
    createExternalLabel (input: {
        projectId: $projectId,
        cycleId: $cycleId,
        documentId: $documentId,
        externalDocumentId: $externalDocumentId,
        contents: $contents,
        metadata: $metadata,
    }) {
        label {
            id
            cycleId
            document {
                id
                externalId
            }
            source
            contents
        }
    }
}
"""
