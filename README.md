# (1차 과제) 소셜 미디어 통합 Feed 서비스

## Table of Contents
- 개요
- Skils
- Installation & Run
- API Reference
- 프로젝트 진행 및 이슈 관리
- 구현과정(설계 및 의도)
- TIL 및 회고
- Authors

## 개요
본 서비스는 유저 계정의 해시태그(”#dani”) 를 기반으로 `인스타그램`, `스레드`, `페이스북`, `트위터` 등 복수의 SNS에 게시된 게시물 중 유저의 해시태그가 포함된 게시물들을 하나의 서비스에서 확인할 수 있는 통합 Feed 어플리케이션 입니다.

이를 통해 본 서비스의 고객은 하나의 채널로 유저(”#dani”), 또는 브랜드(”#danishop”) 의 SNS 노출 게시물 및 통계를 확인할 수 있습니다.

**유저히스토리**

- 유저는 계정(추후 해시태그로 관리), 비밀번호, 이메일로 **가입요청**을 진행합니다.
- 가입 요청 시, 이메일로 발송된 코드를 입력하여 **가입승인**을 받고 서비스 이용이 가능합니다.
- 서비스 로그인 시, 메뉴는 **통합 Feed** 단일 입니다. ****
- 통합 Feed 에선  `인스타그램`, `스레드`, `페이스북`, `트위터` 에서 유저의 계정이 태그된 글들을 확인합니다.
- 또는, 특정 해시태그(1건)를 입력하여, 해당 해시태그가 포함된 게시물들을 확인합니다.
- 유저는 본인 계정명 또는 특정 해시태그 일자별, 시간별 게시물 갯수 통계를 확인할 수 있습니다.


## 요구사항

- 사용자 회원가입
- 사용자 가입승인
- 사용자 로그인
- 게시물 목록
- 게시물 상세
- 게시물 좋아요
- 게시물 공유
- 통계


## API Documentation
- ![APIdoc](/asset/api_doc.png)

## Skils
가상환경: ![venv](https://img.shields.io/badge/%EA%B0%80%EC%83%81%ED%99%98%EA%B2%BD-venv-red)

언어 및 프레임워크: ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)

데이터 베이스: ![MySQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white)

배포 : ![배포](https://img.shields.io/badge/%EB%B0%B0%ED%8F%AC-None-gray)


## Installation & Run
- MySQL DB 세팅
    - DATABASE생성
        - DB_NAME=feed
        - DB_HOST=localhost
        - DB_PORT=3306

    - USER생성
        - DB_USER=wanted
        - 권한주기

- python 환경 설치
```shell
python -m venv venv
source venv/Scripts/activate ## 가상환경 실행. git bash기준
pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
```

## 초기 설정 : 데이터
- Posts 테이블과 HashTags 테이블에 대한 더미 데이터는 csv 파일로 제공합니다.
- Contributer : 강석영, 유진수
- 

## 프로젝트 진행 및 이슈 관리
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white) 의 `ISSUE`로 등록해서 관리했습니다.

GitHub 이슈 페이지 링크 : [링크](https://github.com/I-deul-of-zoo/wanted-feed-service/issues)


## 구현과정(설계 및 의도)

1. 환경설정
    - 공통의 환경을 구축하는 것이 중요하다고 생각해서 첫 팀 프로젝트인 만큼 환경설정 부분에서 시간 소요가 많았습니다.
    - 아래와 같이 환경설정을 시도했지만 결국 로컬에서 직접 가상환경을 설정해 사용하는 것으로 결정했습니다.
        > Poetry 적용한 Docker로 환경설정 > pip 이용한 Docker 환경설정 > 개인 환경설정
    - 결국 Docker는 이용하지 못했지만 다음 프로젝트에는 꼭 도커를 적용한 환경 설정을 성공시킬 수 있는 경험치가 쌓였다고 생각합니다.

2. RESTful API 설계
    - 요구사항을 파악한 뒤 업무를 어떤 방식으로 나눌지 논의하고 그 기준에 따라 GitHub의 Issue에 등록해서 업무를 구분하고 분배했습니다.


## TIL 및 회고
- Discord로 모여 매일 9:00, 14:00 에 모여 진행상황과 공부한 것을 공유했습니다.


## Authors

|이름|github주소|
|---|---------|
|강석영|https://github.com/mathtkang|
|김수현|https://github.com/tneoeo2|
|오동혁|https://github.com/airhac|
|유진수|https://github.com/YuJinsoo|
