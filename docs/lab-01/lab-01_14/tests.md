# Lab 1 — Test Plan and Evidence

All test files live under `server/tests/lab-01/` and `client/tests/lab-01/`.

| # | Tool | Test | Result |
|---|------|------|:------:|
| 1 | Supertest | GET /api/health returns 200, status=ok | ✅ Pass |
| 2 | Supertest | GET /api/categories returns 4 seeded categories in id order | 🔲 Todo |
| 3 | Vitest | Heading renders "UniMerch" | ✅ Pass |
| 4 | Vitest | Success state shows Online + category list | 🔲 Todo |
| 5 | Vitest | Error state shows Offline message | 🔲 Todo |

> Tests 2, 4 and 5 are marked `todo` — they are scaffolded but not yet implemented in this sprint (implementation is part of Issue 4 follow-up).

```bash
$ cd server && npm test -- tests/lab-01/

> unimerch-server@1.0.0 test
> vitest run tests/lab-01/

 RUN  v2.1.9 /home/meownux/Documents/SWE/Vinted/AttalHaterAccount/server

 ✓ tests/lab-01/health.test.ts (1 test) 10ms
 ↓ tests/lab-01/categories.test.ts (1 test | 1 skipped)

 Test Files  1 passed | 1 skipped (2)
      Tests  1 passed | 1 todo (2)
   Start at  20:00:18
   Duration  544ms

$ cd ../client && npm test -- tests/lab-01/App.test.tsx

> toktickit-client@1.0.0 test
> vitest run tests/lab-01/App.test.tsx

 RUN  v2.1.9 /home/meownux/Documents/SWE/Vinted/AttalHaterAccount/client

 ✓ tests/lab-01/App.test.tsx (3 tests | 2 skipped) 29ms

 Test Files  1 passed (1)
      Tests  1 passed | 2 todo (3)
   Start at  20:00:04
   Duration  657ms
```
