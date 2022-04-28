### Requirements
- 데이터베이스 관련 필요사항: `initdb.sql`

### How To Run
- `poetry install`
- `poetry run pytest cookapps/tests` (테스트)
- `poetry run uvicorn "cookapps.app:app"` (서버)

### Endpoints
- 회원가입
    - POST `localhost:8000/users/register`
    - Body json {username: string, password: string}
- 로그인
    - POST `localhost:8000/users/login`
    - Body json {username: string, password: string}
