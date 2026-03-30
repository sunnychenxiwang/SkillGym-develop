# List contents (deprecated)

Gets a nested list of all Home objects shared to the user, including 
dashboards, folders, reports, sheets, and templates, as shown on the "Home"
tab.

DEPRECATED - This endpoint is being removed. To adapt to this change, please see Migrate from using the Sheets folder.

Endpoint: GET /folders/personal
Version: 2.0.0
Security: APIToken, OAuth2

## Header parameters:

  - `Authorization` (string)
    API Access Token used to authenticate requests to Smartsheet APIs.

  - `smartsheet-integration-source` (string)
    Uses the following metadata to distinguish between human-initiated API requests and third-party service-initiated calls by AI Connectors or ITSM:

- Integration source type
- Organization name
- Integration source name 

Format:


TYPE,OrgName,SourceName


Examples: 

AI,SampleOrg,My-AI-Connector-v2

SCRIPT,SampleOrg2,Accounting-updater-script

APPLICATION,SampleOrg3,SheetUpdater
    Example: "AI,SampleOrg,My-AI-Connector-v2"

## Query parameters:

  - `include` (string)
    A comma-separated list of optional elements to include in the response:
  * source - adds the Source object indicating which object the folder was created from, if any
  * distributionLink
  * ownerInfo Returns the user with owner permissions, or the user with admin permissions if there is no owner assigned. If no owner or admins are assigned, the Plan Asset Admin is returned. If no Plan Asset Admin is assigned, the System Admin is returned.
  * sheetVersion
  * permalinks
    Enum: "source", "distributionLink", "ownerInfo", "sheetVersion"

## Response 200 fields (application/json):

  - `folders` (array)

  - `folders.id` (number)
    Folder ID.

  - `folders.folders` (array)
    Folders contained in folder.

  - `folders.name` (string)
    Folder name.

  - `folders.permalink` (string)
    URL that represents a direct link to the folder in Smartsheet.

  - `folders.reports` (array)
    Reports contained in folder.

  - `folders.reports.id` (number)
    Asset ID.

  - `folders.reports.name` (string)
    Asset name.

  - `folders.reports.permalink` (string)
    URL that represents a direct link to the asset in Smartsheet.

  - `folders.sheets` (array)
    Sheets contained in folder.

  - `folders.sheets.id` (number)
    Asset ID.

  - `folders.sheets.name` (string)
    Asset name.

  - `folders.sheets.permalink` (string)
    URL that represents a direct link to the asset in Smartsheet.

  - `folders.sights` (array)
    Dashboards contained in folder.

  - `folders.sights.id` (number)
    Asset ID.

  - `folders.sights.name` (string)
    Asset name.

  - `folders.sights.permalink` (string)
    URL that represents a direct link to the asset in Smartsheet.

  - `folders.sights.createdAt` (any)

  - `folders.sights.modifiedAt` (any)

  - `folders.templates` (array)
    Templates contained in folder.

  - `folders.templates.id` (number)
    Asset ID.

  - `folders.templates.name` (string)
    Asset name.

  - `folders.templates.permalink` (string)
    URL that represents a direct link to the asset in Smartsheet.

  - `folders.favorite` (boolean)
    Deprecated Returned only if the user has marked the folder as a favorite in their "Home" tab (value = true).

  - `reports` (array)

  - `reports.scope` (object)

  - `reports.scope.sheets` (array)
    Array of Sheet objects (containing just the sheet ID) of any sheets that the requester has access to that make up the report.

  - `reports.scope.sheets.id` (number)
    Sheet ID.

  - `reports.scope.sheets.fromId` (number)
    The ID of the template from which to create the sheet. This attribute can be specified in a request, but is never present in a response.

  - `reports.scope.sheets.ownerId` (number)
    User ID of the sheet owner.

  - `reports.scope.sheets.accessLevel` (string)
    Enum: "ADMIN", "COMMENTER", "EDITOR", "EDITOR_SHARE", "OWNER", "VIEWER"

  - `reports.scope.sheets.attachments` (array)
    Array of Attachment objects.
Only returned if the [include](/api/smartsheet/openapi/sheets/getsheet) query string parameter contains attachments.

  - `reports.scope.sheets.attachments.id` (number)
    Attachment ID.

  - `reports.scope.sheets.attachments.parentId` (number)
    The ID of the parent.

  - `reports.scope.sheets.attachments.attachmentType` (string)
    Attachment type. Note--Dropbox, Egnyte, and Evernote are not supported for Smartsheet.gov accounts.
    Enum: "BOX_COM", "DROPBOX", "EGNYTE", "EVERNOTE", "FILE", "GOOGLE_DRIVE", "LINK", "ONEDRIVE", "TRELLO"

  - `reports.scope.sheets.attachments.attachmentSubType` (string)
    Attachment sub type. Note--Folder type is for EGNYTE values and the rest are GOOGLE_DRIVE values.
    Enum: "DOCUMENT", "DRAWING", "FOLDER", "PDF", "PRESENTATION", "SPREADSHEET"

  - `reports.scope.sheets.attachments.mimeType` (string)
    Attachment MIME type.
    Example: "PNG"

  - `reports.scope.sheets.attachments.parentType` (string)
    The type of object the attachment belongs to.
    Enum: "COMMENT", "PROOF", "ROW", "SHEET"

  - `reports.scope.sheets.attachments.createdAt` (any)

  - `reports.scope.sheets.attachments.createdBy` (object)
    User object containing name and email of the user who created this attachment.

  - `reports.scope.sheets.attachments.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.scope.sheets.attachments.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.scope.sheets.attachments.name` (string)
    Attachment name.

  - `reports.scope.sheets.attachments.sizeInKb` (number)
    The size of the file, if the attachmentType is FILE.

  - `reports.scope.sheets.attachments.url` (string)
    Attachment temporary URL (files only).

  - `reports.scope.sheets.attachments.urlExpiresInMillis` (number)
    Attachment temporary URL time to live (files only).

  - `reports.scope.sheets.cellImageUploadEnabled` (boolean)
    The sheet is enabled for cell images to be uploaded.

  - `reports.scope.sheets.columns` (array)

  - `reports.scope.sheets.createdAt` (any)

  - `reports.scope.sheets.crossSheetReferences` (array)
    Array of CrossSheetReference objects.
Only returned if the [include](/api/smartsheet/openapi/sheets/getsheet) query string parameter contains crossSheetReferences.

  - `reports.scope.sheets.crossSheetReferences.endColumnId` (number)
    Defines ending edge of range when specifying one or more columns. To specify an entire column, omit the startRowId and endRowId parameters.

  - `reports.scope.sheets.crossSheetReferences.endRowId` (number)
    Defines ending edge of range when specifying one or more rows. To specify an entire row, omit the startColumnId and endColumnId parameters.

  - `reports.scope.sheets.crossSheetReferences.id` (number)
    Cross-sheet reference ID, guaranteed unique within referencing sheet.

  - `reports.scope.sheets.crossSheetReferences.name` (string)
    Friendly name of reference. Auto-generated unless specified in Create Cross-sheet References.

  - `reports.scope.sheets.crossSheetReferences.startColumnId` (number)
    Defines beginning edge of range when specifying one or more columns. To specify an entire column, omit the startRowId and endRowId parameters.

  - `reports.scope.sheets.crossSheetReferences.startRowId` (number)
    Defines beginning edge of range when specifying one or more rows. To specify an entire row, omit the startColumnId and endColumnId parameters.

  - `reports.scope.sheets.crossSheetReferences.status` (string)
    Status of request:
 * 'BLOCKED' - A reference is downstream of a circular issue.
 * 'BROKEN' - The data source location (column, row or sheet) was deleted.
 * 'CIRCULAR' - The formula reference is self referencing and cannot be resolved.
 * 'DISABLED' - Updating the reference is temporarily disabled due to maintenance.
 * 'INVALID/UNKNOWN' - The reference is new and had not been validated.
 * 'NOT_SHARED' - No common shared users.
 * 'OK' - The reference is in a good state.
    Enum: "BLOCKED", "BROKEN", "CIRCULAR", "DISABLED", "INVALID/UNKNOWN", "NOT-SHARED", "OK"

  - `reports.scope.sheets.crossSheetReferences.sourceSheetId` (number)
    Sheet ID of source sheet.

  - `reports.scope.sheets.dependenciesEnabled` (boolean)
    Indicates whether dependencies are enabled.

  - `reports.scope.sheets.discussions` (array)
    Array of Discussion objects
Only returned if the [include](/api/smartsheet/openapi/sheets/getsheet) query string parameter contains discussions.

  - `reports.scope.sheets.discussions.accessLevel` (string)
    Enum: "ADMIN", "COMMENTER", "EDITOR", "EDITOR_SHARE", "OWNER", "VIEWER"

  - `reports.scope.sheets.discussions.id` (number)
    Discussion ID.

  - `reports.scope.sheets.discussions.comments` (array)
    Array of comments in discussion. Only returned if the include query string parameter contains comments.

  - `reports.scope.sheets.discussions.comments.attachments` (array)
    Array of attachments on comments.

  - `reports.scope.sheets.discussions.comments.attachments.id` (number)
    Attachment ID.

  - `reports.scope.sheets.discussions.comments.attachments.parentId` (number)
    The ID of the parent.

  - `reports.scope.sheets.discussions.comments.attachments.attachmentType` (string)
    Attachment type. Note--Dropbox, Egnyte, and Evernote are not supported for Smartsheet.gov accounts.
    Enum: "BOX_COM", "DROPBOX", "EGNYTE", "EVERNOTE", "FILE", "GOOGLE_DRIVE", "LINK", "ONEDRIVE", "TRELLO"

  - `reports.scope.sheets.discussions.comments.attachments.attachmentSubType` (string)
    Attachment sub type. Note--Folder type is for EGNYTE values and the rest are GOOGLE_DRIVE values.
    Enum: "DOCUMENT", "DRAWING", "FOLDER", "PDF", "PRESENTATION", "SPREADSHEET"

  - `reports.scope.sheets.discussions.comments.attachments.mimeType` (string)
    Attachment MIME type.
    Example: "PNG"

  - `reports.scope.sheets.discussions.comments.attachments.parentType` (string)
    The type of object the attachment belongs to.
    Enum: "COMMENT", "PROOF", "ROW", "SHEET"

  - `reports.scope.sheets.discussions.comments.attachments.createdAt` (any)

  - `reports.scope.sheets.discussions.comments.attachments.createdBy` (object)
    User object containing name and email of the user who created this attachment.

  - `reports.scope.sheets.discussions.comments.attachments.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.scope.sheets.discussions.comments.attachments.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.scope.sheets.discussions.comments.attachments.name` (string)
    Attachment name.

  - `reports.scope.sheets.discussions.comments.attachments.sizeInKb` (number)
    The size of the file, if the attachmentType is FILE.

  - `reports.scope.sheets.discussions.comments.attachments.url` (string)
    Attachment temporary URL (files only).

  - `reports.scope.sheets.discussions.comments.attachments.urlExpiresInMillis` (number)
    Attachment temporary URL time to live (files only).

  - `reports.scope.sheets.discussions.comments.createdAt` (any)

  - `reports.scope.sheets.discussions.comments.createdBy` (object)
    User object containing name and email of the creator of this comment.

  - `reports.scope.sheets.discussions.comments.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.scope.sheets.discussions.comments.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.scope.sheets.discussions.comments.discussionId` (number)
    Discussion ID of discussion that contains comment.

  - `reports.scope.sheets.discussions.comments.id` (number)
    Comment ID.

  - `reports.scope.sheets.discussions.comments.modifiedAt` (any)

  - `reports.scope.sheets.discussions.comments.text` (string)
    Comment body.

  - `reports.scope.sheets.discussions.commentAttachments` (array)
    Array of attachments on discussion comments. Only returned if the include query string parameter contains attachments.

  - `reports.scope.sheets.discussions.commentAttachments.id` (number)
    Attachment ID.

  - `reports.scope.sheets.discussions.commentAttachments.parentId` (number)
    The ID of the parent.

  - `reports.scope.sheets.discussions.commentAttachments.attachmentType` (string)
    Attachment type. Note--Dropbox, Egnyte, and Evernote are not supported for Smartsheet.gov accounts.
    Enum: "BOX_COM", "DROPBOX", "EGNYTE", "EVERNOTE", "FILE", "GOOGLE_DRIVE", "LINK", "ONEDRIVE", "TRELLO"

  - `reports.scope.sheets.discussions.commentAttachments.attachmentSubType` (string)
    Attachment sub type. Note--Folder type is for EGNYTE values and the rest are GOOGLE_DRIVE values.
    Enum: "DOCUMENT", "DRAWING", "FOLDER", "PDF", "PRESENTATION", "SPREADSHEET"

  - `reports.scope.sheets.discussions.commentAttachments.mimeType` (string)
    Attachment MIME type.
    Example: "PNG"

  - `reports.scope.sheets.discussions.commentAttachments.parentType` (string)
    The type of object the attachment belongs to.
    Enum: "COMMENT", "PROOF", "ROW", "SHEET"

  - `reports.scope.sheets.discussions.commentAttachments.createdAt` (any)

  - `reports.scope.sheets.discussions.commentAttachments.createdBy` (object)
    User object containing name and email of the user who created this attachment.

  - `reports.scope.sheets.discussions.commentAttachments.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.scope.sheets.discussions.commentAttachments.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.scope.sheets.discussions.commentAttachments.name` (string)
    Attachment name.

  - `reports.scope.sheets.discussions.commentAttachments.sizeInKb` (number)
    The size of the file, if the attachmentType is FILE.

  - `reports.scope.sheets.discussions.commentAttachments.url` (string)
    Attachment temporary URL (files only).

  - `reports.scope.sheets.discussions.commentAttachments.urlExpiresInMillis` (number)
    Attachment temporary URL time to live (files only).

  - `reports.scope.sheets.discussions.commentCount` (number)
    Number of comments in the discussion.

  - `reports.scope.sheets.discussions.createdBy` (object)
    User object containing name and email of the user who created the discussion.

  - `reports.scope.sheets.discussions.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.scope.sheets.discussions.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.scope.sheets.discussions.lastCommentedAt` (any)

  - `reports.scope.sheets.discussions.lastCommentedUser` (object)
    User object containing name and email of the user who last commented on the discussion.

  - `reports.scope.sheets.discussions.lastCommentedUser.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.scope.sheets.discussions.lastCommentedUser.name` (string)
    Example: "Jane Doe"

  - `reports.scope.sheets.discussions.parentId` (number)
    The ID of the associated row or sheet.

  - `reports.scope.sheets.discussions.parentType` (string)
    Type of parent object.
    Enum: "ROW", "SHEET"

  - `reports.scope.sheets.discussions.readOnly` (boolean)
    Indicates whether the user can modify the discussion.

  - `reports.scope.sheets.discussions.title` (string)
    Title automatically created by duplicating the first 100 characters of top-level comment.

  - `reports.scope.sheets.effectiveAttachmentOptions` (array)
    Array of enum strings (see [Attachment.attachmentType](/api/smartsheet/openapi/attachments) indicating the allowable attachment options for the current user and sheet.

  - `reports.scope.sheets.ganttEnabled` (boolean)
    Indicates whether "Gantt View" is enabled.

  - `reports.scope.sheets.hasSummaryFields` (boolean)
    Indicates whether a sheet summary is present.

  - `reports.scope.sheets.isMultiPicklistEnabled` (boolean)
    Indicates whether multi-select is enabled.

  - `reports.scope.sheets.modifiedAt` (any)

  - `reports.scope.sheets.name` (string)
    Sheet name.

  - `reports.scope.sheets.owner` (string)
    Email address of the sheet owner.

  - `reports.scope.sheets.permalink` (string)
    URL that represents a direct link to the sheet in Smartsheet.

  - `reports.scope.sheets.projectSettings` (object)
    Represents the project settings dependencies for a specific sheet. Project settings may be updated on sheets that the user has editor access.

  - `reports.scope.sheets.projectSettings.lengthOfDay` (number)
    Length of a workday for a project sheet.

  - `reports.scope.sheets.projectSettings.nonWorkingDays` (array)
    Non-working days for a project sheet.

  - `reports.scope.sheets.projectSettings.workingDays` (array)
    Enum: "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"

  - `reports.scope.sheets.readOnly` (boolean)
    Returned only if the sheet belongs to an expired trial (value = true).

  - `reports.scope.sheets.resourceManagementEnabled` (boolean)
    Indicates that resource management is enabled.

  - `reports.scope.sheets.resourceManagementType` (string)
    Resource Management type. Indicates the type of RM that is enabled.
    Enum: "NONE", "LEGACY_RESOURCE_MANAGEMENT", "RESOURCE_MANAGEMENT_BY_SMARTSHEET"

  - `reports.scope.sheets.rows` (array)

  - `reports.scope.sheets.rows.id` (number)
    Row ID.

  - `reports.scope.sheets.rows.sheetId` (number)
    Parent sheet ID.

  - `reports.scope.sheets.rows.siblingId` (number)
    Sibling ID.

  - `reports.scope.sheets.rows.accessLevel` (string)
    Enum: "ADMIN", "COMMENTER", "EDITOR", "EDITOR_SHARE", "OWNER", "VIEWER"

  - `reports.scope.sheets.rows.attachments` (array)
    Attachments on row. Only returned if the include query string parameter contains attachments.

  - `reports.scope.sheets.rows.attachments.id` (number)
    Attachment ID.

  - `reports.scope.sheets.rows.attachments.parentId` (number)
    The ID of the parent.

  - `reports.scope.sheets.rows.attachments.attachmentType` (string)
    Attachment type. Note--Dropbox, Egnyte, and Evernote are not supported for Smartsheet.gov accounts.
    Enum: "BOX_COM", "DROPBOX", "EGNYTE", "EVERNOTE", "FILE", "GOOGLE_DRIVE", "LINK", "ONEDRIVE", "TRELLO"

  - `reports.scope.sheets.rows.attachments.attachmentSubType` (string)
    Attachment sub type. Note--Folder type is for EGNYTE values and the rest are GOOGLE_DRIVE values.
    Enum: "DOCUMENT", "DRAWING", "FOLDER", "PDF", "PRESENTATION", "SPREADSHEET"

  - `reports.scope.sheets.rows.attachments.mimeType` (string)
    Attachment MIME type.
    Example: "PNG"

  - `reports.scope.sheets.rows.attachments.parentType` (string)
    The type of object the attachment belongs to.
    Enum: "COMMENT", "PROOF", "ROW", "SHEET"

  - `reports.scope.sheets.rows.attachments.createdAt` (any)

  - `reports.scope.sheets.rows.attachments.createdBy` (object)
    User object containing name and email of the user who created this attachment.

  - `reports.scope.sheets.rows.attachments.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.scope.sheets.rows.attachments.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.scope.sheets.rows.attachments.name` (string)
    Attachment name.

  - `reports.scope.sheets.rows.attachments.sizeInKb` (number)
    The size of the file, if the attachmentType is FILE.

  - `reports.scope.sheets.rows.attachments.url` (string)
    Attachment temporary URL (files only).

  - `reports.scope.sheets.rows.attachments.urlExpiresInMillis` (number)
    Attachment temporary URL time to live (files only).

  - `reports.scope.sheets.rows.cells` (array)
    Cells belonging to the row.

  - `reports.scope.sheets.rows.cells.columnId` (number)
    The ID of the column that the cell is located in.

  - `reports.scope.sheets.rows.cells.rowId` (number)
    The ID of the row the cell is located in.

  - `reports.scope.sheets.rows.cells.columnType` (string)
    Only returned if the include query string parameter contains columnType.

  - `reports.scope.sheets.rows.cells.conditionalFormat` (string)
    The format descriptor describing this cell's conditional format. Only returned if the include query string parameter contains format and this cell has a conditional format applied.

  - `reports.scope.sheets.rows.cells.displayValue` (string)
    Visual representation of cell contents, as presented to the user in the UI.

  - `reports.scope.sheets.rows.cells.format` (string)
    The format descriptor. Only returned if the include query string parameter contains format and this cell has a non-default format applied.

  - `reports.scope.sheets.rows.cells.formula` (string)
    The formula for a cell, if set, for instance =COUNTM([Assigned To]3). Note that calculation errors or problems with a formula do not cause the API call to return an error code. Instead, the response contains the same value as in the UI, such as cell.value = "#CIRCULAR REFERENCE".

  - `reports.scope.sheets.rows.cells.hyperlink` (object)

  - `reports.scope.sheets.rows.cells.hyperlink.reportId` (number)
    If non-null, this hyperlink is a link to the report with this ID.

  - `reports.scope.sheets.rows.cells.hyperlink.sheetId` (number)
    If non-null, this hyperlink is a link to the sheet with this ID.

  - `reports.scope.sheets.rows.cells.hyperlink.sightId` (number)
    If non-null, this hyperlink is a link to the dashboard with this ID.

  - `reports.scope.sheets.rows.cells.hyperlink.url` (string)
    When the hyperlink is a URL link, this property contains the URL value. When the hyperlink is a dashboard/report/sheet link (that is, dashboardId, reportId, or sheetId is non-null), this property contains the permalink to the dashboard, report, or sheet.

  - `reports.scope.sheets.rows.cells.image` (object)

  - `reports.scope.sheets.rows.cells.image.altText` (string)
    Alternate text for the image.

  - `reports.scope.sheets.rows.cells.image.height` (number)
    Original height (in pixels) of the uploaded image.

  - `reports.scope.sheets.rows.cells.image.id` (string)
    Image ID.

  - `reports.scope.sheets.rows.cells.image.width` (number)
    Original width (in pixels) of the uploaded image.

  - `reports.scope.sheets.rows.cells.linkInFromCell` (object)

  - `reports.scope.sheets.rows.cells.linkInFromCell.columnId` (number)
    Column ID of the linked cell.

  - `reports.scope.sheets.rows.cells.linkInFromCell.rowId` (number)
    Row ID of the linked cell.

  - `reports.scope.sheets.rows.cells.linkInFromCell.sheetId` (number)
    Sheet ID of the sheet that the linked cell belongs to.

  - `reports.scope.sheets.rows.cells.linkInFromCell.sheetName` (string)
    Sheet name of the linked cell.

  - `reports.scope.sheets.rows.cells.linkInFromCell.status` (string)
    * BLOCKED One of several other values indicating unusual error conditions.
* BROKEN The row or sheet linked to was deleted.
* CIRCULAR One of several other values indicating unusual error conditions.
* DISABLED One of several other values indicating unusual error conditions.
* INACCESSIBLE The sheet linked to cannot be viewed by this user.
* INVALID One of several other values indicating unusual error conditions.
* NOT_SHARED One of several other values indicating unusual error conditions.
* OK The link is in a good state.
    Enum: "BLOCKED", "BROKEN", "CIRCULAR", "DISABLED", "INACCESSIBLE", "INVALID", "NOT_SHARED", "OK"

  - `reports.scope.sheets.rows.cells.linksOutToCells` (array)

  - `reports.scope.sheets.rows.cells.linksOutToCells.columnId` (number)
    Column ID of the linked cell.

  - `reports.scope.sheets.rows.cells.linksOutToCells.rowId` (number)
    Row ID of the linked cell.

  - `reports.scope.sheets.rows.cells.linksOutToCells.sheetId` (number)
    Sheet ID of the sheet that the linked cell belongs to.

  - `reports.scope.sheets.rows.cells.linksOutToCells.sheetName` (string)
    Sheet name of the linked cell.

  - `reports.scope.sheets.rows.cells.linksOutToCells.status` (string)
    * BLOCKED One of several other values indicating unusual error conditions.
* BROKEN The row or sheet linked to was deleted.
* CIRCULAR One of several other values indicating unusual error conditions.
* DISABLED One of several other values indicating unusual error conditions.
* INACCESSIBLE The sheet linked to cannot be viewed by this user.
* INVALID One of several other values indicating unusual error conditions.
* NOT_SHARED One of several other values indicating unusual error conditions.
* OK The link is in a good state.
    Enum: "BLOCKED", "BROKEN", "CIRCULAR", "DISABLED", "INACCESSIBLE", "INVALID", "NOT_SHARED", "OK"

  - `reports.scope.sheets.rows.cells.objectValue` (any)

  - `reports.scope.sheets.rows.cells.overrideValidation` (boolean)
    (Admin only) Indicates whether the cell value can contain a value outside of the validation limits (value = true). When using this parameter, you must also set strict to false to bypass value type checking. This property is honored for POST or PUT actions that update rows.

  - `reports.scope.sheets.rows.cells.strict` (boolean)
    Set to false to enable lenient parsing. Defaults to true. You can specify this attribute in a request, but it is never present in a response.

  - `reports.scope.sheets.rows.cells.value` (any)
    A string, number, or a Boolean value -- depending on the cell type and the data in the cell. Cell values larger than 4000 characters are silently truncated. An empty cell returns no value.

  - `reports.scope.sheets.rows.columns` (array)
    Columns of row. Only returned if the include query string parameter contains columns.

  - `reports.scope.sheets.rows.conditionalFormat` (string)
    Describes this row's conditional format. Only returned if the include query string parameter contains format and this row has a conditional format applied.
    Example: ",,1,1,,,,,,,,,,,,,"

  - `reports.scope.sheets.rows.createdAt` (any)

  - `reports.scope.sheets.rows.createdBy` (object)
    User object containing name and email of the creator of this row.

  - `reports.scope.sheets.rows.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.scope.sheets.rows.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.scope.sheets.rows.discussions` (array)
    Discussions on the row. Only returned if the include query string parameter contains discussions.

  - `reports.scope.sheets.rows.discussions.accessLevel` (string)
    Enum: "ADMIN", "COMMENTER", "EDITOR", "EDITOR_SHARE", "OWNER", "VIEWER"

  - `reports.scope.sheets.rows.discussions.id` (number)
    Discussion ID.

  - `reports.scope.sheets.rows.discussions.comments` (array)
    Array of comments in discussion. Only returned if the include query string parameter contains comments.

  - `reports.scope.sheets.rows.discussions.comments.attachments` (array)
    Array of attachments on comments.

  - `reports.scope.sheets.rows.discussions.comments.attachments.id` (number)
    Attachment ID.

  - `reports.scope.sheets.rows.discussions.comments.attachments.parentId` (number)
    The ID of the parent.

  - `reports.scope.sheets.rows.discussions.comments.attachments.attachmentType` (string)
    Attachment type. Note--Dropbox, Egnyte, and Evernote are not supported for Smartsheet.gov accounts.
    Enum: "BOX_COM", "DROPBOX", "EGNYTE", "EVERNOTE", "FILE", "GOOGLE_DRIVE", "LINK", "ONEDRIVE", "TRELLO"

  - `reports.scope.sheets.rows.discussions.comments.attachments.attachmentSubType` (string)
    Attachment sub type. Note--Folder type is for EGNYTE values and the rest are GOOGLE_DRIVE values.
    Enum: "DOCUMENT", "DRAWING", "FOLDER", "PDF", "PRESENTATION", "SPREADSHEET"

  - `reports.scope.sheets.rows.discussions.comments.attachments.mimeType` (string)
    Attachment MIME type.
    Example: "PNG"

  - `reports.scope.sheets.rows.discussions.comments.attachments.parentType` (string)
    The type of object the attachment belongs to.
    Enum: "COMMENT", "PROOF", "ROW", "SHEET"

  - `reports.scope.sheets.rows.discussions.comments.attachments.createdAt` (any)

  - `reports.scope.sheets.rows.discussions.comments.attachments.createdBy` (object)
    User object containing name and email of the user who created this attachment.

  - `reports.scope.sheets.rows.discussions.comments.attachments.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.scope.sheets.rows.discussions.comments.attachments.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.scope.sheets.rows.discussions.comments.attachments.name` (string)
    Attachment name.

  - `reports.scope.sheets.rows.discussions.comments.attachments.sizeInKb` (number)
    The size of the file, if the attachmentType is FILE.

  - `reports.scope.sheets.rows.discussions.comments.attachments.url` (string)
    Attachment temporary URL (files only).

  - `reports.scope.sheets.rows.discussions.comments.attachments.urlExpiresInMillis` (number)
    Attachment temporary URL time to live (files only).

  - `reports.scope.sheets.rows.discussions.comments.createdAt` (any)

  - `reports.scope.sheets.rows.discussions.comments.createdBy` (object)
    User object containing name and email of the creator of this comment.

  - `reports.scope.sheets.rows.discussions.comments.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.scope.sheets.rows.discussions.comments.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.scope.sheets.rows.discussions.comments.discussionId` (number)
    Discussion ID of discussion that contains comment.

  - `reports.scope.sheets.rows.discussions.comments.id` (number)
    Comment ID.

  - `reports.scope.sheets.rows.discussions.comments.modifiedAt` (any)

  - `reports.scope.sheets.rows.discussions.comments.text` (string)
    Comment body.

  - `reports.scope.sheets.rows.discussions.commentAttachments` (array)
    Array of attachments on discussion comments. Only returned if the include query string parameter contains attachments.

  - `reports.scope.sheets.rows.discussions.commentAttachments.id` (number)
    Attachment ID.

  - `reports.scope.sheets.rows.discussions.commentAttachments.parentId` (number)
    The ID of the parent.

  - `reports.scope.sheets.rows.discussions.commentAttachments.attachmentType` (string)
    Attachment type. Note--Dropbox, Egnyte, and Evernote are not supported for Smartsheet.gov accounts.
    Enum: "BOX_COM", "DROPBOX", "EGNYTE", "EVERNOTE", "FILE", "GOOGLE_DRIVE", "LINK", "ONEDRIVE", "TRELLO"

  - `reports.scope.sheets.rows.discussions.commentAttachments.attachmentSubType` (string)
    Attachment sub type. Note--Folder type is for EGNYTE values and the rest are GOOGLE_DRIVE values.
    Enum: "DOCUMENT", "DRAWING", "FOLDER", "PDF", "PRESENTATION", "SPREADSHEET"

  - `reports.scope.sheets.rows.discussions.commentAttachments.mimeType` (string)
    Attachment MIME type.
    Example: "PNG"

  - `reports.scope.sheets.rows.discussions.commentAttachments.parentType` (string)
    The type of object the attachment belongs to.
    Enum: "COMMENT", "PROOF", "ROW", "SHEET"

  - `reports.scope.sheets.rows.discussions.commentAttachments.createdAt` (any)

  - `reports.scope.sheets.rows.discussions.commentAttachments.createdBy` (object)
    User object containing name and email of the user who created this attachment.

  - `reports.scope.sheets.rows.discussions.commentAttachments.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.scope.sheets.rows.discussions.commentAttachments.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.scope.sheets.rows.discussions.commentAttachments.name` (string)
    Attachment name.

  - `reports.scope.sheets.rows.discussions.commentAttachments.sizeInKb` (number)
    The size of the file, if the attachmentType is FILE.

  - `reports.scope.sheets.rows.discussions.commentAttachments.url` (string)
    Attachment temporary URL (files only).

  - `reports.scope.sheets.rows.discussions.commentAttachments.urlExpiresInMillis` (number)
    Attachment temporary URL time to live (files only).

  - `reports.scope.sheets.rows.discussions.commentCount` (number)
    Number of comments in the discussion.

  - `reports.scope.sheets.rows.discussions.createdBy` (object)
    User object containing name and email of the user who created the discussion.

  - `reports.scope.sheets.rows.discussions.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.scope.sheets.rows.discussions.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.scope.sheets.rows.discussions.lastCommentedAt` (any)

  - `reports.scope.sheets.rows.discussions.lastCommentedUser` (object)
    User object containing name and email of the user who last commented on the discussion.

  - `reports.scope.sheets.rows.discussions.lastCommentedUser.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.scope.sheets.rows.discussions.lastCommentedUser.name` (string)
    Example: "Jane Doe"

  - `reports.scope.sheets.rows.discussions.parentId` (number)
    The ID of the associated row or sheet.

  - `reports.scope.sheets.rows.discussions.parentType` (string)
    Type of parent object.
    Enum: "ROW", "SHEET"

  - `reports.scope.sheets.rows.discussions.readOnly` (boolean)
    Indicates whether the user can modify the discussion.

  - `reports.scope.sheets.rows.discussions.title` (string)
    Title automatically created by duplicating the first 100 characters of top-level comment.

  - `reports.scope.sheets.rows.proof` (object)
    Object containing zero or more media items, including images, videos, and documents, for review, editing, or approval.

  - `reports.scope.sheets.rows.proof.id` (number)
    Proof ID of the proof version.

  - `reports.scope.sheets.rows.proof.originalId` (number)
    Proof ID of the original proof version.

  - `reports.scope.sheets.rows.proof.name` (string)
    Proof name. This is the same as primary column value. If the primary column value is empty, name is empty.

  - `reports.scope.sheets.rows.proof.type` (string)
    File type for the proof version.
    Enum: "DOCUMENT", "IMAGE", "MIXED", "NONE", "VIDEO"

  - `reports.scope.sheets.rows.proof.documentType` (string)
    If type=DOCUMENT, then this indicates the type of file, such as PDF.

  - `reports.scope.sheets.rows.proof.proofRequestUrl` (string)
    URL to review a proofing request.

  - `reports.scope.sheets.rows.proof.version` (number)
    The version number of the proof.

  - `reports.scope.sheets.rows.proof.lastUpdatedAt` (any)

  - `reports.scope.sheets.rows.proof.lastUpdatedBy` (object)
    User object containing name and email of the user who last updated the proof.

  - `reports.scope.sheets.rows.proof.lastUpdatedBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.scope.sheets.rows.proof.lastUpdatedBy.name` (string)
    Example: "Jane Doe"

  - `reports.scope.sheets.rows.proof.isCompleted` (boolean)
    Indicates whether the proof is completed.

  - `reports.scope.sheets.rows.proof.attachments` (array)
    Array of Attachment objects. Only returned if the include query string parameter contains attachments.

  - `reports.scope.sheets.rows.proof.attachments.id` (number)
    Attachment ID.

  - `reports.scope.sheets.rows.proof.attachments.parentId` (number)
    The ID of the parent.

  - `reports.scope.sheets.rows.proof.attachments.attachmentType` (string)
    Attachment type. Note--Dropbox, Egnyte, and Evernote are not supported for Smartsheet.gov accounts.
    Enum: "BOX_COM", "DROPBOX", "EGNYTE", "EVERNOTE", "FILE", "GOOGLE_DRIVE", "LINK", "ONEDRIVE", "TRELLO"

  - `reports.scope.sheets.rows.proof.attachments.attachmentSubType` (string)
    Attachment sub type. Note--Folder type is for EGNYTE values and the rest are GOOGLE_DRIVE values.
    Enum: "DOCUMENT", "DRAWING", "FOLDER", "PDF", "PRESENTATION", "SPREADSHEET"

  - `reports.scope.sheets.rows.proof.attachments.mimeType` (string)
    Attachment MIME type.
    Example: "PNG"

  - `reports.scope.sheets.rows.proof.attachments.parentType` (string)
    The type of object the attachment belongs to.
    Enum: "COMMENT", "PROOF", "ROW", "SHEET"

  - `reports.scope.sheets.rows.proof.attachments.createdAt` (any)

  - `reports.scope.sheets.rows.proof.attachments.createdBy` (object)
    User object containing name and email of the user who created this attachment.

  - `reports.scope.sheets.rows.proof.attachments.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.scope.sheets.rows.proof.attachments.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.scope.sheets.rows.proof.attachments.name` (string)
    Attachment name.

  - `reports.scope.sheets.rows.proof.attachments.sizeInKb` (number)
    The size of the file, if the attachmentType is FILE.

  - `reports.scope.sheets.rows.proof.attachments.url` (string)
    Attachment temporary URL (files only).

  - `reports.scope.sheets.rows.proof.attachments.urlExpiresInMillis` (number)
    Attachment temporary URL time to live (files only).

  - `reports.scope.sheets.rows.proof.discussions` (array)
    Array of Discussion objects. Only returned if the include query string parameter contains discussions.

  - `reports.scope.sheets.rows.proof.discussions.accessLevel` (string)
    Enum: "ADMIN", "COMMENTER", "EDITOR", "EDITOR_SHARE", "OWNER", "VIEWER"

  - `reports.scope.sheets.rows.proof.discussions.id` (number)
    Discussion ID.

  - `reports.scope.sheets.rows.proof.discussions.comments` (array)
    Array of comments in discussion. Only returned if the include query string parameter contains comments.

  - `reports.scope.sheets.rows.proof.discussions.comments.attachments` (array)
    Array of attachments on comments.

  - `reports.scope.sheets.rows.proof.discussions.comments.attachments.id` (number)
    Attachment ID.

  - `reports.scope.sheets.rows.proof.discussions.comments.attachments.parentId` (number)
    The ID of the parent.

  - `reports.scope.sheets.rows.proof.discussions.comments.attachments.attachmentType` (string)
    Attachment type. Note--Dropbox, Egnyte, and Evernote are not supported for Smartsheet.gov accounts.
    Enum: "BOX_COM", "DROPBOX", "EGNYTE", "EVERNOTE", "FILE", "GOOGLE_DRIVE", "LINK", "ONEDRIVE", "TRELLO"

  - `reports.scope.sheets.rows.proof.discussions.comments.attachments.attachmentSubType` (string)
    Attachment sub type. Note--Folder type is for EGNYTE values and the rest are GOOGLE_DRIVE values.
    Enum: "DOCUMENT", "DRAWING", "FOLDER", "PDF", "PRESENTATION", "SPREADSHEET"

  - `reports.scope.sheets.rows.proof.discussions.comments.attachments.mimeType` (string)
    Attachment MIME type.
    Example: "PNG"

  - `reports.scope.sheets.rows.proof.discussions.comments.attachments.parentType` (string)
    The type of object the attachment belongs to.
    Enum: "COMMENT", "PROOF", "ROW", "SHEET"

  - `reports.scope.sheets.rows.proof.discussions.comments.attachments.createdAt` (any)

  - `reports.scope.sheets.rows.proof.discussions.comments.attachments.createdBy` (object)
    User object containing name and email of the user who created this attachment.

  - `reports.scope.sheets.rows.proof.discussions.comments.attachments.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.scope.sheets.rows.proof.discussions.comments.attachments.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.scope.sheets.rows.proof.discussions.comments.attachments.name` (string)
    Attachment name.

  - `reports.scope.sheets.rows.proof.discussions.comments.attachments.sizeInKb` (number)
    The size of the file, if the attachmentType is FILE.

  - `reports.scope.sheets.rows.proof.discussions.comments.attachments.url` (string)
    Attachment temporary URL (files only).

  - `reports.scope.sheets.rows.proof.discussions.comments.attachments.urlExpiresInMillis` (number)
    Attachment temporary URL time to live (files only).

  - `reports.scope.sheets.rows.proof.discussions.comments.createdAt` (any)

  - `reports.scope.sheets.rows.proof.discussions.comments.createdBy` (object)
    User object containing name and email of the creator of this comment.

  - `reports.scope.sheets.rows.proof.discussions.comments.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.scope.sheets.rows.proof.discussions.comments.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.scope.sheets.rows.proof.discussions.comments.discussionId` (number)
    Discussion ID of discussion that contains comment.

  - `reports.scope.sheets.rows.proof.discussions.comments.id` (number)
    Comment ID.

  - `reports.scope.sheets.rows.proof.discussions.comments.modifiedAt` (any)

  - `reports.scope.sheets.rows.proof.discussions.comments.text` (string)
    Comment body.

  - `reports.scope.sheets.rows.proof.discussions.commentAttachments` (array)
    Array of attachments on discussion comments. Only returned if the include query string parameter contains attachments.

  - `reports.scope.sheets.rows.proof.discussions.commentAttachments.id` (number)
    Attachment ID.

  - `reports.scope.sheets.rows.proof.discussions.commentAttachments.parentId` (number)
    The ID of the parent.

  - `reports.scope.sheets.rows.proof.discussions.commentAttachments.attachmentType` (string)
    Attachment type. Note--Dropbox, Egnyte, and Evernote are not supported for Smartsheet.gov accounts.
    Enum: "BOX_COM", "DROPBOX", "EGNYTE", "EVERNOTE", "FILE", "GOOGLE_DRIVE", "LINK", "ONEDRIVE", "TRELLO"

  - `reports.scope.sheets.rows.proof.discussions.commentAttachments.attachmentSubType` (string)
    Attachment sub type. Note--Folder type is for EGNYTE values and the rest are GOOGLE_DRIVE values.
    Enum: "DOCUMENT", "DRAWING", "FOLDER", "PDF", "PRESENTATION", "SPREADSHEET"

  - `reports.scope.sheets.rows.proof.discussions.commentAttachments.mimeType` (string)
    Attachment MIME type.
    Example: "PNG"

  - `reports.scope.sheets.rows.proof.discussions.commentAttachments.parentType` (string)
    The type of object the attachment belongs to.
    Enum: "COMMENT", "PROOF", "ROW", "SHEET"

  - `reports.scope.sheets.rows.proof.discussions.commentAttachments.createdAt` (any)

  - `reports.scope.sheets.rows.proof.discussions.commentAttachments.createdBy` (object)
    User object containing name and email of the user who created this attachment.

  - `reports.scope.sheets.rows.proof.discussions.commentAttachments.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.scope.sheets.rows.proof.discussions.commentAttachments.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.scope.sheets.rows.proof.discussions.commentAttachments.name` (string)
    Attachment name.

  - `reports.scope.sheets.rows.proof.discussions.commentAttachments.sizeInKb` (number)
    The size of the file, if the attachmentType is FILE.

  - `reports.scope.sheets.rows.proof.discussions.commentAttachments.url` (string)
    Attachment temporary URL (files only).

  - `reports.scope.sheets.rows.proof.discussions.commentAttachments.urlExpiresInMillis` (number)
    Attachment temporary URL time to live (files only).

  - `reports.scope.sheets.rows.proof.discussions.commentCount` (number)
    Number of comments in the discussion.

  - `reports.scope.sheets.rows.proof.discussions.createdBy` (object)
    User object containing name and email of the user who created the discussion.

  - `reports.scope.sheets.rows.proof.discussions.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.scope.sheets.rows.proof.discussions.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.scope.sheets.rows.proof.discussions.lastCommentedAt` (any)

  - `reports.scope.sheets.rows.proof.discussions.lastCommentedUser` (object)
    User object containing name and email of the user who last commented on the discussion.

  - `reports.scope.sheets.rows.proof.discussions.lastCommentedUser.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.scope.sheets.rows.proof.discussions.lastCommentedUser.name` (string)
    Example: "Jane Doe"

  - `reports.scope.sheets.rows.proof.discussions.parentId` (number)
    The ID of the associated row or sheet.

  - `reports.scope.sheets.rows.proof.discussions.parentType` (string)
    Type of parent object.
    Enum: "ROW", "SHEET"

  - `reports.scope.sheets.rows.proof.discussions.readOnly` (boolean)
    Indicates whether the user can modify the discussion.

  - `reports.scope.sheets.rows.proof.discussions.title` (string)
    Title automatically created by duplicating the first 100 characters of top-level comment.

  - `reports.scope.sheets.rows.expanded` (boolean)
    Indicates whether the row is expanded or collapsed.

  - `reports.scope.sheets.rows.filteredOut` (boolean)
    Indicates if the row is filtered out by a column filter. Only returned if the include query string parameter contains filters.

  - `reports.scope.sheets.rows.format` (string)
    Format descriptor. Only returned if the include query string parameter contains format and this row has a non-default format applied.
    Example: ",,1,1,,,,,,,,,,,,,"

  - `reports.scope.sheets.rows.inCriticalPath` (boolean)
    Only returned, with a value of true, if the sheet is a project sheet with dependencies enabled and this row is in the critical path.

  - `reports.scope.sheets.rows.locked` (boolean)
    Indicates whether the row is locked.

  - `reports.scope.sheets.rows.lockedForUser` (boolean)
    Indicates whether the row is locked for the requesting user.

  - `reports.scope.sheets.rows.modifiedAt` (any)

  - `reports.scope.sheets.rows.modifiedBy` (object)
    User object containing name and email of the last person to modify this row.

  - `reports.scope.sheets.rows.modifiedBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.scope.sheets.rows.modifiedBy.name` (string)
    Example: "Jane Doe"

  - `reports.scope.sheets.rows.permaLink` (string)
    URL that represents a direct link to the row in Smartsheet. Only returned if the include query string parameter contains rowPermalink.

  - `reports.scope.sheets.rows.rowNumber` (number)
    Row number within the sheet.

  - `reports.scope.sheets.rows.version` (number)
    Sheet version number that is incremented every time a sheet is modified.

  - `reports.scope.sheets.showParentRowsForFilters` (boolean)
    Returned only if there are column filters on the sheet. Value = true if "show parent rows" is enabled for the filters.

  - `reports.scope.sheets.source` (object)

  - `reports.scope.sheets.source.id` (number)
    The ID of the dashboard, report, sheet, or template from which the enclosing dashboard, report, sheet, or template was created.

  - `reports.scope.sheets.source.type` (string)
    report, sheet, sight (aka dashboard), or template.

  - `reports.scope.sheets.summary` (object)
    Represents the entire summary, or a list of defined fields and values, for a specific sheet.

  - `reports.scope.sheets.summary.fields` (array)
    Array of summary (or metadata) fields defined on the sheet.

  - `reports.scope.sheets.summary.fields.id` (number)
    SummaryField ID.

  - `reports.scope.sheets.summary.fields.contactOptions` (array)
    Array of ContactOption objects to specify a pre-defined list of values for the column. Column type must be CONTACT_LIST.

  - `reports.scope.sheets.summary.fields.contactOptions.email` (string)
    A parsable email address.

  - `reports.scope.sheets.summary.fields.contactOptions.name` (string)
    Can be a user's name, display name, or free text.

  - `reports.scope.sheets.summary.fields.createdAt` (any)

  - `reports.scope.sheets.summary.fields.createdBy` (object)
    User object containing name and email of the creator of this summary field.

  - `reports.scope.sheets.summary.fields.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.scope.sheets.summary.fields.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.scope.sheets.summary.fields.displayValue` (string)
    Visual representation of cell contents, as presented to the user in the UI.

  - `reports.scope.sheets.summary.fields.format` (string)
    The format descriptor. Only returned if the include query string parameter contains format and this column has a non-default format applied to it.

  - `reports.scope.sheets.summary.fields.formula` (string)
    The formula for a cell, if set.

  - `reports.scope.sheets.summary.fields.hyperlink` (object)

  - `reports.scope.sheets.summary.fields.hyperlink.reportId` (number)
    If non-null, this hyperlink is a link to the report with this ID.

  - `reports.scope.sheets.summary.fields.hyperlink.sheetId` (number)
    If non-null, this hyperlink is a link to the sheet with this ID.

  - `reports.scope.sheets.summary.fields.hyperlink.sightId` (number)
    If non-null, this hyperlink is a link to the dashboard with this ID.

  - `reports.scope.sheets.summary.fields.hyperlink.url` (string)
    When the hyperlink is a URL link, this property contains the URL value. When the hyperlink is a dashboard/report/sheet link (that is, dashboardId, reportId, or sheetId is non-null), this property contains the permalink to the dashboard, report, or sheet.

  - `reports.scope.sheets.summary.fields.image` (object)

  - `reports.scope.sheets.summary.fields.image.altText` (string)
    Alternate text for the image.

  - `reports.scope.sheets.summary.fields.image.height` (number)
    Original height (in pixels) of the uploaded image.

  - `reports.scope.sheets.summary.fields.image.id` (string)
    Image ID.

  - `reports.scope.sheets.summary.fields.image.width` (number)
    Original width (in pixels) of the uploaded image.

  - `reports.scope.sheets.summary.fields.index` (number)
    Field index or position. This number is zero-based.

  - `reports.scope.sheets.summary.fields.locked` (boolean)
    Indicates whether the field is locked.

  - `reports.scope.sheets.summary.fields.lockedForUser` (boolean)
    Indicates whether the field is locked for the requesting user.

  - `reports.scope.sheets.summary.fields.modifiedAt` (any)

  - `reports.scope.sheets.summary.fields.modifiedBy` (object)
    User object containing name and email of the user who most recently modified this summary field.

  - `reports.scope.sheets.summary.fields.modifiedBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.scope.sheets.summary.fields.modifiedBy.name` (string)
    Example: "Jane Doe"

  - `reports.scope.sheets.summary.fields.objectValue` (any)

  - `reports.scope.sheets.summary.fields.options` (array)
    When applicable for PICKLIST column type. Array of the options available for the field.

  - `reports.scope.sheets.summary.fields.symbol` (string)
    When applicable for PICKLIST column type.

  - `reports.scope.sheets.summary.fields.title` (string)
    Arbitrary name, must be unique within summary.

  - `reports.scope.sheets.summary.fields.type` (string)
    Enum: "ABSTRACT_DATETIME", "CHECKBOX", "CONTACT_LIST", "DATE", "DATETIME", "DURATION", "MULTI_CONTACT_LIST", "MULTI_PICKLIST", "PICKLIST", "PREDECESSOR", "TEXT_NUMBER"

  - `reports.scope.sheets.summary.fields.validation` (boolean)
    Indicates whether summary field values are restricted to the type.

  - `reports.scope.sheets.totalRowCount` (number)
    The total number of rows in the sheet.

  - `reports.scope.sheets.userPermissions` (object)
    Describes the current user's editing permissions for a specific sheet.

  - `reports.scope.sheets.userPermissions.summaryPermissions` (string)
    One of:
  * ADMIN: full control over fields.
  * READ_DELETE: sheet is owned by an individual account that doesn't have summary capabilities. If a summary exists, the only possible operations are GET and DELETE fields.
  * READ_ONLY.
  * READ_WRITE: can edit values of existing fields, but not create or delete fields, nor modify field type.
    Enum: "ADMIN", "READ_DELETE", "READ_ONLY", "READ_WRITE"

  - `reports.scope.sheets.userSettings` (object)
    Represents individual user settings for a specific sheet. User settings may be updated even on sheets where the current user only has read access (for example, viewer permissions or a read-only sheet).

  - `reports.scope.sheets.userSettings.criticalPathEnabled` (boolean)
    Does this user have "Show Critical Path" turned on for this sheet? NOTE: This setting only has an effect on project sheets with dependencies enabled.

  - `reports.scope.sheets.userSettings.displaySummaryTasks` (boolean)
    Does this user have "Display Summary Tasks" turned on for this sheet? Applies only to sheets where "Calendar View" has been configured.

  - `reports.scope.sheets.version` (number)
    A number that is incremented every time a sheet is modified.

  - `reports.scope.sheets.workspace` (object)

  - `reports.scope.sheets.workspace.id` (number)
    Workspace ID.

  - `reports.scope.sheets.workspace.name` (string)
    Workspace name.

  - `reports.scope.sheets.workspace.accessLevel` (string)
    Enum: "ADMIN", "COMMENTER", "EDITOR", "EDITOR_SHARE", "OWNER", "VIEWER"

  - `reports.scope.sheets.workspace.permalink` (string)
    URL that represents a direct link to the workspace in Smartsheet.

  - `reports.scope.sheets.favorite` (boolean)
    Deprecated Returned only if the user has marked this sheet as a favorite in their Home tab (value = true).

  - `reports.scope.workspaces` (array)
    Array of Workspace objects (containing just the workspace ID) that the requester has access to that make up the report.

  - `reports.scope.workspaces.id` (number)
    Workspace ID.

  - `reports.scope.workspaces.name` (string)
    Workspace name.

  - `reports.scope.workspaces.accessLevel` (string)
    Enum: "ADMIN", "COMMENTER", "EDITOR", "EDITOR_SHARE", "OWNER", "VIEWER"

  - `reports.scope.workspaces.permalink` (string)
    URL that represents a direct link to the workspace in Smartsheet.

  - `reports.sourceSheets` (array)
    An array of Sheet objects (without rows), representing the sheets that rows in the report originated from. Only included in the Get Report response if the include parameter specifies sourceSheets.

  - `reports.sourceSheets.id` (number)
    Sheet ID.

  - `reports.sourceSheets.fromId` (number)
    The ID of the template from which to create the sheet. This attribute can be specified in a request, but is never present in a response.

  - `reports.sourceSheets.ownerId` (number)
    User ID of the sheet owner.

  - `reports.sourceSheets.accessLevel` (string)
    Enum: "ADMIN", "COMMENTER", "EDITOR", "EDITOR_SHARE", "OWNER", "VIEWER"

  - `reports.sourceSheets.attachments` (array)
    Array of Attachment objects.
Only returned if the [include](/api/smartsheet/openapi/sheets/getsheet) query string parameter contains attachments.

  - `reports.sourceSheets.attachments.id` (number)
    Attachment ID.

  - `reports.sourceSheets.attachments.parentId` (number)
    The ID of the parent.

  - `reports.sourceSheets.attachments.attachmentType` (string)
    Attachment type. Note--Dropbox, Egnyte, and Evernote are not supported for Smartsheet.gov accounts.
    Enum: "BOX_COM", "DROPBOX", "EGNYTE", "EVERNOTE", "FILE", "GOOGLE_DRIVE", "LINK", "ONEDRIVE", "TRELLO"

  - `reports.sourceSheets.attachments.attachmentSubType` (string)
    Attachment sub type. Note--Folder type is for EGNYTE values and the rest are GOOGLE_DRIVE values.
    Enum: "DOCUMENT", "DRAWING", "FOLDER", "PDF", "PRESENTATION", "SPREADSHEET"

  - `reports.sourceSheets.attachments.mimeType` (string)
    Attachment MIME type.
    Example: "PNG"

  - `reports.sourceSheets.attachments.parentType` (string)
    The type of object the attachment belongs to.
    Enum: "COMMENT", "PROOF", "ROW", "SHEET"

  - `reports.sourceSheets.attachments.createdAt` (any)

  - `reports.sourceSheets.attachments.createdBy` (object)
    User object containing name and email of the user who created this attachment.

  - `reports.sourceSheets.attachments.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.sourceSheets.attachments.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.sourceSheets.attachments.name` (string)
    Attachment name.

  - `reports.sourceSheets.attachments.sizeInKb` (number)
    The size of the file, if the attachmentType is FILE.

  - `reports.sourceSheets.attachments.url` (string)
    Attachment temporary URL (files only).

  - `reports.sourceSheets.attachments.urlExpiresInMillis` (number)
    Attachment temporary URL time to live (files only).

  - `reports.sourceSheets.cellImageUploadEnabled` (boolean)
    The sheet is enabled for cell images to be uploaded.

  - `reports.sourceSheets.columns` (array)

  - `reports.sourceSheets.createdAt` (any)

  - `reports.sourceSheets.crossSheetReferences` (array)
    Array of CrossSheetReference objects.
Only returned if the [include](/api/smartsheet/openapi/sheets/getsheet) query string parameter contains crossSheetReferences.

  - `reports.sourceSheets.crossSheetReferences.endColumnId` (number)
    Defines ending edge of range when specifying one or more columns. To specify an entire column, omit the startRowId and endRowId parameters.

  - `reports.sourceSheets.crossSheetReferences.endRowId` (number)
    Defines ending edge of range when specifying one or more rows. To specify an entire row, omit the startColumnId and endColumnId parameters.

  - `reports.sourceSheets.crossSheetReferences.id` (number)
    Cross-sheet reference ID, guaranteed unique within referencing sheet.

  - `reports.sourceSheets.crossSheetReferences.name` (string)
    Friendly name of reference. Auto-generated unless specified in Create Cross-sheet References.

  - `reports.sourceSheets.crossSheetReferences.startColumnId` (number)
    Defines beginning edge of range when specifying one or more columns. To specify an entire column, omit the startRowId and endRowId parameters.

  - `reports.sourceSheets.crossSheetReferences.startRowId` (number)
    Defines beginning edge of range when specifying one or more rows. To specify an entire row, omit the startColumnId and endColumnId parameters.

  - `reports.sourceSheets.crossSheetReferences.status` (string)
    Status of request:
 * 'BLOCKED' - A reference is downstream of a circular issue.
 * 'BROKEN' - The data source location (column, row or sheet) was deleted.
 * 'CIRCULAR' - The formula reference is self referencing and cannot be resolved.
 * 'DISABLED' - Updating the reference is temporarily disabled due to maintenance.
 * 'INVALID/UNKNOWN' - The reference is new and had not been validated.
 * 'NOT_SHARED' - No common shared users.
 * 'OK' - The reference is in a good state.
    Enum: "BLOCKED", "BROKEN", "CIRCULAR", "DISABLED", "INVALID/UNKNOWN", "NOT-SHARED", "OK"

  - `reports.sourceSheets.crossSheetReferences.sourceSheetId` (number)
    Sheet ID of source sheet.

  - `reports.sourceSheets.dependenciesEnabled` (boolean)
    Indicates whether dependencies are enabled.

  - `reports.sourceSheets.discussions` (array)
    Array of Discussion objects
Only returned if the [include](/api/smartsheet/openapi/sheets/getsheet) query string parameter contains discussions.

  - `reports.sourceSheets.discussions.accessLevel` (string)
    Enum: "ADMIN", "COMMENTER", "EDITOR", "EDITOR_SHARE", "OWNER", "VIEWER"

  - `reports.sourceSheets.discussions.id` (number)
    Discussion ID.

  - `reports.sourceSheets.discussions.comments` (array)
    Array of comments in discussion. Only returned if the include query string parameter contains comments.

  - `reports.sourceSheets.discussions.comments.attachments` (array)
    Array of attachments on comments.

  - `reports.sourceSheets.discussions.comments.attachments.id` (number)
    Attachment ID.

  - `reports.sourceSheets.discussions.comments.attachments.parentId` (number)
    The ID of the parent.

  - `reports.sourceSheets.discussions.comments.attachments.attachmentType` (string)
    Attachment type. Note--Dropbox, Egnyte, and Evernote are not supported for Smartsheet.gov accounts.
    Enum: "BOX_COM", "DROPBOX", "EGNYTE", "EVERNOTE", "FILE", "GOOGLE_DRIVE", "LINK", "ONEDRIVE", "TRELLO"

  - `reports.sourceSheets.discussions.comments.attachments.attachmentSubType` (string)
    Attachment sub type. Note--Folder type is for EGNYTE values and the rest are GOOGLE_DRIVE values.
    Enum: "DOCUMENT", "DRAWING", "FOLDER", "PDF", "PRESENTATION", "SPREADSHEET"

  - `reports.sourceSheets.discussions.comments.attachments.mimeType` (string)
    Attachment MIME type.
    Example: "PNG"

  - `reports.sourceSheets.discussions.comments.attachments.parentType` (string)
    The type of object the attachment belongs to.
    Enum: "COMMENT", "PROOF", "ROW", "SHEET"

  - `reports.sourceSheets.discussions.comments.attachments.createdAt` (any)

  - `reports.sourceSheets.discussions.comments.attachments.createdBy` (object)
    User object containing name and email of the user who created this attachment.

  - `reports.sourceSheets.discussions.comments.attachments.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.sourceSheets.discussions.comments.attachments.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.sourceSheets.discussions.comments.attachments.name` (string)
    Attachment name.

  - `reports.sourceSheets.discussions.comments.attachments.sizeInKb` (number)
    The size of the file, if the attachmentType is FILE.

  - `reports.sourceSheets.discussions.comments.attachments.url` (string)
    Attachment temporary URL (files only).

  - `reports.sourceSheets.discussions.comments.attachments.urlExpiresInMillis` (number)
    Attachment temporary URL time to live (files only).

  - `reports.sourceSheets.discussions.comments.createdAt` (any)

  - `reports.sourceSheets.discussions.comments.createdBy` (object)
    User object containing name and email of the creator of this comment.

  - `reports.sourceSheets.discussions.comments.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.sourceSheets.discussions.comments.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.sourceSheets.discussions.comments.discussionId` (number)
    Discussion ID of discussion that contains comment.

  - `reports.sourceSheets.discussions.comments.id` (number)
    Comment ID.

  - `reports.sourceSheets.discussions.comments.modifiedAt` (any)

  - `reports.sourceSheets.discussions.comments.text` (string)
    Comment body.

  - `reports.sourceSheets.discussions.commentAttachments` (array)
    Array of attachments on discussion comments. Only returned if the include query string parameter contains attachments.

  - `reports.sourceSheets.discussions.commentAttachments.id` (number)
    Attachment ID.

  - `reports.sourceSheets.discussions.commentAttachments.parentId` (number)
    The ID of the parent.

  - `reports.sourceSheets.discussions.commentAttachments.attachmentType` (string)
    Attachment type. Note--Dropbox, Egnyte, and Evernote are not supported for Smartsheet.gov accounts.
    Enum: "BOX_COM", "DROPBOX", "EGNYTE", "EVERNOTE", "FILE", "GOOGLE_DRIVE", "LINK", "ONEDRIVE", "TRELLO"

  - `reports.sourceSheets.discussions.commentAttachments.attachmentSubType` (string)
    Attachment sub type. Note--Folder type is for EGNYTE values and the rest are GOOGLE_DRIVE values.
    Enum: "DOCUMENT", "DRAWING", "FOLDER", "PDF", "PRESENTATION", "SPREADSHEET"

  - `reports.sourceSheets.discussions.commentAttachments.mimeType` (string)
    Attachment MIME type.
    Example: "PNG"

  - `reports.sourceSheets.discussions.commentAttachments.parentType` (string)
    The type of object the attachment belongs to.
    Enum: "COMMENT", "PROOF", "ROW", "SHEET"

  - `reports.sourceSheets.discussions.commentAttachments.createdAt` (any)

  - `reports.sourceSheets.discussions.commentAttachments.createdBy` (object)
    User object containing name and email of the user who created this attachment.

  - `reports.sourceSheets.discussions.commentAttachments.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.sourceSheets.discussions.commentAttachments.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.sourceSheets.discussions.commentAttachments.name` (string)
    Attachment name.

  - `reports.sourceSheets.discussions.commentAttachments.sizeInKb` (number)
    The size of the file, if the attachmentType is FILE.

  - `reports.sourceSheets.discussions.commentAttachments.url` (string)
    Attachment temporary URL (files only).

  - `reports.sourceSheets.discussions.commentAttachments.urlExpiresInMillis` (number)
    Attachment temporary URL time to live (files only).

  - `reports.sourceSheets.discussions.commentCount` (number)
    Number of comments in the discussion.

  - `reports.sourceSheets.discussions.createdBy` (object)
    User object containing name and email of the user who created the discussion.

  - `reports.sourceSheets.discussions.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.sourceSheets.discussions.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.sourceSheets.discussions.lastCommentedAt` (any)

  - `reports.sourceSheets.discussions.lastCommentedUser` (object)
    User object containing name and email of the user who last commented on the discussion.

  - `reports.sourceSheets.discussions.lastCommentedUser.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.sourceSheets.discussions.lastCommentedUser.name` (string)
    Example: "Jane Doe"

  - `reports.sourceSheets.discussions.parentId` (number)
    The ID of the associated row or sheet.

  - `reports.sourceSheets.discussions.parentType` (string)
    Type of parent object.
    Enum: "ROW", "SHEET"

  - `reports.sourceSheets.discussions.readOnly` (boolean)
    Indicates whether the user can modify the discussion.

  - `reports.sourceSheets.discussions.title` (string)
    Title automatically created by duplicating the first 100 characters of top-level comment.

  - `reports.sourceSheets.effectiveAttachmentOptions` (array)
    Array of enum strings (see [Attachment.attachmentType](/api/smartsheet/openapi/attachments) indicating the allowable attachment options for the current user and sheet.

  - `reports.sourceSheets.ganttEnabled` (boolean)
    Indicates whether "Gantt View" is enabled.

  - `reports.sourceSheets.hasSummaryFields` (boolean)
    Indicates whether a sheet summary is present.

  - `reports.sourceSheets.isMultiPicklistEnabled` (boolean)
    Indicates whether multi-select is enabled.

  - `reports.sourceSheets.modifiedAt` (any)

  - `reports.sourceSheets.name` (string)
    Sheet name.

  - `reports.sourceSheets.owner` (string)
    Email address of the sheet owner.

  - `reports.sourceSheets.permalink` (string)
    URL that represents a direct link to the sheet in Smartsheet.

  - `reports.sourceSheets.projectSettings` (object)
    Represents the project settings dependencies for a specific sheet. Project settings may be updated on sheets that the user has editor access.

  - `reports.sourceSheets.projectSettings.lengthOfDay` (number)
    Length of a workday for a project sheet.

  - `reports.sourceSheets.projectSettings.nonWorkingDays` (array)
    Non-working days for a project sheet.

  - `reports.sourceSheets.projectSettings.workingDays` (array)
    Enum: "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"

  - `reports.sourceSheets.readOnly` (boolean)
    Returned only if the sheet belongs to an expired trial (value = true).

  - `reports.sourceSheets.resourceManagementEnabled` (boolean)
    Indicates that resource management is enabled.

  - `reports.sourceSheets.resourceManagementType` (string)
    Resource Management type. Indicates the type of RM that is enabled.
    Enum: "NONE", "LEGACY_RESOURCE_MANAGEMENT", "RESOURCE_MANAGEMENT_BY_SMARTSHEET"

  - `reports.sourceSheets.rows` (array)

  - `reports.sourceSheets.rows.id` (number)
    Row ID.

  - `reports.sourceSheets.rows.sheetId` (number)
    Parent sheet ID.

  - `reports.sourceSheets.rows.siblingId` (number)
    Sibling ID.

  - `reports.sourceSheets.rows.accessLevel` (string)
    Enum: "ADMIN", "COMMENTER", "EDITOR", "EDITOR_SHARE", "OWNER", "VIEWER"

  - `reports.sourceSheets.rows.attachments` (array)
    Attachments on row. Only returned if the include query string parameter contains attachments.

  - `reports.sourceSheets.rows.attachments.id` (number)
    Attachment ID.

  - `reports.sourceSheets.rows.attachments.parentId` (number)
    The ID of the parent.

  - `reports.sourceSheets.rows.attachments.attachmentType` (string)
    Attachment type. Note--Dropbox, Egnyte, and Evernote are not supported for Smartsheet.gov accounts.
    Enum: "BOX_COM", "DROPBOX", "EGNYTE", "EVERNOTE", "FILE", "GOOGLE_DRIVE", "LINK", "ONEDRIVE", "TRELLO"

  - `reports.sourceSheets.rows.attachments.attachmentSubType` (string)
    Attachment sub type. Note--Folder type is for EGNYTE values and the rest are GOOGLE_DRIVE values.
    Enum: "DOCUMENT", "DRAWING", "FOLDER", "PDF", "PRESENTATION", "SPREADSHEET"

  - `reports.sourceSheets.rows.attachments.mimeType` (string)
    Attachment MIME type.
    Example: "PNG"

  - `reports.sourceSheets.rows.attachments.parentType` (string)
    The type of object the attachment belongs to.
    Enum: "COMMENT", "PROOF", "ROW", "SHEET"

  - `reports.sourceSheets.rows.attachments.createdAt` (any)

  - `reports.sourceSheets.rows.attachments.createdBy` (object)
    User object containing name and email of the user who created this attachment.

  - `reports.sourceSheets.rows.attachments.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.sourceSheets.rows.attachments.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.sourceSheets.rows.attachments.name` (string)
    Attachment name.

  - `reports.sourceSheets.rows.attachments.sizeInKb` (number)
    The size of the file, if the attachmentType is FILE.

  - `reports.sourceSheets.rows.attachments.url` (string)
    Attachment temporary URL (files only).

  - `reports.sourceSheets.rows.attachments.urlExpiresInMillis` (number)
    Attachment temporary URL time to live (files only).

  - `reports.sourceSheets.rows.cells` (array)
    Cells belonging to the row.

  - `reports.sourceSheets.rows.cells.columnId` (number)
    The ID of the column that the cell is located in.

  - `reports.sourceSheets.rows.cells.rowId` (number)
    The ID of the row the cell is located in.

  - `reports.sourceSheets.rows.cells.columnType` (string)
    Only returned if the include query string parameter contains columnType.

  - `reports.sourceSheets.rows.cells.conditionalFormat` (string)
    The format descriptor describing this cell's conditional format. Only returned if the include query string parameter contains format and this cell has a conditional format applied.

  - `reports.sourceSheets.rows.cells.displayValue` (string)
    Visual representation of cell contents, as presented to the user in the UI.

  - `reports.sourceSheets.rows.cells.format` (string)
    The format descriptor. Only returned if the include query string parameter contains format and this cell has a non-default format applied.

  - `reports.sourceSheets.rows.cells.formula` (string)
    The formula for a cell, if set, for instance =COUNTM([Assigned To]3). Note that calculation errors or problems with a formula do not cause the API call to return an error code. Instead, the response contains the same value as in the UI, such as cell.value = "#CIRCULAR REFERENCE".

  - `reports.sourceSheets.rows.cells.hyperlink` (object)

  - `reports.sourceSheets.rows.cells.hyperlink.reportId` (number)
    If non-null, this hyperlink is a link to the report with this ID.

  - `reports.sourceSheets.rows.cells.hyperlink.sheetId` (number)
    If non-null, this hyperlink is a link to the sheet with this ID.

  - `reports.sourceSheets.rows.cells.hyperlink.sightId` (number)
    If non-null, this hyperlink is a link to the dashboard with this ID.

  - `reports.sourceSheets.rows.cells.hyperlink.url` (string)
    When the hyperlink is a URL link, this property contains the URL value. When the hyperlink is a dashboard/report/sheet link (that is, dashboardId, reportId, or sheetId is non-null), this property contains the permalink to the dashboard, report, or sheet.

  - `reports.sourceSheets.rows.cells.image` (object)

  - `reports.sourceSheets.rows.cells.image.altText` (string)
    Alternate text for the image.

  - `reports.sourceSheets.rows.cells.image.height` (number)
    Original height (in pixels) of the uploaded image.

  - `reports.sourceSheets.rows.cells.image.id` (string)
    Image ID.

  - `reports.sourceSheets.rows.cells.image.width` (number)
    Original width (in pixels) of the uploaded image.

  - `reports.sourceSheets.rows.cells.linkInFromCell` (object)

  - `reports.sourceSheets.rows.cells.linkInFromCell.columnId` (number)
    Column ID of the linked cell.

  - `reports.sourceSheets.rows.cells.linkInFromCell.rowId` (number)
    Row ID of the linked cell.

  - `reports.sourceSheets.rows.cells.linkInFromCell.sheetId` (number)
    Sheet ID of the sheet that the linked cell belongs to.

  - `reports.sourceSheets.rows.cells.linkInFromCell.sheetName` (string)
    Sheet name of the linked cell.

  - `reports.sourceSheets.rows.cells.linkInFromCell.status` (string)
    * BLOCKED One of several other values indicating unusual error conditions.
* BROKEN The row or sheet linked to was deleted.
* CIRCULAR One of several other values indicating unusual error conditions.
* DISABLED One of several other values indicating unusual error conditions.
* INACCESSIBLE The sheet linked to cannot be viewed by this user.
* INVALID One of several other values indicating unusual error conditions.
* NOT_SHARED One of several other values indicating unusual error conditions.
* OK The link is in a good state.
    Enum: "BLOCKED", "BROKEN", "CIRCULAR", "DISABLED", "INACCESSIBLE", "INVALID", "NOT_SHARED", "OK"

  - `reports.sourceSheets.rows.cells.linksOutToCells` (array)

  - `reports.sourceSheets.rows.cells.linksOutToCells.columnId` (number)
    Column ID of the linked cell.

  - `reports.sourceSheets.rows.cells.linksOutToCells.rowId` (number)
    Row ID of the linked cell.

  - `reports.sourceSheets.rows.cells.linksOutToCells.sheetId` (number)
    Sheet ID of the sheet that the linked cell belongs to.

  - `reports.sourceSheets.rows.cells.linksOutToCells.sheetName` (string)
    Sheet name of the linked cell.

  - `reports.sourceSheets.rows.cells.linksOutToCells.status` (string)
    * BLOCKED One of several other values indicating unusual error conditions.
* BROKEN The row or sheet linked to was deleted.
* CIRCULAR One of several other values indicating unusual error conditions.
* DISABLED One of several other values indicating unusual error conditions.
* INACCESSIBLE The sheet linked to cannot be viewed by this user.
* INVALID One of several other values indicating unusual error conditions.
* NOT_SHARED One of several other values indicating unusual error conditions.
* OK The link is in a good state.
    Enum: "BLOCKED", "BROKEN", "CIRCULAR", "DISABLED", "INACCESSIBLE", "INVALID", "NOT_SHARED", "OK"

  - `reports.sourceSheets.rows.cells.objectValue` (any)

  - `reports.sourceSheets.rows.cells.overrideValidation` (boolean)
    (Admin only) Indicates whether the cell value can contain a value outside of the validation limits (value = true). When using this parameter, you must also set strict to false to bypass value type checking. This property is honored for POST or PUT actions that update rows.

  - `reports.sourceSheets.rows.cells.strict` (boolean)
    Set to false to enable lenient parsing. Defaults to true. You can specify this attribute in a request, but it is never present in a response.

  - `reports.sourceSheets.rows.cells.value` (any)
    A string, number, or a Boolean value -- depending on the cell type and the data in the cell. Cell values larger than 4000 characters are silently truncated. An empty cell returns no value.

  - `reports.sourceSheets.rows.columns` (array)
    Columns of row. Only returned if the include query string parameter contains columns.

  - `reports.sourceSheets.rows.conditionalFormat` (string)
    Describes this row's conditional format. Only returned if the include query string parameter contains format and this row has a conditional format applied.
    Example: ",,1,1,,,,,,,,,,,,,"

  - `reports.sourceSheets.rows.createdAt` (any)

  - `reports.sourceSheets.rows.createdBy` (object)
    User object containing name and email of the creator of this row.

  - `reports.sourceSheets.rows.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.sourceSheets.rows.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.sourceSheets.rows.discussions` (array)
    Discussions on the row. Only returned if the include query string parameter contains discussions.

  - `reports.sourceSheets.rows.discussions.accessLevel` (string)
    Enum: "ADMIN", "COMMENTER", "EDITOR", "EDITOR_SHARE", "OWNER", "VIEWER"

  - `reports.sourceSheets.rows.discussions.id` (number)
    Discussion ID.

  - `reports.sourceSheets.rows.discussions.comments` (array)
    Array of comments in discussion. Only returned if the include query string parameter contains comments.

  - `reports.sourceSheets.rows.discussions.comments.attachments` (array)
    Array of attachments on comments.

  - `reports.sourceSheets.rows.discussions.comments.attachments.id` (number)
    Attachment ID.

  - `reports.sourceSheets.rows.discussions.comments.attachments.parentId` (number)
    The ID of the parent.

  - `reports.sourceSheets.rows.discussions.comments.attachments.attachmentType` (string)
    Attachment type. Note--Dropbox, Egnyte, and Evernote are not supported for Smartsheet.gov accounts.
    Enum: "BOX_COM", "DROPBOX", "EGNYTE", "EVERNOTE", "FILE", "GOOGLE_DRIVE", "LINK", "ONEDRIVE", "TRELLO"

  - `reports.sourceSheets.rows.discussions.comments.attachments.attachmentSubType` (string)
    Attachment sub type. Note--Folder type is for EGNYTE values and the rest are GOOGLE_DRIVE values.
    Enum: "DOCUMENT", "DRAWING", "FOLDER", "PDF", "PRESENTATION", "SPREADSHEET"

  - `reports.sourceSheets.rows.discussions.comments.attachments.mimeType` (string)
    Attachment MIME type.
    Example: "PNG"

  - `reports.sourceSheets.rows.discussions.comments.attachments.parentType` (string)
    The type of object the attachment belongs to.
    Enum: "COMMENT", "PROOF", "ROW", "SHEET"

  - `reports.sourceSheets.rows.discussions.comments.attachments.createdAt` (any)

  - `reports.sourceSheets.rows.discussions.comments.attachments.createdBy` (object)
    User object containing name and email of the user who created this attachment.

  - `reports.sourceSheets.rows.discussions.comments.attachments.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.sourceSheets.rows.discussions.comments.attachments.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.sourceSheets.rows.discussions.comments.attachments.name` (string)
    Attachment name.

  - `reports.sourceSheets.rows.discussions.comments.attachments.sizeInKb` (number)
    The size of the file, if the attachmentType is FILE.

  - `reports.sourceSheets.rows.discussions.comments.attachments.url` (string)
    Attachment temporary URL (files only).

  - `reports.sourceSheets.rows.discussions.comments.attachments.urlExpiresInMillis` (number)
    Attachment temporary URL time to live (files only).

  - `reports.sourceSheets.rows.discussions.comments.createdAt` (any)

  - `reports.sourceSheets.rows.discussions.comments.createdBy` (object)
    User object containing name and email of the creator of this comment.

  - `reports.sourceSheets.rows.discussions.comments.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.sourceSheets.rows.discussions.comments.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.sourceSheets.rows.discussions.comments.discussionId` (number)
    Discussion ID of discussion that contains comment.

  - `reports.sourceSheets.rows.discussions.comments.id` (number)
    Comment ID.

  - `reports.sourceSheets.rows.discussions.comments.modifiedAt` (any)

  - `reports.sourceSheets.rows.discussions.comments.text` (string)
    Comment body.

  - `reports.sourceSheets.rows.discussions.commentAttachments` (array)
    Array of attachments on discussion comments. Only returned if the include query string parameter contains attachments.

  - `reports.sourceSheets.rows.discussions.commentAttachments.id` (number)
    Attachment ID.

  - `reports.sourceSheets.rows.discussions.commentAttachments.parentId` (number)
    The ID of the parent.

  - `reports.sourceSheets.rows.discussions.commentAttachments.attachmentType` (string)
    Attachment type. Note--Dropbox, Egnyte, and Evernote are not supported for Smartsheet.gov accounts.
    Enum: "BOX_COM", "DROPBOX", "EGNYTE", "EVERNOTE", "FILE", "GOOGLE_DRIVE", "LINK", "ONEDRIVE", "TRELLO"

  - `reports.sourceSheets.rows.discussions.commentAttachments.attachmentSubType` (string)
    Attachment sub type. Note--Folder type is for EGNYTE values and the rest are GOOGLE_DRIVE values.
    Enum: "DOCUMENT", "DRAWING", "FOLDER", "PDF", "PRESENTATION", "SPREADSHEET"

  - `reports.sourceSheets.rows.discussions.commentAttachments.mimeType` (string)
    Attachment MIME type.
    Example: "PNG"

  - `reports.sourceSheets.rows.discussions.commentAttachments.parentType` (string)
    The type of object the attachment belongs to.
    Enum: "COMMENT", "PROOF", "ROW", "SHEET"

  - `reports.sourceSheets.rows.discussions.commentAttachments.createdAt` (any)

  - `reports.sourceSheets.rows.discussions.commentAttachments.createdBy` (object)
    User object containing name and email of the user who created this attachment.

  - `reports.sourceSheets.rows.discussions.commentAttachments.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.sourceSheets.rows.discussions.commentAttachments.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.sourceSheets.rows.discussions.commentAttachments.name` (string)
    Attachment name.

  - `reports.sourceSheets.rows.discussions.commentAttachments.sizeInKb` (number)
    The size of the file, if the attachmentType is FILE.

  - `reports.sourceSheets.rows.discussions.commentAttachments.url` (string)
    Attachment temporary URL (files only).

  - `reports.sourceSheets.rows.discussions.commentAttachments.urlExpiresInMillis` (number)
    Attachment temporary URL time to live (files only).

  - `reports.sourceSheets.rows.discussions.commentCount` (number)
    Number of comments in the discussion.

  - `reports.sourceSheets.rows.discussions.createdBy` (object)
    User object containing name and email of the user who created the discussion.

  - `reports.sourceSheets.rows.discussions.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.sourceSheets.rows.discussions.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.sourceSheets.rows.discussions.lastCommentedAt` (any)

  - `reports.sourceSheets.rows.discussions.lastCommentedUser` (object)
    User object containing name and email of the user who last commented on the discussion.

  - `reports.sourceSheets.rows.discussions.lastCommentedUser.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.sourceSheets.rows.discussions.lastCommentedUser.name` (string)
    Example: "Jane Doe"

  - `reports.sourceSheets.rows.discussions.parentId` (number)
    The ID of the associated row or sheet.

  - `reports.sourceSheets.rows.discussions.parentType` (string)
    Type of parent object.
    Enum: "ROW", "SHEET"

  - `reports.sourceSheets.rows.discussions.readOnly` (boolean)
    Indicates whether the user can modify the discussion.

  - `reports.sourceSheets.rows.discussions.title` (string)
    Title automatically created by duplicating the first 100 characters of top-level comment.

  - `reports.sourceSheets.rows.proof` (object)
    Object containing zero or more media items, including images, videos, and documents, for review, editing, or approval.

  - `reports.sourceSheets.rows.proof.id` (number)
    Proof ID of the proof version.

  - `reports.sourceSheets.rows.proof.originalId` (number)
    Proof ID of the original proof version.

  - `reports.sourceSheets.rows.proof.name` (string)
    Proof name. This is the same as primary column value. If the primary column value is empty, name is empty.

  - `reports.sourceSheets.rows.proof.type` (string)
    File type for the proof version.
    Enum: "DOCUMENT", "IMAGE", "MIXED", "NONE", "VIDEO"

  - `reports.sourceSheets.rows.proof.documentType` (string)
    If type=DOCUMENT, then this indicates the type of file, such as PDF.

  - `reports.sourceSheets.rows.proof.proofRequestUrl` (string)
    URL to review a proofing request.

  - `reports.sourceSheets.rows.proof.version` (number)
    The version number of the proof.

  - `reports.sourceSheets.rows.proof.lastUpdatedAt` (any)

  - `reports.sourceSheets.rows.proof.lastUpdatedBy` (object)
    User object containing name and email of the user who last updated the proof.

  - `reports.sourceSheets.rows.proof.lastUpdatedBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.sourceSheets.rows.proof.lastUpdatedBy.name` (string)
    Example: "Jane Doe"

  - `reports.sourceSheets.rows.proof.isCompleted` (boolean)
    Indicates whether the proof is completed.

  - `reports.sourceSheets.rows.proof.attachments` (array)
    Array of Attachment objects. Only returned if the include query string parameter contains attachments.

  - `reports.sourceSheets.rows.proof.attachments.id` (number)
    Attachment ID.

  - `reports.sourceSheets.rows.proof.attachments.parentId` (number)
    The ID of the parent.

  - `reports.sourceSheets.rows.proof.attachments.attachmentType` (string)
    Attachment type. Note--Dropbox, Egnyte, and Evernote are not supported for Smartsheet.gov accounts.
    Enum: "BOX_COM", "DROPBOX", "EGNYTE", "EVERNOTE", "FILE", "GOOGLE_DRIVE", "LINK", "ONEDRIVE", "TRELLO"

  - `reports.sourceSheets.rows.proof.attachments.attachmentSubType` (string)
    Attachment sub type. Note--Folder type is for EGNYTE values and the rest are GOOGLE_DRIVE values.
    Enum: "DOCUMENT", "DRAWING", "FOLDER", "PDF", "PRESENTATION", "SPREADSHEET"

  - `reports.sourceSheets.rows.proof.attachments.mimeType` (string)
    Attachment MIME type.
    Example: "PNG"

  - `reports.sourceSheets.rows.proof.attachments.parentType` (string)
    The type of object the attachment belongs to.
    Enum: "COMMENT", "PROOF", "ROW", "SHEET"

  - `reports.sourceSheets.rows.proof.attachments.createdAt` (any)

  - `reports.sourceSheets.rows.proof.attachments.createdBy` (object)
    User object containing name and email of the user who created this attachment.

  - `reports.sourceSheets.rows.proof.attachments.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.sourceSheets.rows.proof.attachments.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.sourceSheets.rows.proof.attachments.name` (string)
    Attachment name.

  - `reports.sourceSheets.rows.proof.attachments.sizeInKb` (number)
    The size of the file, if the attachmentType is FILE.

  - `reports.sourceSheets.rows.proof.attachments.url` (string)
    Attachment temporary URL (files only).

  - `reports.sourceSheets.rows.proof.attachments.urlExpiresInMillis` (number)
    Attachment temporary URL time to live (files only).

  - `reports.sourceSheets.rows.proof.discussions` (array)
    Array of Discussion objects. Only returned if the include query string parameter contains discussions.

  - `reports.sourceSheets.rows.proof.discussions.accessLevel` (string)
    Enum: "ADMIN", "COMMENTER", "EDITOR", "EDITOR_SHARE", "OWNER", "VIEWER"

  - `reports.sourceSheets.rows.proof.discussions.id` (number)
    Discussion ID.

  - `reports.sourceSheets.rows.proof.discussions.comments` (array)
    Array of comments in discussion. Only returned if the include query string parameter contains comments.

  - `reports.sourceSheets.rows.proof.discussions.comments.attachments` (array)
    Array of attachments on comments.

  - `reports.sourceSheets.rows.proof.discussions.comments.attachments.id` (number)
    Attachment ID.

  - `reports.sourceSheets.rows.proof.discussions.comments.attachments.parentId` (number)
    The ID of the parent.

  - `reports.sourceSheets.rows.proof.discussions.comments.attachments.attachmentType` (string)
    Attachment type. Note--Dropbox, Egnyte, and Evernote are not supported for Smartsheet.gov accounts.
    Enum: "BOX_COM", "DROPBOX", "EGNYTE", "EVERNOTE", "FILE", "GOOGLE_DRIVE", "LINK", "ONEDRIVE", "TRELLO"

  - `reports.sourceSheets.rows.proof.discussions.comments.attachments.attachmentSubType` (string)
    Attachment sub type. Note--Folder type is for EGNYTE values and the rest are GOOGLE_DRIVE values.
    Enum: "DOCUMENT", "DRAWING", "FOLDER", "PDF", "PRESENTATION", "SPREADSHEET"

  - `reports.sourceSheets.rows.proof.discussions.comments.attachments.mimeType` (string)
    Attachment MIME type.
    Example: "PNG"

  - `reports.sourceSheets.rows.proof.discussions.comments.attachments.parentType` (string)
    The type of object the attachment belongs to.
    Enum: "COMMENT", "PROOF", "ROW", "SHEET"

  - `reports.sourceSheets.rows.proof.discussions.comments.attachments.createdAt` (any)

  - `reports.sourceSheets.rows.proof.discussions.comments.attachments.createdBy` (object)
    User object containing name and email of the user who created this attachment.

  - `reports.sourceSheets.rows.proof.discussions.comments.attachments.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.sourceSheets.rows.proof.discussions.comments.attachments.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.sourceSheets.rows.proof.discussions.comments.attachments.name` (string)
    Attachment name.

  - `reports.sourceSheets.rows.proof.discussions.comments.attachments.sizeInKb` (number)
    The size of the file, if the attachmentType is FILE.

  - `reports.sourceSheets.rows.proof.discussions.comments.attachments.url` (string)
    Attachment temporary URL (files only).

  - `reports.sourceSheets.rows.proof.discussions.comments.attachments.urlExpiresInMillis` (number)
    Attachment temporary URL time to live (files only).

  - `reports.sourceSheets.rows.proof.discussions.comments.createdAt` (any)

  - `reports.sourceSheets.rows.proof.discussions.comments.createdBy` (object)
    User object containing name and email of the creator of this comment.

  - `reports.sourceSheets.rows.proof.discussions.comments.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.sourceSheets.rows.proof.discussions.comments.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.sourceSheets.rows.proof.discussions.comments.discussionId` (number)
    Discussion ID of discussion that contains comment.

  - `reports.sourceSheets.rows.proof.discussions.comments.id` (number)
    Comment ID.

  - `reports.sourceSheets.rows.proof.discussions.comments.modifiedAt` (any)

  - `reports.sourceSheets.rows.proof.discussions.comments.text` (string)
    Comment body.

  - `reports.sourceSheets.rows.proof.discussions.commentAttachments` (array)
    Array of attachments on discussion comments. Only returned if the include query string parameter contains attachments.

  - `reports.sourceSheets.rows.proof.discussions.commentAttachments.id` (number)
    Attachment ID.

  - `reports.sourceSheets.rows.proof.discussions.commentAttachments.parentId` (number)
    The ID of the parent.

  - `reports.sourceSheets.rows.proof.discussions.commentAttachments.attachmentType` (string)
    Attachment type. Note--Dropbox, Egnyte, and Evernote are not supported for Smartsheet.gov accounts.
    Enum: "BOX_COM", "DROPBOX", "EGNYTE", "EVERNOTE", "FILE", "GOOGLE_DRIVE", "LINK", "ONEDRIVE", "TRELLO"

  - `reports.sourceSheets.rows.proof.discussions.commentAttachments.attachmentSubType` (string)
    Attachment sub type. Note--Folder type is for EGNYTE values and the rest are GOOGLE_DRIVE values.
    Enum: "DOCUMENT", "DRAWING", "FOLDER", "PDF", "PRESENTATION", "SPREADSHEET"

  - `reports.sourceSheets.rows.proof.discussions.commentAttachments.mimeType` (string)
    Attachment MIME type.
    Example: "PNG"

  - `reports.sourceSheets.rows.proof.discussions.commentAttachments.parentType` (string)
    The type of object the attachment belongs to.
    Enum: "COMMENT", "PROOF", "ROW", "SHEET"

  - `reports.sourceSheets.rows.proof.discussions.commentAttachments.createdAt` (any)

  - `reports.sourceSheets.rows.proof.discussions.commentAttachments.createdBy` (object)
    User object containing name and email of the user who created this attachment.

  - `reports.sourceSheets.rows.proof.discussions.commentAttachments.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.sourceSheets.rows.proof.discussions.commentAttachments.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.sourceSheets.rows.proof.discussions.commentAttachments.name` (string)
    Attachment name.

  - `reports.sourceSheets.rows.proof.discussions.commentAttachments.sizeInKb` (number)
    The size of the file, if the attachmentType is FILE.

  - `reports.sourceSheets.rows.proof.discussions.commentAttachments.url` (string)
    Attachment temporary URL (files only).

  - `reports.sourceSheets.rows.proof.discussions.commentAttachments.urlExpiresInMillis` (number)
    Attachment temporary URL time to live (files only).

  - `reports.sourceSheets.rows.proof.discussions.commentCount` (number)
    Number of comments in the discussion.

  - `reports.sourceSheets.rows.proof.discussions.createdBy` (object)
    User object containing name and email of the user who created the discussion.

  - `reports.sourceSheets.rows.proof.discussions.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.sourceSheets.rows.proof.discussions.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.sourceSheets.rows.proof.discussions.lastCommentedAt` (any)

  - `reports.sourceSheets.rows.proof.discussions.lastCommentedUser` (object)
    User object containing name and email of the user who last commented on the discussion.

  - `reports.sourceSheets.rows.proof.discussions.lastCommentedUser.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.sourceSheets.rows.proof.discussions.lastCommentedUser.name` (string)
    Example: "Jane Doe"

  - `reports.sourceSheets.rows.proof.discussions.parentId` (number)
    The ID of the associated row or sheet.

  - `reports.sourceSheets.rows.proof.discussions.parentType` (string)
    Type of parent object.
    Enum: "ROW", "SHEET"

  - `reports.sourceSheets.rows.proof.discussions.readOnly` (boolean)
    Indicates whether the user can modify the discussion.

  - `reports.sourceSheets.rows.proof.discussions.title` (string)
    Title automatically created by duplicating the first 100 characters of top-level comment.

  - `reports.sourceSheets.rows.expanded` (boolean)
    Indicates whether the row is expanded or collapsed.

  - `reports.sourceSheets.rows.filteredOut` (boolean)
    Indicates if the row is filtered out by a column filter. Only returned if the include query string parameter contains filters.

  - `reports.sourceSheets.rows.format` (string)
    Format descriptor. Only returned if the include query string parameter contains format and this row has a non-default format applied.
    Example: ",,1,1,,,,,,,,,,,,,"

  - `reports.sourceSheets.rows.inCriticalPath` (boolean)
    Only returned, with a value of true, if the sheet is a project sheet with dependencies enabled and this row is in the critical path.

  - `reports.sourceSheets.rows.locked` (boolean)
    Indicates whether the row is locked.

  - `reports.sourceSheets.rows.lockedForUser` (boolean)
    Indicates whether the row is locked for the requesting user.

  - `reports.sourceSheets.rows.modifiedAt` (any)

  - `reports.sourceSheets.rows.modifiedBy` (object)
    User object containing name and email of the last person to modify this row.

  - `reports.sourceSheets.rows.modifiedBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.sourceSheets.rows.modifiedBy.name` (string)
    Example: "Jane Doe"

  - `reports.sourceSheets.rows.permaLink` (string)
    URL that represents a direct link to the row in Smartsheet. Only returned if the include query string parameter contains rowPermalink.

  - `reports.sourceSheets.rows.rowNumber` (number)
    Row number within the sheet.

  - `reports.sourceSheets.rows.version` (number)
    Sheet version number that is incremented every time a sheet is modified.

  - `reports.sourceSheets.showParentRowsForFilters` (boolean)
    Returned only if there are column filters on the sheet. Value = true if "show parent rows" is enabled for the filters.

  - `reports.sourceSheets.source` (object)

  - `reports.sourceSheets.source.id` (number)
    The ID of the dashboard, report, sheet, or template from which the enclosing dashboard, report, sheet, or template was created.

  - `reports.sourceSheets.source.type` (string)
    report, sheet, sight (aka dashboard), or template.

  - `reports.sourceSheets.summary` (object)
    Represents the entire summary, or a list of defined fields and values, for a specific sheet.

  - `reports.sourceSheets.summary.fields` (array)
    Array of summary (or metadata) fields defined on the sheet.

  - `reports.sourceSheets.summary.fields.id` (number)
    SummaryField ID.

  - `reports.sourceSheets.summary.fields.contactOptions` (array)
    Array of ContactOption objects to specify a pre-defined list of values for the column. Column type must be CONTACT_LIST.

  - `reports.sourceSheets.summary.fields.contactOptions.email` (string)
    A parsable email address.

  - `reports.sourceSheets.summary.fields.contactOptions.name` (string)
    Can be a user's name, display name, or free text.

  - `reports.sourceSheets.summary.fields.createdAt` (any)

  - `reports.sourceSheets.summary.fields.createdBy` (object)
    User object containing name and email of the creator of this summary field.

  - `reports.sourceSheets.summary.fields.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.sourceSheets.summary.fields.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.sourceSheets.summary.fields.displayValue` (string)
    Visual representation of cell contents, as presented to the user in the UI.

  - `reports.sourceSheets.summary.fields.format` (string)
    The format descriptor. Only returned if the include query string parameter contains format and this column has a non-default format applied to it.

  - `reports.sourceSheets.summary.fields.formula` (string)
    The formula for a cell, if set.

  - `reports.sourceSheets.summary.fields.hyperlink` (object)

  - `reports.sourceSheets.summary.fields.hyperlink.reportId` (number)
    If non-null, this hyperlink is a link to the report with this ID.

  - `reports.sourceSheets.summary.fields.hyperlink.sheetId` (number)
    If non-null, this hyperlink is a link to the sheet with this ID.

  - `reports.sourceSheets.summary.fields.hyperlink.sightId` (number)
    If non-null, this hyperlink is a link to the dashboard with this ID.

  - `reports.sourceSheets.summary.fields.hyperlink.url` (string)
    When the hyperlink is a URL link, this property contains the URL value. When the hyperlink is a dashboard/report/sheet link (that is, dashboardId, reportId, or sheetId is non-null), this property contains the permalink to the dashboard, report, or sheet.

  - `reports.sourceSheets.summary.fields.image` (object)

  - `reports.sourceSheets.summary.fields.image.altText` (string)
    Alternate text for the image.

  - `reports.sourceSheets.summary.fields.image.height` (number)
    Original height (in pixels) of the uploaded image.

  - `reports.sourceSheets.summary.fields.image.id` (string)
    Image ID.

  - `reports.sourceSheets.summary.fields.image.width` (number)
    Original width (in pixels) of the uploaded image.

  - `reports.sourceSheets.summary.fields.index` (number)
    Field index or position. This number is zero-based.

  - `reports.sourceSheets.summary.fields.locked` (boolean)
    Indicates whether the field is locked.

  - `reports.sourceSheets.summary.fields.lockedForUser` (boolean)
    Indicates whether the field is locked for the requesting user.

  - `reports.sourceSheets.summary.fields.modifiedAt` (any)

  - `reports.sourceSheets.summary.fields.modifiedBy` (object)
    User object containing name and email of the user who most recently modified this summary field.

  - `reports.sourceSheets.summary.fields.modifiedBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.sourceSheets.summary.fields.modifiedBy.name` (string)
    Example: "Jane Doe"

  - `reports.sourceSheets.summary.fields.objectValue` (any)

  - `reports.sourceSheets.summary.fields.options` (array)
    When applicable for PICKLIST column type. Array of the options available for the field.

  - `reports.sourceSheets.summary.fields.symbol` (string)
    When applicable for PICKLIST column type.

  - `reports.sourceSheets.summary.fields.title` (string)
    Arbitrary name, must be unique within summary.

  - `reports.sourceSheets.summary.fields.type` (string)
    Enum: "ABSTRACT_DATETIME", "CHECKBOX", "CONTACT_LIST", "DATE", "DATETIME", "DURATION", "MULTI_CONTACT_LIST", "MULTI_PICKLIST", "PICKLIST", "PREDECESSOR", "TEXT_NUMBER"

  - `reports.sourceSheets.summary.fields.validation` (boolean)
    Indicates whether summary field values are restricted to the type.

  - `reports.sourceSheets.totalRowCount` (number)
    The total number of rows in the sheet.

  - `reports.sourceSheets.userPermissions` (object)
    Describes the current user's editing permissions for a specific sheet.

  - `reports.sourceSheets.userPermissions.summaryPermissions` (string)
    One of:
  * ADMIN: full control over fields.
  * READ_DELETE: sheet is owned by an individual account that doesn't have summary capabilities. If a summary exists, the only possible operations are GET and DELETE fields.
  * READ_ONLY.
  * READ_WRITE: can edit values of existing fields, but not create or delete fields, nor modify field type.
    Enum: "ADMIN", "READ_DELETE", "READ_ONLY", "READ_WRITE"

  - `reports.sourceSheets.userSettings` (object)
    Represents individual user settings for a specific sheet. User settings may be updated even on sheets where the current user only has read access (for example, viewer permissions or a read-only sheet).

  - `reports.sourceSheets.userSettings.criticalPathEnabled` (boolean)
    Does this user have "Show Critical Path" turned on for this sheet? NOTE: This setting only has an effect on project sheets with dependencies enabled.

  - `reports.sourceSheets.userSettings.displaySummaryTasks` (boolean)
    Does this user have "Display Summary Tasks" turned on for this sheet? Applies only to sheets where "Calendar View" has been configured.

  - `reports.sourceSheets.version` (number)
    A number that is incremented every time a sheet is modified.

  - `reports.sourceSheets.workspace` (object)

  - `reports.sourceSheets.workspace.id` (number)
    Workspace ID.

  - `reports.sourceSheets.workspace.name` (string)
    Workspace name.

  - `reports.sourceSheets.workspace.accessLevel` (string)
    Enum: "ADMIN", "COMMENTER", "EDITOR", "EDITOR_SHARE", "OWNER", "VIEWER"

  - `reports.sourceSheets.workspace.permalink` (string)
    URL that represents a direct link to the workspace in Smartsheet.

  - `reports.sourceSheets.favorite` (boolean)
    Deprecated Returned only if the user has marked this sheet as a favorite in their Home tab (value = true).

  - `reports.isSummaryReport` (boolean)
    A boolean to represent whether the report is a sheet summary report or not. If this property is false, it is a row report.

  - `reports.id` (number)
    Sheet ID.

  - `reports.fromId` (number)
    The ID of the template from which to create the sheet. This attribute can be specified in a request, but is never present in a response.

  - `reports.ownerId` (number)
    User ID of the sheet owner.

  - `reports.accessLevel` (string)
    Enum: "ADMIN", "COMMENTER", "EDITOR", "EDITOR_SHARE", "OWNER", "VIEWER"

  - `reports.attachments` (array)
    Array of Attachment objects.
Only returned if the [include](/api/smartsheet/openapi/sheets/getsheet) query string parameter contains attachments.

  - `reports.attachments.id` (number)
    Attachment ID.

  - `reports.attachments.parentId` (number)
    The ID of the parent.

  - `reports.attachments.attachmentType` (string)
    Attachment type. Note--Dropbox, Egnyte, and Evernote are not supported for Smartsheet.gov accounts.
    Enum: "BOX_COM", "DROPBOX", "EGNYTE", "EVERNOTE", "FILE", "GOOGLE_DRIVE", "LINK", "ONEDRIVE", "TRELLO"

  - `reports.attachments.attachmentSubType` (string)
    Attachment sub type. Note--Folder type is for EGNYTE values and the rest are GOOGLE_DRIVE values.
    Enum: "DOCUMENT", "DRAWING", "FOLDER", "PDF", "PRESENTATION", "SPREADSHEET"

  - `reports.attachments.mimeType` (string)
    Attachment MIME type.
    Example: "PNG"

  - `reports.attachments.parentType` (string)
    The type of object the attachment belongs to.
    Enum: "COMMENT", "PROOF", "ROW", "SHEET"

  - `reports.attachments.createdAt` (any)

  - `reports.attachments.createdBy` (object)
    User object containing name and email of the user who created this attachment.

  - `reports.attachments.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.attachments.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.attachments.name` (string)
    Attachment name.

  - `reports.attachments.sizeInKb` (number)
    The size of the file, if the attachmentType is FILE.

  - `reports.attachments.url` (string)
    Attachment temporary URL (files only).

  - `reports.attachments.urlExpiresInMillis` (number)
    Attachment temporary URL time to live (files only).

  - `reports.cellImageUploadEnabled` (boolean)
    The sheet is enabled for cell images to be uploaded.

  - `reports.columns` (array)

  - `reports.createdAt` (any)

  - `reports.crossSheetReferences` (array)
    Array of CrossSheetReference objects.
Only returned if the [include](/api/smartsheet/openapi/sheets/getsheet) query string parameter contains crossSheetReferences.

  - `reports.crossSheetReferences.endColumnId` (number)
    Defines ending edge of range when specifying one or more columns. To specify an entire column, omit the startRowId and endRowId parameters.

  - `reports.crossSheetReferences.endRowId` (number)
    Defines ending edge of range when specifying one or more rows. To specify an entire row, omit the startColumnId and endColumnId parameters.

  - `reports.crossSheetReferences.id` (number)
    Cross-sheet reference ID, guaranteed unique within referencing sheet.

  - `reports.crossSheetReferences.name` (string)
    Friendly name of reference. Auto-generated unless specified in Create Cross-sheet References.

  - `reports.crossSheetReferences.startColumnId` (number)
    Defines beginning edge of range when specifying one or more columns. To specify an entire column, omit the startRowId and endRowId parameters.

  - `reports.crossSheetReferences.startRowId` (number)
    Defines beginning edge of range when specifying one or more rows. To specify an entire row, omit the startColumnId and endColumnId parameters.

  - `reports.crossSheetReferences.status` (string)
    Status of request:
 * 'BLOCKED' - A reference is downstream of a circular issue.
 * 'BROKEN' - The data source location (column, row or sheet) was deleted.
 * 'CIRCULAR' - The formula reference is self referencing and cannot be resolved.
 * 'DISABLED' - Updating the reference is temporarily disabled due to maintenance.
 * 'INVALID/UNKNOWN' - The reference is new and had not been validated.
 * 'NOT_SHARED' - No common shared users.
 * 'OK' - The reference is in a good state.
    Enum: "BLOCKED", "BROKEN", "CIRCULAR", "DISABLED", "INVALID/UNKNOWN", "NOT-SHARED", "OK"

  - `reports.crossSheetReferences.sourceSheetId` (number)
    Sheet ID of source sheet.

  - `reports.dependenciesEnabled` (boolean)
    Indicates whether dependencies are enabled.

  - `reports.discussions` (array)
    Array of Discussion objects
Only returned if the [include](/api/smartsheet/openapi/sheets/getsheet) query string parameter contains discussions.

  - `reports.discussions.accessLevel` (string)
    Enum: "ADMIN", "COMMENTER", "EDITOR", "EDITOR_SHARE", "OWNER", "VIEWER"

  - `reports.discussions.id` (number)
    Discussion ID.

  - `reports.discussions.comments` (array)
    Array of comments in discussion. Only returned if the include query string parameter contains comments.

  - `reports.discussions.comments.attachments` (array)
    Array of attachments on comments.

  - `reports.discussions.comments.attachments.id` (number)
    Attachment ID.

  - `reports.discussions.comments.attachments.parentId` (number)
    The ID of the parent.

  - `reports.discussions.comments.attachments.attachmentType` (string)
    Attachment type. Note--Dropbox, Egnyte, and Evernote are not supported for Smartsheet.gov accounts.
    Enum: "BOX_COM", "DROPBOX", "EGNYTE", "EVERNOTE", "FILE", "GOOGLE_DRIVE", "LINK", "ONEDRIVE", "TRELLO"

  - `reports.discussions.comments.attachments.attachmentSubType` (string)
    Attachment sub type. Note--Folder type is for EGNYTE values and the rest are GOOGLE_DRIVE values.
    Enum: "DOCUMENT", "DRAWING", "FOLDER", "PDF", "PRESENTATION", "SPREADSHEET"

  - `reports.discussions.comments.attachments.mimeType` (string)
    Attachment MIME type.
    Example: "PNG"

  - `reports.discussions.comments.attachments.parentType` (string)
    The type of object the attachment belongs to.
    Enum: "COMMENT", "PROOF", "ROW", "SHEET"

  - `reports.discussions.comments.attachments.createdAt` (any)

  - `reports.discussions.comments.attachments.createdBy` (object)
    User object containing name and email of the user who created this attachment.

  - `reports.discussions.comments.attachments.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.discussions.comments.attachments.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.discussions.comments.attachments.name` (string)
    Attachment name.

  - `reports.discussions.comments.attachments.sizeInKb` (number)
    The size of the file, if the attachmentType is FILE.

  - `reports.discussions.comments.attachments.url` (string)
    Attachment temporary URL (files only).

  - `reports.discussions.comments.attachments.urlExpiresInMillis` (number)
    Attachment temporary URL time to live (files only).

  - `reports.discussions.comments.createdAt` (any)

  - `reports.discussions.comments.createdBy` (object)
    User object containing name and email of the creator of this comment.

  - `reports.discussions.comments.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.discussions.comments.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.discussions.comments.discussionId` (number)
    Discussion ID of discussion that contains comment.

  - `reports.discussions.comments.id` (number)
    Comment ID.

  - `reports.discussions.comments.modifiedAt` (any)

  - `reports.discussions.comments.text` (string)
    Comment body.

  - `reports.discussions.commentAttachments` (array)
    Array of attachments on discussion comments. Only returned if the include query string parameter contains attachments.

  - `reports.discussions.commentAttachments.id` (number)
    Attachment ID.

  - `reports.discussions.commentAttachments.parentId` (number)
    The ID of the parent.

  - `reports.discussions.commentAttachments.attachmentType` (string)
    Attachment type. Note--Dropbox, Egnyte, and Evernote are not supported for Smartsheet.gov accounts.
    Enum: "BOX_COM", "DROPBOX", "EGNYTE", "EVERNOTE", "FILE", "GOOGLE_DRIVE", "LINK", "ONEDRIVE", "TRELLO"

  - `reports.discussions.commentAttachments.attachmentSubType` (string)
    Attachment sub type. Note--Folder type is for EGNYTE values and the rest are GOOGLE_DRIVE values.
    Enum: "DOCUMENT", "DRAWING", "FOLDER", "PDF", "PRESENTATION", "SPREADSHEET"

  - `reports.discussions.commentAttachments.mimeType` (string)
    Attachment MIME type.
    Example: "PNG"

  - `reports.discussions.commentAttachments.parentType` (string)
    The type of object the attachment belongs to.
    Enum: "COMMENT", "PROOF", "ROW", "SHEET"

  - `reports.discussions.commentAttachments.createdAt` (any)

  - `reports.discussions.commentAttachments.createdBy` (object)
    User object containing name and email of the user who created this attachment.

  - `reports.discussions.commentAttachments.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.discussions.commentAttachments.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.discussions.commentAttachments.name` (string)
    Attachment name.

  - `reports.discussions.commentAttachments.sizeInKb` (number)
    The size of the file, if the attachmentType is FILE.

  - `reports.discussions.commentAttachments.url` (string)
    Attachment temporary URL (files only).

  - `reports.discussions.commentAttachments.urlExpiresInMillis` (number)
    Attachment temporary URL time to live (files only).

  - `reports.discussions.commentCount` (number)
    Number of comments in the discussion.

  - `reports.discussions.createdBy` (object)
    User object containing name and email of the user who created the discussion.

  - `reports.discussions.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.discussions.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.discussions.lastCommentedAt` (any)

  - `reports.discussions.lastCommentedUser` (object)
    User object containing name and email of the user who last commented on the discussion.

  - `reports.discussions.lastCommentedUser.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.discussions.lastCommentedUser.name` (string)
    Example: "Jane Doe"

  - `reports.discussions.parentId` (number)
    The ID of the associated row or sheet.

  - `reports.discussions.parentType` (string)
    Type of parent object.
    Enum: "ROW", "SHEET"

  - `reports.discussions.readOnly` (boolean)
    Indicates whether the user can modify the discussion.

  - `reports.discussions.title` (string)
    Title automatically created by duplicating the first 100 characters of top-level comment.

  - `reports.effectiveAttachmentOptions` (array)
    Array of enum strings (see [Attachment.attachmentType](/api/smartsheet/openapi/attachments) indicating the allowable attachment options for the current user and sheet.

  - `reports.ganttEnabled` (boolean)
    Indicates whether "Gantt View" is enabled.

  - `reports.hasSummaryFields` (boolean)
    Indicates whether a sheet summary is present.

  - `reports.isMultiPicklistEnabled` (boolean)
    Indicates whether multi-select is enabled.

  - `reports.modifiedAt` (any)

  - `reports.name` (string)
    Sheet name.

  - `reports.owner` (string)
    Email address of the sheet owner.

  - `reports.permalink` (string)
    URL that represents a direct link to the sheet in Smartsheet.

  - `reports.projectSettings` (object)
    Represents the project settings dependencies for a specific sheet. Project settings may be updated on sheets that the user has editor access.

  - `reports.projectSettings.lengthOfDay` (number)
    Length of a workday for a project sheet.

  - `reports.projectSettings.nonWorkingDays` (array)
    Non-working days for a project sheet.

  - `reports.projectSettings.workingDays` (array)
    Enum: "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"

  - `reports.readOnly` (boolean)
    Returned only if the sheet belongs to an expired trial (value = true).

  - `reports.resourceManagementEnabled` (boolean)
    Indicates that resource management is enabled.

  - `reports.resourceManagementType` (string)
    Resource Management type. Indicates the type of RM that is enabled.
    Enum: "NONE", "LEGACY_RESOURCE_MANAGEMENT", "RESOURCE_MANAGEMENT_BY_SMARTSHEET"

  - `reports.rows` (array)

  - `reports.rows.id` (number)
    Row ID.

  - `reports.rows.sheetId` (number)
    Parent sheet ID.

  - `reports.rows.siblingId` (number)
    Sibling ID.

  - `reports.rows.accessLevel` (string)
    Enum: "ADMIN", "COMMENTER", "EDITOR", "EDITOR_SHARE", "OWNER", "VIEWER"

  - `reports.rows.attachments` (array)
    Attachments on row. Only returned if the include query string parameter contains attachments.

  - `reports.rows.attachments.id` (number)
    Attachment ID.

  - `reports.rows.attachments.parentId` (number)
    The ID of the parent.

  - `reports.rows.attachments.attachmentType` (string)
    Attachment type. Note--Dropbox, Egnyte, and Evernote are not supported for Smartsheet.gov accounts.
    Enum: "BOX_COM", "DROPBOX", "EGNYTE", "EVERNOTE", "FILE", "GOOGLE_DRIVE", "LINK", "ONEDRIVE", "TRELLO"

  - `reports.rows.attachments.attachmentSubType` (string)
    Attachment sub type. Note--Folder type is for EGNYTE values and the rest are GOOGLE_DRIVE values.
    Enum: "DOCUMENT", "DRAWING", "FOLDER", "PDF", "PRESENTATION", "SPREADSHEET"

  - `reports.rows.attachments.mimeType` (string)
    Attachment MIME type.
    Example: "PNG"

  - `reports.rows.attachments.parentType` (string)
    The type of object the attachment belongs to.
    Enum: "COMMENT", "PROOF", "ROW", "SHEET"

  - `reports.rows.attachments.createdAt` (any)

  - `reports.rows.attachments.createdBy` (object)
    User object containing name and email of the user who created this attachment.

  - `reports.rows.attachments.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.rows.attachments.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.rows.attachments.name` (string)
    Attachment name.

  - `reports.rows.attachments.sizeInKb` (number)
    The size of the file, if the attachmentType is FILE.

  - `reports.rows.attachments.url` (string)
    Attachment temporary URL (files only).

  - `reports.rows.attachments.urlExpiresInMillis` (number)
    Attachment temporary URL time to live (files only).

  - `reports.rows.cells` (array)
    Cells belonging to the row.

  - `reports.rows.cells.columnId` (number)
    The ID of the column that the cell is located in.

  - `reports.rows.cells.rowId` (number)
    The ID of the row the cell is located in.

  - `reports.rows.cells.columnType` (string)
    Only returned if the include query string parameter contains columnType.

  - `reports.rows.cells.conditionalFormat` (string)
    The format descriptor describing this cell's conditional format. Only returned if the include query string parameter contains format and this cell has a conditional format applied.

  - `reports.rows.cells.displayValue` (string)
    Visual representation of cell contents, as presented to the user in the UI.

  - `reports.rows.cells.format` (string)
    The format descriptor. Only returned if the include query string parameter contains format and this cell has a non-default format applied.

  - `reports.rows.cells.formula` (string)
    The formula for a cell, if set, for instance =COUNTM([Assigned To]3). Note that calculation errors or problems with a formula do not cause the API call to return an error code. Instead, the response contains the same value as in the UI, such as cell.value = "#CIRCULAR REFERENCE".

  - `reports.rows.cells.hyperlink` (object)

  - `reports.rows.cells.hyperlink.reportId` (number)
    If non-null, this hyperlink is a link to the report with this ID.

  - `reports.rows.cells.hyperlink.sheetId` (number)
    If non-null, this hyperlink is a link to the sheet with this ID.

  - `reports.rows.cells.hyperlink.sightId` (number)
    If non-null, this hyperlink is a link to the dashboard with this ID.

  - `reports.rows.cells.hyperlink.url` (string)
    When the hyperlink is a URL link, this property contains the URL value. When the hyperlink is a dashboard/report/sheet link (that is, dashboardId, reportId, or sheetId is non-null), this property contains the permalink to the dashboard, report, or sheet.

  - `reports.rows.cells.image` (object)

  - `reports.rows.cells.image.altText` (string)
    Alternate text for the image.

  - `reports.rows.cells.image.height` (number)
    Original height (in pixels) of the uploaded image.

  - `reports.rows.cells.image.id` (string)
    Image ID.

  - `reports.rows.cells.image.width` (number)
    Original width (in pixels) of the uploaded image.

  - `reports.rows.cells.linkInFromCell` (object)

  - `reports.rows.cells.linkInFromCell.columnId` (number)
    Column ID of the linked cell.

  - `reports.rows.cells.linkInFromCell.rowId` (number)
    Row ID of the linked cell.

  - `reports.rows.cells.linkInFromCell.sheetId` (number)
    Sheet ID of the sheet that the linked cell belongs to.

  - `reports.rows.cells.linkInFromCell.sheetName` (string)
    Sheet name of the linked cell.

  - `reports.rows.cells.linkInFromCell.status` (string)
    * BLOCKED One of several other values indicating unusual error conditions.
* BROKEN The row or sheet linked to was deleted.
* CIRCULAR One of several other values indicating unusual error conditions.
* DISABLED One of several other values indicating unusual error conditions.
* INACCESSIBLE The sheet linked to cannot be viewed by this user.
* INVALID One of several other values indicating unusual error conditions.
* NOT_SHARED One of several other values indicating unusual error conditions.
* OK The link is in a good state.
    Enum: "BLOCKED", "BROKEN", "CIRCULAR", "DISABLED", "INACCESSIBLE", "INVALID", "NOT_SHARED", "OK"

  - `reports.rows.cells.linksOutToCells` (array)

  - `reports.rows.cells.linksOutToCells.columnId` (number)
    Column ID of the linked cell.

  - `reports.rows.cells.linksOutToCells.rowId` (number)
    Row ID of the linked cell.

  - `reports.rows.cells.linksOutToCells.sheetId` (number)
    Sheet ID of the sheet that the linked cell belongs to.

  - `reports.rows.cells.linksOutToCells.sheetName` (string)
    Sheet name of the linked cell.

  - `reports.rows.cells.linksOutToCells.status` (string)
    * BLOCKED One of several other values indicating unusual error conditions.
* BROKEN The row or sheet linked to was deleted.
* CIRCULAR One of several other values indicating unusual error conditions.
* DISABLED One of several other values indicating unusual error conditions.
* INACCESSIBLE The sheet linked to cannot be viewed by this user.
* INVALID One of several other values indicating unusual error conditions.
* NOT_SHARED One of several other values indicating unusual error conditions.
* OK The link is in a good state.
    Enum: "BLOCKED", "BROKEN", "CIRCULAR", "DISABLED", "INACCESSIBLE", "INVALID", "NOT_SHARED", "OK"

  - `reports.rows.cells.objectValue` (any)

  - `reports.rows.cells.overrideValidation` (boolean)
    (Admin only) Indicates whether the cell value can contain a value outside of the validation limits (value = true). When using this parameter, you must also set strict to false to bypass value type checking. This property is honored for POST or PUT actions that update rows.

  - `reports.rows.cells.strict` (boolean)
    Set to false to enable lenient parsing. Defaults to true. You can specify this attribute in a request, but it is never present in a response.

  - `reports.rows.cells.value` (any)
    A string, number, or a Boolean value -- depending on the cell type and the data in the cell. Cell values larger than 4000 characters are silently truncated. An empty cell returns no value.

  - `reports.rows.columns` (array)
    Columns of row. Only returned if the include query string parameter contains columns.

  - `reports.rows.conditionalFormat` (string)
    Describes this row's conditional format. Only returned if the include query string parameter contains format and this row has a conditional format applied.
    Example: ",,1,1,,,,,,,,,,,,,"

  - `reports.rows.createdAt` (any)

  - `reports.rows.createdBy` (object)
    User object containing name and email of the creator of this row.

  - `reports.rows.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.rows.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.rows.discussions` (array)
    Discussions on the row. Only returned if the include query string parameter contains discussions.

  - `reports.rows.discussions.accessLevel` (string)
    Enum: "ADMIN", "COMMENTER", "EDITOR", "EDITOR_SHARE", "OWNER", "VIEWER"

  - `reports.rows.discussions.id` (number)
    Discussion ID.

  - `reports.rows.discussions.comments` (array)
    Array of comments in discussion. Only returned if the include query string parameter contains comments.

  - `reports.rows.discussions.comments.attachments` (array)
    Array of attachments on comments.

  - `reports.rows.discussions.comments.attachments.id` (number)
    Attachment ID.

  - `reports.rows.discussions.comments.attachments.parentId` (number)
    The ID of the parent.

  - `reports.rows.discussions.comments.attachments.attachmentType` (string)
    Attachment type. Note--Dropbox, Egnyte, and Evernote are not supported for Smartsheet.gov accounts.
    Enum: "BOX_COM", "DROPBOX", "EGNYTE", "EVERNOTE", "FILE", "GOOGLE_DRIVE", "LINK", "ONEDRIVE", "TRELLO"

  - `reports.rows.discussions.comments.attachments.attachmentSubType` (string)
    Attachment sub type. Note--Folder type is for EGNYTE values and the rest are GOOGLE_DRIVE values.
    Enum: "DOCUMENT", "DRAWING", "FOLDER", "PDF", "PRESENTATION", "SPREADSHEET"

  - `reports.rows.discussions.comments.attachments.mimeType` (string)
    Attachment MIME type.
    Example: "PNG"

  - `reports.rows.discussions.comments.attachments.parentType` (string)
    The type of object the attachment belongs to.
    Enum: "COMMENT", "PROOF", "ROW", "SHEET"

  - `reports.rows.discussions.comments.attachments.createdAt` (any)

  - `reports.rows.discussions.comments.attachments.createdBy` (object)
    User object containing name and email of the user who created this attachment.

  - `reports.rows.discussions.comments.attachments.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.rows.discussions.comments.attachments.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.rows.discussions.comments.attachments.name` (string)
    Attachment name.

  - `reports.rows.discussions.comments.attachments.sizeInKb` (number)
    The size of the file, if the attachmentType is FILE.

  - `reports.rows.discussions.comments.attachments.url` (string)
    Attachment temporary URL (files only).

  - `reports.rows.discussions.comments.attachments.urlExpiresInMillis` (number)
    Attachment temporary URL time to live (files only).

  - `reports.rows.discussions.comments.createdAt` (any)

  - `reports.rows.discussions.comments.createdBy` (object)
    User object containing name and email of the creator of this comment.

  - `reports.rows.discussions.comments.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.rows.discussions.comments.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.rows.discussions.comments.discussionId` (number)
    Discussion ID of discussion that contains comment.

  - `reports.rows.discussions.comments.id` (number)
    Comment ID.

  - `reports.rows.discussions.comments.modifiedAt` (any)

  - `reports.rows.discussions.comments.text` (string)
    Comment body.

  - `reports.rows.discussions.commentAttachments` (array)
    Array of attachments on discussion comments. Only returned if the include query string parameter contains attachments.

  - `reports.rows.discussions.commentAttachments.id` (number)
    Attachment ID.

  - `reports.rows.discussions.commentAttachments.parentId` (number)
    The ID of the parent.

  - `reports.rows.discussions.commentAttachments.attachmentType` (string)
    Attachment type. Note--Dropbox, Egnyte, and Evernote are not supported for Smartsheet.gov accounts.
    Enum: "BOX_COM", "DROPBOX", "EGNYTE", "EVERNOTE", "FILE", "GOOGLE_DRIVE", "LINK", "ONEDRIVE", "TRELLO"

  - `reports.rows.discussions.commentAttachments.attachmentSubType` (string)
    Attachment sub type. Note--Folder type is for EGNYTE values and the rest are GOOGLE_DRIVE values.
    Enum: "DOCUMENT", "DRAWING", "FOLDER", "PDF", "PRESENTATION", "SPREADSHEET"

  - `reports.rows.discussions.commentAttachments.mimeType` (string)
    Attachment MIME type.
    Example: "PNG"

  - `reports.rows.discussions.commentAttachments.parentType` (string)
    The type of object the attachment belongs to.
    Enum: "COMMENT", "PROOF", "ROW", "SHEET"

  - `reports.rows.discussions.commentAttachments.createdAt` (any)

  - `reports.rows.discussions.commentAttachments.createdBy` (object)
    User object containing name and email of the user who created this attachment.

  - `reports.rows.discussions.commentAttachments.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.rows.discussions.commentAttachments.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.rows.discussions.commentAttachments.name` (string)
    Attachment name.

  - `reports.rows.discussions.commentAttachments.sizeInKb` (number)
    The size of the file, if the attachmentType is FILE.

  - `reports.rows.discussions.commentAttachments.url` (string)
    Attachment temporary URL (files only).

  - `reports.rows.discussions.commentAttachments.urlExpiresInMillis` (number)
    Attachment temporary URL time to live (files only).

  - `reports.rows.discussions.commentCount` (number)
    Number of comments in the discussion.

  - `reports.rows.discussions.createdBy` (object)
    User object containing name and email of the user who created the discussion.

  - `reports.rows.discussions.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.rows.discussions.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.rows.discussions.lastCommentedAt` (any)

  - `reports.rows.discussions.lastCommentedUser` (object)
    User object containing name and email of the user who last commented on the discussion.

  - `reports.rows.discussions.lastCommentedUser.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.rows.discussions.lastCommentedUser.name` (string)
    Example: "Jane Doe"

  - `reports.rows.discussions.parentId` (number)
    The ID of the associated row or sheet.

  - `reports.rows.discussions.parentType` (string)
    Type of parent object.
    Enum: "ROW", "SHEET"

  - `reports.rows.discussions.readOnly` (boolean)
    Indicates whether the user can modify the discussion.

  - `reports.rows.discussions.title` (string)
    Title automatically created by duplicating the first 100 characters of top-level comment.

  - `reports.rows.proof` (object)
    Object containing zero or more media items, including images, videos, and documents, for review, editing, or approval.

  - `reports.rows.proof.id` (number)
    Proof ID of the proof version.

  - `reports.rows.proof.originalId` (number)
    Proof ID of the original proof version.

  - `reports.rows.proof.name` (string)
    Proof name. This is the same as primary column value. If the primary column value is empty, name is empty.

  - `reports.rows.proof.type` (string)
    File type for the proof version.
    Enum: "DOCUMENT", "IMAGE", "MIXED", "NONE", "VIDEO"

  - `reports.rows.proof.documentType` (string)
    If type=DOCUMENT, then this indicates the type of file, such as PDF.

  - `reports.rows.proof.proofRequestUrl` (string)
    URL to review a proofing request.

  - `reports.rows.proof.version` (number)
    The version number of the proof.

  - `reports.rows.proof.lastUpdatedAt` (any)

  - `reports.rows.proof.lastUpdatedBy` (object)
    User object containing name and email of the user who last updated the proof.

  - `reports.rows.proof.lastUpdatedBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.rows.proof.lastUpdatedBy.name` (string)
    Example: "Jane Doe"

  - `reports.rows.proof.isCompleted` (boolean)
    Indicates whether the proof is completed.

  - `reports.rows.proof.attachments` (array)
    Array of Attachment objects. Only returned if the include query string parameter contains attachments.

  - `reports.rows.proof.attachments.id` (number)
    Attachment ID.

  - `reports.rows.proof.attachments.parentId` (number)
    The ID of the parent.

  - `reports.rows.proof.attachments.attachmentType` (string)
    Attachment type. Note--Dropbox, Egnyte, and Evernote are not supported for Smartsheet.gov accounts.
    Enum: "BOX_COM", "DROPBOX", "EGNYTE", "EVERNOTE", "FILE", "GOOGLE_DRIVE", "LINK", "ONEDRIVE", "TRELLO"

  - `reports.rows.proof.attachments.attachmentSubType` (string)
    Attachment sub type. Note--Folder type is for EGNYTE values and the rest are GOOGLE_DRIVE values.
    Enum: "DOCUMENT", "DRAWING", "FOLDER", "PDF", "PRESENTATION", "SPREADSHEET"

  - `reports.rows.proof.attachments.mimeType` (string)
    Attachment MIME type.
    Example: "PNG"

  - `reports.rows.proof.attachments.parentType` (string)
    The type of object the attachment belongs to.
    Enum: "COMMENT", "PROOF", "ROW", "SHEET"

  - `reports.rows.proof.attachments.createdAt` (any)

  - `reports.rows.proof.attachments.createdBy` (object)
    User object containing name and email of the user who created this attachment.

  - `reports.rows.proof.attachments.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.rows.proof.attachments.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.rows.proof.attachments.name` (string)
    Attachment name.

  - `reports.rows.proof.attachments.sizeInKb` (number)
    The size of the file, if the attachmentType is FILE.

  - `reports.rows.proof.attachments.url` (string)
    Attachment temporary URL (files only).

  - `reports.rows.proof.attachments.urlExpiresInMillis` (number)
    Attachment temporary URL time to live (files only).

  - `reports.rows.proof.discussions` (array)
    Array of Discussion objects. Only returned if the include query string parameter contains discussions.

  - `reports.rows.proof.discussions.accessLevel` (string)
    Enum: "ADMIN", "COMMENTER", "EDITOR", "EDITOR_SHARE", "OWNER", "VIEWER"

  - `reports.rows.proof.discussions.id` (number)
    Discussion ID.

  - `reports.rows.proof.discussions.comments` (array)
    Array of comments in discussion. Only returned if the include query string parameter contains comments.

  - `reports.rows.proof.discussions.comments.attachments` (array)
    Array of attachments on comments.

  - `reports.rows.proof.discussions.comments.attachments.id` (number)
    Attachment ID.

  - `reports.rows.proof.discussions.comments.attachments.parentId` (number)
    The ID of the parent.

  - `reports.rows.proof.discussions.comments.attachments.attachmentType` (string)
    Attachment type. Note--Dropbox, Egnyte, and Evernote are not supported for Smartsheet.gov accounts.
    Enum: "BOX_COM", "DROPBOX", "EGNYTE", "EVERNOTE", "FILE", "GOOGLE_DRIVE", "LINK", "ONEDRIVE", "TRELLO"

  - `reports.rows.proof.discussions.comments.attachments.attachmentSubType` (string)
    Attachment sub type. Note--Folder type is for EGNYTE values and the rest are GOOGLE_DRIVE values.
    Enum: "DOCUMENT", "DRAWING", "FOLDER", "PDF", "PRESENTATION", "SPREADSHEET"

  - `reports.rows.proof.discussions.comments.attachments.mimeType` (string)
    Attachment MIME type.
    Example: "PNG"

  - `reports.rows.proof.discussions.comments.attachments.parentType` (string)
    The type of object the attachment belongs to.
    Enum: "COMMENT", "PROOF", "ROW", "SHEET"

  - `reports.rows.proof.discussions.comments.attachments.createdAt` (any)

  - `reports.rows.proof.discussions.comments.attachments.createdBy` (object)
    User object containing name and email of the user who created this attachment.

  - `reports.rows.proof.discussions.comments.attachments.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.rows.proof.discussions.comments.attachments.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.rows.proof.discussions.comments.attachments.name` (string)
    Attachment name.

  - `reports.rows.proof.discussions.comments.attachments.sizeInKb` (number)
    The size of the file, if the attachmentType is FILE.

  - `reports.rows.proof.discussions.comments.attachments.url` (string)
    Attachment temporary URL (files only).

  - `reports.rows.proof.discussions.comments.attachments.urlExpiresInMillis` (number)
    Attachment temporary URL time to live (files only).

  - `reports.rows.proof.discussions.comments.createdAt` (any)

  - `reports.rows.proof.discussions.comments.createdBy` (object)
    User object containing name and email of the creator of this comment.

  - `reports.rows.proof.discussions.comments.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.rows.proof.discussions.comments.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.rows.proof.discussions.comments.discussionId` (number)
    Discussion ID of discussion that contains comment.

  - `reports.rows.proof.discussions.comments.id` (number)
    Comment ID.

  - `reports.rows.proof.discussions.comments.modifiedAt` (any)

  - `reports.rows.proof.discussions.comments.text` (string)
    Comment body.

  - `reports.rows.proof.discussions.commentAttachments` (array)
    Array of attachments on discussion comments. Only returned if the include query string parameter contains attachments.

  - `reports.rows.proof.discussions.commentAttachments.id` (number)
    Attachment ID.

  - `reports.rows.proof.discussions.commentAttachments.parentId` (number)
    The ID of the parent.

  - `reports.rows.proof.discussions.commentAttachments.attachmentType` (string)
    Attachment type. Note--Dropbox, Egnyte, and Evernote are not supported for Smartsheet.gov accounts.
    Enum: "BOX_COM", "DROPBOX", "EGNYTE", "EVERNOTE", "FILE", "GOOGLE_DRIVE", "LINK", "ONEDRIVE", "TRELLO"

  - `reports.rows.proof.discussions.commentAttachments.attachmentSubType` (string)
    Attachment sub type. Note--Folder type is for EGNYTE values and the rest are GOOGLE_DRIVE values.
    Enum: "DOCUMENT", "DRAWING", "FOLDER", "PDF", "PRESENTATION", "SPREADSHEET"

  - `reports.rows.proof.discussions.commentAttachments.mimeType` (string)
    Attachment MIME type.
    Example: "PNG"

  - `reports.rows.proof.discussions.commentAttachments.parentType` (string)
    The type of object the attachment belongs to.
    Enum: "COMMENT", "PROOF", "ROW", "SHEET"

  - `reports.rows.proof.discussions.commentAttachments.createdAt` (any)

  - `reports.rows.proof.discussions.commentAttachments.createdBy` (object)
    User object containing name and email of the user who created this attachment.

  - `reports.rows.proof.discussions.commentAttachments.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.rows.proof.discussions.commentAttachments.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.rows.proof.discussions.commentAttachments.name` (string)
    Attachment name.

  - `reports.rows.proof.discussions.commentAttachments.sizeInKb` (number)
    The size of the file, if the attachmentType is FILE.

  - `reports.rows.proof.discussions.commentAttachments.url` (string)
    Attachment temporary URL (files only).

  - `reports.rows.proof.discussions.commentAttachments.urlExpiresInMillis` (number)
    Attachment temporary URL time to live (files only).

  - `reports.rows.proof.discussions.commentCount` (number)
    Number of comments in the discussion.

  - `reports.rows.proof.discussions.createdBy` (object)
    User object containing name and email of the user who created the discussion.

  - `reports.rows.proof.discussions.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.rows.proof.discussions.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.rows.proof.discussions.lastCommentedAt` (any)

  - `reports.rows.proof.discussions.lastCommentedUser` (object)
    User object containing name and email of the user who last commented on the discussion.

  - `reports.rows.proof.discussions.lastCommentedUser.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.rows.proof.discussions.lastCommentedUser.name` (string)
    Example: "Jane Doe"

  - `reports.rows.proof.discussions.parentId` (number)
    The ID of the associated row or sheet.

  - `reports.rows.proof.discussions.parentType` (string)
    Type of parent object.
    Enum: "ROW", "SHEET"

  - `reports.rows.proof.discussions.readOnly` (boolean)
    Indicates whether the user can modify the discussion.

  - `reports.rows.proof.discussions.title` (string)
    Title automatically created by duplicating the first 100 characters of top-level comment.

  - `reports.rows.expanded` (boolean)
    Indicates whether the row is expanded or collapsed.

  - `reports.rows.filteredOut` (boolean)
    Indicates if the row is filtered out by a column filter. Only returned if the include query string parameter contains filters.

  - `reports.rows.format` (string)
    Format descriptor. Only returned if the include query string parameter contains format and this row has a non-default format applied.
    Example: ",,1,1,,,,,,,,,,,,,"

  - `reports.rows.inCriticalPath` (boolean)
    Only returned, with a value of true, if the sheet is a project sheet with dependencies enabled and this row is in the critical path.

  - `reports.rows.locked` (boolean)
    Indicates whether the row is locked.

  - `reports.rows.lockedForUser` (boolean)
    Indicates whether the row is locked for the requesting user.

  - `reports.rows.modifiedAt` (any)

  - `reports.rows.modifiedBy` (object)
    User object containing name and email of the last person to modify this row.

  - `reports.rows.modifiedBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.rows.modifiedBy.name` (string)
    Example: "Jane Doe"

  - `reports.rows.permaLink` (string)
    URL that represents a direct link to the row in Smartsheet. Only returned if the include query string parameter contains rowPermalink.

  - `reports.rows.rowNumber` (number)
    Row number within the sheet.

  - `reports.rows.version` (number)
    Sheet version number that is incremented every time a sheet is modified.

  - `reports.showParentRowsForFilters` (boolean)
    Returned only if there are column filters on the sheet. Value = true if "show parent rows" is enabled for the filters.

  - `reports.source` (object)

  - `reports.source.id` (number)
    The ID of the dashboard, report, sheet, or template from which the enclosing dashboard, report, sheet, or template was created.

  - `reports.source.type` (string)
    report, sheet, sight (aka dashboard), or template.

  - `reports.summary` (object)
    Represents the entire summary, or a list of defined fields and values, for a specific sheet.

  - `reports.summary.fields` (array)
    Array of summary (or metadata) fields defined on the sheet.

  - `reports.summary.fields.id` (number)
    SummaryField ID.

  - `reports.summary.fields.contactOptions` (array)
    Array of ContactOption objects to specify a pre-defined list of values for the column. Column type must be CONTACT_LIST.

  - `reports.summary.fields.contactOptions.email` (string)
    A parsable email address.

  - `reports.summary.fields.contactOptions.name` (string)
    Can be a user's name, display name, or free text.

  - `reports.summary.fields.createdAt` (any)

  - `reports.summary.fields.createdBy` (object)
    User object containing name and email of the creator of this summary field.

  - `reports.summary.fields.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.summary.fields.createdBy.name` (string)
    Example: "Jane Doe"

  - `reports.summary.fields.displayValue` (string)
    Visual representation of cell contents, as presented to the user in the UI.

  - `reports.summary.fields.format` (string)
    The format descriptor. Only returned if the include query string parameter contains format and this column has a non-default format applied to it.

  - `reports.summary.fields.formula` (string)
    The formula for a cell, if set.

  - `reports.summary.fields.hyperlink` (object)

  - `reports.summary.fields.hyperlink.reportId` (number)
    If non-null, this hyperlink is a link to the report with this ID.

  - `reports.summary.fields.hyperlink.sheetId` (number)
    If non-null, this hyperlink is a link to the sheet with this ID.

  - `reports.summary.fields.hyperlink.sightId` (number)
    If non-null, this hyperlink is a link to the dashboard with this ID.

  - `reports.summary.fields.hyperlink.url` (string)
    When the hyperlink is a URL link, this property contains the URL value. When the hyperlink is a dashboard/report/sheet link (that is, dashboardId, reportId, or sheetId is non-null), this property contains the permalink to the dashboard, report, or sheet.

  - `reports.summary.fields.image` (object)

  - `reports.summary.fields.image.altText` (string)
    Alternate text for the image.

  - `reports.summary.fields.image.height` (number)
    Original height (in pixels) of the uploaded image.

  - `reports.summary.fields.image.id` (string)
    Image ID.

  - `reports.summary.fields.image.width` (number)
    Original width (in pixels) of the uploaded image.

  - `reports.summary.fields.index` (number)
    Field index or position. This number is zero-based.

  - `reports.summary.fields.locked` (boolean)
    Indicates whether the field is locked.

  - `reports.summary.fields.lockedForUser` (boolean)
    Indicates whether the field is locked for the requesting user.

  - `reports.summary.fields.modifiedAt` (any)

  - `reports.summary.fields.modifiedBy` (object)
    User object containing name and email of the user who most recently modified this summary field.

  - `reports.summary.fields.modifiedBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `reports.summary.fields.modifiedBy.name` (string)
    Example: "Jane Doe"

  - `reports.summary.fields.objectValue` (any)

  - `reports.summary.fields.options` (array)
    When applicable for PICKLIST column type. Array of the options available for the field.

  - `reports.summary.fields.symbol` (string)
    When applicable for PICKLIST column type.

  - `reports.summary.fields.title` (string)
    Arbitrary name, must be unique within summary.

  - `reports.summary.fields.type` (string)
    Enum: "ABSTRACT_DATETIME", "CHECKBOX", "CONTACT_LIST", "DATE", "DATETIME", "DURATION", "MULTI_CONTACT_LIST", "MULTI_PICKLIST", "PICKLIST", "PREDECESSOR", "TEXT_NUMBER"

  - `reports.summary.fields.validation` (boolean)
    Indicates whether summary field values are restricted to the type.

  - `reports.totalRowCount` (number)
    The total number of rows in the sheet.

  - `reports.userPermissions` (object)
    Describes the current user's editing permissions for a specific sheet.

  - `reports.userPermissions.summaryPermissions` (string)
    One of:
  * ADMIN: full control over fields.
  * READ_DELETE: sheet is owned by an individual account that doesn't have summary capabilities. If a summary exists, the only possible operations are GET and DELETE fields.
  * READ_ONLY.
  * READ_WRITE: can edit values of existing fields, but not create or delete fields, nor modify field type.
    Enum: "ADMIN", "READ_DELETE", "READ_ONLY", "READ_WRITE"

  - `reports.userSettings` (object)
    Represents individual user settings for a specific sheet. User settings may be updated even on sheets where the current user only has read access (for example, viewer permissions or a read-only sheet).

  - `reports.userSettings.criticalPathEnabled` (boolean)
    Does this user have "Show Critical Path" turned on for this sheet? NOTE: This setting only has an effect on project sheets with dependencies enabled.

  - `reports.userSettings.displaySummaryTasks` (boolean)
    Does this user have "Display Summary Tasks" turned on for this sheet? Applies only to sheets where "Calendar View" has been configured.

  - `reports.version` (number)
    A number that is incremented every time a sheet is modified.

  - `reports.workspace` (object)

  - `reports.workspace.id` (number)
    Workspace ID.

  - `reports.workspace.name` (string)
    Workspace name.

  - `reports.workspace.accessLevel` (string)
    Enum: "ADMIN", "COMMENTER", "EDITOR", "EDITOR_SHARE", "OWNER", "VIEWER"

  - `reports.workspace.permalink` (string)
    URL that represents a direct link to the workspace in Smartsheet.

  - `reports.favorite` (boolean)
    Deprecated Returned only if the user has marked this sheet as a favorite in their Home tab (value = true).

  - `sheets` (array)

  - `sheets.id` (number)
    Sheet ID.

  - `sheets.fromId` (number)
    The ID of the template from which to create the sheet. This attribute can be specified in a request, but is never present in a response.

  - `sheets.ownerId` (number)
    User ID of the sheet owner.

  - `sheets.accessLevel` (string)
    Enum: "ADMIN", "COMMENTER", "EDITOR", "EDITOR_SHARE", "OWNER", "VIEWER"

  - `sheets.attachments` (array)
    Array of Attachment objects.
Only returned if the [include](/api/smartsheet/openapi/sheets/getsheet) query string parameter contains attachments.

  - `sheets.attachments.id` (number)
    Attachment ID.

  - `sheets.attachments.parentId` (number)
    The ID of the parent.

  - `sheets.attachments.attachmentType` (string)
    Attachment type. Note--Dropbox, Egnyte, and Evernote are not supported for Smartsheet.gov accounts.
    Enum: "BOX_COM", "DROPBOX", "EGNYTE", "EVERNOTE", "FILE", "GOOGLE_DRIVE", "LINK", "ONEDRIVE", "TRELLO"

  - `sheets.attachments.attachmentSubType` (string)
    Attachment sub type. Note--Folder type is for EGNYTE values and the rest are GOOGLE_DRIVE values.
    Enum: "DOCUMENT", "DRAWING", "FOLDER", "PDF", "PRESENTATION", "SPREADSHEET"

  - `sheets.attachments.mimeType` (string)
    Attachment MIME type.
    Example: "PNG"

  - `sheets.attachments.parentType` (string)
    The type of object the attachment belongs to.
    Enum: "COMMENT", "PROOF", "ROW", "SHEET"

  - `sheets.attachments.createdAt` (any)

  - `sheets.attachments.createdBy` (object)
    User object containing name and email of the user who created this attachment.

  - `sheets.attachments.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `sheets.attachments.createdBy.name` (string)
    Example: "Jane Doe"

  - `sheets.attachments.name` (string)
    Attachment name.

  - `sheets.attachments.sizeInKb` (number)
    The size of the file, if the attachmentType is FILE.

  - `sheets.attachments.url` (string)
    Attachment temporary URL (files only).

  - `sheets.attachments.urlExpiresInMillis` (number)
    Attachment temporary URL time to live (files only).

  - `sheets.cellImageUploadEnabled` (boolean)
    The sheet is enabled for cell images to be uploaded.

  - `sheets.columns` (array)

  - `sheets.createdAt` (any)

  - `sheets.crossSheetReferences` (array)
    Array of CrossSheetReference objects.
Only returned if the [include](/api/smartsheet/openapi/sheets/getsheet) query string parameter contains crossSheetReferences.

  - `sheets.crossSheetReferences.endColumnId` (number)
    Defines ending edge of range when specifying one or more columns. To specify an entire column, omit the startRowId and endRowId parameters.

  - `sheets.crossSheetReferences.endRowId` (number)
    Defines ending edge of range when specifying one or more rows. To specify an entire row, omit the startColumnId and endColumnId parameters.

  - `sheets.crossSheetReferences.id` (number)
    Cross-sheet reference ID, guaranteed unique within referencing sheet.

  - `sheets.crossSheetReferences.name` (string)
    Friendly name of reference. Auto-generated unless specified in Create Cross-sheet References.

  - `sheets.crossSheetReferences.startColumnId` (number)
    Defines beginning edge of range when specifying one or more columns. To specify an entire column, omit the startRowId and endRowId parameters.

  - `sheets.crossSheetReferences.startRowId` (number)
    Defines beginning edge of range when specifying one or more rows. To specify an entire row, omit the startColumnId and endColumnId parameters.

  - `sheets.crossSheetReferences.status` (string)
    Status of request:
 * 'BLOCKED' - A reference is downstream of a circular issue.
 * 'BROKEN' - The data source location (column, row or sheet) was deleted.
 * 'CIRCULAR' - The formula reference is self referencing and cannot be resolved.
 * 'DISABLED' - Updating the reference is temporarily disabled due to maintenance.
 * 'INVALID/UNKNOWN' - The reference is new and had not been validated.
 * 'NOT_SHARED' - No common shared users.
 * 'OK' - The reference is in a good state.
    Enum: "BLOCKED", "BROKEN", "CIRCULAR", "DISABLED", "INVALID/UNKNOWN", "NOT-SHARED", "OK"

  - `sheets.crossSheetReferences.sourceSheetId` (number)
    Sheet ID of source sheet.

  - `sheets.dependenciesEnabled` (boolean)
    Indicates whether dependencies are enabled.

  - `sheets.discussions` (array)
    Array of Discussion objects
Only returned if the [include](/api/smartsheet/openapi/sheets/getsheet) query string parameter contains discussions.

  - `sheets.discussions.accessLevel` (string)
    Enum: "ADMIN", "COMMENTER", "EDITOR", "EDITOR_SHARE", "OWNER", "VIEWER"

  - `sheets.discussions.id` (number)
    Discussion ID.

  - `sheets.discussions.comments` (array)
    Array of comments in discussion. Only returned if the include query string parameter contains comments.

  - `sheets.discussions.comments.attachments` (array)
    Array of attachments on comments.

  - `sheets.discussions.comments.attachments.id` (number)
    Attachment ID.

  - `sheets.discussions.comments.attachments.parentId` (number)
    The ID of the parent.

  - `sheets.discussions.comments.attachments.attachmentType` (string)
    Attachment type. Note--Dropbox, Egnyte, and Evernote are not supported for Smartsheet.gov accounts.
    Enum: "BOX_COM", "DROPBOX", "EGNYTE", "EVERNOTE", "FILE", "GOOGLE_DRIVE", "LINK", "ONEDRIVE", "TRELLO"

  - `sheets.discussions.comments.attachments.attachmentSubType` (string)
    Attachment sub type. Note--Folder type is for EGNYTE values and the rest are GOOGLE_DRIVE values.
    Enum: "DOCUMENT", "DRAWING", "FOLDER", "PDF", "PRESENTATION", "SPREADSHEET"

  - `sheets.discussions.comments.attachments.mimeType` (string)
    Attachment MIME type.
    Example: "PNG"

  - `sheets.discussions.comments.attachments.parentType` (string)
    The type of object the attachment belongs to.
    Enum: "COMMENT", "PROOF", "ROW", "SHEET"

  - `sheets.discussions.comments.attachments.createdAt` (any)

  - `sheets.discussions.comments.attachments.createdBy` (object)
    User object containing name and email of the user who created this attachment.

  - `sheets.discussions.comments.attachments.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `sheets.discussions.comments.attachments.createdBy.name` (string)
    Example: "Jane Doe"

  - `sheets.discussions.comments.attachments.name` (string)
    Attachment name.

  - `sheets.discussions.comments.attachments.sizeInKb` (number)
    The size of the file, if the attachmentType is FILE.

  - `sheets.discussions.comments.attachments.url` (string)
    Attachment temporary URL (files only).

  - `sheets.discussions.comments.attachments.urlExpiresInMillis` (number)
    Attachment temporary URL time to live (files only).

  - `sheets.discussions.comments.createdAt` (any)

  - `sheets.discussions.comments.createdBy` (object)
    User object containing name and email of the creator of this comment.

  - `sheets.discussions.comments.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `sheets.discussions.comments.createdBy.name` (string)
    Example: "Jane Doe"

  - `sheets.discussions.comments.discussionId` (number)
    Discussion ID of discussion that contains comment.

  - `sheets.discussions.comments.id` (number)
    Comment ID.

  - `sheets.discussions.comments.modifiedAt` (any)

  - `sheets.discussions.comments.text` (string)
    Comment body.

  - `sheets.discussions.commentAttachments` (array)
    Array of attachments on discussion comments. Only returned if the include query string parameter contains attachments.

  - `sheets.discussions.commentAttachments.id` (number)
    Attachment ID.

  - `sheets.discussions.commentAttachments.parentId` (number)
    The ID of the parent.

  - `sheets.discussions.commentAttachments.attachmentType` (string)
    Attachment type. Note--Dropbox, Egnyte, and Evernote are not supported for Smartsheet.gov accounts.
    Enum: "BOX_COM", "DROPBOX", "EGNYTE", "EVERNOTE", "FILE", "GOOGLE_DRIVE", "LINK", "ONEDRIVE", "TRELLO"

  - `sheets.discussions.commentAttachments.attachmentSubType` (string)
    Attachment sub type. Note--Folder type is for EGNYTE values and the rest are GOOGLE_DRIVE values.
    Enum: "DOCUMENT", "DRAWING", "FOLDER", "PDF", "PRESENTATION", "SPREADSHEET"

  - `sheets.discussions.commentAttachments.mimeType` (string)
    Attachment MIME type.
    Example: "PNG"

  - `sheets.discussions.commentAttachments.parentType` (string)
    The type of object the attachment belongs to.
    Enum: "COMMENT", "PROOF", "ROW", "SHEET"

  - `sheets.discussions.commentAttachments.createdAt` (any)

  - `sheets.discussions.commentAttachments.createdBy` (object)
    User object containing name and email of the user who created this attachment.

  - `sheets.discussions.commentAttachments.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `sheets.discussions.commentAttachments.createdBy.name` (string)
    Example: "Jane Doe"

  - `sheets.discussions.commentAttachments.name` (string)
    Attachment name.

  - `sheets.discussions.commentAttachments.sizeInKb` (number)
    The size of the file, if the attachmentType is FILE.

  - `sheets.discussions.commentAttachments.url` (string)
    Attachment temporary URL (files only).

  - `sheets.discussions.commentAttachments.urlExpiresInMillis` (number)
    Attachment temporary URL time to live (files only).

  - `sheets.discussions.commentCount` (number)
    Number of comments in the discussion.

  - `sheets.discussions.createdBy` (object)
    User object containing name and email of the user who created the discussion.

  - `sheets.discussions.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `sheets.discussions.createdBy.name` (string)
    Example: "Jane Doe"

  - `sheets.discussions.lastCommentedAt` (any)

  - `sheets.discussions.lastCommentedUser` (object)
    User object containing name and email of the user who last commented on the discussion.

  - `sheets.discussions.lastCommentedUser.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `sheets.discussions.lastCommentedUser.name` (string)
    Example: "Jane Doe"

  - `sheets.discussions.parentId` (number)
    The ID of the associated row or sheet.

  - `sheets.discussions.parentType` (string)
    Type of parent object.
    Enum: "ROW", "SHEET"

  - `sheets.discussions.readOnly` (boolean)
    Indicates whether the user can modify the discussion.

  - `sheets.discussions.title` (string)
    Title automatically created by duplicating the first 100 characters of top-level comment.

  - `sheets.effectiveAttachmentOptions` (array)
    Array of enum strings (see [Attachment.attachmentType](/api/smartsheet/openapi/attachments) indicating the allowable attachment options for the current user and sheet.

  - `sheets.ganttEnabled` (boolean)
    Indicates whether "Gantt View" is enabled.

  - `sheets.hasSummaryFields` (boolean)
    Indicates whether a sheet summary is present.

  - `sheets.isMultiPicklistEnabled` (boolean)
    Indicates whether multi-select is enabled.

  - `sheets.modifiedAt` (any)

  - `sheets.name` (string)
    Sheet name.

  - `sheets.owner` (string)
    Email address of the sheet owner.

  - `sheets.permalink` (string)
    URL that represents a direct link to the sheet in Smartsheet.

  - `sheets.projectSettings` (object)
    Represents the project settings dependencies for a specific sheet. Project settings may be updated on sheets that the user has editor access.

  - `sheets.projectSettings.lengthOfDay` (number)
    Length of a workday for a project sheet.

  - `sheets.projectSettings.nonWorkingDays` (array)
    Non-working days for a project sheet.

  - `sheets.projectSettings.workingDays` (array)
    Enum: "MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"

  - `sheets.readOnly` (boolean)
    Returned only if the sheet belongs to an expired trial (value = true).

  - `sheets.resourceManagementEnabled` (boolean)
    Indicates that resource management is enabled.

  - `sheets.resourceManagementType` (string)
    Resource Management type. Indicates the type of RM that is enabled.
    Enum: "NONE", "LEGACY_RESOURCE_MANAGEMENT", "RESOURCE_MANAGEMENT_BY_SMARTSHEET"

  - `sheets.rows` (array)

  - `sheets.rows.id` (number)
    Row ID.

  - `sheets.rows.sheetId` (number)
    Parent sheet ID.

  - `sheets.rows.siblingId` (number)
    Sibling ID.

  - `sheets.rows.accessLevel` (string)
    Enum: "ADMIN", "COMMENTER", "EDITOR", "EDITOR_SHARE", "OWNER", "VIEWER"

  - `sheets.rows.attachments` (array)
    Attachments on row. Only returned if the include query string parameter contains attachments.

  - `sheets.rows.attachments.id` (number)
    Attachment ID.

  - `sheets.rows.attachments.parentId` (number)
    The ID of the parent.

  - `sheets.rows.attachments.attachmentType` (string)
    Attachment type. Note--Dropbox, Egnyte, and Evernote are not supported for Smartsheet.gov accounts.
    Enum: "BOX_COM", "DROPBOX", "EGNYTE", "EVERNOTE", "FILE", "GOOGLE_DRIVE", "LINK", "ONEDRIVE", "TRELLO"

  - `sheets.rows.attachments.attachmentSubType` (string)
    Attachment sub type. Note--Folder type is for EGNYTE values and the rest are GOOGLE_DRIVE values.
    Enum: "DOCUMENT", "DRAWING", "FOLDER", "PDF", "PRESENTATION", "SPREADSHEET"

  - `sheets.rows.attachments.mimeType` (string)
    Attachment MIME type.
    Example: "PNG"

  - `sheets.rows.attachments.parentType` (string)
    The type of object the attachment belongs to.
    Enum: "COMMENT", "PROOF", "ROW", "SHEET"

  - `sheets.rows.attachments.createdAt` (any)

  - `sheets.rows.attachments.createdBy` (object)
    User object containing name and email of the user who created this attachment.

  - `sheets.rows.attachments.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `sheets.rows.attachments.createdBy.name` (string)
    Example: "Jane Doe"

  - `sheets.rows.attachments.name` (string)
    Attachment name.

  - `sheets.rows.attachments.sizeInKb` (number)
    The size of the file, if the attachmentType is FILE.

  - `sheets.rows.attachments.url` (string)
    Attachment temporary URL (files only).

  - `sheets.rows.attachments.urlExpiresInMillis` (number)
    Attachment temporary URL time to live (files only).

  - `sheets.rows.cells` (array)
    Cells belonging to the row.

  - `sheets.rows.cells.columnId` (number)
    The ID of the column that the cell is located in.

  - `sheets.rows.cells.rowId` (number)
    The ID of the row the cell is located in.

  - `sheets.rows.cells.columnType` (string)
    Only returned if the include query string parameter contains columnType.

  - `sheets.rows.cells.conditionalFormat` (string)
    The format descriptor describing this cell's conditional format. Only returned if the include query string parameter contains format and this cell has a conditional format applied.

  - `sheets.rows.cells.displayValue` (string)
    Visual representation of cell contents, as presented to the user in the UI.

  - `sheets.rows.cells.format` (string)
    The format descriptor. Only returned if the include query string parameter contains format and this cell has a non-default format applied.

  - `sheets.rows.cells.formula` (string)
    The formula for a cell, if set, for instance =COUNTM([Assigned To]3). Note that calculation errors or problems with a formula do not cause the API call to return an error code. Instead, the response contains the same value as in the UI, such as cell.value = "#CIRCULAR REFERENCE".

  - `sheets.rows.cells.hyperlink` (object)

  - `sheets.rows.cells.hyperlink.reportId` (number)
    If non-null, this hyperlink is a link to the report with this ID.

  - `sheets.rows.cells.hyperlink.sheetId` (number)
    If non-null, this hyperlink is a link to the sheet with this ID.

  - `sheets.rows.cells.hyperlink.sightId` (number)
    If non-null, this hyperlink is a link to the dashboard with this ID.

  - `sheets.rows.cells.hyperlink.url` (string)
    When the hyperlink is a URL link, this property contains the URL value. When the hyperlink is a dashboard/report/sheet link (that is, dashboardId, reportId, or sheetId is non-null), this property contains the permalink to the dashboard, report, or sheet.

  - `sheets.rows.cells.image` (object)

  - `sheets.rows.cells.image.altText` (string)
    Alternate text for the image.

  - `sheets.rows.cells.image.height` (number)
    Original height (in pixels) of the uploaded image.

  - `sheets.rows.cells.image.id` (string)
    Image ID.

  - `sheets.rows.cells.image.width` (number)
    Original width (in pixels) of the uploaded image.

  - `sheets.rows.cells.linkInFromCell` (object)

  - `sheets.rows.cells.linkInFromCell.columnId` (number)
    Column ID of the linked cell.

  - `sheets.rows.cells.linkInFromCell.rowId` (number)
    Row ID of the linked cell.

  - `sheets.rows.cells.linkInFromCell.sheetId` (number)
    Sheet ID of the sheet that the linked cell belongs to.

  - `sheets.rows.cells.linkInFromCell.sheetName` (string)
    Sheet name of the linked cell.

  - `sheets.rows.cells.linkInFromCell.status` (string)
    * BLOCKED One of several other values indicating unusual error conditions.
* BROKEN The row or sheet linked to was deleted.
* CIRCULAR One of several other values indicating unusual error conditions.
* DISABLED One of several other values indicating unusual error conditions.
* INACCESSIBLE The sheet linked to cannot be viewed by this user.
* INVALID One of several other values indicating unusual error conditions.
* NOT_SHARED One of several other values indicating unusual error conditions.
* OK The link is in a good state.
    Enum: "BLOCKED", "BROKEN", "CIRCULAR", "DISABLED", "INACCESSIBLE", "INVALID", "NOT_SHARED", "OK"

  - `sheets.rows.cells.linksOutToCells` (array)

  - `sheets.rows.cells.linksOutToCells.columnId` (number)
    Column ID of the linked cell.

  - `sheets.rows.cells.linksOutToCells.rowId` (number)
    Row ID of the linked cell.

  - `sheets.rows.cells.linksOutToCells.sheetId` (number)
    Sheet ID of the sheet that the linked cell belongs to.

  - `sheets.rows.cells.linksOutToCells.sheetName` (string)
    Sheet name of the linked cell.

  - `sheets.rows.cells.linksOutToCells.status` (string)
    * BLOCKED One of several other values indicating unusual error conditions.
* BROKEN The row or sheet linked to was deleted.
* CIRCULAR One of several other values indicating unusual error conditions.
* DISABLED One of several other values indicating unusual error conditions.
* INACCESSIBLE The sheet linked to cannot be viewed by this user.
* INVALID One of several other values indicating unusual error conditions.
* NOT_SHARED One of several other values indicating unusual error conditions.
* OK The link is in a good state.
    Enum: "BLOCKED", "BROKEN", "CIRCULAR", "DISABLED", "INACCESSIBLE", "INVALID", "NOT_SHARED", "OK"

  - `sheets.rows.cells.objectValue` (any)

  - `sheets.rows.cells.overrideValidation` (boolean)
    (Admin only) Indicates whether the cell value can contain a value outside of the validation limits (value = true). When using this parameter, you must also set strict to false to bypass value type checking. This property is honored for POST or PUT actions that update rows.

  - `sheets.rows.cells.strict` (boolean)
    Set to false to enable lenient parsing. Defaults to true. You can specify this attribute in a request, but it is never present in a response.

  - `sheets.rows.cells.value` (any)
    A string, number, or a Boolean value -- depending on the cell type and the data in the cell. Cell values larger than 4000 characters are silently truncated. An empty cell returns no value.

  - `sheets.rows.columns` (array)
    Columns of row. Only returned if the include query string parameter contains columns.

  - `sheets.rows.conditionalFormat` (string)
    Describes this row's conditional format. Only returned if the include query string parameter contains format and this row has a conditional format applied.
    Example: ",,1,1,,,,,,,,,,,,,"

  - `sheets.rows.createdAt` (any)

  - `sheets.rows.createdBy` (object)
    User object containing name and email of the creator of this row.

  - `sheets.rows.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `sheets.rows.createdBy.name` (string)
    Example: "Jane Doe"

  - `sheets.rows.discussions` (array)
    Discussions on the row. Only returned if the include query string parameter contains discussions.

  - `sheets.rows.discussions.accessLevel` (string)
    Enum: "ADMIN", "COMMENTER", "EDITOR", "EDITOR_SHARE", "OWNER", "VIEWER"

  - `sheets.rows.discussions.id` (number)
    Discussion ID.

  - `sheets.rows.discussions.comments` (array)
    Array of comments in discussion. Only returned if the include query string parameter contains comments.

  - `sheets.rows.discussions.comments.attachments` (array)
    Array of attachments on comments.

  - `sheets.rows.discussions.comments.attachments.id` (number)
    Attachment ID.

  - `sheets.rows.discussions.comments.attachments.parentId` (number)
    The ID of the parent.

  - `sheets.rows.discussions.comments.attachments.attachmentType` (string)
    Attachment type. Note--Dropbox, Egnyte, and Evernote are not supported for Smartsheet.gov accounts.
    Enum: "BOX_COM", "DROPBOX", "EGNYTE", "EVERNOTE", "FILE", "GOOGLE_DRIVE", "LINK", "ONEDRIVE", "TRELLO"

  - `sheets.rows.discussions.comments.attachments.attachmentSubType` (string)
    Attachment sub type. Note--Folder type is for EGNYTE values and the rest are GOOGLE_DRIVE values.
    Enum: "DOCUMENT", "DRAWING", "FOLDER", "PDF", "PRESENTATION", "SPREADSHEET"

  - `sheets.rows.discussions.comments.attachments.mimeType` (string)
    Attachment MIME type.
    Example: "PNG"

  - `sheets.rows.discussions.comments.attachments.parentType` (string)
    The type of object the attachment belongs to.
    Enum: "COMMENT", "PROOF", "ROW", "SHEET"

  - `sheets.rows.discussions.comments.attachments.createdAt` (any)

  - `sheets.rows.discussions.comments.attachments.createdBy` (object)
    User object containing name and email of the user who created this attachment.

  - `sheets.rows.discussions.comments.attachments.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `sheets.rows.discussions.comments.attachments.createdBy.name` (string)
    Example: "Jane Doe"

  - `sheets.rows.discussions.comments.attachments.name` (string)
    Attachment name.

  - `sheets.rows.discussions.comments.attachments.sizeInKb` (number)
    The size of the file, if the attachmentType is FILE.

  - `sheets.rows.discussions.comments.attachments.url` (string)
    Attachment temporary URL (files only).

  - `sheets.rows.discussions.comments.attachments.urlExpiresInMillis` (number)
    Attachment temporary URL time to live (files only).

  - `sheets.rows.discussions.comments.createdAt` (any)

  - `sheets.rows.discussions.comments.createdBy` (object)
    User object containing name and email of the creator of this comment.

  - `sheets.rows.discussions.comments.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `sheets.rows.discussions.comments.createdBy.name` (string)
    Example: "Jane Doe"

  - `sheets.rows.discussions.comments.discussionId` (number)
    Discussion ID of discussion that contains comment.

  - `sheets.rows.discussions.comments.id` (number)
    Comment ID.

  - `sheets.rows.discussions.comments.modifiedAt` (any)

  - `sheets.rows.discussions.comments.text` (string)
    Comment body.

  - `sheets.rows.discussions.commentAttachments` (array)
    Array of attachments on discussion comments. Only returned if the include query string parameter contains attachments.

  - `sheets.rows.discussions.commentAttachments.id` (number)
    Attachment ID.

  - `sheets.rows.discussions.commentAttachments.parentId` (number)
    The ID of the parent.

  - `sheets.rows.discussions.commentAttachments.attachmentType` (string)
    Attachment type. Note--Dropbox, Egnyte, and Evernote are not supported for Smartsheet.gov accounts.
    Enum: "BOX_COM", "DROPBOX", "EGNYTE", "EVERNOTE", "FILE", "GOOGLE_DRIVE", "LINK", "ONEDRIVE", "TRELLO"

  - `sheets.rows.discussions.commentAttachments.attachmentSubType` (string)
    Attachment sub type. Note--Folder type is for EGNYTE values and the rest are GOOGLE_DRIVE values.
    Enum: "DOCUMENT", "DRAWING", "FOLDER", "PDF", "PRESENTATION", "SPREADSHEET"

  - `sheets.rows.discussions.commentAttachments.mimeType` (string)
    Attachment MIME type.
    Example: "PNG"

  - `sheets.rows.discussions.commentAttachments.parentType` (string)
    The type of object the attachment belongs to.
    Enum: "COMMENT", "PROOF", "ROW", "SHEET"

  - `sheets.rows.discussions.commentAttachments.createdAt` (any)

  - `sheets.rows.discussions.commentAttachments.createdBy` (object)
    User object containing name and email of the user who created this attachment.

  - `sheets.rows.discussions.commentAttachments.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `sheets.rows.discussions.commentAttachments.createdBy.name` (string)
    Example: "Jane Doe"

  - `sheets.rows.discussions.commentAttachments.name` (string)
    Attachment name.

  - `sheets.rows.discussions.commentAttachments.sizeInKb` (number)
    The size of the file, if the attachmentType is FILE.

  - `sheets.rows.discussions.commentAttachments.url` (string)
    Attachment temporary URL (files only).

  - `sheets.rows.discussions.commentAttachments.urlExpiresInMillis` (number)
    Attachment temporary URL time to live (files only).

  - `sheets.rows.discussions.commentCount` (number)
    Number of comments in the discussion.

  - `sheets.rows.discussions.createdBy` (object)
    User object containing name and email of the user who created the discussion.

  - `sheets.rows.discussions.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `sheets.rows.discussions.createdBy.name` (string)
    Example: "Jane Doe"

  - `sheets.rows.discussions.lastCommentedAt` (any)

  - `sheets.rows.discussions.lastCommentedUser` (object)
    User object containing name and email of the user who last commented on the discussion.

  - `sheets.rows.discussions.lastCommentedUser.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `sheets.rows.discussions.lastCommentedUser.name` (string)
    Example: "Jane Doe"

  - `sheets.rows.discussions.parentId` (number)
    The ID of the associated row or sheet.

  - `sheets.rows.discussions.parentType` (string)
    Type of parent object.
    Enum: "ROW", "SHEET"

  - `sheets.rows.discussions.readOnly` (boolean)
    Indicates whether the user can modify the discussion.

  - `sheets.rows.discussions.title` (string)
    Title automatically created by duplicating the first 100 characters of top-level comment.

  - `sheets.rows.proof` (object)
    Object containing zero or more media items, including images, videos, and documents, for review, editing, or approval.

  - `sheets.rows.proof.id` (number)
    Proof ID of the proof version.

  - `sheets.rows.proof.originalId` (number)
    Proof ID of the original proof version.

  - `sheets.rows.proof.name` (string)
    Proof name. This is the same as primary column value. If the primary column value is empty, name is empty.

  - `sheets.rows.proof.type` (string)
    File type for the proof version.
    Enum: "DOCUMENT", "IMAGE", "MIXED", "NONE", "VIDEO"

  - `sheets.rows.proof.documentType` (string)
    If type=DOCUMENT, then this indicates the type of file, such as PDF.

  - `sheets.rows.proof.proofRequestUrl` (string)
    URL to review a proofing request.

  - `sheets.rows.proof.version` (number)
    The version number of the proof.

  - `sheets.rows.proof.lastUpdatedAt` (any)

  - `sheets.rows.proof.lastUpdatedBy` (object)
    User object containing name and email of the user who last updated the proof.

  - `sheets.rows.proof.lastUpdatedBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `sheets.rows.proof.lastUpdatedBy.name` (string)
    Example: "Jane Doe"

  - `sheets.rows.proof.isCompleted` (boolean)
    Indicates whether the proof is completed.

  - `sheets.rows.proof.attachments` (array)
    Array of Attachment objects. Only returned if the include query string parameter contains attachments.

  - `sheets.rows.proof.attachments.id` (number)
    Attachment ID.

  - `sheets.rows.proof.attachments.parentId` (number)
    The ID of the parent.

  - `sheets.rows.proof.attachments.attachmentType` (string)
    Attachment type. Note--Dropbox, Egnyte, and Evernote are not supported for Smartsheet.gov accounts.
    Enum: "BOX_COM", "DROPBOX", "EGNYTE", "EVERNOTE", "FILE", "GOOGLE_DRIVE", "LINK", "ONEDRIVE", "TRELLO"

  - `sheets.rows.proof.attachments.attachmentSubType` (string)
    Attachment sub type. Note--Folder type is for EGNYTE values and the rest are GOOGLE_DRIVE values.
    Enum: "DOCUMENT", "DRAWING", "FOLDER", "PDF", "PRESENTATION", "SPREADSHEET"

  - `sheets.rows.proof.attachments.mimeType` (string)
    Attachment MIME type.
    Example: "PNG"

  - `sheets.rows.proof.attachments.parentType` (string)
    The type of object the attachment belongs to.
    Enum: "COMMENT", "PROOF", "ROW", "SHEET"

  - `sheets.rows.proof.attachments.createdAt` (any)

  - `sheets.rows.proof.attachments.createdBy` (object)
    User object containing name and email of the user who created this attachment.

  - `sheets.rows.proof.attachments.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `sheets.rows.proof.attachments.createdBy.name` (string)
    Example: "Jane Doe"

  - `sheets.rows.proof.attachments.name` (string)
    Attachment name.

  - `sheets.rows.proof.attachments.sizeInKb` (number)
    The size of the file, if the attachmentType is FILE.

  - `sheets.rows.proof.attachments.url` (string)
    Attachment temporary URL (files only).

  - `sheets.rows.proof.attachments.urlExpiresInMillis` (number)
    Attachment temporary URL time to live (files only).

  - `sheets.rows.proof.discussions` (array)
    Array of Discussion objects. Only returned if the include query string parameter contains discussions.

  - `sheets.rows.proof.discussions.accessLevel` (string)
    Enum: "ADMIN", "COMMENTER", "EDITOR", "EDITOR_SHARE", "OWNER", "VIEWER"

  - `sheets.rows.proof.discussions.id` (number)
    Discussion ID.

  - `sheets.rows.proof.discussions.comments` (array)
    Array of comments in discussion. Only returned if the include query string parameter contains comments.

  - `sheets.rows.proof.discussions.comments.attachments` (array)
    Array of attachments on comments.

  - `sheets.rows.proof.discussions.comments.attachments.id` (number)
    Attachment ID.

  - `sheets.rows.proof.discussions.comments.attachments.parentId` (number)
    The ID of the parent.

  - `sheets.rows.proof.discussions.comments.attachments.attachmentType` (string)
    Attachment type. Note--Dropbox, Egnyte, and Evernote are not supported for Smartsheet.gov accounts.
    Enum: "BOX_COM", "DROPBOX", "EGNYTE", "EVERNOTE", "FILE", "GOOGLE_DRIVE", "LINK", "ONEDRIVE", "TRELLO"

  - `sheets.rows.proof.discussions.comments.attachments.attachmentSubType` (string)
    Attachment sub type. Note--Folder type is for EGNYTE values and the rest are GOOGLE_DRIVE values.
    Enum: "DOCUMENT", "DRAWING", "FOLDER", "PDF", "PRESENTATION", "SPREADSHEET"

  - `sheets.rows.proof.discussions.comments.attachments.mimeType` (string)
    Attachment MIME type.
    Example: "PNG"

  - `sheets.rows.proof.discussions.comments.attachments.parentType` (string)
    The type of object the attachment belongs to.
    Enum: "COMMENT", "PROOF", "ROW", "SHEET"

  - `sheets.rows.proof.discussions.comments.attachments.createdAt` (any)

  - `sheets.rows.proof.discussions.comments.attachments.createdBy` (object)
    User object containing name and email of the user who created this attachment.

  - `sheets.rows.proof.discussions.comments.attachments.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `sheets.rows.proof.discussions.comments.attachments.createdBy.name` (string)
    Example: "Jane Doe"

  - `sheets.rows.proof.discussions.comments.attachments.name` (string)
    Attachment name.

  - `sheets.rows.proof.discussions.comments.attachments.sizeInKb` (number)
    The size of the file, if the attachmentType is FILE.

  - `sheets.rows.proof.discussions.comments.attachments.url` (string)
    Attachment temporary URL (files only).

  - `sheets.rows.proof.discussions.comments.attachments.urlExpiresInMillis` (number)
    Attachment temporary URL time to live (files only).

  - `sheets.rows.proof.discussions.comments.createdAt` (any)

  - `sheets.rows.proof.discussions.comments.createdBy` (object)
    User object containing name and email of the creator of this comment.

  - `sheets.rows.proof.discussions.comments.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `sheets.rows.proof.discussions.comments.createdBy.name` (string)
    Example: "Jane Doe"

  - `sheets.rows.proof.discussions.comments.discussionId` (number)
    Discussion ID of discussion that contains comment.

  - `sheets.rows.proof.discussions.comments.id` (number)
    Comment ID.

  - `sheets.rows.proof.discussions.comments.modifiedAt` (any)

  - `sheets.rows.proof.discussions.comments.text` (string)
    Comment body.

  - `sheets.rows.proof.discussions.commentAttachments` (array)
    Array of attachments on discussion comments. Only returned if the include query string parameter contains attachments.

  - `sheets.rows.proof.discussions.commentAttachments.id` (number)
    Attachment ID.

  - `sheets.rows.proof.discussions.commentAttachments.parentId` (number)
    The ID of the parent.

  - `sheets.rows.proof.discussions.commentAttachments.attachmentType` (string)
    Attachment type. Note--Dropbox, Egnyte, and Evernote are not supported for Smartsheet.gov accounts.
    Enum: "BOX_COM", "DROPBOX", "EGNYTE", "EVERNOTE", "FILE", "GOOGLE_DRIVE", "LINK", "ONEDRIVE", "TRELLO"

  - `sheets.rows.proof.discussions.commentAttachments.attachmentSubType` (string)
    Attachment sub type. Note--Folder type is for EGNYTE values and the rest are GOOGLE_DRIVE values.
    Enum: "DOCUMENT", "DRAWING", "FOLDER", "PDF", "PRESENTATION", "SPREADSHEET"

  - `sheets.rows.proof.discussions.commentAttachments.mimeType` (string)
    Attachment MIME type.
    Example: "PNG"

  - `sheets.rows.proof.discussions.commentAttachments.parentType` (string)
    The type of object the attachment belongs to.
    Enum: "COMMENT", "PROOF", "ROW", "SHEET"

  - `sheets.rows.proof.discussions.commentAttachments.createdAt` (any)

  - `sheets.rows.proof.discussions.commentAttachments.createdBy` (object)
    User object containing name and email of the user who created this attachment.

  - `sheets.rows.proof.discussions.commentAttachments.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `sheets.rows.proof.discussions.commentAttachments.createdBy.name` (string)
    Example: "Jane Doe"

  - `sheets.rows.proof.discussions.commentAttachments.name` (string)
    Attachment name.

  - `sheets.rows.proof.discussions.commentAttachments.sizeInKb` (number)
    The size of the file, if the attachmentType is FILE.

  - `sheets.rows.proof.discussions.commentAttachments.url` (string)
    Attachment temporary URL (files only).

  - `sheets.rows.proof.discussions.commentAttachments.urlExpiresInMillis` (number)
    Attachment temporary URL time to live (files only).

  - `sheets.rows.proof.discussions.commentCount` (number)
    Number of comments in the discussion.

  - `sheets.rows.proof.discussions.createdBy` (object)
    User object containing name and email of the user who created the discussion.

  - `sheets.rows.proof.discussions.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `sheets.rows.proof.discussions.createdBy.name` (string)
    Example: "Jane Doe"

  - `sheets.rows.proof.discussions.lastCommentedAt` (any)

  - `sheets.rows.proof.discussions.lastCommentedUser` (object)
    User object containing name and email of the user who last commented on the discussion.

  - `sheets.rows.proof.discussions.lastCommentedUser.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `sheets.rows.proof.discussions.lastCommentedUser.name` (string)
    Example: "Jane Doe"

  - `sheets.rows.proof.discussions.parentId` (number)
    The ID of the associated row or sheet.

  - `sheets.rows.proof.discussions.parentType` (string)
    Type of parent object.
    Enum: "ROW", "SHEET"

  - `sheets.rows.proof.discussions.readOnly` (boolean)
    Indicates whether the user can modify the discussion.

  - `sheets.rows.proof.discussions.title` (string)
    Title automatically created by duplicating the first 100 characters of top-level comment.

  - `sheets.rows.expanded` (boolean)
    Indicates whether the row is expanded or collapsed.

  - `sheets.rows.filteredOut` (boolean)
    Indicates if the row is filtered out by a column filter. Only returned if the include query string parameter contains filters.

  - `sheets.rows.format` (string)
    Format descriptor. Only returned if the include query string parameter contains format and this row has a non-default format applied.
    Example: ",,1,1,,,,,,,,,,,,,"

  - `sheets.rows.inCriticalPath` (boolean)
    Only returned, with a value of true, if the sheet is a project sheet with dependencies enabled and this row is in the critical path.

  - `sheets.rows.locked` (boolean)
    Indicates whether the row is locked.

  - `sheets.rows.lockedForUser` (boolean)
    Indicates whether the row is locked for the requesting user.

  - `sheets.rows.modifiedAt` (any)

  - `sheets.rows.modifiedBy` (object)
    User object containing name and email of the last person to modify this row.

  - `sheets.rows.modifiedBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `sheets.rows.modifiedBy.name` (string)
    Example: "Jane Doe"

  - `sheets.rows.permaLink` (string)
    URL that represents a direct link to the row in Smartsheet. Only returned if the include query string parameter contains rowPermalink.

  - `sheets.rows.rowNumber` (number)
    Row number within the sheet.

  - `sheets.rows.version` (number)
    Sheet version number that is incremented every time a sheet is modified.

  - `sheets.showParentRowsForFilters` (boolean)
    Returned only if there are column filters on the sheet. Value = true if "show parent rows" is enabled for the filters.

  - `sheets.source` (object)

  - `sheets.source.id` (number)
    The ID of the dashboard, report, sheet, or template from which the enclosing dashboard, report, sheet, or template was created.

  - `sheets.source.type` (string)
    report, sheet, sight (aka dashboard), or template.

  - `sheets.summary` (object)
    Represents the entire summary, or a list of defined fields and values, for a specific sheet.

  - `sheets.summary.fields` (array)
    Array of summary (or metadata) fields defined on the sheet.

  - `sheets.summary.fields.id` (number)
    SummaryField ID.

  - `sheets.summary.fields.contactOptions` (array)
    Array of ContactOption objects to specify a pre-defined list of values for the column. Column type must be CONTACT_LIST.

  - `sheets.summary.fields.contactOptions.email` (string)
    A parsable email address.

  - `sheets.summary.fields.contactOptions.name` (string)
    Can be a user's name, display name, or free text.

  - `sheets.summary.fields.createdAt` (any)

  - `sheets.summary.fields.createdBy` (object)
    User object containing name and email of the creator of this summary field.

  - `sheets.summary.fields.createdBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `sheets.summary.fields.createdBy.name` (string)
    Example: "Jane Doe"

  - `sheets.summary.fields.displayValue` (string)
    Visual representation of cell contents, as presented to the user in the UI.

  - `sheets.summary.fields.format` (string)
    The format descriptor. Only returned if the include query string parameter contains format and this column has a non-default format applied to it.

  - `sheets.summary.fields.formula` (string)
    The formula for a cell, if set.

  - `sheets.summary.fields.hyperlink` (object)

  - `sheets.summary.fields.hyperlink.reportId` (number)
    If non-null, this hyperlink is a link to the report with this ID.

  - `sheets.summary.fields.hyperlink.sheetId` (number)
    If non-null, this hyperlink is a link to the sheet with this ID.

  - `sheets.summary.fields.hyperlink.sightId` (number)
    If non-null, this hyperlink is a link to the dashboard with this ID.

  - `sheets.summary.fields.hyperlink.url` (string)
    When the hyperlink is a URL link, this property contains the URL value. When the hyperlink is a dashboard/report/sheet link (that is, dashboardId, reportId, or sheetId is non-null), this property contains the permalink to the dashboard, report, or sheet.

  - `sheets.summary.fields.image` (object)

  - `sheets.summary.fields.image.altText` (string)
    Alternate text for the image.

  - `sheets.summary.fields.image.height` (number)
    Original height (in pixels) of the uploaded image.

  - `sheets.summary.fields.image.id` (string)
    Image ID.

  - `sheets.summary.fields.image.width` (number)
    Original width (in pixels) of the uploaded image.

  - `sheets.summary.fields.index` (number)
    Field index or position. This number is zero-based.

  - `sheets.summary.fields.locked` (boolean)
    Indicates whether the field is locked.

  - `sheets.summary.fields.lockedForUser` (boolean)
    Indicates whether the field is locked for the requesting user.

  - `sheets.summary.fields.modifiedAt` (any)

  - `sheets.summary.fields.modifiedBy` (object)
    User object containing name and email of the user who most recently modified this summary field.

  - `sheets.summary.fields.modifiedBy.email` (string)
    Example: "jane.doe@smartsheet.com"

  - `sheets.summary.fields.modifiedBy.name` (string)
    Example: "Jane Doe"

  - `sheets.summary.fields.objectValue` (any)

  - `sheets.summary.fields.options` (array)
    When applicable for PICKLIST column type. Array of the options available for the field.

  - `sheets.summary.fields.symbol` (string)
    When applicable for PICKLIST column type.

  - `sheets.summary.fields.title` (string)
    Arbitrary name, must be unique within summary.

  - `sheets.summary.fields.type` (string)
    Enum: "ABSTRACT_DATETIME", "CHECKBOX", "CONTACT_LIST", "DATE", "DATETIME", "DURATION", "MULTI_CONTACT_LIST", "MULTI_PICKLIST", "PICKLIST", "PREDECESSOR", "TEXT_NUMBER"

  - `sheets.summary.fields.validation` (boolean)
    Indicates whether summary field values are restricted to the type.

  - `sheets.totalRowCount` (number)
    The total number of rows in the sheet.

  - `sheets.userPermissions` (object)
    Describes the current user's editing permissions for a specific sheet.

  - `sheets.userPermissions.summaryPermissions` (string)
    One of:
  * ADMIN: full control over fields.
  * READ_DELETE: sheet is owned by an individual account that doesn't have summary capabilities. If a summary exists, the only possible operations are GET and DELETE fields.
  * READ_ONLY.
  * READ_WRITE: can edit values of existing fields, but not create or delete fields, nor modify field type.
    Enum: "ADMIN", "READ_DELETE", "READ_ONLY", "READ_WRITE"

  - `sheets.userSettings` (object)
    Represents individual user settings for a specific sheet. User settings may be updated even on sheets where the current user only has read access (for example, viewer permissions or a read-only sheet).

  - `sheets.userSettings.criticalPathEnabled` (boolean)
    Does this user have "Show Critical Path" turned on for this sheet? NOTE: This setting only has an effect on project sheets with dependencies enabled.

  - `sheets.userSettings.displaySummaryTasks` (boolean)
    Does this user have "Display Summary Tasks" turned on for this sheet? Applies only to sheets where "Calendar View" has been configured.

  - `sheets.version` (number)
    A number that is incremented every time a sheet is modified.

  - `sheets.workspace` (object)

  - `sheets.workspace.id` (number)
    Workspace ID.

  - `sheets.workspace.name` (string)
    Workspace name.

  - `sheets.workspace.accessLevel` (string)
    Enum: "ADMIN", "COMMENTER", "EDITOR", "EDITOR_SHARE", "OWNER", "VIEWER"

  - `sheets.workspace.permalink` (string)
    URL that represents a direct link to the workspace in Smartsheet.

  - `sheets.favorite` (boolean)
    Deprecated Returned only if the user has marked this sheet as a favorite in their Home tab (value = true).

  - `sights` (array)

  - `sights.backgroundColor` (string)
    The hex color, for instance #E6F5FE.

  - `sights.defaultWidgetBackgroundColor` (string)
    The hex color of the background color for all widgets except for title widgets on the dashboard, for instance #E6F5FEF4 or #E6F5FE.

  - `sights.columnCount` (number)
    Number of columns that the dashboard contains.

  - `sights.source` (object)

  - `sights.source.id` (number)
    The ID of the dashboard, report, sheet, or template from which the enclosing dashboard, report, sheet, or template was created.

  - `sights.source.type` (string)
    report, sheet, sight (aka dashboard), or template.

  - `sights.widgets` (array)

  - `sights.widgets.id` (number)
    Widget ID.

  - `sights.widgets.type` (string)
    Type of widget.
    Enum: "CHART", "GRIDGANTT", "IMAGE", "METRIC", "RICHTEXT", "SHEETSUMMARY", "SHORTCUT", "SHORTCUTICON", "SHORTCUTLIST", "TITLE", "WEBCONTENT"

  - `sights.widgets.contents` (any)
    The type of widget content depends on the value of widget.type.

  - `sights.widgets.height` (number)
    Number of rows that the widget occupies on the dashboard.

  - `sights.widgets.showTitle` (boolean)
    True indicates that the client should display the widget title. This is independent of the title string which may be null or empty.

  - `sights.widgets.showTitleIcon` (boolean)
    True indicates that the client should display the sheet icon in the widget title.

  - `sights.widgets.title` (string)
    Title of the widget.

  - `sights.widgets.titleFormat` (string)
    Title format descriptor (see [Cell formatting](/api/smartsheet/guides/advanced-topics/cell-formatting)).
    Example: ",,1,,,,,,,3,,,,,,1,"

  - `sights.widgets.titleFont` (string)
    List of supported fonts in Dashboards
    Enum: "Arial", "Courier", "Georgia", "Gill Sans", "Helvetica", "Luminari", "Monaco", "Tahoma", "Times New Roman", "Verdana"

  - `sights.widgets.version` (number)
    Widget version number.

  - `sights.widgets.viewMode` (number)
    Indicates the content layout. Must use a query parameter of level=2 to see this information.

  * 1 - centered
  * 2 - left aligned
    Enum: 1, 2

  - `sights.widgets.width` (number)
    Number of columns that the widget occupies on the dashboard.

  - `sights.widgets.xPosition` (number)
    X-coordinate of widget's position on the dashboard.

  - `sights.widgets.yPosition` (number)
    Y-coordinate of widget's position on the dashboard.

  - `sights.workspace` (object)
    A reference to the dashboard's workspace, if the dashboard is in a workspace; otherwise an empty value.
    Example: {"id":1234567890,"name":"Some Workspace"}

  - `sights.workspace.id` (number)
    Workspace ID.
    Example: 1234567890

  - `sights.workspace.name` (string)
    Workspace name.
    Example: "Some Workspace"

  - `sights.createdAt` (any)

  - `sights.modifiedAt` (any)

  - `sights.id` (number)
    Dashboard ID.

  - `sights.accessLevel` (string)
    Enum: "ADMIN", "COMMENTER", "EDITOR", "EDITOR_SHARE", "OWNER", "VIEWER"

  - `sights.permalink` (string)
    URL that represents a direct link to the dashboard in Smartsheet.

  - `sights.name` (string)
    Dashboard name.

  - `templates` (array)

  - `templates.id` (number)
    Template ID.

  - `templates.type` (string)
    Type of template. Only applicable to public templates.
    Enum: "report", "sheet"

  - `templates.accessLevel` (string)
    Enum: "ADMIN", "COMMENTER", "EDITOR", "EDITOR_SHARE", "OWNER", "VIEWER"

  - `templates.blank` (boolean)
    Indicates whether the template is blank. Only applicable to public templates.

  - `templates.categories` (array)
    Indicates whether the template is blank. Only applicable to public templates.

  - `templates.description` (string)
    Template description.

  - `templates.globalTemplate` (string)
    Type of global template. Only applicable to blank public templates.
    Enum: "BLANK_SHEET", "PROJECT_SHEET", "TASK_LIST"

  - `templates.image` (string)
    URL to the small preview image for this template. Only applicable to non-blank public templates.

  - `templates.largeImage` (string)
    URL to the large preview image for this template. Only applicable to non-blank public templates.

  - `templates.locale` (string)
    Locale of the template. Only applicable to public templates.
    Enum: "ar_AE", "ar_BH", "ar_DZ", "ar_EG", "ar_IQ", "ar_JO", "ar_KW", "ar_LB", "ar_LY", "ar_MA", "ar_OM", "ar_QA", "ar_SA", "ar_SD", "ar_SY", "ar_TN", "ar_YE", "be_BY", "bg_BG", "ca_ES", "cs_CZ", "da_DK", "de_AT", "de_CH", "de_DE", "de_LU", "el_CY", "el_GR", "en_AU", "en_CA", "en_GB", "en_IE", "en_IN", "en_MT", "en_NZ", "en_PH", "en_SG", "en_US", "en_ZA", "es_AR", "es_BO", "es_CL", "es_CO", "es_CR", "es_DO", "es_EC", "es_ES", "es_GT", "es_HN", "es_MX", "es_NI", "es_PA", "es_PE", "es_PR", "es_PY", "es_SV", "es_US", "es_UY", "es_VE", "et_EE", "fi_FI", "fr_BE", "fr_CA", "fr_CH", "fr_FR", "fr_LU", "ga_IE", "hi_US", "hr_HR", "hu_HU", "in_ID", "is_IS", "it_CH", "it_IT", "iw_IL", "ja_JP", "ko_KR", "lt_LT", "lv_LV", "mk_MK", "ms_MY", "mt_MT", "nl_BE", "nl_NL", "no_NO", "pl_PL", "pt_BR", "pt_PT", "ro_RO", "ru_RU", "sk_SK", "sl_SI", "sq_AL", "sr_BA", "sr_CS", "sv_SE", "th_US", "tr_TR", "uk_UA", "vi_VN", "zh_CN", "zh_HK", "zh_SG", "zh_TW"

  - `templates.name` (string)
    Type of global template.
    Example: "Awesome Project Template"

  - `templates.tags` (array)
    List of search tags for this template. Only applicable to non-blank public templates.

## Response default fields (application/json):

  - `refId` (string)
    The ID of the specific error occurrence. Please include this information when contacting Smartsheet support.

  - `errorCode` (number)
    Custom error code from Smartsheet. See the complete [Error Code List](/api/smartsheet/error-codes).

  - `message` (string)
    Descriptive error message.


