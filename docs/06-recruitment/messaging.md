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

Messaging is durable in-application communication scoped to one interested-participant relationship.
A physical conversation table does not exist. A conversation is derived from all `USER_MESSAGE` rows
for one `STUDY_VOLUNTEER.ID`.

## Initiation and expected behavior

A study team member initiates communication from an interested-participant profile or list. Matching
and Ask if interested do not create a conversation.

After a study-team message exists, the participant interface exposes the conversation and permits
replies. The backend send authorization itself verifies the interest relationship and sender identity,
but does not test that a prior study-team message exists. The study-team-initiation rule is therefore
primarily enforced by participant-interface routing rather than a persisted conversation state.

All authorized members of the study share the same conversation history because messages are scoped
to the study-participant relationship rather than to one staff recipient.

## Physical message model

`USER_MESSAGE` stores:

| Column               | Meaning                                                             |
| -------------------- | ------------------------------------------------------------------- |
| `ID`                 | Sequence-generated primary key                                      |
| `FROM_USER_ID`       | Sender; restrictive foreign key to `APP_USER.ID`                    |
| `STUDY_VOLUNTEER_ID` | Conversation scope; restrictive foreign key to `STUDY_VOLUNTEER.ID` |
| `SENT_DATE`          | Message timestamp                                                   |
| `STATUS`             | `READ` or `UNREAD`                                                  |
| `BODY`               | Message body                                                        |

Indexes support status, sender, relationship, and combined relationship-sender-status queries.

Recipient direction is derived: if `FROM_USER_ID` differs from the interested participant's user ID,
the participant is the recipient; otherwise the shared study team is the recipient. There is no
separate recipient row, conversation owner, subject, edit history, deleted flag, or per-study-member
read receipt.

Conversation views derive study-team and participant inbox summaries from `USER_MESSAGE`,
`STUDY_VOLUNTEER`, active-user views, and study title. They calculate unread counts and most recent
received dates.

## Authorization

A send request must use the logged-in user as `FROM_USER_ID`.

For one conversation:

- the participant sender must be the participant represented by `STUDY_VOLUNTEER`;
- a staff sender must be a member of that study unless the caller is an administrator;
- the participant-study interest relationship must exist; and
- the submitted relationship is replaced with the authoritative database row before persistence.

Conversation reads require the participant to own the relationship or staff to have study access.
The study-team conversation list additionally requires `PUBLISHABLE = 1`.

Participant conversation-list access is restricted to that participant or an administrator.
Participant attachment access requires interest in the owning study. Staff attachment access requires
study membership or administrator access.

Known boundary: message sending checks interest and study membership but does not call the
publishability-specific interested-participant authorization. Existing UI hides or disables messaging
in inaccessible study states, but the send service itself does not establish `PUBLISHABLE = 1` as a
backend precondition.

## Read status

New message objects default to `UNREAD`.

Fetching the full conversation marks each message addressed to the logged-in side as `READ`.
Consequences:

- participant reads mark staff-to-participant messages read;
- staff reads mark participant-to-study messages read;
- one study member's read changes the shared status for all study members; and
- there is no read timestamp or reader identity.

Inbox summaries are derived from current status, not an immutable delivery or read audit.

## Templates

`MESSAGE_TEMPLATE` stores a study-specific template with type, name, text, creation time, and creator.
The unique constraint is `(STUDY_ID, TYPE, NAME)`.

`MESSAGE_TEMPLATE_ATTACHMENT` is the composite-key many-to-many join to reusable attachments. Template
substitution replaces first-name and last-name placeholders before the message row is saved. The
resulting message body is durable and independent of later template edits or deletion.

Templates are authoring aids; a message does not retain a foreign key to the template used.

## Attachments

`ATTACHMENT` stores the study ID, display title, globally unique generated filename, creator, and
creation date. File bytes are stored in the application's configured attachment directory, not in the
database.

`MESSAGE_ATTACHMENT` connects messages and reusable attachments with a composite primary key. Both
foreign keys cascade when the message or attachment is deleted.

For a staff-to-participant message, submitted attachment IDs are intersected with attachments owned by
that study. Invalid or foreign-study IDs are silently removed. Participant replies contain no
attachment-selection interface.

Current client validation permits any file type and limits size to 5 MB. The reviewed backend service
does not independently enforce that 5 MB limit or a file-type allowlist.

## Attachment lifecycle concern

Creation writes the file before inserting the database row. A later database failure can therefore
leave an orphan file.

Deletion schedules the database row for deletion before deleting the file. A file-deletion exception
can roll back the relational transaction while the external file operation is not transactionally
compensated. Conversely, failures after an external deletion can leave a retained row with no file.

Deleting an attachment cascades message and template joins, so historical messages remain but no
longer expose that attachment. The participant interface reports that a removed attachment is no
longer available.

These relational and filesystem operations are not one atomic transaction. No automatic orphan-file
reconciliation was found.

## Message transaction and email notification

Single-message sending runs in a required Spring transaction:

1. Authorize the caller.
1. Validate the interested-participant relationship.
1. Substitute participant name values when applicable.
1. Save `USER_MESSAGE`.
1. Request the configured email notification.
1. Return the persisted message.

The notification call occurs before relational commit. An uncaught notification or email exception can
roll back the message transaction, while an email or queue side effect already handed off cannot be
recalled by database rollback.

Email is a notification about durable in-application data; it is not the durable message source.
`USER_MESSAGE` remains authoritative when the transaction commits.

Bulk sends create a separate `REQUIRES_NEW` transaction for each selected participant. One
participant's failure need not roll back successful messages for other participants. The method
explicitly catches and logs `UnexpectedRollbackException`, so bulk completion is not proof that every
selected message committed.

## Visibility, deletion, audit, and retention

A study becoming inactive by date while remaining publishable can retain conversation access.
`PUBLISHABLE = 0` blocks the study-team conversation list. Participant deactivation removes the
participant from active-user-based conversation views.

Administrator hard deletion explicitly deletes `USER_MESSAGE` rows before deleting
`STUDY_VOLUNTEER`. Ordinary message deletion, edit, archive, or recall is not exposed.

Message rows themselves retain sender, body, timestamp, status, relationship, and attachment links.
No separate message audit duplicates those facts. No immutable evidence records original templates,
readers, read timestamps, failed notification attempts, edits, or deleted messages.

Retention duration for messages and files remains an institutional policy question.

## Attachment security and lifecycle

**Current implementation:** Attachment metadata is stored relationally while bytes are written under
the configured work directory's `attachments` path. Upload and listing require study access. Rename,
delete, and download use attachment-specific authorization for the study and attachment identifier.
The reviewed path establishes study-level authorization, not a creator-only ownership rule.

The stored filename is a SHA3-256 digest of the attachment creation timestamp with the original
extension appended. This avoids using the submitted basename as the stored basename, but it is not a
content-security, encryption, or secrecy control.

The study-team client rejects files larger than 5 MiB. Although the generic file service can validate
size, the reviewed attachment upload service does not invoke that validator. No attachment-specific
backend enforcement was established for allowed extensions, declared or detected content type,
extension-content agreement, malware scanning, quarantine, archive inspection, active content, or
decompression limits. Download MIME type is guessed from the file stream and falls back to
`application/octet-stream`; that download behavior is not upload validation.

**Known implementation concern:** Filesystem and relational changes are not atomic. Creation writes
the file before saving metadata, so a later database failure can leave an orphaned file. Deletion
removes metadata and then attempts file deletion. The file helper logs deletion failure without
propagating it, so metadata deletion can commit while bytes remain. No automatic attachment-orphan
reconciliation or retry was established.

Deletion is an attempted hard deletion of current metadata and current filesystem bytes. No recycle
bin, tombstone, restore workflow, or dedicated upload, rename, download, or delete audit was found.
Generic age-based file deletion support exists, but reviewed evidence does not establish that it is
scheduled for attachments.

**Deployment-specific facts and open decisions:** Filesystem or volume encryption, service-account
permissions, backup encryption and retention, external malware scanning, replication, monitoring, and
secure disposal must be verified per environment. Authoritative server-side size and content rules,
retention, deletion guarantees, orphan reconciliation, lifecycle auditing, and creator-versus-study
member deletion policy remain institutional security and privacy decisions.

## Related pages

- [Interested-Participant Management](interested-participant-management.md)
- [Study Notifications](../05-study-management/study-notifications.md)
- [Recruitment Operations Model](../07-data-model/recruitment-operations-model.md)
- [PHI Audit](../08-operations/phi-audit.md)
