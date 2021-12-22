# 👶🏻 MLOps를 활용한 2세 얼굴 예측 서비스
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-6-orange.svg?style=flat-square)](#Team)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

## 🍼 Project Summary
- StyleGAN 기반의 생성 모델인 BabyGAN을 사용하여 두 사람의 얼굴을 입력으로 받아 2세 얼굴을 합성하는 서비스입니다.
- 모델 서빙과 배포 경험을 위한 프로젝트이며, <b> FastAPI, Airflow, AWS, Docker </b> 를 사용하였습니다.

<br/>

## 🍼 Repository Structure
- Front-end, Back-end, Airflow, Docker


```
├── README.md
├── .env
├── airflow
│   └── dag
├── back-end
│   ├── api
│   │   ├── controller
│   │   ├── model
│   │   └── service
│   ├── babygan
│   └── main
├── docker
└── front-end
```

<br/>

## 🍼 Architecture Flow Map
![final_project](https://user-images.githubusercontent.com/58676931/146967626-1c5a4b50-f97f-45be-8d44-fc7b59daf876.png)

<br/>

## 🍼 Demo 
> [데모링크](http://12war-front.s3-website.ap-northeast-2.amazonaws.com/) (12월 25일 이후로 babygan의 inference 기능이 중단됩니다.)
- Dashboard : airflow의 batchjob을 분석한 결과를 보여주는 페이지
    <img width="1000" alt="dashboard" src="https://user-images.githubusercontent.com/58676931/147118544-919f9a8d-cfe8-4371-966b-69dace308d7f.png">
- BabyGAN : 사용자의 입력 이미지에 따른 인퍼런스 결과물을 보여주는 페이지
    * input
    <img width="1000" alt="babygan_input" src="https://user-images.githubusercontent.com/58676931/147118555-91e8a580-676a-4e34-abe2-04488e9c4aad.png">
    * output & share
    <img width="1220" alt="스크린샷 2021-12-23 오전 12 43 29" src="https://user-images.githubusercontent.com/58676931/147119056-05b2351f-b0ef-4640-9c26-f400da4d6088.png">
- Gallery : 사용자가 공유한 결과물을 모아 볼 수 있는 페이지
    <img width="1000" alt="스크린샷 2021-12-23 오전 12 45 50" src="https://user-images.githubusercontent.com/58676931/147118585-d79119b7-7c3e-4518-acd3-35d92f1f621a.png">

<br/>

## 🍼 Contributors <a name = 'Team'>

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/hojihun5516"><img src="https://avatars.githubusercontent.com/u/32387358?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Jihun Heo</b></sub></a><br /><a href="#projectManagement" title="Project Management">📆</a> <a href="https://github.com/boostcampaitech2/final-project-level3-cv-02/commits/develop?author=hojihun5516" title="Code">💻</a> <a href="https://github.com/boostcampaitech2/final-project-level3-cv-02/commits/develop?author=hojihun5516" title="Documentation">📖</a></td>
    <td align="center"><a href="https://github.com/JODONG2"><img src="https://avatars.githubusercontent.com/u/61579014?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Hyundong Jo</b></sub></a><br /><a href="https://github.com/boostcampaitech2/final-project-level3-cv-02/commits/develop?author=JODONG2" title="Code">💻</a> <a href="https://github.com/boostcampaitech2/final-project-level3-cv-02/commits/develop?author=JODONG2" title="Documentation">📖</a></td>
    <td align="center"><a href="https://github.com/sejongjeong"><img src="https://avatars.githubusercontent.com/u/37677446?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Sejong Jeong</b></sub></a><br /><a href="https://github.com/boostcampaitech2/final-project-level3-cv-02/commits/develop?author=sejongjeong" title="Code">💻</a> <a href="https://github.com/boostcampaitech2/final-project-level3-cv-02/commits/develop?author=sejongjeong" title="Documentation">📖</a></td>
    <td align="center"><a href="https://github.com/Yiujin"><img src="https://avatars.githubusercontent.com/u/43367868?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Yujin Lee</b></sub></a><br /><a href="https://github.com/boostcampaitech2/final-project-level3-cv-02/commits/develop?author=Yiujin" title="Code">💻</a> <a href="https://github.com/boostcampaitech2/final-project-level3-cv-02/commits/develop?author=Yiujin" title="Documentation">📖</a></td>
    <td align="center"><a href="https://github.com/binlee52"><img src="https://avatars.githubusercontent.com/u/24227863?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Hanbin Lee</b></sub></a><br /><a href="https://github.com/boostcampaitech2/final-project-level3-cv-02/commits/develop?author=binlee52" title="Code">💻</a> <a href="https://github.com/boostcampaitech2/final-project-level3-cv-02/commits/develop?author=binlee52" title="Documentation">📖</a></td>
    <td align="center"><a href="https://github.com/swkim-sm"><img src="https://avatars.githubusercontent.com/u/58676931?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Seowon Kim</b></sub></a><br /><a href="https://github.com/boostcampaitech2/final-project-level3-cv-02/commits/develop?author=swkim-sm" title="Code">💻</a> <a href="https://github.com/boostcampaitech2/final-project-level3-cv-02/commits/develop?author=swkim-sm" title="Documentation">📖</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!


<br/>

## 🍼 Reference

- [BabyGAN](https://github.com/tg-bomze/BabyGAN)
- [FastAPI](https://fastapi.tiangolo.com/)