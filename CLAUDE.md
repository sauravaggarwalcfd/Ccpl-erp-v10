# CLAUDE.md - ERP Inventory Management System

This document provides comprehensive guidance for AI assistants (Claude) working on this ERP Inventory Management System codebase.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Repository Structure](#repository-structure)
3. [Technology Stack](#technology-stack)
4. [Development Workflows](#development-workflows)
5. [Code Conventions & Patterns](#code-conventions--patterns)
6. [Design System & Guidelines](#design-system--guidelines)
7. [Testing Guidelines](#testing-guidelines)
8. [Common Tasks & Workflows](#common-tasks--workflows)
9. [Critical Rules for AI Assistants](#critical-rules-for-ai-assistants)

---

## Project Overview

**Project Name:** CCPL ERP v10 - Inventory Management System

**Purpose:** A comprehensive ERP system designed for manufacturing professionals (Store managers, Purchase officers, QC inspectors, Accounts team) to manage inventory, purchases, quality control, and reporting.

**Architecture:** Full-stack application with:
- **Backend:** Python FastAPI + MongoDB (async with Motor)
- **Frontend:** React 19 + Tailwind CSS + Shadcn UI
- **Authentication:** JWT-based with role-based access control

**Key Business Domains:**
- Masters (Items, Categories, Suppliers, Warehouses, etc.)
- Purchase Management (Indents, Orders, Approvals)
- Quality Control (QC Checks)
- Inventory Transactions (GRN, Stock Transfer, Issues, Adjustments)
- Reports (Stock Ledger, Balance, Pending Orders)
- Settings (Approval Flows, Number Series, Roles)

---

## Repository Structure

```
Ccpl-erp-v10/
├── backend/
│   ├── server.py              # Main FastAPI application
│   └── requirements.txt       # Python dependencies
│
├── frontend/
│   ├── public/                # Static assets
│   ├── src/
│   │   ├── components/        # Shared React components
│   │   │   └── ui/           # Shadcn UI components
│   │   ├── contexts/         # React Context providers (Auth, etc.)
│   │   ├── hooks/            # Custom React hooks
│   │   ├── layouts/          # Layout components (MainLayout, InventoryLayout)
│   │   ├── lib/              # Utility functions
│   │   ├── pages/            # Page components organized by feature
│   │   │   ├── masters/      # Master data pages
│   │   │   ├── purchase/     # Purchase module pages
│   │   │   ├── quality/      # Quality control pages
│   │   │   ├── inventory/    # Inventory transaction pages
│   │   │   ├── reports/      # Report pages
│   │   │   └── settings/     # Settings pages
│   │   ├── router/           # Route definitions by module
│   │   ├── services/         # API service layer
│   │   │   ├── api.js        # Main API configuration & endpoints
│   │   │   └── inventoryApi.js
│   │   ├── inventory/        # Alternative inventory module structure
│   │   │   ├── masters/
│   │   │   ├── transactions/
│   │   │   ├── reports/
│   │   │   └── settings/
│   │   ├── App.js            # Main application component
│   │   ├── App.css           # Global styles
│   │   └── index.js          # Application entry point
│   ├── package.json          # Node dependencies
│   ├── tailwind.config.js    # Tailwind CSS configuration
│   ├── craco.config.js       # CRACO configuration for CRA customization
│   ├── components.json       # Shadcn UI configuration
│   └── jsconfig.json         # Path aliases configuration
│
├── scripts/
│   ├── create_dummy_data.py  # Data seeding scripts
│   ├── create_additional_dummy_data.py
│   ├── seed_garment_categories.py
│   └── fix_category_ids.py
│
├── tests/                    # Test files
├── design_guidelines.json    # Comprehensive design system specification
├── backend_test.py          # Backend tests
├── test_result.md           # Test results documentation
├── .gitignore
└── README.md

```

**Key Structural Notes:**
- **Dual Structure:** The project has both `/pages` and `/inventory` folders with some overlap - prefer `/pages` for new features unless working specifically on the inventory module
- **Path Aliases:** Uses `@/` prefix for absolute imports (configured in jsconfig.json and craco.config.js)
- **Feature Organization:** Code is organized by business domain (masters, purchase, quality, inventory, reports, settings)

---

## Technology Stack

### Backend
- **Framework:** FastAPI 0.110.1
- **Database:** MongoDB (async with Motor 3.3.1)
- **ODM/Validation:** Pydantic 2.6.4+
- **Authentication:** JWT (PyJWT 2.10.1+, python-jose 3.3.0+)
- **Password Hashing:** bcrypt 4.1.3, passlib 1.7.4+
- **Server:** Uvicorn 0.25.0
- **Data Processing:** pandas 2.2.0+, numpy 1.26.0+
- **Testing:** pytest 8.0.0+
- **Code Quality:** black, isort, flake8, mypy

**Backend Key Features:**
- Async/await pattern throughout
- Enum-based constants (UserRole, InventoryType, ApprovalStatus, etc.)
- Pydantic models for request/response validation
- JWT-based authentication with role-based access control
- CORS enabled for frontend integration

### Frontend
- **Framework:** React 19.0.0
- **Router:** React Router DOM 7.5.1
- **Styling:** Tailwind CSS 3.4.17 + tailwindcss-animate
- **UI Components:** Shadcn UI (based on Radix UI primitives)
  - Full set: Dialog, Dropdown, Select, Table, Form, Toast (Sonner), etc.
- **Forms:** React Hook Form 7.56.2 + Zod 3.24.4 + @hookform/resolvers
- **HTTP Client:** Axios 1.8.4
- **Icons:** lucide-react 0.507.0
- **Date Handling:** date-fns 4.1.0, react-day-picker 8.10.1
- **Build Tool:** Create React App with CRACO 7.1.0
- **Package Manager:** Yarn 1.22.22

**Frontend Key Libraries:**
- **Radix UI:** Complete set of accessible primitives
- **class-variance-authority:** Component variant management
- **clsx + tailwind-merge:** Conditional CSS classes
- **cmdk:** Command palette component
- **next-themes:** Theme management (light/dark mode support)
- **sonner:** Toast notifications
- **vaul:** Drawer component

---

## Development Workflows

### Frontend Development

**Starting the Dev Server:**
```bash
cd frontend
yarn start
# Runs on http://localhost:3000
```

**Building for Production:**
```bash
cd frontend
yarn build
# Creates optimized build in frontend/build/
```

**Running Tests:**
```bash
cd frontend
yarn test
```

**Environment Variables:**
Frontend uses `REACT_APP_*` prefixed environment variables:
- `REACT_APP_BACKEND_URL` - Backend API base URL

### Backend Development

**Starting the Server:**
```bash
cd backend
# Ensure virtual environment is activated
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

**Environment Variables (backend/.env):**
```
MONGO_URL=mongodb://...
DB_NAME=erp_db
JWT_SECRET=your-secret-key-change-in-production
```

**Code Quality:**
```bash
# Format code
black backend/server.py
isort backend/server.py

# Lint
flake8 backend/server.py
mypy backend/server.py
```

**Running Tests:**
```bash
pytest backend_test.py -v
```

### Database Seeding

```bash
# Seed categories
python scripts/seed_garment_categories.py

# Create dummy data
python scripts/create_dummy_data.py

# Create additional dummy data
python scripts/create_additional_dummy_data.py

# Fix category IDs (if needed)
python scripts/fix_category_ids.py
```

---

## Code Conventions & Patterns

### Frontend Conventions

#### File Naming & Structure
- **Components:** PascalCase with `.jsx` extension (e.g., `ItemMaster.jsx`)
- **Services:** camelCase with `.js` extension (e.g., `api.js`)
- **Routes:** camelCase with `.js` extension (e.g., `inventoryRoutes.js`)
- **Named Exports:** Use for reusable components
- **Default Exports:** Use for page components

#### Import Patterns
```javascript
// ALWAYS use @ alias for absolute imports
import { Button } from '@/components/ui/button';
import MainLayout from '@/layouts/MainLayout';
import { mastersAPI } from '@/services/api';

// React imports first
import React, { useState, useEffect } from 'react';

// Then third-party libraries
import { useNavigate } from 'react-router-dom';
import { toast } from 'sonner';

// Then local imports
import { useAuth } from '@/contexts/AuthContext';
```

#### Component Structure
```javascript
// Page components (default export)
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '@/components/ui/button';

const ItemMaster = () => {
  // 1. Hooks
  const navigate = useNavigate();
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(false);

  // 2. Effects
  useEffect(() => {
    fetchItems();
  }, []);

  // 3. Handlers
  const fetchItems = async () => {
    setLoading(true);
    try {
      const response = await mastersAPI.getItems();
      setItems(response.data);
    } catch (error) {
      toast.error('Failed to fetch items');
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = () => {
    navigate('/masters/items/new');
  };

  // 4. Render
  return (
    <div className="p-6">
      {/* Component JSX */}
    </div>
  );
};

export default ItemMaster;
```

#### State Management
- **Local State:** `useState` for component-specific data
- **Global State:** Context API (see `AuthContext.jsx`)
- **Server State:** Direct API calls with loading/error states (no react-query currently)

#### API Service Layer
All API calls go through `/services/api.js`:
```javascript
// In service file
export const mastersAPI = {
  getItems: () => api.get('/masters/items'),
  createItem: (data) => api.post('/masters/items', data),
  updateItem: (id, data) => api.put(`/masters/items/${id}`, data),
  deleteItem: (id) => api.delete(`/masters/items/${id}`),
};

// In component
import { mastersAPI } from '@/services/api';
const response = await mastersAPI.getItems();
```

#### Routing Patterns
- Routes defined in separate route files (e.g., `inventoryRoutes.js`)
- Nested routes using React Router v7 pattern
- Private routes wrapped with `PrivateRoute` component (see `App.js:70`)

#### Form Handling
```javascript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';

const formSchema = z.object({
  itemName: z.string().min(1, 'Item name is required'),
  categoryId: z.string().min(1, 'Category is required'),
});

const form = useForm({
  resolver: zodResolver(formSchema),
  defaultValues: { itemName: '', categoryId: '' },
});

const onSubmit = async (data) => {
  try {
    await mastersAPI.createItem(data);
    toast.success('Item created successfully');
    navigate('/masters/items');
  } catch (error) {
    toast.error('Failed to create item');
  }
};
```

#### Error Handling
```javascript
try {
  const response = await mastersAPI.getItems();
  setItems(response.data);
} catch (error) {
  console.error('Error fetching items:', error);
  toast.error(error.response?.data?.detail || 'Failed to fetch items');
}
```

#### Toast Notifications
```javascript
import { toast } from 'sonner';

// Success
toast.success('Item created successfully');

// Error
toast.error('Failed to create item');

// Info
toast.info('Processing...');

// Warning
toast.warning('Stock level is low');
```

### Backend Conventions

#### File Structure
- Single `server.py` file currently (monolithic)
- Models defined using Pydantic BaseModel
- Routes grouped by feature using `APIRouter`

#### Model Patterns
```python
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
import uuid

class ItemMaster(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    item_code: str
    item_name: str
    category_id: str
    uom: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
```

#### API Endpoint Patterns
```python
@api_router.post("/masters/items", response_model=ItemMaster)
async def create_item(item: ItemMaster, user: User = Depends(get_current_user)):
    """Create a new item in the system."""
    try:
        # Validate business rules
        existing = await db.items.find_one({"item_name": item.item_name, "category_id": item.category_id})
        if existing:
            raise HTTPException(status_code=400, detail="Item with this name already exists in category")

        # Insert to database
        item_dict = item.model_dump()
        result = await db.items.insert_one(item_dict)

        return item
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

#### Authentication Pattern
```python
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Verify JWT token and return current user."""
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

        user_dict = await db.users.find_one({"id": user_id})
        if not user_dict:
            raise HTTPException(status_code=401, detail="User not found")

        return User(**user_dict)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
```

#### Enums
Use Python Enums for status fields and constants:
```python
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "Admin"
    STORE = "Store"
    PURCHASE = "Purchase"
    QC = "QC"
    ACCOUNTS = "Accounts"

class ApprovalStatus(str, Enum):
    DRAFT = "Draft"
    PENDING = "Pending"
    APPROVED = "Approved"
    REJECTED = "Rejected"
```

---

## Design System & Guidelines

The project has comprehensive design guidelines in `design_guidelines.json`. Key points:

### Design Philosophy
- **Target Users:** Manufacturing professionals (desktop-first, extended daily use)
- **Approach:** Professional ERP interface with clean industrial layout
- **Principles:**
  - Data density with clarity
  - Functional beauty - every element serves a purpose
  - Scanability - users find information in under 3 seconds
  - Consistency across all modules
  - Efficiency - minimize clicks and cognitive load

### Typography
```javascript
// Font families (defined in tailwind.config.js)
font-sans       // Work Sans - body text, labels, tables
font-heading    // IBM Plex Sans - headings, titles
font-mono       // IBM Plex Mono - codes, SKUs, IDs

// Text sizes
text-3xl font-semibold tracking-tight  // Page titles
text-2xl font-semibold tracking-tight  // Section headers
text-xl font-semibold                  // Card titles
text-lg font-medium                    // Subsections
text-base font-normal                  // Body text
text-sm font-medium                    // Labels
text-xs                                // Captions
```

### Color System
**Archetype:** Swiss & High-Contrast (Authority, Clarity, Truth)

```javascript
// Primary colors
bg-primary text-primary-foreground     // Deep blue for CTAs
hover:bg-primary-hover                 // Darker blue on hover

// Neutral grays
bg-neutral-50   // Page background
bg-white        // Cards, forms
border-neutral-200  // Default borders

// Status colors
text-status-pending      // Yellow
text-status-approved     // Green
text-status-rejected     // Red
text-status-draft        // Gray
text-status-in-progress  // Blue
```

**CRITICAL:** Always use explicit text AND background colors on hover states to maintain contrast.

### Layout Patterns
```javascript
// Sidebar navigation + Top header + Main content
<div className="flex h-screen">
  <Sidebar className="w-64 border-r border-neutral-200 bg-neutral-50" />
  <div className="flex-1 flex flex-col">
    <Header className="h-16 border-b border-neutral-200 bg-white" />
    <main className="flex-1 overflow-auto bg-neutral-50 p-6 md:p-8">
      {/* Page content */}
    </main>
  </div>
</div>

// Dashboard grid (Control Room Grid pattern)
<div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6">
  <Card className="col-span-1" />      {/* Summary card */}
  <Card className="col-span-2" />      {/* Chart */}
  <Card className="col-span-1 row-span-2" />  {/* Activity feed */}
</div>

// Form layouts (Two-column responsive)
<div className="grid grid-cols-1 md:grid-cols-2 gap-6">
  <FormField />
  <FormField />
  <FormField className="col-span-full" />  {/* Full-width fields */}
</div>
```

### Component Usage
**Use Shadcn UI components for ALL interactive elements:**
- Forms: `Input`, `Select`, `Textarea`, `Checkbox`, `RadioGroup`, `Calendar`, `Form`
- Data Display: `Table`, `Badge`, `Card`, `Separator`, `Tabs`
- Navigation: `Breadcrumb`, `Tabs`, `DropdownMenu`
- Feedback: `Toast (Sonner)`, `Alert`, `Dialog`, `AlertDialog`
- Overlays: `Dialog`, `Sheet`, `Popover`, `Tooltip`

### Surface Treatments
```javascript
// Cards and containers
className="bg-white border border-neutral-200 rounded-lg p-6"

// Tables
className="bg-white border border-neutral-200 rounded-lg overflow-hidden"

// Minimal shadows (rely on borders for definition)
shadow-sm        // Subtle ambient
shadow-md        // Hover states
shadow-xl        // Modals only
```

### Interactive States
```javascript
// Buttons
className="transition-colors duration-200 hover:bg-primary-hover hover:text-white"

// Table rows
className="transition-colors duration-150 hover:bg-neutral-50"

// Focus states (ALWAYS include)
className="focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2"
```

### Data Tables
- Fixed header with sticky positioning
- Sortable columns with visual indicators
- Row hover states (`hover:bg-neutral-50`)
- Zebra striping for long tables (optional)
- Action column (right-aligned) with dropdown menu
- Pagination at bottom

### Accessibility Requirements
- **WCAG AA minimum**, AAA for text contrast
- All interactive elements keyboard accessible
- Proper ARIA labels and semantic HTML
- `data-testid` attributes on all interactive elements (kebab-case)
- Never rely on color alone to convey information

### Motion & Interactions
- **Philosophy:** Minimal, purposeful animations
- Use `transition-colors`, `transition-opacity`, `transition-transform` - **NEVER** `transition: all`
- Durations: 150ms for micro-interactions, 200ms for state changes, 300ms for page transitions
- Respect `prefers-reduced-motion` media query

---

## Testing Guidelines

### Frontend Testing
- `data-testid` attributes required on all interactive elements
- Naming convention: kebab-case, role-based (e.g., `login-submit-button`, `item-master-form`)
- Test files: `*.test.js` or `*.spec.js`

**Required data-testid elements:**
- All buttons
- All form inputs
- All navigation links
- All table action buttons
- All status indicators
- All error/success messages

### Backend Testing
- Test file: `backend_test.py`
- Use pytest for testing
- Test authentication, CRUD operations, business logic validation

---

## Common Tasks & Workflows

### Adding a New Page

1. **Create the page component** in appropriate feature folder:
```javascript
// frontend/src/pages/masters/NewMaster.jsx
import React from 'react';
import { Button } from '@/components/ui/button';

const NewMaster = () => {
  return (
    <div className="p-6">
      <h1 className="text-3xl font-semibold tracking-tight mb-6">New Master</h1>
      {/* Page content */}
    </div>
  );
};

export default NewMaster;
```

2. **Add route** in `App.js` or appropriate route file:
```javascript
import NewMaster from '@/pages/masters/NewMaster';

// In routes section
<Route path="masters/new-master" element={<NewMaster />} />
```

3. **Add navigation link** in sidebar/menu component.

### Adding a New API Endpoint

1. **Define Pydantic model** (if needed):
```python
class NewMaster(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
```

2. **Create endpoint** in `backend/server.py`:
```python
@api_router.get("/masters/new-masters", response_model=List[NewMaster])
async def get_new_masters(user: User = Depends(get_current_user)):
    """Get all new masters."""
    masters = await db.new_masters.find().to_list(None)
    return [NewMaster(**m) for m in masters]

@api_router.post("/masters/new-masters", response_model=NewMaster)
async def create_new_master(master: NewMaster, user: User = Depends(get_current_user)):
    """Create a new master."""
    master_dict = master.model_dump()
    await db.new_masters.insert_one(master_dict)
    return master
```

3. **Add to service layer** in `frontend/src/services/api.js`:
```javascript
export const mastersAPI = {
  // ... existing methods
  getNewMasters: () => api.get('/masters/new-masters'),
  createNewMaster: (data) => api.post('/masters/new-masters', data),
};
```

### Adding a New Shadcn Component

```bash
cd frontend
npx shadcn@latest add [component-name]
# Example: npx shadcn@latest add accordion
```

Components are added to `frontend/src/components/ui/`

### Creating a Form with Validation

```javascript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { toast } from 'sonner';

const formSchema = z.object({
  name: z.string().min(1, 'Name is required'),
  email: z.string().email('Invalid email address'),
  role: z.string().min(1, 'Role is required'),
});

const MyForm = () => {
  const form = useForm({
    resolver: zodResolver(formSchema),
    defaultValues: { name: '', email: '', role: '' },
  });

  const onSubmit = async (data) => {
    try {
      await mastersAPI.createItem(data);
      toast.success('Created successfully');
    } catch (error) {
      toast.error('Failed to create');
    }
  };

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Name</FormLabel>
              <FormControl>
                <Input {...field} data-testid="name-input" />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit" data-testid="submit-button">Submit</Button>
      </form>
    </Form>
  );
};
```

### Database Operations (Backend)

```python
# Find one
item = await db.items.find_one({"id": item_id})

# Find many
items = await db.items.find({"category_id": category_id}).to_list(None)

# Insert one
result = await db.items.insert_one(item_dict)

# Update one
await db.items.update_one({"id": item_id}, {"$set": update_dict})

# Delete one
await db.items.delete_one({"id": item_id})

# Aggregation
pipeline = [
    {"$match": {"is_active": True}},
    {"$group": {"_id": "$category_id", "count": {"$sum": 1}}},
]
results = await db.items.aggregate(pipeline).to_list(None)
```

---

## Critical Rules for AI Assistants

### ALWAYS DO

1. **Read before modifying:** ALWAYS read existing files before making changes
2. **Use design guidelines:** Reference `design_guidelines.json` for all UI decisions
3. **Follow conventions:** Match existing code style and patterns
4. **Use path aliases:** Import with `@/` prefix for all local modules
5. **Add data-testid:** Include on all interactive elements
6. **Handle errors:** Wrap API calls in try-catch with toast notifications
7. **Validate forms:** Use react-hook-form + zod for all forms
8. **Use Shadcn UI:** Use existing Shadcn components instead of building from scratch
9. **Respect design system:** Follow color, typography, spacing from tailwind.config.js
10. **Async/await:** Use async/await for all backend database operations
11. **JWT authentication:** Protect all backend routes with `Depends(get_current_user)`
12. **Type validation:** Use Pydantic models for all request/response bodies

### NEVER DO

1. **❌ Universal transitions:** Never use `transition: all` - use specific properties
2. **❌ Guess imports:** Never assume paths - check the actual file structure
3. **❌ Skip error handling:** Never make API calls without try-catch
4. **❌ Ignore accessibility:** Never omit ARIA labels, keyboard support, or focus states
5. **❌ Color-only information:** Never rely on color alone without text/icons
6. **❌ Hardcode values:** Never hardcode API URLs, use environment variables
7. **❌ Skip validation:** Never skip form validation or backend data validation
8. **❌ Ignore loading states:** Never forget loading indicators for async operations
9. **❌ Break auth:** Never expose endpoints without authentication checks
10. **❌ Use emojis in UI:** Only use lucide-react icons, not emoji icons
11. **❌ Center-align app:** Don't disrupt natural reading flow with centered layouts
12. **❌ Over-engineer:** Don't add unnecessary abstractions or future-proofing

### File Location Decisions

**When adding new features:**

| Feature Type | Location | Example |
|--------------|----------|---------|
| Shared UI Component | `frontend/src/components/` | `StatusBadge.jsx` |
| Shadcn Component | `frontend/src/components/ui/` | `button.jsx` |
| Master Page | `frontend/src/pages/masters/` | `ItemMaster.jsx` |
| Purchase Page | `frontend/src/pages/purchase/` | `PurchaseOrders.jsx` |
| Inventory Page | `frontend/src/pages/inventory/` | `StockTransfer.jsx` |
| Report Page | `frontend/src/pages/reports/` | `StockLedger.jsx` |
| Settings Page | `frontend/src/pages/settings/` | `ApprovalFlows.jsx` |
| Layout Component | `frontend/src/layouts/` | `MainLayout.jsx` |
| Context Provider | `frontend/src/contexts/` | `AuthContext.jsx` |
| Custom Hook | `frontend/src/hooks/` | `useAuth.js` |
| API Service | `frontend/src/services/` | `api.js` |
| Utility Function | `frontend/src/lib/` | `utils.js` |
| Route Definition | `frontend/src/router/` | `inventoryRoutes.js` |

### Performance Considerations

1. **Table virtualization:** Use for tables with 100+ rows
2. **Lazy loading:** Lazy load charts and heavy components
3. **Debouncing:** Debounce search and filter inputs (300ms)
4. **Caching:** Cache master data in memory/localStorage for session
5. **Pagination:** Always paginate large data sets

### Security Best Practices

1. **JWT expiration:** Tokens expire in 24 hours (JWT_EXPIRATION_HOURS)
2. **Password hashing:** Always use bcrypt for password storage
3. **Token storage:** Store JWT in localStorage (client-side)
4. **Authorization header:** Include Bearer token in all authenticated requests
5. **CORS:** Configured in FastAPI for frontend origin
6. **Input validation:** Validate all inputs on both frontend (Zod) and backend (Pydantic)
7. **SQL injection:** Not applicable (using MongoDB), but validate document queries

---

## Quick Reference

### Common Imports (Frontend)

```javascript
// UI Components
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Select } from '@/components/ui/select';
import { Table } from '@/components/ui/table';
import { Dialog } from '@/components/ui/dialog';
import { Card } from '@/components/ui/card';

// Form Handling
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';

// Navigation & State
import { useNavigate, useParams } from 'react-router-dom';
import { useState, useEffect } from 'react';

// Notifications
import { toast } from 'sonner';

// API & Auth
import { mastersAPI } from '@/services/api';
import { useAuth } from '@/contexts/AuthContext';
```

### Common Imports (Backend)

```python
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone, timedelta
from enum import Enum
import uuid
import bcrypt
import jwt
from motor.motor_asyncio import AsyncIOMotorClient
```

### Common Tailwind Classes

```javascript
// Layout
"flex items-center justify-between"
"grid grid-cols-1 md:grid-cols-2 gap-6"
"p-6 md:p-8"

// Cards & Containers
"bg-white border border-neutral-200 rounded-lg p-6"
"bg-neutral-50"

// Typography
"text-3xl font-semibold tracking-tight"  // Page title
"text-sm font-medium"                     // Label
"text-neutral-600"                        // Muted text

// Buttons
"bg-primary text-primary-foreground hover:bg-primary-hover transition-colors duration-200"

// Focus States
"focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2"

// Table Rows
"hover:bg-neutral-50 transition-colors duration-150"

// Borders
"border border-neutral-200"
"border-b border-neutral-200"  // Bottom only
```

---

## Additional Resources

- **Design Guidelines:** See `design_guidelines.json` for complete design system
- **Shadcn UI Docs:** https://ui.shadcn.com
- **Radix UI Docs:** https://www.radix-ui.com
- **Tailwind CSS Docs:** https://tailwindcss.com
- **FastAPI Docs:** https://fastapi.tiangolo.com
- **React Router Docs:** https://reactrouter.com
- **React Hook Form Docs:** https://react-hook-form.com

---

## Changelog & Maintenance

**Document Version:** 1.0.0
**Last Updated:** 2025-12-10
**Codebase State:** ERP v10 with inventory, purchase, quality, and reporting modules

**Key Features Implemented:**
- Authentication with JWT and role-based access
- Master data management (Items, Categories, Suppliers, Warehouses, etc.)
- Purchase module (Indents, Orders, Approvals)
- Quality control checks
- Inventory transactions (GRN, Issues, Transfers, Adjustments, Audits)
- Reports (Stock Ledger, Balance, BIN Stock, Dead Stock)
- Settings (Approval Flows, Number Series, Roles, Account Mapping)

**When updating this document:**
- Add new patterns and conventions as the codebase evolves
- Document breaking changes
- Update examples with actual working code patterns
- Keep the Critical Rules section strict and comprehensive
