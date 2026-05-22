# Database Schema

## Overview

The Halal Management System uses a relational database to track products, suppliers, certifications, audits, and compliance records.

---

## Tables

### 1. Products Table

**Purpose:** Store halal-certified products

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | VARCHAR(36) | PRIMARY KEY | Unique UUID |
| name | VARCHAR(255) | NOT NULL, UNIQUE | Product name |
| description | TEXT | - | Product description |
| sku | VARCHAR(50) | NOT NULL, UNIQUE | Stock Keeping Unit |
| category | VARCHAR(100) | NOT NULL, INDEX | Product category |
| is_halal_certified | BOOLEAN | DEFAULT: FALSE | Certification status |
| certification_date | DATETIME | - | When certified |
| certification_expiry | DATETIME | - | Expiration date |
| supplier_id | VARCHAR(36) | FOREIGN KEY | Reference to Supplier |
| ingredients | TEXT | - | JSON list of ingredients |
| price | FLOAT | - | Product price |
| status | VARCHAR(50) | DEFAULT: 'active' | active/inactive/pending |
| created_at | DATETIME | DEFAULT: NOW() | Creation timestamp |
| updated_at | DATETIME | DEFAULT: NOW() | Last update timestamp |

**Indexes:**
- PRIMARY: id
- UNIQUE: name, sku
- INDEX: category, is_halal_certified, status, created_at

---

### 2. Suppliers Table

**Purpose:** Store supplier information and compliance status

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | VARCHAR(36) | PRIMARY KEY | Unique UUID |
| name | VARCHAR(255) | NOT NULL, UNIQUE | Supplier name |
| email | VARCHAR(255) | UNIQUE | Contact email |
| phone | VARCHAR(20) | - | Contact phone |
| address | TEXT | - | Physical address |
| city | VARCHAR(100) | - | City |
| country | VARCHAR(100) | - | Country |
| halal_certified | BOOLEAN | DEFAULT: FALSE | Certification status |
| certification_date | DATETIME | - | When certified |
| certification_expiry | DATETIME | - | Expiration date |
| certification_body | VARCHAR(255) | - | Certifying authority |
| compliance_score | INTEGER | DEFAULT: 0 | Score 0-100 |
| status | VARCHAR(50) | DEFAULT: 'active' | active/inactive/suspended |
| created_at | DATETIME | DEFAULT: NOW() | Creation timestamp |
| updated_at | DATETIME | DEFAULT: NOW() | Last update timestamp |

**Indexes:**
- PRIMARY: id
- UNIQUE: name, email
- INDEX: halal_certified, status, created_at

**Relationships:**
- One-to-Many: Suppliers → Products
- One-to-Many: Suppliers → Audits

---

### 3. Certifications Table

**Purpose:** Store halal certification records

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | VARCHAR(36) | PRIMARY KEY | Unique UUID |
| certificate_number | VARCHAR(100) | NOT NULL, UNIQUE | Official cert number |
| organization_name | VARCHAR(255) | NOT NULL | Certified organization |
| certification_body | VARCHAR(255) | NOT NULL | Certifying authority |
| issue_date | DATETIME | NOT NULL | When issued |
| expiry_date | DATETIME | NOT NULL | When expires |
| scope | TEXT | - | JSON array of scope |
| standard | VARCHAR(100) | - | HAS/JAKIM/ESMA/etc |
| status | VARCHAR(50) | DEFAULT: 'active' | active/expired/suspended/pending |
| audit_score | FLOAT | - | Last audit score 0-100 |
| notes | TEXT | - | Additional notes |
| created_at | DATETIME | DEFAULT: NOW() | Creation timestamp |
| updated_at | DATETIME | DEFAULT: NOW() | Last update timestamp |

**Indexes:**
- PRIMARY: id
- UNIQUE: certificate_number
- INDEX: organization_name, expiry_date, status, created_at

---

### 4. Audits Table

**Purpose:** Track halal compliance audits

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | VARCHAR(36) | PRIMARY KEY | Unique UUID |
| audit_type | VARCHAR(50) | NOT NULL | initial/renewal/surveillance/unannounced |
| supplier_id | VARCHAR(36) | NOT NULL, FOREIGN KEY | Reference to Supplier |
| product_id | VARCHAR(36) | FOREIGN KEY | Reference to Product (optional) |
| audit_date | DATETIME | NOT NULL | When audit occurred |
| auditor_name | VARCHAR(255) | - | Name of auditor |
| score | FLOAT | - | Audit score 0-100 |
| findings | TEXT | - | JSON detailed findings |
| non_conformities | TEXT | - | JSON array of issues |
| corrective_actions | TEXT | - | JSON array of actions |
| status | VARCHAR(50) | DEFAULT: 'completed' | completed/pending/in_progress |
| passed | BOOLEAN | DEFAULT: TRUE | Pass/fail status |
| next_audit_date | DATETIME | - | Scheduled next audit |
| created_at | DATETIME | DEFAULT: NOW() | Creation timestamp |
| updated_at | DATETIME | DEFAULT: NOW() | Last update timestamp |

**Indexes:**
- PRIMARY: id
- INDEX: audit_type, supplier_id, product_id, audit_date, status, created_at

**Relationships:**
- Many-to-One: Audits → Suppliers
- Many-to-One: Audits → Products

---

### 5. Compliance Records Table

**Purpose:** Track compliance status and history

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | VARCHAR(36) | PRIMARY KEY | Unique UUID |
| product_id | VARCHAR(36) | NOT NULL, FOREIGN KEY | Reference to Product |
| compliance_status | VARCHAR(50) | DEFAULT: 'compliant' | compliant/non-compliant/warning/pending |
| last_check_date | DATETIME | - | Last compliance check |
| next_check_date | DATETIME | - | Next scheduled check |
| issues_count | INTEGER | DEFAULT: 0 | Number of issues |
| is_compliant | BOOLEAN | DEFAULT: TRUE | Overall status |
| notes | TEXT | - | Compliance notes |
| created_at | DATETIME | DEFAULT: NOW() | Creation timestamp |
| updated_at | DATETIME | DEFAULT: NOW() | Last update timestamp |

**Indexes:**
- PRIMARY: id
- INDEX: product_id, compliance_status, created_at

**Relationships:**
- Many-to-One: ComplianceRecords → Products

---

## Entity Relationship Diagram (ERD)

```
┌─────────────────────────────────────────────────────────────┐
│                     SUPPLIERS                               │
├──────────────────────────────────────────────────────────────┤
│ id (PK)                                                      │
│ name (UNIQUE)                                                │
│ email                                                        │
│ phone                                                        │
│ address                                                      │
│ city, country                                                │
│ halal_certified, certification_date, certification_expiry   │
│ certification_body, compliance_score, status                │
│ created_at, updated_at                                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ 1:N
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     PRODUCTS                                │
├──────────────────────────────────────────────────────────────┤
│ id (PK)                                                      │
│ name (UNIQUE), sku (UNIQUE)                                  │
│ description, category                                        │
│ is_halal_certified                                           │
│ certification_date, certification_expiry                     │
│ supplier_id (FK) ───────────────────────┐                    │
│ ingredients, price, status              │                    │
│ created_at, updated_at                  │                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ 1:N
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                COMPLIANCE_RECORDS                           │
├────────────────────────────────────���─────────────────────────┤
│ id (PK)                                                      │
│ product_id (FK) ────────────────────────┐                    │
│ compliance_status                       │                    │
│ last_check_date, next_check_date        │                    │
│ issues_count, is_compliant              │                    │
│ notes                                   │                    │
│ created_at, updated_at                  │                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ 1:N
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     AUDITS                                  │
├──────────────────────────────────────────────────────────────┤
│ id (PK)                                                      │
│ audit_type                                                   │
│ supplier_id (FK)                                             │
│ product_id (FK)                                              │
│ audit_date, auditor_name                                     │
│ score, findings, non_conformities                            │
│ corrective_actions, status, passed                           │
│ next_audit_date                                              │
│ created_at, updated_at                                       │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                CERTIFICATIONS                               │
├──────────────────────────────────────────────────────────────┤
│ id (PK)                                                      │
│ certificate_number (UNIQUE)                                  │
│ organization_name                                            │
│ certification_body                                           │
│ issue_date, expiry_date                                      │
│ scope, standard                                              │
│ status, audit_score                                          │
│ notes                                                        │
│ created_at, updated_at                                       │
└─────────────────────────────────────────────────────────────┘
```

---

## Key Queries

### Find Expiring Certifications
```sql
SELECT p.* FROM products p
WHERE p.is_halal_certified = TRUE
AND p.certification_expiry BETWEEN NOW() AND DATE_ADD(NOW(), INTERVAL 30 DAY)
ORDER BY p.certification_expiry ASC;
```

### Get Supplier Compliance Score
```sql
SELECT s.id, s.name, COUNT(a.id) as audit_count, AVG(a.score) as avg_score
FROM suppliers s
LEFT JOIN audits a ON s.id = a.supplier_id
GROUP BY s.id, s.name
ORDER BY avg_score DESC;
```

### Non-Compliant Products
```sql
SELECT p.* FROM products p
JOIN compliance_records cr ON p.id = cr.product_id
WHERE cr.is_compliant = FALSE
AND cr.compliance_status != 'compliant';
```

### Recent Audits
```sql
SELECT a.*, s.name as supplier_name, p.name as product_name
FROM audits a
LEFT JOIN suppliers s ON a.supplier_id = s.id
LEFT JOIN products p ON a.product_id = p.id
WHERE a.audit_date >= DATE_SUB(NOW(), INTERVAL 30 DAY)
ORDER BY a.audit_date DESC;
```

---

## Indexing Strategy

- **Composite Indexes:**
  - (supplier_id, created_at) on products
  - (status, expiry_date) on certifications
  - (audit_type, supplier_id, created_at) on audits

- **Full-Text Search (Future):**
  - Product names
  - Supplier names
  - Certification numbers

---

## Data Retention Policy

- **Products:** Keep indefinitely (mark as inactive if no longer used)
- **Suppliers:** Keep indefinitely
- **Certifications:** Keep indefinitely
- **Audits:** Minimum 5 years
- **Compliance Records:** Minimum 2 years
- **Logs:** 1 year for compliance, 3 months for operational
