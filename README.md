# 소셜 미디어 통합 Feed 서비스

## 목차
- [개요](#개요)
- [요구사항](#요구사항)
- [개발환경세팅](#개발환경세팅)
- [Installation & Run](#Installation)
- [ER-Diagram](#ER-Diagram)
- [API Documentation](#API)
- [프로젝트 진행 및 이슈 관리](#프로젝트)
- [구현과정(설계 및 의도)](#구현과정)
- [TIL 및 회고](#TIL)
- [Authors](#Authors)


## 📃 프로젝트 개요
- 본 서비스는 유저 계정의 해시태그(#seokyoung)를 기반으로 `인스타그램`, `스레드`, `페이스북`, `트위터` 등 **복수의 SNS에 게시된 게시물 중 유저의 해시태그가 포함된 게시물들을 하나의 서비스에서 확인**할 수 있는 통합 Feed 어플리케이션 입니다.
- 이를 통해 본 서비스의 고객은 하나의 채널로 유저(#seokyoung), 또는 브랜드(#seokyoungshop) 의 SNS 노출 게시물 및 통계를 확인할 수 있습니다.


## 🍄 요구사항

#### 유저 히스토리
- 유저는 계정(추후 해시태그로 관리), 비밀번호, 이메일로 **가입요청**을 진행합니다.
- 가입 요청 시, 이메일로 발송된 코드를 입력하여 **가입승인**을 받고 서비스 이용이 가능합니다.
- 서비스 로그인 시, 메뉴는 **통합 Feed** 단일 입니다. ****
- 통합 Feed 에선  `인스타그램`, `스레드`, `페이스북`, `트위터` 에서 유저의 계정이 태그된 글들을 확인합니다.
- 또는, 특정 해시태그(1건)를 입력하여, 해당 해시태그가 포함된 게시물들을 확인합니다.
- 유저는 본인 계정명 또는 특정 해시태그 일자별, 시간별 게시물 갯수 통계를 확인할 수 있습니다.

#### 사용자 회원가입
- `계정` 은 unique 합니다.
- `이메일` 은 올바른 이메일 구조인지 검증 되어야 합니다.
- `비밀번호` 는 아래 중 2 가지 이상의 제약 조건을 가지며, 암호화 되어 저장됩니다.
- 제약조건
    > 다른 개인 정보와 유사한 비밀번호는 사용할 수 없습니다.
        비밀번호는 최소 10자 이상이어야 합니다.
        통상적으로 자주 사용되는 비밀번호는 사용할 수 없습니다.
        숫자로만 이루어진 비밀번호는 사용할 수 없습니다.
        숫자, 문자, 특수문자 중 2가지 이상을 포함해야 합니다.
        다른 개인 정보와 유사한 비밀번호는 사용할 수 없습니다.
        이전 비밀번호와 동일하게 설정할 수 없습니다.
        3회 이상 연속되는 문자 사용이 불가합니다.

#### 사용자 가입승인
- 가입요청시, 유저가 생성되고 6자리의 랜덤한 코드가 입력한 이메일로 발송됩니다.
    > 현재는 email 직접 구현이 되지 않고, 코드상으로만 구현되어 있습니다.
- `계정`, `인증코드` 가 올바르게 입력되었을 시 가입승인 이 되어 서비스 이용이 가능합니다.

#### 사용자 로그인
- `계정`, `비밀번호`로 로그인시 `JWT` 가 발급됩니다.
- **이후 모든 API 요청 Header 에 `JWT` 가 항시 포함되며, `JWT` 유효성을 검증합니다.**

#### 게시물 목록
- 아래 쿼리 파라미터를 사용 가능합니다.
    - `hashtag`: [string] 정확히 **일치**하는 값만 검색
    - `type`: [string] SNS의 종류를 입력, 미입력시 모든 SNS 검색
    - `order_by`: [string] `created_at`, `updated_at`, `like_count`, `share_count`,`view_count` 가 사용 가능합니다. `오름차순`, `내림차순` 모두 가능
    - `search_by`: [string] `title` 과 `content` 혹은 둘 동시`title,content` (default = `title,content`)
    - `search`: [string] `search_by`영역에서 검색할 키워드. 포함되는 것
    - `page_count`
    - `page`
- 게시물 목록 API에선 content 는 최대 20자 까지만 포함됩니다. 
- 한 번에 10개씩(default) 불러오도록 페이지네이션을 구현하였습니다.

#### 게시물 상세
- 유저가 게시물 1개 확인 시 사용되는 API
- 모든 필드 값을 확인 합니다.
- API 호출 시, 해당 게시물 `view_count`가 1 증가합니다.

#### 게시물 좋아요 / 취소
- facebook, twitter, instagram, thread 별 각각 명시된 API를 호출합니다. (실제 데이터는 SNS와 연동 X)
- 좋아요 호출 성공시 `response status 200`을 반환하고 `like_count`가 1 증가합니다.
- 좋아요 취소 호출 성공시 `response status 200`을 반환하고 `like_count`가 1 감소합니다.

#### 게시물 공유
- 해당 호출이 성공할 시 `response status 200` 해당 게시물의 `share_count`가 1 증가합니다.
- 횟수 제한이 없습니다. 한 유저가 몇 번의 공유를 호출하든 공유 수는 계속 상승합니다.
    
#### 통계
- 아래 쿼리 파라미터를 사용 가능합니다.
    - `hashtag`: [string] default = 본인계정
    - `type`: [string, 열거형] `date` 혹은 `hour` (Required) 
    - `start`: [date] `2023-10-23` end의 7일전. 검색 범위 시작일
    - `end`: [date] `2023-10-30` 과 같은 형식. 검색 범위 종료일
    - `value`: [string] `count`, `view_count`, `like_count`, `share_count` 가 사용 가능(default = `count`)

<br>

## ⚙️ 개발 환경 세팅
- ![macosm1 badge](https://img.shields.io/badge/MacOS%20M1-000000.svg?style=flat&logo=macOS&logoColor=white)
- ![Visual Studio Code badge](https://img.shields.io/badge/Visual%20Studio%20Code-007ACC.svg?style=flat&logo=Visual-Studio-Code&logoColor=white)
- ![github badge](https://img.shields.io/badge/GitHub-181717.svg?style=flat&logo=GitHub&logoColor=white)
- ![venv](https://img.shields.io/badge/Virtualenv-183A61.svg?style=flat&logo=eventbrite&logoColor=black) ![docker badge](https://img.shields.io/badge/Docker-2496ED.svg?style=flate&logo=Docker&logoColor=white)
- ![postman badge](https://img.shields.io/badge/postman-FF6C37?style=flat&logo=Postman&logoColor=white)
- ![swagger badge](https://img.shields.io/badge/Swagger-85EA2D.svg?style=flat&logo=Swagger&logoColor=black)

<br>

## 🛠 기술 스택

#### Language & Framework
- ![python badge](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=Python&logoColor=white)
- ![django badge](https://img.shields.io/badge/Django-4.2-%23092E20?&logo=Django&logoColor=white)
- ![DjangoREST](https://img.shields.io/badge/Django-REST-ff1709?&logo=django&logoColor=white&color=ff1709&labelColor=gray)

#### Database
- ![MySQL badge](https://img.shields.io/badge/MySQL-4479A1.svg?&logo=MySQL&logoColor=white)


## 🥁 Installation & Run
### MySQL DB 세팅
> 
    - DATABASE생성
        - DB_NAME=feed
        - DB_HOST=localhost
        - DB_PORT=3306
    - USER생성
        - DB_USER=wanted
        - 유저에게 db권한주기

### 환경 세팅

#### 애플리케이션의 실행 방법
(전제) `python >= 3.10` 과 `mysql >= 8.0` 은 설치되어 있습니다.
```
1. python -m venv [가상환경이름]
2. source activate [가상환경이름]
3. pip install -r requirements.txt
4. python manage.py migrate
5. python manage.py runserver [port_num]
```
[참고]
- `python manage.py makemigrations` : 아직 데이터베이스에 적용되지 않음, 데이터베이스 스키마 변경사항을 기록하는 용
- `python manage.py migrate` : 위의 명령어에서 생성된 마이그레이션 파일들을 데이터베이스에 적용
(지금은 두번째 명령어만 작성하는게 맞습니다. 변경사항 없이 DB에 적용하기 위함이기 때문입니다.)
- 필요에 따라 명령어 뒤에 포트번호를 붙입니다.

#### 초기 설정 : 데이터
- Posts 테이블과 HashTags 테이블에 대한 더미 데이터는 csv 파일로 제공합니다.
- Posts 더미 데이터 위치 : `asset/dummy_posts.csv`
- HashTags 더미 데이터 위치 : `asset/dummy_hash.csv`

<br>

## 📋 E-R Diagram
<img width="800" alt="ER-Diagram" src="https://user-images.githubusercontent.com/51039577/279062267-56eb25e7-01ae-405a-8020-85496cd52a32.png">
- post(feed)의 author는 각 소셜서비스의 작성자이기 때문에, 해당 서비스의 user와는 서로 다른 객체이다. 따라서 post와 user 테이블과는 관계가 없다.
- hashtag의 목적은 search이기 때문에, 처음에는 post안에 하나의 필드로 존재했지만, 정규화/데이터 일관성/유연한 쿼리 검색을 위해 새로운 테이블로 빼내어 구현하게 되었다.
- 이메일 인증코드 등록을 위해 user테이블에 auth_code 필드를 추가했다.
    - 회원가입 API 요청으로 User 레코드를 생성할 때 auth_code가 자동 생성되어 입력됩니다.
    - 이메일 인증 API를 통해 auth_code 를 None으로 만들 수 있고, **auth_code가 None이면 인증된 유저라는 것을 확인하는 방법**으로 이용할 필드입니다.

<br>

## 📑 API Documentation
<img width="800" alt="API-Documentation" src="https://user-images.githubusercontent.com/51039577/279063514-ed88af8d-56a5-4a19-8f4e-c132487a2ba8.png">

> 아래의 토글을 열면 request/response를 확인할 수 있습니다.
<details>
<summary>1. 회원가입 API</summary>

#### Request
```plain
  POST /v1/posts/registration
```
- Auth Required: False

| Body Parameter | Type     | Description                   |
| :------------- | :------- | :---------------------------- |
| `username`     | `string` | **Required**. 아이디(해시태그) |
| `email`        | `string` | **Required**.                 |
| `password1`    | `string` | **Required**.                 |
| `password1`    | `string` | **Required**.                 |

#### Response
```http
    HTTP 201 Created
    Allow: POST, OPTIONS
    Content-Type: application/json
    Vary: Accept

    [{
    "access": "eyJh...",
    "refresh": "eyJhbGci...",
    "user": {
        "pk": 2,
        "username": "user2",
        "email": "user1@gmail.com",
        "first_name": "",
        "last_name": ""
    }
}
    ]
```
</details>
<details>
<summary>2. JWT로그인 API</summary>

#### Request
```plain
  POST /v1/auth/login
```
- Auth Required: False

| Body Parameter | Type     | Description                   |
| :------------- | :------- | :---------------------------- |
| `username`     | `string` | **Required**. 아이디(해시태그) |
| `auth_code`    | `string` | **Required**. 승인코드         |

#### Response
```http
    HTTP 200 OK
    Allow: POST, OPTIONS
    Content-Type: application/json
    Vary: Accept

    {
        "access": "eyJhbG...."
        "refresh": "eyJhbG....",
        "user": {
            "pk": 1,
            "username": "testuser",
            "email": "testuser@email.com",
            "first_name": "",
            "last_name": ""
        }
    }
```
</details>
<details>
<summary>3. 가입승인(인증코드) API</summary>

#### Request
```plain
  POST /v1/auth/code
```
- Auth Required: False

| Body Parameter | Type | Description          |
| :-------- | :------- | :------------------------- |
| `username` | `string` | **Required**. 아이디(해시태그) |
| `auth_code` | `string` | **Required**. 승인코드 |

#### Response
```http
    HTTP/1.1 200
    Content-Type: application/json
    {
        "message": "가입승인이 완료되었습니다."
    }
```
</details>
<details>
<summary>4. 가입승인(재전송) API</summary>

#### Request
```plain
  GET /v1/auth/code/<username>
```
- Auth Required: False

#### Response
```http
    HTTP/1.1 200
    Content-Type: application/json

    {
    "메일 전송 완료": {
        "subject": "메일제목",
        "message": "RD8W2X",
        "to": [
            "test3@test.com"
            ]
        }
    }
```
</details>
<details>
<summary>5. 로그아웃 API</summary>

#### Request
```plain
  GET /v1/auth/logout
```
- Auth Required: True

| Body Parameter | Type     | Description          |
| :------------- | :------- | :------------------------- |
| `username`     | `string` | **Required**. 아이디(해시태그) |
| `auth_code`    | `string` | **Required**. 승인코드 |

#### Response
```http
    HTTP 200 OK
    Allow: GET, POST, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept

    {
        "detail": "로그아웃되었습니다."
    }
```
</details>
<details>
<summary>6. 게시물 목록 API</summary>

#### Request
```plain
  GET /v1/posts/
  example) GET /v1/posts/?hashtag=user2&page_count=5&search=날씨
```
- Auth Required: True

#### Rquest Header
| Parameter       | Type     | Description                             |
| :-------------- | :------- | :-------------------------------------- |
| `Authorization` | `string` | **Required**. 'Bearer eyJhbGciOiJIU...' |
| `Content-Type`  | `string` | **Required**. `application/json`        |

| Query Parameter | Type     | Description                                   |
| :-------------- | :------- | :-------------------------------------------- |
| `hashtag`       | `string` | default: 계정의 username, **정확히 일치**      |
| `type`          | `string` | 미설정시 모두 검색                             |
| `order_by`      | `string` | default: `created_at` (`created_at`, `updated_at`,`like_count`,`share_count`, `view_count`)   |
| `search_by`     | `string` | default: `title,content` (`title`, `content`) |
| `search`        | `string` | 미설정시 모두 검색, **포함**                    |
| `page_count`    | `number` | default: 10                                   |
| `page`          | `number` | default: 1                                    |

#### Response
```http
    HTTP/1.1 200
    Content-Type: application/json

    {
        "count": 16,
        "next": "http://127.0.0.1:8000/v1/posts/?hashtag=user2&page=2&page_count=5",
        "previous": null,
        "results": [
            {
                "id": 1,
                "content": "오늘은 날씨가 정말 좋네요! 햇빛이 ...",
                "content_id": "XyZ4aBcD9e",
                "type": "facebook",
                "title": "facebook",
                "view_count": 1000,
                "like_count": 500,
                "share_count": 500,
                "updated_at": "2023-10-27T00:00:00",
                "created_at": "2023-10-27T00:00:00",
                "author": "author_F1"
            },
            {
                "id": 4,
                "content": "오늘은 친구들과 함께 영화를 보러 갔...",
                "content_id": "dV8fGhIu2J",
                "type": "facebook",
                "title": "facebook",
                "view_count": 1000,
                "like_count": 500,
                "share_count": 500,
                "updated_at": "2023-10-30T00:00:00",
                "created_at": "2023-10-30T00:00:00",
                "author": "author_F2"
            },
            {
                "id": 6,
                "content": "미세먼지도 적고 해도 좋아서 등산했어...",
                "content_id": "XyZ4aBcD10e",
                "type": "facebook",
                "title": "facebook",
                "view_count": 1000,
                "like_count": 500,
                "share_count": 500,
                "updated_at": "2023-11-01T00:00:00",
                "created_at": "2023-11-01T00:00:00",
                "author": "author_F4"
            },
            {
                "id": 8,
                "content": "방금 새로운 책을 다 읽었어요. 이 ...",
                "content_id": "L3mN0oP2iQ",
                "type": "facebook",
                "title": "facebook",
                "view_count": 1000,
                "like_count": 500,
                "share_count": 500,
                "updated_at": "2023-11-03T00:00:00",
                "created_at": "2023-11-03T00:00:00",
                "author": "author_F6"
            },
            {
                "id": 11,
                "content": "오늘은 날씨가 정말 좋네요! 햇빛이 ...",
                "content_id": "9pRtYqWxKz",
                "type": "instagram",
                "title": "instagram",
                "view_count": 1000,
                "like_count": 500,
                "share_count": 500,
                "updated_at": "2023-11-06T00:00:00",
                "created_at": "2023-11-06T00:00:00",
                "author": "author_I1"
            }
        ]
    }
```
</details>
<details>
<summary>7. 게시물 상세 API</summary>

#### Request
```plain
  GET /v1/posts/<int:id>
  EX) GET /v1/posts/1/
```
- Auth Required: True

#### Rquest Header
| Parameter       | Type     | Description                             |
| :-------------- | :------- | :-------------------------------------- |
| `Authorization` | `string` | **Required**. 'Bearer eyJhbGciOiJIU...' |
| `Content-Type`  | `string` | **Required**. `application/json`        |

#### Response
```http
    HTTP 200 OK
    Allow: GET, PUT, PATCH, DELETE, HEAD, OPTIONS
    Content-Type: application/json
    Vary: Accept

    {
        "id": 1,
        "content": "오늘은 날씨가 정말 좋네요! 햇빛이 ...",
        "content_id": "XyZ4aBcD9e",
        "type": "facebook",
        "title": "facebook",
        "view_count": 1003,
        "like_count": 501,
        "share_count": 500,
        "updated_at": "2023-10-30T22:15:19.275050",
        "created_at": "2023-10-27T00:00:00",
        "author": "author_F1"
    }
```
</details>
<details>
<summary>8. 게시물 좋아요 API</summary>

#### Request
```plain
  POST /v1/posts/<int:id>/like
  EX) POST /v1/posts/1/like
```
- Auth Required: True

#### Rquest Header
| Parameter       | Type     | Description                             |
| :-------------- | :------- | :-------------------------------------- |
| `Authorization` | `string` | **Required**. 'Bearer eyJhbGciOiJIU...' |
| `Content-Type`  | `string` | **Required**. `application/json`        |

#### Response
```http
    HTTP 200 OK
    Allow: POST, OPTIONS
    Content-Type: application/json
    Vary: Accept

    {
        "message": "facebook 게시글에 좋아요 개수가 올라갔습니다.",
        "like_count": 501
    }
```
</details>
<details>
<summary>9. 게시물 좋아요 취소 API (추가기능)</summary>

#### Request
```plain
  DELETE /v1/posts/<int:id>/like
  EX) DELETE /v1/posts/1/like
```
- Auth Required: True

#### Rquest Header
| Parameter       | Type     | Description                             |
| :-------------- | :------- | :-------------------------------------- |
| `Authorization` | `string` | **Required**. 'Bearer eyJhbGciOiJIU...' |
| `Content-Type`  | `string` | **Required**. `application/json`        |

#### Response
```http
    HTTP 200 OK
    Allow: POST, DELETE, OPTIONS
    Content-Type: application/json
    Vary: Accept

    {
        "message": "facebook 게시글에 좋아요 표시가 취소되었습니다.",
        "like_count": 499
    }
```
</details>
<details>
<summary>10. 게시물 공유 API</summary>

#### Request
```plain
  POST /v1/posts/<int:pk>/share/
  ex) /v1/posts/1/share/
```
- Auth Required: True

#### Rquest Header
| Parameter       | Type     | Description                             |
| :-------------- | :------- | :-------------------------------------- |
| `Authorization` | `string` | **Required**. 'Bearer eyJhbGciOiJIU...' |
| `Content-Type`  | `string` | **Required**. `application/json`        |

| Body Parameter | Type     | Description             |
| :------------- | :------- | :---------------------- |
| `content_id`   | `string` | **Required**. 게시글 id |
| `type`         | `string` | **Required**. SNS 타입  |

#### Response
```http
    HTTP/1.1 200
    Content-Type: application/json

    {
    "message": "공유 성공",
    "share_count": 525,
    "sns_type": "facebook",
    "url": "https://www.facebook.com/share/XyZ4aBcD9e"
    }
```
</details>
<details>
<summary>11. 통계 API</summary>

#### Request
```plain
  GET /v1/posts/statistics/?value=view_count&type=date&hashtag=사용자계정(날씨)'
```
- Auth Required: True

#### Rquest Header
| Parameter       | Type     | Description                             |
| :-------------- | :------- | :-------------------------------------- |
| `Authorization` | `string` | **Required**. 'Bearer eyJhbGciOiJIU...' |
| `Content-Type`  | `string` | **Required**. `application/json`        |

| Query Parameter | Type     | Description                               |
| :-------------- | :------- | :-----------------------------------------|
| `hashtag`       | `string` | default: 계정의 username, **정확히 일치**      |
| `type`          | `string` | **필수**, (`date`, `hour`)                    |
| `start`         | `date`   | default: 2023-10-01 과 같이 데이트 형식이며 조회 기준 시작일을 의미합니다. (오늘로 부터 7일전)                         |
| `end`           | `date`   | default: 2023-10-25 과 같이 데이트 형식이며 조회 기준 시작일을 의미합니다. (오늘 날짜)
| `value`         | `string` | default: `count` (`count`,`view_count`,`like_count`,`share_count`) |

#### Response
```http
    HTTP/1.1 200
    Content-Type: application/json

    [{
    "total": 2000, // 오늘부터 7일전 사이의 모든 게시글 조회수
    "count_dict": { // 7일전부터 오늘까지 하루당 총 조회수
        "2023-10-23": 0,
        "2023-10-24": 0,
        "2023-10-25": 0,
        "2023-10-26": 0,
        "2023-10-27": 1000,
        "2023-10-28": 0,
        "2023-10-29": 1000
    }
}
    ]
```
</details>

<br>

<!-- 
## ✅ Test Case
## 🕸 System Architecture

<br> -->


## 프로젝트 진행 및 이슈 관리
- ![GitHub](https://img.shields.io/badge/github-%23121011.svg?&logo=github&logoColor=white) 의 `ISSUE`로 등록해서 관리했습니다.
- GitHub 이슈 페이지 [링크](https://github.com/I-deul-of-zoo/wanted-feed-service/issues)

<br>

## 설계 및 구현 의도

#### 1. 환경설정
- 동일한 개발환경 구축을 위해 아래와 같이 환경설정을 진행하였습니다.
- 프로젝트 구현할 때는 로컬에서 직접 가상환경을 설정해 사용하는 것으로 결정하고, 추후 배포할 때 AWS EC2에서 docker & poetry 를 사용하기로 했습니다.
    - poetry 적용한 Docker로 환경설정 시도 > requirements.txt 이용한 Docker 환경설정 시도 > 개인 로컬에서 requirements.txt로 환경설정 세팅

#### 1-1. pyenv, docker, poetry의 목적과 사용 이유 [참고링크](https://kkangsg.tistory.com/108)
- `pyenv`
    - 로컬 개발 환경에서 python 버전 관리를 위해 사용
- `docker`
    - 애플리케이션을 컨테이너로 패키징하고 실행하는 데 사용
    - 즉, 다른 사람들과 (다양한 환경에서) 개발할 때 '같은 실행 환경을 보장하기 위해' 사용
- `poetry`
    - python 프로젝트의 종속성 관리 도구
    - `pyenv` 또는 `docker` 위에서 라이브러리 버전을 관리하기 위해 사용

#### 2. RESTful API 설계
    - 리소스 간 계층 구조를 나타내는 URI로 구현했습니다.
    - 각 API의 Response에 맞는 HTTP status code를 적절하게 사용하였고, 발생할 수 있는 에러 상황에 대한 예외처리를 진행하였습니다.

#### 3. gitmessage 사용

<br>

## TIL 및 회고
- Discord로 모여 매일 9:00, 14:00 에 모여 진행상황과 공부한 것을 공유했습니다.
- TIL 노션 페이지 [링크](https://sprinkle-piccolo-9fc.notion.site/TIL-677e52f238c0442697a3e03cc6f3edd9?pvs=4)

## 일정 관리
- 요구사항 분석 이후 작업 가능한 최소 단위의 task로 업무를 나누었습니다.
- 각 task에 대한 우선순위를 설정하고, 노션의 Timeline 기능을 사용하여 주어진 기간 동안 필수 기능과 선택 기능을 모두 구현할 수 있도록 일정 관리를 진행하였습니다.

<br>

## Authors

|이름|역할|github주소|
|---|---|---------|
|**강석영**|**팀장**|https://github.com/mathtkang|
|김수현|팀원|https://github.com/tneoeo2|
|오동혁|팀원|https://github.com/airhac|
|유진수|팀원|https://github.com/YuJinsoo|
