# Invoices

Invoices provides information about customers' accounts for invoices, for examples, dates, status, and amounts. 

For more information about invoices, see <a href="https://knowledgecenter.zuora.com/Billing/Billing_and_Payments/IA_Invoices/A1_Invoice_Introduction" target="_blank">Invoice</a>.


## Create a standalone invoice

 - [POST /v1/invoices](https://developer.zuora.com/v1-api-reference/api/invoices/post_standaloneinvoice.md): Creates a standalone invoice for selling physical goods, services or other items on a non-recurring basis to your subscription customers.

To use this operation, you must have the Modify Invoice and at least one of the Create Standalone Invoice With Product Catalog or Create Standalone Invoice Without Product Catalog user permissions.
See Billing Roles for more information.

## Update invoices

 - [PUT /v1/invoices](https://developer.zuora.com/v1-api-reference/api/invoices/put_batchupdateinvoices.md): Updates multiple invoices in batches with one call. The following tutorials demonstrate how to use this operation:
  - Add and delete invoice items of draft standalone invoices
  - Edit due dates of draft standalone invoices
  - Edit invoice item prices and custom fields of draft standalone invoices
  

### Limitations


  - You can update a maximum of 50 invoices by one call.

## Create standalone invoices

 - [POST /v1/invoices/batch](https://developer.zuora.com/v1-api-reference/api/invoices/post_standaloneinvoices.md): Creates multiple standalone invoices for selling physical goods, services or other items on a non-recurring basis to your subscription customers.


To use this operation, you must have the Modify Invoice and at least one of the Create Standalone Invoice With Product Catalog or Create Standalone Invoice Without Product Catalog user permissions.
See Billing Roles for more information.

### Limitations

This operation has the following limitations:

* You can create a maximum of 50 invoices in one request.

* You can create a maximum of 1,000 invoice items in one request.

## Post invoices

 - [POST /v1/invoices/bulk-post](https://developer.zuora.com/v1-api-reference/api/invoices/post_postinvoices.md): Posts multiple invoices.

You can post a maximum of 50 invoices in one single request. Additionally, you can also update invoice dates while posting the invoices.
Note : This operation is synchronous and invoices within the bulk request are posted one by one.  The maximum batch size depends on the posting performance, which varies with invoice complexity and integrations with external tax engines.

## Retrieve the PDF file generation status of invoices

 - [GET /v1/invoices/pdf-status](https://developer.zuora.com/v1-api-reference/api/invoices/getinvoicepdfstatus.md): Retrieves the PDF generation statuses of a batch of invoices.

## Delete an invoice

 - [DELETE /v1/invoices/{invoiceKey}](https://developer.zuora.com/v1-api-reference/api/invoices/delete_deleteinvoice.md): Deletes a specific invoice.

Whether to delete an invoice synchronously or asynchronously depends on the number of invoice items contained in the invoice. By default, if an invoice contains less than 100 items, the invoice is deleted synchronously. Otherwise, the invoice is deleted asynchronously. If you want to change the threshold, submit a request at Zuora Global Support.

## Retrieve an invoice

 - [GET /v1/invoices/{invoiceKey}](https://developer.zuora.com/v1-api-reference/api/invoices/get_getinvoice.md): Retrieves a specific invoice.

## Update an invoice

 - [PUT /v1/invoices/{invoiceKey}](https://developer.zuora.com/v1-api-reference/api/invoices/put_updateinvoice.md): Updates a specific invoice.
The following tutorials demonstrate how to use this operation:
  - Add and delete invoice items of draft standalone invoices
  - Edit due dates of draft standalone invoices
  - Edit invoice item prices and custom fields of draft standalone invoices

## List all application parts of an invoice

 - [GET /v1/invoices/{invoiceKey}/application-parts](https://developer.zuora.com/v1-api-reference/api/invoices/get_invoiceapplicationparts.md): Note: This operation is only available if you have Invoice Settlement
enabled. The Invoice Settlement feature is generally available as of Zuora Billing
Release 296 (March 2021). This feature includes Unapplied Payments, Credit and
Debit Memo, and Invoice Item Settlement. If you want to enable Invoice Settlement,
see Invoice Settlement Enablement and Checklist Guide
for more information.

If you are in Zuora version 341, this operation will return only processed payments applied to the invoices. If you are in the Zuora version less than 341, this operation behavior remains the same and returns all payments associated with the invoice regardless of the payment status.

Retrieves information about the payments or credit memos that are applied to a
specified invoice.

## Email an invoice

 - [POST /v1/invoices/{invoiceKey}/emails](https://developer.zuora.com/v1-api-reference/api/invoices/post_emailinvoice.md): Sends a posted invoice to the specified email addresses manually.
### Notes
  - You must activate the Manual Email For Invoice | Manual Email For Invoice notification before emailing invoices. To include the invoice PDF in the email, select the Include Invoice PDF check box in the Edit notification dialog from the Zuora UI. See Create and Edit Notifications for more information.

  - Zuora sends the email messages based on the email template you set. You can set the email template to use in the Delivery Options panel of the Edit notification dialog from the Zuora UI. By default, the Invoice Posted Default Email Template template is used. See Create and Edit Email Templates for more information.

  - The invoices are sent only to the work email addresses or personal email addresses of the Bill To contact if the following conditions are all met:
    * The useEmailTemplateSetting field is set to false.
    * The email addresses are not specified in the emailAddresses field.

## List all files of an invoice

 - [GET /v1/invoices/{invoiceKey}/files](https://developer.zuora.com/v1-api-reference/api/invoices/get_invoicefiles.md): Retrieves the information about all PDF files of a specified invoice. 

Invoice PDF files are returned in reverse chronological order by the value of the versionNumber field.
Note: This API only retrieves the PDF files that have been generated. If the latest PDF file is being generated, it will not be included in the response.
You can use the Query action to get the latest PDF file, for example: "select Body from Invoice where Id = '2c93808457d787030157e0324aea5158'".
See Query an Invoice Body for more information.

## Upload a file for an invoice

 - [POST /v1/invoices/{invoiceKey}/files](https://developer.zuora.com/v1-api-reference/api/invoices/post_uploadfileforinvoice.md): Uploads an externally generated invoice PDF file for an invoice that is in Draft or Posted status.
To use this operation, you must enable the Modify Invoice permission. See Billing Permissions for more information.
This operation has the following restrictions:
- Only the PDF file format is supported.
- The maximum size of the PDF file to upload is 4 MB.
- A maximum of 50 PDF files can be uploaded for one invoice.
- Ensure that each uploaded PDF file has a unique name. Duplicate filenames are not allowed when attaching files to an invoice.

## List all items of an invoice

 - [GET /v1/invoices/{invoiceKey}/items](https://developer.zuora.com/v1-api-reference/api/invoices/get_invoiceitems.md): Retrieves the information about all items of a specified invoice.

## List all taxation items of an invoice item

 - [GET /v1/invoices/{invoiceKey}/items/{itemId}/taxation-items](https://developer.zuora.com/v1-api-reference/api/invoices/get_taxationitemsofinvoiceitem.md): Retrieves information about the taxation items of a specific invoice item.

## Reverse an invoice

 - [PUT /v1/invoices/{invoiceKey}/reverse](https://developer.zuora.com/v1-api-reference/api/invoices/put_reverseinvoice.md): Note: This operation is only available if you have Invoice Settlement enabled. The Invoice Settlement feature is generally available as of Zuora Billing Release 296 (March 2021). This feature includes Unapplied Payments, Credit and Debit Memo, and Invoice Item Settlement. If you want to enable Invoice Settlement, see Invoice Settlement Enablement and Checklist Guide for more information.

Reverses a posted invoice. The reversal operation is performed asynchronously when the invoice contains more than 2,000 items in total. 

Restrictions

You are not allowed to reverse an invoice if any of the following restrictions is met:
* Payments and credit memos are applied to the invoice.
* The invoice is split.
* The invoice is not in Posted status.
* The total amount of the invoice is less than 0 (a negative invoice).
* Using Tax Connector for Extension Platform to calculate taxes.
* An invoice contains more than 50,000 items in total, including invoice items, discount items, and taxation items.

See Invoice Reversal for more information.

## Create taxation items for an invoice

 - [POST /v1/invoices/{invoiceKey}/taxation-items](https://developer.zuora.com/v1-api-reference/api/invoices/post_inv_taxationitems.md): Creates taxation items for an invoice.

## Write off an invoice

 - [PUT /v1/invoices/{invoiceKey}/write-off](https://developer.zuora.com/v1-api-reference/api/invoices/put_writeoffinvoice.md): Note: This operation is only available if you have Invoice Settlement enabled. The Invoice Settlement feature is generally available as of Zuora Billing Release 296 (March 2021). This feature includes Unapplied Payments, Credit and Debit Memo, and Invoice Item Settlement. If you want to enable Invoice Settlement, see Invoice Settlement Enablement and Checklist Guide for more information.

Writes off a posted invoice. 

By writing off an invoice, a credit memo is created and applied to the invoice. The generated credit memo items and credit memo taxation items are applied to invoice items and invoice taxation items based on the configured default application rule. If an invoice is written off, the balance of each invoice item and invoice taxation item must be zero.

If you set the Create credit memos mirroring invoice items billing rule to Yes, you can write off an invoice even if all its items have zero balance.

Restrictions: You cannot write off an invoice if any of the following restrictions is met:
* The balance of an invoice has been changed before Invoice Settlement is enabled.
  For example, before Invoice Settlement is enabled, any credit balance adjustments, invoice item adjustments, or invoice adjustments have been applied to an invoice.
* An invoice contains more than 2,000 items in total, including invoice items, discount items, and taxation items.
See Invoice Write-off for more information.

