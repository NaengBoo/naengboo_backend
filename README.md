# naengboo_backend
냉장고를 부탁해 프로젝트 백 &amp; AI


# Spring Boot meals & fridge API

Spring Boot로 만든 간단한 API 백엔드입니다.  
프론트엔드 개발자가 API를 쉽게 테스트할 수 있도록 H2 인메모리 데이터베이스를 사용합니다.

---

## ✅ 실행 전 준비사항

### 1. Java 설치 (필수)

- Java 21 이상.
- 설치 안 되어 있다면 아래 링크에서 설치하세요:

👉 [https://adoptium.net/](https://adoptium.net/) 에서 JDK 21 설치

설치 후 버전 확인:

```bash
java -version
```

2. 서버 실행
```bash
./gradlew bootRun
```

실행 후 서버는 http://localhost:8080에서 동작합니다.


✅ H2 DB 콘솔 접속
접속 주소: http://localhost:8080/h2-console

JDBC URL: jdbc:h2:mem:testdb

Username: sa

Password: (비워둠)

