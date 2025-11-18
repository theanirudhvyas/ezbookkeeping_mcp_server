# EzBookkeeping API Documentation

## Overview

EzBookkeeping is a self-hosted personal bookkeeping application with a comprehensive RESTful HTTP API. The API uses token-based authentication and provides endpoints for managing users, accounts, transactions, categories, tags, and more.

**Base URL:** `https://your-instance.com/api`

**API Version:** v1 (most endpoints under `/api/v1/`)

## Authentication

All API requests (except registration and login) require authentication via Bearer token in the Authorization header:

```http
Authorization: Bearer ${TOKEN}
```

### Authentication Requirements
- Tokens must be enabled via configuration (`enable_api_token`) or environment variables
- Generate tokens through the UI, CLI, or API endpoints
- Multiple token types supported: API tokens, MCP tokens, session tokens

### Response Format

**Success Response:**
```json
{
    "success": true,
    "result": {}
}
```

**Error Response:**
```json
{
    "success": false,
    "errorCode": 0,
    "errorMessage": "error details",
    "path": "/api/v1/..."
}
```

---

## API Endpoints

### Authentication & Authorization

#### Login (Standard)
- **Path:** `POST /api/authorize.json`
- **Description:** Standard login with username/password credentials
- **Request Body:**
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Response:** `AuthResponse`
  - `token`: Authentication token
  - `need2FA`: Boolean indicating if 2FA is required
  - `user`: Basic user information
  - User settings and cloud settings

#### Two-Factor Authentication Login
- **Path:** `POST /api/2fa/authorize.json`
- **Description:** Complete 2FA authentication using TOTP passcode
- **Request Body:**
  ```json
  {
    "username": "string",
    "password": "string",
    "passcode": "string"
  }
  ```
- **Response:** `AuthResponse`

#### Two-Factor Authentication via Recovery Code
- **Path:** `POST /api/2fa/recovery.json`
- **Description:** Complete 2FA authentication using recovery code
- **Request Body:**
  ```json
  {
    "username": "string",
    "password": "string",
    "recoveryCode": "string"
  }
  ```
- **Response:** `AuthResponse`

#### OAuth2 Callback Authentication
- **Path:** `POST /api/oauth2/authorize.json`
- **Description:** Handle OAuth 2.0 callback authentication flow
- **Request Body:**
  ```json
  {
    "code": "string",
    "state": "string"
  }
  ```
- **Response:** `AuthResponse`

#### Logout
- **Path:** `GET /api/logout.json`
- **Description:** Revoke current authentication token
- **Response:** Boolean

---

### User Management

#### User Registration
- **Path:** `POST /api/register.json`
- **Description:** Create a new user account
- **Request Body:**
  ```json
  {
    "username": "string",
    "email": "string",
    "password": "string",
    "nickname": "string",
    "defaultCurrency": "USD"
  }
  ```
- **Response:** `RegisterResponse`

#### Verify Email (Unregistered User)
- **Path:** `POST /api/verify_email/resend.json`
- **Description:** Resend verification email for unregistered users
- **Request Body:**
  ```json
  {
    "email": "string"
  }
  ```
- **Response:** Boolean

#### Verify Email by Token
- **Path:** `POST /api/verify_email/by_token.json`
- **Description:** Verify user email using token from email
- **Request Body:**
  ```json
  {
    "token": "string"
  }
  ```
- **Response:** `UserVerifyEmailResponse`

#### Request Password Reset
- **Path:** `POST /api/forget_password/request.json`
- **Description:** Generate password reset link and send email
- **Request Body:**
  ```json
  {
    "email": "string"
  }
  ```
- **Response:** Boolean

#### Reset Password by Token
- **Path:** `POST /api/forget_password/reset/by_token.json`
- **Description:** Reset user password using token from email
- **Request Body:**
  ```json
  {
    "token": "string",
    "email": "string",
    "password": "string"
  }
  ```
- **Response:** Boolean

---

### User Profile (Authenticated)

#### Get User Profile
- **Path:** `GET /api/v1/users/profile/get.json`
- **Description:** Retrieve current user profile information
- **Response:** `UserProfileResponse`
  - User ID, username, email, nickname
  - Avatar, default currency
  - Transaction settings
  - Language preferences

#### Update User Profile
- **Path:** `POST /api/v1/users/profile/update.json`
- **Description:** Update user profile settings
- **Request Body:**
  ```json
  {
    "email": "string",
    "nickname": "string",
    "password": "string",
    "oldPassword": "string",
    "defaultCurrency": "USD",
    "firstDayOfWeek": 0
  }
  ```
- **Response:** `UserProfileUpdateResponse`

#### Update User Avatar
- **Path:** `POST /api/v1/users/avatar/update.json`
- **Description:** Upload new user avatar image
- **Request:** Multipart form data with `avatar` file field
- **Response:** `UserProfileResponse`

#### Remove User Avatar
- **Path:** `POST /api/v1/users/avatar/remove.json`
- **Description:** Delete user avatar
- **Response:** `UserProfileResponse`

#### Resend Verification Email (Logged In)
- **Path:** `POST /api/v1/users/verify_email/resend.json`
- **Description:** Send verification email for authenticated user
- **Response:** Boolean

#### Get User Avatar
- **Path:** `GET /api/v1/users/avatar/{fileName}`
- **Description:** Retrieve avatar image data
- **Response:** Binary image data with appropriate content-type

---

### Token Management

#### List Tokens
- **Path:** `GET /api/v1/tokens/list.json`
- **Description:** Retrieve all active tokens/sessions for current user
- **Response:** Array of `TokenInfoResponse`
  ```json
  [
    {
      "tokenId": "string",
      "tokenType": "string",
      "userAgent": "string",
      "lastSeen": 1234567890,
      "isCurrent": true
    }
  ]
  ```

#### Generate API Token
- **Path:** `POST /api/v1/tokens/generate/api.json`
- **Description:** Create new API token for programmatic access
- **Request Body:**
  ```json
  {
    "password": "string",
    "expiredInSeconds": 3600
  }
  ```
- **Response:**
  ```json
  {
    "token": "string",
    "apiBaseUrl": "https://..."
  }
  ```

#### Generate MCP Token
- **Path:** `POST /api/v1/tokens/generate/mcp.json`
- **Description:** Create new MCP (Model Context Protocol) token
- **Request Body:**
  ```json
  {
    "password": "string",
    "expiredInSeconds": 3600
  }
  ```
- **Response:**
  ```json
  {
    "token": "string",
    "mcpUrl": "https://..."
  }
  ```

#### Revoke Specific Token
- **Path:** `POST /api/v1/tokens/revoke.json`
- **Description:** Revoke a specific token by ID
- **Request Body:**
  ```json
  {
    "tokenId": "string"
  }
  ```
- **Response:** Boolean

#### Revoke All Other Tokens
- **Path:** `POST /api/v1/tokens/revoke_all.json`
- **Description:** Revoke all tokens except the current one
- **Response:** Boolean

#### Refresh Token
- **Path:** `POST /api/v1/tokens/refresh.json`
- **Description:** Refresh/renew current authentication token
- **Response:** `TokenRefreshResponse`
  - New token
  - Updated user information
  - Cloud settings
  - Notifications

---

### Two-Factor Authentication Management

#### Get 2FA Status
- **Path:** `GET /api/v1/users/2fa/status.json`
- **Description:** Check if 2FA is enabled for current user
- **Response:**
  ```json
  {
    "enable": true,
    "createdAt": 1234567890
  }
  ```

#### Request 2FA Enable
- **Path:** `POST /api/v1/users/2fa/enable/request.json`
- **Description:** Generate new 2FA secret and QR code for setup
- **Response:**
  ```json
  {
    "secret": "string",
    "qrCode": "data:image/png;base64,..."
  }
  ```

#### Confirm 2FA Enable
- **Path:** `POST /api/v1/users/2fa/enable/confirm.json`
- **Description:** Confirm and activate 2FA after passcode verification
- **Request Body:**
  ```json
  {
    "secret": "string",
    "passcode": "string"
  }
  ```
- **Response:**
  ```json
  {
    "token": "string",
    "recoveryCodes": ["code1", "code2", ...]
  }
  ```

#### Disable 2FA
- **Path:** `POST /api/v1/users/2fa/disable.json`
- **Description:** Disable two-factor authentication
- **Request Body:**
  ```json
  {
    "password": "string"
  }
  ```
- **Response:** Boolean

#### Regenerate Recovery Codes
- **Path:** `POST /api/v1/users/2fa/recovery/regenerate.json`
- **Description:** Generate fresh recovery codes (invalidates previous ones)
- **Request Body:**
  ```json
  {
    "password": "string"
  }
  ```
- **Response:**
  ```json
  {
    "recoveryCodes": ["code1", "code2", ...]
  }
  ```

---

### External Authentication

#### List External Authentications
- **Path:** `GET /api/v1/users/external_auth/list.json`
- **Description:** Get list of linked external authentication providers
- **Response:** Array of `UserExternalAuthInfoResponse`
  ```json
  [
    {
      "category": "string",
      "type": "string",
      "linked": true
    }
  ]
  ```

#### Unlink External Authentication
- **Path:** `POST /api/v1/users/external_auth/unlink.json`
- **Description:** Remove external authentication link
- **Request Body:**
  ```json
  {
    "password": "string",
    "type": "string"
  }
  ```
- **Response:** Boolean

---

### Cloud Application Settings

#### Get Cloud Settings
- **Path:** `GET /api/v1/users/settings/cloud/get.json`
- **Description:** Retrieve user's cloud application settings
- **Response:** Array of application settings or `false` if none exist

#### Update Cloud Settings
- **Path:** `POST /api/v1/users/settings/cloud/update.json`
- **Description:** Update user cloud application settings
- **Request Body:**
  ```json
  {
    "settings": [
      {
        "key": "string",
        "value": "string|number|boolean"
      }
    ],
    "fullUpdate": true
  }
  ```
- **Response:** Boolean

#### Disable Cloud Settings
- **Path:** `POST /api/v1/users/settings/cloud/disable.json`
- **Description:** Clear all cloud application settings
- **Response:** Boolean

---

### Account Management

#### List All Accounts
- **Path:** `GET /api/v1/accounts/list.json`
- **Description:** Get all accounts for the current user
- **Query Parameters:**
  - `visibleOnly` (optional): Filter by visibility
- **Response:** Array of `AccountInfoResponse`
  ```json
  [
    {
      "id": "string",
      "name": "string",
      "category": 1,
      "type": 1,
      "icon": "string",
      "color": "RRGGBB",
      "currency": "USD",
      "balance": 10000,
      "hidden": false,
      "subAccounts": []
    }
  ]
  ```

#### Get Single Account
- **Path:** `GET /api/v1/accounts/get.json`
- **Description:** Retrieve a specific account with sub-accounts
- **Query Parameters:**
  - `id`: Account ID
- **Response:** `AccountInfoResponse`

#### Create Account
- **Path:** `POST /api/v1/accounts/add.json`
- **Headers:**
  - `X-Timezone-Offset`: Timezone offset in minutes
- **Request Body:**
  ```json
  {
    "name": "string",
    "category": 1,
    "type": 1,
    "icon": "string",
    "color": "RRGGBB",
    "currency": "USD",
    "balance": 0,
    "balanceTime": 1234567890,
    "comment": "string",
    "creditCardStatementDate": 1,
    "subAccounts": [
      {
        "name": "string",
        "icon": "string",
        "color": "RRGGBB",
        "balance": 0
      }
    ]
  }
  ```
- **Response:** `AccountInfoResponse`

#### Modify Account
- **Path:** `POST /api/v1/accounts/modify.json`
- **Headers:**
  - `X-Timezone-Offset`: Timezone offset in minutes
- **Request Body:**
  ```json
  {
    "id": "string",
    "name": "string",
    "icon": "string",
    "color": "RRGGBB",
    "comment": "string",
    "hidden": false
  }
  ```
- **Response:** `AccountInfoResponse`

#### Hide/Show Account
- **Path:** `POST /api/v1/accounts/hide.json`
- **Description:** Toggle account visibility
- **Request Body:**
  ```json
  {
    "id": "string",
    "hidden": true
  }
  ```
- **Response:** Boolean

#### Move Account
- **Path:** `POST /api/v1/accounts/move.json`
- **Description:** Reorder account display positions
- **Request Body:**
  ```json
  {
    "newDisplayOrders": [
      {
        "id": "string",
        "displayOrder": 1
      }
    ]
  }
  ```
- **Response:** Boolean

#### Delete Account
- **Path:** `POST /api/v1/accounts/delete.json`
- **Description:** Permanently remove an account
- **Request Body:**
  ```json
  {
    "id": "string"
  }
  ```
- **Response:** Boolean

#### Delete Sub-Account
- **Path:** `POST /api/v1/accounts/sub_account/delete.json`
- **Description:** Remove a sub-account from parent
- **Request Body:**
  ```json
  {
    "id": "string"
  }
  ```
- **Response:** Boolean

---

### Transaction Categories

#### List Categories
- **Path:** `GET /api/v1/transaction/categories/list.json`
- **Description:** Get all transaction categories
- **Query Parameters:**
  - `type` (optional): Filter by category type (Income/Expense/Transfer)
  - `visibleOnly` (optional): Show only visible categories
- **Response:** Map organized by category type
  ```json
  {
    "Income": [
      {
        "id": "string",
        "name": "string",
        "type": 1,
        "parentId": "0",
        "icon": "string",
        "color": "RRGGBB",
        "comment": "string",
        "hidden": false,
        "subCategories": []
      }
    ],
    "Expense": [...],
    "Transfer": [...]
  }
  ```

#### Get Single Category
- **Path:** `GET /api/v1/transaction/categories/get.json`
- **Description:** Retrieve a specific category
- **Query Parameters:**
  - `id`: Category ID
- **Response:** `TransactionCategoryInfoResponse`

#### Create Category
- **Path:** `POST /api/v1/transaction/categories/add.json`
- **Request Body:**
  ```json
  {
    "name": "string",
    "type": 1,
    "parentId": "0",
    "icon": "string",
    "color": "RRGGBB",
    "comment": "string"
  }
  ```
- **Response:** `TransactionCategoryInfoResponse`

#### Create Categories in Batch
- **Path:** `POST /api/v1/transaction/categories/add_batch.json`
- **Request Body:**
  ```json
  {
    "categories": [
      {
        "name": "string",
        "type": 1,
        "icon": "string",
        "color": "RRGGBB"
      }
    ],
    "skipExisting": true
  }
  ```
- **Response:** Map of categories by type

#### Modify Category
- **Path:** `POST /api/v1/transaction/categories/modify.json`
- **Request Body:**
  ```json
  {
    "id": "string",
    "name": "string",
    "icon": "string",
    "color": "RRGGBB",
    "comment": "string"
  }
  ```
- **Response:** `TransactionCategoryInfoResponse`

#### Hide/Show Category
- **Path:** `POST /api/v1/transaction/categories/hide.json`
- **Request Body:**
  ```json
  {
    "id": "string",
    "hidden": true
  }
  ```
- **Response:** Boolean

#### Move Category
- **Path:** `POST /api/v1/transaction/categories/move.json`
- **Description:** Reorder category display positions
- **Request Body:**
  ```json
  {
    "newDisplayOrders": [
      {
        "id": "string",
        "displayOrder": 1
      }
    ]
  }
  ```
- **Response:** Boolean

#### Delete Category
- **Path:** `POST /api/v1/transaction/categories/delete.json`
- **Request Body:**
  ```json
  {
    "id": "string"
  }
  ```
- **Response:** Boolean

---

### Transaction Tags

#### List Tags
- **Path:** `GET /api/v1/transaction/tags/list.json`
- **Description:** Get all transaction tags for current user
- **Response:** Array of `TransactionTagInfoResponse`
  ```json
  [
    {
      "id": "string",
      "name": "string",
      "displayOrder": 1,
      "hidden": false
    }
  ]
  ```

#### Get Single Tag
- **Path:** `GET /api/v1/transaction/tags/get.json`
- **Query Parameters:**
  - `id`: Tag ID
- **Response:** `TransactionTagInfoResponse`

#### Create Tag
- **Path:** `POST /api/v1/transaction/tags/add.json`
- **Request Body:**
  ```json
  {
    "name": "string"
  }
  ```
- **Response:** `TransactionTagInfoResponse`

#### Create Tags in Batch
- **Path:** `POST /api/v1/transaction/tags/add_batch.json`
- **Request Body:**
  ```json
  {
    "tags": [
      {
        "name": "string"
      }
    ],
    "skipExisting": true
  }
  ```
- **Response:** Array of `TransactionTagInfoResponse`

#### Modify Tag
- **Path:** `POST /api/v1/transaction/tags/modify.json`
- **Request Body:**
  ```json
  {
    "id": "string",
    "name": "string"
  }
  ```
- **Response:** `TransactionTagInfoResponse`

#### Hide/Show Tag
- **Path:** `POST /api/v1/transaction/tags/hide.json`
- **Request Body:**
  ```json
  {
    "id": "string",
    "hidden": true
  }
  ```
- **Response:** Boolean

#### Move Tag
- **Path:** `POST /api/v1/transaction/tags/move.json`
- **Description:** Reorder tag display positions
- **Request Body:**
  ```json
  {
    "newDisplayOrders": [
      {
        "id": "string",
        "displayOrder": 1
      }
    ]
  }
  ```
- **Response:** Boolean

#### Delete Tag
- **Path:** `POST /api/v1/transaction/tags/delete.json`
- **Request Body:**
  ```json
  {
    "id": "string"
  }
  ```
- **Response:** Boolean

---

### Transactions

#### Count Transactions
- **Path:** `GET /api/v1/transactions/count.json`
- **Headers:**
  - `X-Timezone-Offset`: Timezone offset in minutes
- **Query Parameters:**
  - `type`: Transaction type filter
  - `categoryIds`: Comma-separated category IDs
  - `accountIds`: Comma-separated account IDs
  - `tagIds`: Comma-separated tag IDs
  - `keyword`: Search keyword
  - `maxTime`, `minTime`: Time range filters
- **Response:** `TransactionCountResponse`

#### List Transactions
- **Path:** `GET /api/v1/transactions/list.json`
- **Headers:**
  - `X-Timezone-Offset`: Timezone offset in minutes
- **Query Parameters:**
  - `count` (required, max 50): Number of results per page
  - `type`: Filter by transaction type
  - `category_ids`: Comma-separated category IDs
  - `account_ids`: Comma-separated account IDs
  - `tag_ids`: Comma-separated tag IDs
  - `tag_filter_type`: Tag filter mode (any/all)
  - `amount_filter`: Amount range filter
  - `keyword`: Search keyword
  - `max_time`, `min_time`: Time range (Unix timestamp)
  - `page`: Page number for pagination
  - `with_count`: Include total count
  - `with_pictures`: Include picture attachments
  - `trim_account`, `trim_category`, `trim_tag`: Minimize response data
- **Response:**
  ```json
  {
    "items": [
      {
        "id": "string",
        "type": 1,
        "categoryId": "string",
        "time": 1234567890,
        "sourceAccountId": "string",
        "sourceAmount": 10000,
        "destinationAccountId": "string",
        "destinationAmount": 10000,
        "hideAmount": false,
        "tagIds": ["tag1", "tag2"],
        "comment": "string",
        "geoLocation": {
          "latitude": 0.0,
          "longitude": 0.0
        }
      }
    ],
    "nextTimeSequenceId": "string",
    "totalCount": 100
  }
  ```

#### List Transactions by Month
- **Path:** `GET /api/v1/transactions/list/by_month.json`
- **Headers:**
  - `X-Timezone-Offset`: Timezone offset in minutes
- **Query Parameters:**
  - `year`, `month`: Target month
  - `type`, `categoryIds`, `accountIds`, `tagIds`: Filters
  - `page`: Page number
  - Other pagination options
- **Response:** `TransactionInfoPageWrapperResponse2`

#### Get Reconciliation Statement
- **Path:** `GET /api/v1/transactions/reconciliation_statements.json`
- **Headers:**
  - `X-Timezone-Offset`: Timezone offset in minutes
- **Query Parameters:**
  - `accountId`: Account to reconcile
  - `startTime`, `endTime`: Time range
- **Response:** `TransactionReconciliationStatementResponse`

#### Transaction Statistics
- **Path:** `GET /api/v1/transactions/statistics.json`
- **Headers:**
  - `X-Timezone-Offset`: Timezone offset in minutes
- **Query Parameters:**
  - `startTime`, `endTime`: Time range
  - `type`: Transaction type
  - `categoryIds`, `accountIds`, `tagIds`: Filters
- **Response:** `TransactionStatisticResponse`

#### Transaction Trends
- **Path:** `GET /api/v1/transactions/statistics/trends.json`
- **Headers:**
  - `X-Timezone-Offset`: Timezone offset in minutes
- **Query Parameters:**
  - `startTime`, `endTime`: Time range
  - `type`: Transaction type
  - `categoryIds`, `accountIds`, `tagIds`: Filters
  - `interval`: Time interval (day/week/month)
- **Response:** Array of `TransactionStatisticTrendsResponseItem`

#### Asset Trends
- **Path:** `GET /api/v1/transactions/statistics/asset_trends.json`
- **Headers:**
  - `X-Timezone-Offset`: Timezone offset in minutes
- **Query Parameters:**
  - `startTime`, `endTime`: Time range
  - `accountIds`: Specific accounts
  - `interval`: Time interval
- **Response:** Array of `TransactionStatisticAssetTrendsResponseItem`

#### Transaction Amounts
- **Path:** `GET /api/v1/transactions/amounts.json`
- **Headers:**
  - `X-Timezone-Offset`: Timezone offset in minutes
- **Query Parameters:**
  - Filtering options similar to list endpoint
- **Response:** Ordered map of `TransactionAmountsResponseItem`

#### Get Single Transaction
- **Path:** `GET /api/v1/transactions/get.json`
- **Headers:**
  - `X-Timezone-Offset`: Timezone offset in minutes
- **Query Parameters:**
  - `id`: Transaction ID
- **Response:** `TransactionInfoResponse`

#### Create Transaction
- **Path:** `POST /api/v1/transactions/add.json`
- **Headers:**
  - `X-Timezone-Offset`: Timezone offset in minutes
- **Request Body:**
  ```json
  {
    "type": 1,
    "categoryId": "string",
    "time": 1234567890,
    "utcOffset": 480,
    "sourceAccountId": "string",
    "sourceAmount": 10000,
    "destinationAccountId": "string",
    "destinationAmount": 10000,
    "hideAmount": false,
    "tagIds": ["tag1", "tag2"],
    "pictureIds": ["pic1"],
    "comment": "string",
    "geoLocation": {
      "latitude": 0.0,
      "longitude": 0.0
    }
  }
  ```
- **Response:** `TransactionInfoResponse`

#### Modify Transaction
- **Path:** `POST /api/v1/transactions/modify.json`
- **Headers:**
  - `X-Timezone-Offset`: Timezone offset in minutes
- **Request Body:**
  ```json
  {
    "id": "string",
    "categoryId": "string",
    "time": 1234567890,
    "sourceAccountId": "string",
    "sourceAmount": 10000,
    "destinationAccountId": "string",
    "destinationAmount": 10000,
    "tagIds": ["tag1"],
    "comment": "string"
  }
  ```
- **Response:** `TransactionInfoResponse`

#### Move Transactions Between Accounts
- **Path:** `POST /api/v1/transactions/move/all.json`
- **Description:** Move all transactions from one account to another
- **Request Body:**
  ```json
  {
    "fromAccountId": "string",
    "toAccountId": "string"
  }
  ```
- **Response:** Boolean

#### Delete Transaction
- **Path:** `POST /api/v1/transactions/delete.json`
- **Request Body:**
  ```json
  {
    "id": "string"
  }
  ```
- **Response:** Boolean

#### Parse DSV Import File
- **Path:** `POST /api/v1/transactions/parse_dsv_file.json`
- **Description:** Parse CSV/TSV file for transaction import
- **Request:** Multipart form data with file
- **Response:** Parsed DSV lines

#### Parse Import File
- **Path:** `POST /api/v1/transactions/parse_import.json`
- **Description:** Parse transaction import file
- **Request:** Multipart form data with file
- **Response:** `ImportTransactionResponsePageWrapper`

#### Import Transactions
- **Path:** `POST /api/v1/transactions/import.json`
- **Request Body:**
  ```json
  {
    "transactions": [...]
  }
  ```
- **Response:** Integer count of imported transactions

#### Get Import Process Status
- **Path:** `GET /api/v1/transactions/import/process.json`
- **Query Parameters:**
  - `processId`: Import process ID
- **Response:** Progress percentage or null

---

### Transaction Pictures

#### Upload Transaction Picture
- **Path:** `POST /api/v1/transaction/pictures/upload.json`
- **Description:** Upload receipt or transaction picture
- **Request:** Multipart form data
  - `picture`: Image file (required)
  - `clientSessionId`: Optional duplicate detection ID
- **Response:** `TransactionPictureInfo`
  ```json
  {
    "id": "string",
    "fileName": "string",
    "size": 12345,
    "uploadedAt": 1234567890
  }
  ```

#### Get Transaction Picture
- **Path:** `GET /api/v1/transaction/pictures/{fileName}`
- **Description:** Retrieve transaction picture data
- **Response:** Binary image data with content-type header

#### Remove Unused Picture
- **Path:** `POST /api/v1/transaction/pictures/remove_unused.json`
- **Description:** Delete uploaded picture not attached to any transaction
- **Request Body:**
  ```json
  {
    "id": "string"
  }
  ```
- **Response:** Boolean

---

### Transaction Templates

#### List Templates
- **Path:** `GET /api/v1/transaction/templates/list.json`
- **Description:** Get all transaction templates
- **Query Parameters:**
  - `type`: Filter by template type (normal/scheduled)
  - `visibleOnly`: Show only visible templates
- **Response:** Array of `TransactionTemplateInfoResponse`
  ```json
  [
    {
      "id": "string",
      "name": "string",
      "type": 1,
      "categoryId": "string",
      "sourceAccountId": "string",
      "sourceAmount": 10000,
      "destinationAccountId": "string",
      "destinationAmount": 10000,
      "tagIds": ["tag1"],
      "comment": "string",
      "frequency": "DAILY",
      "startDate": 1234567890,
      "endDate": 1234567890,
      "hidden": false
    }
  ]
  ```

#### Get Single Template
- **Path:** `GET /api/v1/transaction/templates/get.json`
- **Query Parameters:**
  - `id`: Template ID
- **Response:** `TransactionTemplateInfoResponse`

#### Create Template
- **Path:** `POST /api/v1/transaction/templates/add.json`
- **Request Body:**
  ```json
  {
    "name": "string",
    "type": 1,
    "categoryId": "string",
    "sourceAccountId": "string",
    "sourceAmount": 10000,
    "destinationAccountId": "string",
    "destinationAmount": 10000,
    "tagIds": ["tag1", "tag2"],
    "comment": "string",
    "frequency": "MONTHLY",
    "startDate": 1234567890,
    "endDate": 1234567890,
    "utcOffset": 480
  }
  ```
- **Validation:**
  - Maximum 10 tags per template
  - Scheduled templates require frequency and valid date range
- **Response:** `TransactionTemplateInfoResponse`

#### Modify Template
- **Path:** `POST /api/v1/transaction/templates/modify.json`
- **Request Body:**
  ```json
  {
    "id": "string",
    "name": "string",
    "categoryId": "string",
    "sourceAccountId": "string",
    "sourceAmount": 10000,
    "tagIds": ["tag1"]
  }
  ```
- **Response:** `TransactionTemplateInfoResponse`

#### Hide/Show Template
- **Path:** `POST /api/v1/transaction/templates/hide.json`
- **Request Body:**
  ```json
  {
    "id": "string",
    "hidden": true
  }
  ```
- **Response:** Boolean

#### Move Template
- **Path:** `POST /api/v1/transaction/templates/move.json`
- **Description:** Reorder template display positions
- **Request Body:**
  ```json
  {
    "newDisplayOrders": [
      {
        "id": "string",
        "displayOrder": 1
      }
    ]
  }
  ```
- **Response:** Boolean

#### Delete Template
- **Path:** `POST /api/v1/transaction/templates/delete.json`
- **Request Body:**
  ```json
  {
    "id": "string"
  }
  ```
- **Response:** Boolean

---

### Exchange Rates

#### Get Latest Exchange Rates
- **Path:** `GET /api/v1/exchange_rates/latest.json`
- **Description:** Retrieve latest exchange rate data
- **Response:** Exchange rate data object

#### Update User Custom Exchange Rate
- **Path:** `POST /api/v1/exchange_rates/user_custom/update.json`
- **Description:** Set custom exchange rate for a currency
- **Request Body:**
  ```json
  {
    "currency": "EUR",
    "rate": 1.18
  }
  ```
- **Response:** User custom exchange rate update response

#### Delete User Custom Exchange Rate
- **Path:** `POST /api/v1/exchange_rates/user_custom/delete.json`
- **Description:** Remove custom exchange rate
- **Request Body:**
  ```json
  {
    "currency": "EUR"
  }
  ```
- **Response:** Boolean

---

### Data Management

#### Get Data Statistics
- **Path:** `GET /api/v1/data/statistics.json`
- **Description:** Retrieve aggregated user data metrics
- **Response:** `DataStatisticsResponse`
  ```json
  {
    "totalAccountCount": 10,
    "totalCategoryCount": 25,
    "totalTagCount": 15,
    "totalTransactionCount": 1000,
    "totalPictureCount": 50,
    "totalTemplateCount": 5,
    "totalScheduledTransactionCount": 3
  }
  ```

#### Export Data to CSV
- **Path:** `GET /api/v1/data/export.csv`
- **Description:** Export all user data in CSV format
- **Query Parameters:** `ExportTransactionDataRequest`
- **Response:** CSV file download

#### Export Data to TSV
- **Path:** `GET /api/v1/data/export.tsv`
- **Description:** Export all user data in TSV format
- **Query Parameters:** `ExportTransactionDataRequest`
- **Response:** TSV file download

#### Clear All Data
- **Path:** `POST /api/v1/data/clear/all.json`
- **Description:** Delete all user data (requires password confirmation)
- **Request Body:**
  ```json
  {
    "password": "string"
  }
  ```
- **Response:** Boolean

#### Clear All Transactions
- **Path:** `POST /api/v1/data/clear/transactions.json`
- **Description:** Delete all transactions (requires password)
- **Request Body:**
  ```json
  {
    "password": "string"
  }
  ```
- **Response:** Boolean

#### Clear Transactions by Account
- **Path:** `POST /api/v1/data/clear/transactions/by_account.json`
- **Description:** Remove all transactions for specific account
- **Request Body:**
  ```json
  {
    "password": "string",
    "accountId": "string"
  }
  ```
- **Response:** Boolean

---

### Large Language Model (LLM)

#### Recognize Receipt Image
- **Path:** `POST /api/v1/llm/transactions/recognize_receipt_image.json`
- **Description:** Use AI to extract transaction details from receipt image
- **Request:** Multipart form data with image file
- **Response:** `RecognizedReceiptImageResponse`
  ```json
  {
    "type": 1,
    "categoryId": "string",
    "time": 1234567890,
    "sourceAmount": 10000,
    "sourceAccountId": "string",
    "destinationAmount": 10000,
    "destinationAccountId": "string",
    "tagIds": ["tag1"],
    "comment": "Extracted description"
  }
  ```

---

### System & Health

#### Get System Version
- **Path:** `GET /api/v1/systems/version.json`
- **Description:** Retrieve server version information
- **Response:**
  ```json
  {
    "version": "1.2.0",
    "commitHash": "abc123",
    "buildTime": "2025-01-15T10:00:00Z"
  }
  ```

#### Health Check
- **Path:** `GET /healthz.json`
- **Description:** Check service operational status
- **Response:**
  ```json
  {
    "status": "ok",
    "version": "1.2.0",
    "commit": "abc123"
  }
  ```

---

### OAuth2

#### OAuth2 Login
- **Path:** `GET /oauth2/login`
- **Description:** Initiate OAuth 2.0 authorization flow
- **Query Parameters:**
  - `platform`: "mobile" or "desktop"
  - `clientSessionId`: Client session identifier
  - `token` (optional): Existing user token for binding
- **Response:** Redirect to OAuth2 provider authorization endpoint

#### OAuth2 Callback
- **Path:** `GET /oauth2/callback`
- **Description:** Handle OAuth 2.0 provider callback
- **Query Parameters:**
  - `state`: State parameter for CSRF protection
  - `code`: Authorization code from provider
  - `error`, `errorDescription`: Provider error information
- **Response:** Redirect with authentication token or error

---

### QR Code

#### Mobile URL QR Code
- **Path:** `GET /qrcode/mobile_url.png`
- **Description:** Generate QR code for mobile app pairing
- **Response:** PNG image

---

### Model Context Protocol (MCP)

#### MCP JSON-RPC Endpoint
- **Path:** `POST /mcp`
- **Description:** MCP server endpoint for AI/LLM integration
- **Request:** JSON-RPC 2.0 requests
- **Response:** JSON-RPC 2.0 responses
- **Supported Methods:** Multiple MCP protocol methods

---

### Map Proxy Services

#### Map Tile Image Proxy
- **Path:** `GET /proxy/map/tile/*`
- **Description:** Proxy for map tile images
- **Response:** Binary image data

#### Map Annotation Image Proxy
- **Path:** `GET /proxy/map/annotation/*`
- **Description:** Proxy for map annotation images
- **Response:** Binary image data

#### Amap API Proxy
- **Path:** `GET /_AMapService/*`
- **Description:** Proxy for Amap (Gaode Maps) services
- **Response:** Proxied API response

---

## Data Types & Enumerations

### Account Categories
- `1` - Asset
- `2` - Liability
- `3` - Income
- `4` - Expense

### Account Types
- `1` - Cash
- `2` - Checking Account
- `3` - Savings Account
- `4` - Credit Card
- `5` - Debit Card
- `6` - Virtual Account
- `7` - Investment Account
- `8` - Debt/Loan
- `9` - Other

### Transaction Types
- `1` - Income (Modify Balance)
- `2` - Expense (Modify Balance)
- `3` - Transfer (Between Accounts)
- `4` - Balance Modification

### Category Types
- `1` - Income
- `2` - Expense
- `3` - Transfer

### Template Types
- `1` - Normal Template
- `2` - Scheduled Template

### Template Frequencies (for Scheduled Transactions)
- `DAILY`
- `WEEKLY`
- `MONTHLY`
- `YEARLY`

### Currency Codes
ISO 4217 currency codes (e.g., USD, EUR, GBP, JPY, CNY)

### Color Format
Hex RGB format without # prefix: `RRGGBB` (e.g., "FF5733")

### Timezone Offset
Minutes from UTC (e.g., 480 for UTC+8)

### Timestamp Format
Unix timestamp in milliseconds (e.g., 1234567890123)

---

## Common Headers

### Authentication
```http
Authorization: Bearer ${TOKEN}
```

### Timezone
```http
X-Timezone-Offset: 480
```
Value in minutes from UTC

---

## Error Codes

Common error codes returned in the `errorCode` field:

- Authentication errors
- Validation errors
- Permission errors
- Resource not found errors
- Database errors
- External service errors

Specific error codes and messages are returned in the `errorMessage` field.

---

## Rate Limiting

The API implements rate limiting for authentication endpoints to prevent brute force attacks. Failed login attempts are tracked and may result in temporary account lockouts.

---

## Pagination

List endpoints support pagination via:
- `page`: Page number (0-indexed)
- `count`: Items per page (max 50 for transactions)
- `with_count`: Include total count in response

Responses include:
- `items`: Array of results
- `totalCount`: Total number of items (if requested)
- `nextTimeSequenceId`: Cursor for next page (time-based pagination)

---

## Feature Flags & Configuration

Various features can be enabled/disabled via configuration:
- `enable_api_token`: Enable API token generation
- Email verification requirements
- SMTP for email notifications
- Two-factor authentication
- External authentication providers
- Cloud settings synchronization
- LLM integration for receipt recognition

---

## Source Code Reference

The API is implemented in Go and organized as follows:
- **Route Definitions:** `/cmd/webserver.go`
- **API Handlers:** `/pkg/api/*.go`
- **Data Models:** `/pkg/models/*.go`
- **Services:** `/pkg/services/*.go`
- **Database:** `/pkg/datastore/*.go`

**GitHub Repository:** https://github.com/mayswind/ezbookkeeping

---

## Notes

- The API is designed for self-hosted deployments
- Not all features may be enabled in all configurations
- Some endpoints require specific feature flags to be enabled
- The API is primarily designed for the official web and mobile clients
- Custom integrations are possible but not officially supported
- This documentation may not be comprehensive; refer to source code for complete details

---

**Document Version:** 1.0
**Last Updated:** 2025-01-19
**API Version:** v1
