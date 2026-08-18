---
title: Messaging
summary: Study-team-initiated messaging with interested participants, shared conversations, templates, and attachments.
status: authoritative
canonical_for:
  - interested_participant_messaging
  - message_conversations
  - message_templates
  - message_attachments
relevant_when:
  - messaging_an_interested_participant
  - replying_to_a_study_team
  - troubleshooting_messages
  - using_message_templates
---

# Messaging

Messaging is available only after a participant successfully expresses interest.

## Conversation initiation

A study team member must initiate the conversation.

Before study-team initiation:

- The participant cannot message the study
- Matching alone does not permit messaging
- Ask if interested does not create a conversation

After initiation:

- The interested participant may reply
- Study team members may continue the conversation

## Authorization

A study team may message only interested participants.

Exact and partial matching participants cannot be messaged before interest.

All members associated with the study share the conversation history.

## Message identity

Each message identifies:

- Sender
- Recipient interested-participant relationship
- Study
- Timestamp
- Message content
- Attachments, when present

The participant-side recipient is represented through `STUDY_VOLUNTEER`, which associates the participant account with the study.

## Templates

Message templates are study-specific.

A study team member may:

- Compose free text
- Insert a study-specific template
- Modify the composed message before sending

Template substitution uses the represented participant's name, including when the account is a loved-one account.

## Attachments

Reusable message attachments are study-specific and stored by the application.

Rules:

- File type is unrestricted
- Maximum file size is 5 MB
- Attachments may be selected when composing a message

## Conversation visibility

| Condition | Conversation visibility |
|---|---|
| Study inactive by date and `PUBLISHABLE = 1` | Existing conversations remain visible |
| `PUBLISHABLE = 0` | Conversations are hidden |
| Participant deactivated | Historical conversations are hidden from study team |
| Participant active and study publishable | Authorized study team and participant may view |

## Notifications

New messages may generate study-specific email notifications.

See [Study Notifications](../05-study-management/study-notifications.md).

## Audit

Messages contain sender, recipient, and timestamp as business data.

The application does not create a separate message audit event solely to duplicate those facts.

Participant-profile and list viewing remain subject to `PHI_AUDIT`.

## Related pages

- [Interested-Participant Management](interested-participant-management.md)
- [Study Notifications](../05-study-management/study-notifications.md)
- [Recruitment Operations Model](../07-data-model/recruitment-operations-model.md)
- [PHI Audit](../08-operations/phi-audit.md)
