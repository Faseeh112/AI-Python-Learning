# VisualImpairedDiaryDB — Flask Backend Project

> AI-powered diary system for visually impaired users with voice input, NLP processing, zakat/tax tracking, and knowledge graph.

---

## Quick Start

```bash
# 1. Clone and enter project
cd visual_diary

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your DB credentials, API keys, etc.

# 5. Initialize database migrations
flask db init
flask db migrate -m "initial schema"
flask db upgrade

# 6. Run development server
flask run
# or
python run.py
```

---

## Project Structure (90 Python files)

```
visual_diary/
├── run.py                          # Entry point
├── config/settings.py              # Dev/Prod/Test configs
├── requirements.txt                # Dependencies
├── .env.example                    # Environment template
│
├── app/
│   ├── __init__.py                 # App factory + blueprint registration
│   ├── extensions.py               # SQLAlchemy, JWT, CORS, Marshmallow
│   │
│   ├── models/        (22 files)   # SQLAlchemy ORM — FULLY IMPLEMENTED
│   ├── routes/        (19 files)   # Flask Blueprints — ALL ROUTES DEFINED
│   ├── controllers/                # Request handlers — stubs
│   ├── services/                   # Business logic — stubs
│   ├── ai/            (7 files)    # AI integrations — stubs
│   ├── utils/         (6 files)    # Helpers — stubs
│   ├── middleware/    (5 files)    # Auth, RBAC, rate limit — stubs
│   └── jobs/          (6 files)    # Background tasks — stubs
│
├── migrations/                     # Alembic migrations
└── tests/             (9 files)    # Test stubs
```

---

## What's Implemented vs Stub

| Layer | Status | Details |
|-------|--------|---------|
| **Models** | ✅ FULL | 22 SQLAlchemy models with all fields, relationships, constraints, CHECK constraints |
| **Routes** | ✅ FULL | 19 blueprints, 80+ endpoints with method/URL/purpose/auth docs |
| **App Factory** | ✅ FULL | Blueprint registration, error handlers, CORS, extensions |
| **Config** | ✅ FULL | Dev/Prod/Test configs, .env template |
| **Response Helpers** | ✅ FULL | success_response, error_response, paginated_response |
| **Error Classes** | ✅ FULL | AppError, ValidationError, NotFoundError, etc. |
| Controllers | 📝 Stub | Function names + purpose comments |
| Services | 📝 Stub | Function names + logic description comments |
| AI Modules | 📝 Stub | 7 services with interface docs |
| Middleware | 📝 Stub | Auth, RBAC, rate limit, sanitizer placeholders |
| Jobs | 📝 Stub | 6 background jobs with flow comments |
| Tests | 📝 Stub | 9 test files with test case outlines |

---

## Database Models — Relationship Map

```
User (central)
 ├──► Person          (1:N, cascade delete)
 │     ├──► TransactionLog  (1:N)
 │     ├──► Event           (1:N via host_person_id)
 │     └──◄► Notes          (M:N via note_person)
 │
 ├──► Location        (1:N, cascade delete)
 │     ├──► Location        (self-ref: parent → children)
 │     ├──► Item            (1:N)
 │     ├──► Event           (1:N)
 │     └──► Document        (1:N)
 │
 ├──► Notes           (1:N, cascade delete)
 │     ├──◄► Tag            (M:N via note_tag)
 │     ├──◄► Person         (M:N via note_person + role)
 │     ├──► VoiceEntry      (1:N)
 │     ├──► Attachment      (1:N)
 │     ├──► FileUpload      (1:N)
 │     └──► KnowledgeTriple (1:N)
 │
 ├──► Event           (1:N, cascade delete)
 │     ├──► Reminder        (1:N)
 │     └──► TransactionLog  (1:N)
 │
 ├──► Item            (1:N, cascade delete)
 │     ├──► Asset           (1:N)
 │     ├──► Document        (1:N)
 │     └──► TransactionLog  (1:N)
 │
 ├──► VoiceEntry      (1:N, cascade delete)
 │     ├──► RawTextLog      (1:N)
 │     └──► KnowledgeTriple (1:N)
 │
 ├──► TransactionLog  (1:N, cascade delete)
 ├──► Asset           (1:N, cascade delete)
 ├──► FileUpload      (1:N, cascade delete)
 │     ├──► Document        (1:N)
 │     ├──► TransactionLog  (1:N)
 │     ├──► Asset           (1:N)
 │     ├──► RawTextLog      (1:N)
 │     └──► KnowledgeTriple (1:N)
 │
 └──► UserQuranListen (1:N, cascade delete)

Category ──► Item, TransactionLog, Asset  (1:N)
Currency ──► TransactionLog, Asset        (FK reference)
QuranAudio ──► UserQuranListen            (1:N, cascade delete)

KnowledgeTriple: polymorphic FKs
  subject_id + subject_type → person|item|asset|location|event|document|user
  object_id  + object_type  → person|item|asset|location|event|document|user
  (integrity enforced at app layer)
```

---

## API Endpoints — Complete Reference (80+ routes)

### Auth (`/api/auth`)
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/register` | Register new user |
| POST | `/login` | Login → JWT tokens |
| POST | `/refresh` | Refresh access token |
| POST | `/logout` | Blacklist token |
| POST | `/forgot-password` | Send reset email |
| POST | `/reset-password` | Set new password |

### User (`/api/users`)
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/me` | Get profile |
| PUT | `/me` | Update profile |
| DELETE | `/me` | Deactivate account |
| PUT | `/me/password` | Change password |

### Notes (`/api/notes`)
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | List notes (paginated) |
| POST | `/` | Create note |
| GET | `/<id>` | Get note detail |
| PUT | `/<id>` | Update note |
| DELETE | `/<id>` | Soft-delete note |
| POST | `/<id>/tags` | Add tags |
| DELETE | `/<id>/tags/<tag_id>` | Remove tag |
| POST | `/<id>/persons` | Link person |
| GET | `/search` | Full-text search |

### Voice (`/api/voice`)
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/` | Audio → STT → NLP → store/query |
| GET | `/history` | Voice entry history |
| GET | `/<id>` | Entry detail |
| DELETE | `/<id>` | Soft-delete entry |

### Transactions (`/api/transactions`)
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | List (filterable) |
| POST | `/` | Create transaction |
| GET | `/<id>` | Detail |
| PUT | `/<id>` | Update |
| DELETE | `/<id>` | Soft-delete |
| GET | `/summary` | Aggregated summary |

### Assets (`/api/assets`)
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | List (filterable) |
| POST | `/` | Create (auto zakat/depr) |
| GET | `/<id>` | Detail |
| PUT | `/<id>` | Update |
| DELETE | `/<id>` | Soft-delete |
| GET | `/net-worth` | Net worth by category |
| POST | `/depreciate` | Run depreciation |

### Persons (`/api/persons`)
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | List contacts |
| POST | `/` | Create person |
| GET | `/<id>` | Detail |
| PUT | `/<id>` | Update |
| DELETE | `/<id>` | Soft-delete |

### Locations (`/api/locations`)
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | List (flat or tree) |
| POST | `/` | Create |
| GET | `/<id>` | Detail |
| PUT | `/<id>` | Update |
| DELETE | `/<id>` | Soft-delete |
| GET | `/<id>/tree` | Subtree hierarchy |

### Events (`/api/events`)
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | List |
| POST | `/` | Create |
| GET | `/<id>` | Detail |
| PUT | `/<id>` | Update |
| DELETE | `/<id>` | Soft-delete |

### Reminders (`/api/reminders`)
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | List |
| POST | `/` | Create |
| PUT | `/<id>` | Update |
| DELETE | `/<id>` | Soft-delete |
| POST | `/<id>/done` | Mark completed |
| GET | `/upcoming` | Due within N hours |

### Documents (`/api/documents`)
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | List |
| POST | `/` | Create |
| GET | `/<id>` | Detail |
| PUT | `/<id>` | Update |
| DELETE | `/<id>` | Soft-delete |
| GET | `/expiring` | Expiring within 90 days |

### Uploads (`/api/uploads`)
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/` | Upload file → queue extraction |
| GET | `/` | List uploads |
| GET | `/<id>` | Detail |
| GET | `/<id>/download` | Download file |
| DELETE | `/<id>` | Soft-delete |
| POST | `/<id>/reprocess` | Re-queue failed |
| GET | `/queue` | Pending/failed queue |
| GET | `/summary` | Upload stats |

### Categories (`/api/categories`)
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | List categories |
| POST | `/` | Create (admin) |
| PUT | `/<id>` | Update (admin) |
| GET | `/<id>/assets` | Assets in category |

### Tags (`/api/tags`)
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | List all tags |
| POST | `/` | Create tag |
| DELETE | `/<id>` | Delete tag |
| GET | `/search` | Autocomplete search |

### Quran (`/api/quran`)
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/surahs` | List surahs |
| GET | `/surahs/<id>/stream` | Stream audio |
| POST | `/listen` | Log session |
| GET | `/history` | Listen history |

### Knowledge (`/api/knowledge`)
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | List triples |
| POST | `/` | Create triple |
| GET | `/<id>` | Detail |
| DELETE | `/<id>` | Soft-delete |
| GET | `/graph/<type>/<id>` | Entity graph |
| GET | `/search` | Search triples |

### Query (`/api/query`)
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/` | Text question → NLP → answer |
| POST | `/voice` | Audio question → STT → answer + TTS |

### Zakat (`/api/zakat`)
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/due` | Zakat due calculation |
| GET | `/paid` | Payments this year |
| GET | `/summary` | Due vs paid vs remaining |
| POST | `/pay` | Record payment |

### Tax (`/api/tax`)
| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/assets` | Tax assets with depreciation |
| GET | `/report` | Annual tax report |

---

## Implementation Order (Recommended)

1. **Auth** — register, login, JWT (unblocks everything)
2. **User** — profile CRUD
3. **Category + Currency** — seed data
4. **Person + Location** — core entities
5. **Notes + Tags** — diary entries with M:M
6. **Transactions + Assets** — financial tracking
7. **Events + Reminders** — scheduling
8. **Documents** — document management
9. **Uploads + File Processing** — extraction pipeline
10. **Voice** — STT + NLP integration
11. **Query** — RAG pipeline
12. **Knowledge Triples** — graph features
13. **Zakat + Tax** — financial reports
14. **Quran** — audio features
15. **Background Jobs** — automation
