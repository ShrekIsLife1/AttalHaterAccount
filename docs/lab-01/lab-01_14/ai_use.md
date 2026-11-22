# Lab 1 — AI Use and Reflection

**Student:** Baptiste Carré — 69540460014 — GitHub: @ShrekIsLife1  
**LLM/agent used:** Claude (Anthropic) / Antigravity

## Selected key prompts (6–10)
| # | Prompt (summarised) | What I did with the result |
|---|---------------------|----------------------------|
| 1 | Help me initialize the project repository foundation with Node.js, Express, TypeScript and React scaffold. | Set up the root and package scripts, validated directory structure and Git branches. |
| 2 | Write the GET /api/health endpoint and Supertest integration test verifying 200 OK and status JSON. | Added health endpoint in server router and verified Supertest assertions. |
| 3 | Create the Prisma database schema for categories and write an idempotent seed script. | Ran Prisma migration and seeded initial category records in database. |
| 4 | Write the Supertest suite for GET /api/categories returning the 4 seeded categories in ID order. | Verified category ordering and schema response format. |
| 5 | Build the React frontend App component displaying the heading and fetching categories with loading/error states. | Implemented state hooks for API requests and displayed Bootstrap styled list. |
| 6 | Fix module import syntax in client tests so Vitest can mock the API methods with vi.spyOn cleanly. | Corrected the API module namespace import to allow clean test mocking. |

## Reflection
Working with the AI helped clarify complex testing patterns like mocking API calls with vi.spyOn and structuring full-stack requests. One instance where I had to manually adjust the output was correcting a minor syntax typo in the module import statement during test debugging, which allowed the test suite to pass successfully.
