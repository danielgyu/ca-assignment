### Requirements
- 데이터베이스 관련 필요사항: `initdb.sql`

### How To Run
- `poetry install`
- `poetry run pytest cookapps/tests` (테스트)
- `poetry run uvicorn "cookapps.app:app"` (서버)
