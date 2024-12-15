# Backend Project

Flask 기반 백엔드 프로젝트로, RESTful API와 Swagger UI를 제공합니다.

이 프로젝트는 사용자 인증, 채용 공고 관리, 지원서 처리 및 북마크 등 다양한 기능을 제공합니다.

## 프로젝트 URL
- **API URL**: [http://113.198.66.75:18115](http://113.198.66.75:18115)

## 주요 기능
- 사용자 인증 및 관리 (회원가입, 로그인)
- 채용 공고 CRUD
- 지원서 관리 (지원, 조회, 삭제)
- 북마크 기능 (추가/삭제, 조회)
- 필터링 및 검색 기능
- 활동 로그 조회
- 회사 목록, 정보 조회
- 회사 리뷰 추가, 삭제
- 홈페이지에 대한 피드백 조회,제출
- Swagger UI를 통한 API 문서화

## 프로젝트 실행 및 테스트 가이드

1. 프로젝트 클론

GitHub에서 프로젝트를 클론합니다

```bash
git clone <https://github.com/imsh429/backend-project.git>
cd backend-project
```

2. 환경설정

```
가상환경 생성: python3 -m venv venv
가상환경 활성화: venv\Scripts\activate
```

3. 의존성 설치

```
pip install -r requirements.txt

```

4. Postman을 사용한 테스트

현재 jcloud에서 백그라운드로 서버가 구동중이기 때문에 
http://113.198.66.75:18115 를 통해 postman으로 테스트 해 볼 수 있습니다.

아니면 clone한 프로젝트에 python run.py를 입력해서 local에서 테스트 해 볼 수도 있습니다.

<실행방법>
1) Postman 설치
2) API 엔드포인트 테스트


5. api 엔드포인트 목록

[AUTH]
POST /auth/register : 사용자 회원가입 api
POST /auth/login : 로그인 api
POST /auth/refresh : 토큰 refresh api
GET /auth/profile : 프로필 조회 api
PUT /auth/profile : 프로필 수정 api
DELETE /auth/profile : 프로필 삭제 api

[Activity-logs]
GET  /activity-logs : 사용자 활동 로그 조회 api

[Jobs]
GET /jobs : 채용 공고 목록 조회 api
POST /jobs : 채용 공고 등록 api
GET /jobs/{job_id} : 채용 공고 상세 조회 api
PUT /jobs/{job_id} : 채용 공고 수정 api
DELETE /jobs/{job_id} : 채용 공고 삭제 api

[Companies]
GET /companies : 회사 목록 조회 api
GET /companies/company_id : 회사 정보 조회 api

[Reviews]
POST /reviews : 회사 리뷰 추가 api
GET /reviews/{company_id} : 회사 리뷰 조회 api
DELETE /reviews/{review_id} : 리뷰 삭제 api

[Applications]
POST /applications : 이력서 지원하기 api
GET /applications : 지원 내역 조회 api
DELETE /applications/{application_id} : 지원 취소 api

[Bookmarks]
POST /bookmarks : 북마크 추가/제거 api
GET /bookmarks : 북마크 목록 조회 api

[FeedBack]
POST /feedback : 피드백 제출 api
GET /feedback : 피드백 조회 api


6. 크롤링 코드 실행 방법

```
python crawl_saramin.py 실행
saramin에서 크롤링 된 데이터가 saramin_python.csv로 저장됨

python csv_to_mongodb.py 실행
mongodb의 jobs컬렉션에 데이터를 집어넣음

python initialize_company.py 실행
jobs컬렉션 데이터 중 회사 정보만 companies컬렉션에 저장됨

```



