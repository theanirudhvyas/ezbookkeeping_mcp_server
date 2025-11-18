# EzBookkeeping MCP Server - Design & Architecture

## Executive Summary

This document outlines the comprehensive design for an MCP server that integrates with EzBookkeeping's HTTP API, providing AI assistants with the ability to manage personal finances through natural language interactions.

## API Analysis Overview

The EzBookkeeping API provides **99 documented endpoints** across 16 functional categories:

### Core Categories
1. **Authentication & Authorization** (11 endpoints) - Login, OAuth2, 2FA, password reset
2. **User Management** (9 endpoints) - Profile, settings, avatar
3. **Token Management** (7 endpoints) - API tokens, MCP tokens, sessions
4. **Two-Factor Authentication** (5 endpoints) - Setup, enable/disable, recovery
5. **Account Management** (8 endpoints) - CRUD operations for financial accounts
6. **Transaction Categories** (8 endpoints) - CRUD operations for categories
7. **Transaction Tags** (8 endpoints) - CRUD operations for tags
8. **Transactions** (17 endpoints) - Full lifecycle + statistics/trends
9. **Transaction Pictures** (3 endpoints) - Receipt image management
10. **Transaction Templates** (7 endpoints) - Recurring transaction templates
11. **Exchange Rates** (3 endpoints) - Currency conversion management
12. **Data Management** (5 endpoints) - Statistics, export, bulk operations
13. **LLM Integration** (1 endpoint) - AI receipt recognition
14. **System & Utilities** (7 endpoints) - Health, version, proxies

## MCP Server Architecture

### 1. Tools (Write Operations - Side Effects)

Tools perform actions that modify state. Based on the API analysis:

#### Transaction Management Tools
- `add_transaction` - Create new transaction (POST /transactions/add.json)
- `update_transaction` - Modify existing transaction (POST /transactions/modify.json)
- `delete_transaction` - Remove transaction (POST /transactions/delete.json)
- `batch_delete_transactions` - Delete multiple transactions (POST /data-management/clear.json)
- `recognize_transaction_from_image` - AI-powered receipt parsing (POST /llm/parse-transaction-picture.json)

#### Account Management Tools
- `create_account` - Add new account (POST /accounts/add.json)
- `update_account` - Modify account details (POST /accounts/modify.json)
- `delete_account` - Remove account (POST /accounts/delete.json)
- `hide_account` - Hide account from views (POST /accounts/hide.json)
- `show_account` - Unhide account (POST /accounts/show.json)
- `update_account_display_orders` - Reorder accounts (POST /accounts/modify-display-orders.json)

#### Category Management Tools
- `create_category` - Add new category (POST /transaction-categories/add.json)
- `update_category` - Modify category (POST /transaction-categories/modify.json)
- `delete_category` - Remove category (POST /transaction-categories/delete.json)
- `batch_create_categories` - Create multiple categories (POST /transaction-categories/add-batch.json)

#### Tag Management Tools
- `create_tag` - Add new tag (POST /transaction-tags/add.json)
- `update_tag` - Modify tag (POST /transaction-tags/modify.json)
- `delete_tag` - Remove tag (POST /transaction-tags/delete.json)
- `batch_create_tags` - Create multiple tags (POST /transaction-tags/add-batch.json)

#### Template Management Tools
- `create_transaction_template` - Add template (POST /transaction-templates/add.json)
- `update_transaction_template` - Modify template (POST /transaction-templates/modify.json)
- `delete_transaction_template` - Remove template (POST /transaction-templates/delete.json)

#### Exchange Rate Tools
- `update_exchange_rates` - Update currency rates (POST /exchange-rates/update.json)
- `add_custom_exchange_rate` - Add custom rate (POST /exchange-rates/custom.json)

#### Data Export Tools
- `export_transactions` - Export to CSV/TSV (GET /data-management/export.json)

### 2. Resources (Read Operations - No Side Effects)

Resources expose data without modification. Template resources use URI parameters:

#### Account Resources
- `ezbookkeeping://accounts` - List all accounts (GET /accounts/list.json)
- `ezbookkeeping://accounts/{account_id}` - Get specific account details

#### Transaction Resources  
- `ezbookkeeping://transactions` - List transactions with filters (GET /transactions/list.json)
- `ezbookkeeping://transactions/{transaction_id}` - Get specific transaction
- `ezbookkeeping://transactions/month-totals` - Monthly statistics (GET /transactions/month-total-amount.json)
- `ezbookkeeping://transactions/trends/{period}` - Trend analysis (GET /transactions/trend-analysis.json)
- `ezbookkeeping://transactions/statistics` - Statistical overview (GET /data-management/statistics.json)

#### Category Resources
- `ezbookkeeping://categories` - List all categories (GET /transaction-categories/list.json)
- `ezbookkeeping://categories/{category_id}` - Get specific category
- `ezbookkeeping://categories/sub/{parent_id}` - Get subcategories (GET /transaction-categories/sub-list.json)

#### Tag Resources
- `ezbookkeeping://tags` - List all tags (GET /transaction-tags/list.json)
- `ezbookkeeping://tags/{tag_id}` - Get specific tag

#### Template Resources
- `ezbookkeeping://templates` - List all templates (GET /transaction-templates/list.json)
- `ezbookkeeping://templates/{template_id}` - Get specific template

#### Exchange Rate Resources
- `ezbookkeeping://exchange-rates/{date}` - Get rates for date (GET /exchange-rates/list.json)
- `ezbookkeeping://exchange-rates/latest` - Get latest rates (GET /exchange-rates/latest.json)

### 3. Prompts

Prompt templates for common financial queries:

- `analyze_spending` - Generate spending analysis prompts
- `budget_review` - Generate budget review prompts
- `financial_summary` - Generate summary report prompts
- `categorize_transaction` - Help categorize uncategorized transactions
- `detect_duplicate_transactions` - Identify potential duplicates

## Authentication Strategy

### Approach: Environment Variable + User Configuration

The MCP server will support multiple authentication methods:

#### Option 1: API Token (Recommended)
```python
# Configuration via environment variables
EZBOOKKEEPING_URL=https://your-instance.com
EZBOOKKEEPING_TOKEN=your_api_token_here
```

#### Option 2: Username/Password + Session Management
```python
# Server handles login and token refresh
EZBOOKKEEPING_URL=https://your-instance.com
EZBOOKKEEPING_USERNAME=username
EZBOOKKEEPING_PASSWORD=password
```

#### Option 3: MCP-Specific Token
EzBookkeeping supports dedicated MCP tokens (token type 5):
```bash
# Generate via CLI
ezbookkeeping user-session-new --type=mcp --user=username
```

### Implementation Details

1. **Token Storage:** Use environment variables or config file
2. **Token Refresh:** Implement automatic refresh for session tokens (POST /tokens/refresh.json)
3. **Error Handling:** Handle 401/403 errors gracefully
4. **Multi-User Support:** Allow configuration of multiple instances

## Technical Implementation Plan

### Phase 1: Core Foundation
1. Setup HTTP client with authentication
2. Implement token management and refresh
3. Create base API wrapper class
4. Add error handling and retry logic
5. Implement timezone handling (X-Timezone-Offset header)

### Phase 2: Essential Tools & Resources  
1. Transaction tools (add, update, delete)
2. Account resources (list, get)
3. Transaction resources (list, statistics)
4. Category/tag resources

### Phase 3: Advanced Features
1. Batch operations
2. Transaction templates
3. LLM receipt recognition integration
4. Export functionality
5. Exchange rate management

### Phase 4: Intelligence & Prompts
1. Spending analysis prompts
2. Budget tracking prompts
3. Financial insights generation
4. Duplicate detection
5. Category suggestions

## Data Model Mapping

### Key Entities

**Account Categories (AccountCategory enum)**
- 1: Cash
- 2: Checking Account
- 3: Credit Card
- 4: Virtual Account
- 5: Debt Account
- 6: Receivables
- 7: Investment Account
- 8: Savings Account
- 9: Certificate of Deposit

**Transaction Types (TransactionType enum)**
- 1: Modify Balance (Expense)
- 2: Modify Balance (Income)
- 3: Transfer Out
- 4: Transfer In

**Category Types (CategoryType enum)**
- 1: Expense Category
- 2: Income Category
- 3: Transfer Category

### Complex Operations

**Date Handling**
- All timestamps are Unix time in milliseconds
- Timezone offset sent via `X-Timezone-Offset` header (minutes)
- Server uses UTC internally

**Balance Calculations**
- Asset accounts: positive balance
- Liability accounts: negative balance
- Account balance field is read-only (calculated from transactions)

**Multi-Currency Support**
- Each account has a currency (ISO 4217 code)
- Exchange rates can be managed via API
- Transactions can be in different currencies

## Security Considerations

1. **Token Security**
   - Store tokens securely (environment variables)
   - Never log tokens
   - Support token rotation

2. **Input Validation**
   - Validate amounts (positive integers)
   - Validate dates (Unix timestamps)
   - Validate currencies (ISO 4217)
   - Validate account/category/tag IDs

3. **Rate Limiting**
   - Implement client-side rate limiting
   - Handle 429 responses gracefully
   - Add exponential backoff

4. **Data Privacy**
   - Financial data is sensitive
   - Implement secure error messages
   - Avoid exposing account details in logs

## Error Handling Strategy

### Common Error Codes
- **401 Unauthorized:** Token expired/invalid → Refresh token
- **403 Forbidden:** Insufficient permissions → Inform user
- **404 Not Found:** Resource doesn't exist → Clear error message
- **422 Validation Error:** Invalid input → Show validation details
- **500 Server Error:** Backend issue → Retry with backoff

### Error Response Format
```python
{
    "success": false,
    "errorCode": 100001,
    "errorMessage": "Invalid token",
    "path": "/api/v1/transactions/list.json"
}
```

## Configuration Schema

```json
{
  "ezbookkeeping": {
    "url": "https://your-instance.com",
    "auth": {
      "type": "token|credentials",
      "token": "api_token_here",
      "username": "user",
      "password": "pass"
    },
    "timezone_offset": 0,
    "default_currency": "USD",
    "cache_ttl": 300
  }
}
```

## Performance Optimization

1. **Caching Strategy**
   - Cache account list (TTL: 5 minutes)
   - Cache category/tag lists (TTL: 10 minutes)
   - Cache exchange rates (TTL: 1 hour)
   - Invalidate on write operations

2. **Batch Operations**
   - Use batch endpoints when available
   - Batch create categories/tags
   - Batch delete transactions

3. **Pagination**
   - Support pagination for transaction lists
   - Default page size: 50
   - Maximum page size: 200

## Testing Strategy

1. **Unit Tests**
   - Test each tool function
   - Test authentication flow
   - Test error handling
   - Test data validation

2. **Integration Tests**
   - Test against mock API server
   - Test end-to-end flows
   - Test error scenarios

3. **Manual Testing**
   - Use MCP Inspector
   - Test with actual EzBookkeeping instance
   - Verify all tools and resources

## Deployment Considerations

### Claude Desktop Configuration
```json
{
  "mcpServers": {
    "ezbookkeeping": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/ezbookkeeping_mcp_server",
        "run",
        "mcp",
        "run",
        "main.py"
      ],
      "env": {
        "EZBOOKKEEPING_URL": "https://your-instance.com",
        "EZBOOKKEEPING_TOKEN": "your_token"
      }
    }
  }
}
```

### Environment Variables
```bash
# Required
EZBOOKKEEPING_URL=https://your-instance.com
EZBOOKKEEPING_TOKEN=your_api_token

# Optional
EZBOOKKEEPING_TIMEZONE_OFFSET=0
EZBOOKKEEPING_DEFAULT_CURRENCY=USD
EZBOOKKEEPING_CACHE_TTL=300
```

## Future Enhancements

1. **Advanced Analytics**
   - Spending pattern detection
   - Budget forecasting
   - Anomaly detection

2. **Smart Features**
   - Auto-categorization based on history
   - Duplicate transaction detection
   - Receipt OCR improvements

3. **Multi-Instance Support**
   - Manage multiple EzBookkeeping instances
   - Cross-instance reporting

4. **Webhooks & Real-time**
   - Listen for transaction events
   - Real-time balance updates

## Success Metrics

1. **Functionality Coverage:** Implement 80%+ of core API endpoints
2. **Response Time:** <500ms for read operations, <1s for write operations
3. **Error Rate:** <1% error rate under normal conditions
4. **User Experience:** Natural language interactions feel intuitive
5. **Reliability:** 99.9% uptime with proper error handling

---

## Next Steps

1. ✅ Complete API documentation analysis
2. ⏭️ Implement authentication layer
3. ⏭️ Build core transaction tools
4. ⏭️ Implement account/category resources
5. ⏭️ Add statistical/reporting resources
6. ⏭️ Create intelligent prompts
7. ⏭️ Test with MCP Inspector
8. ⏭️ Deploy and iterate based on feedback
