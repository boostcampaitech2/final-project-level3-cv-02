# πΆπ» MLOpsλ₯Ό νμ©ν 2μΈ μΌκ΅΄ μμΈ‘ μλΉμ€
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-6-orange.svg?style=flat-square)](#Team)
<!-- ALL-CONTRIBUTORS-BADGE:END -->
<img src="https://img.shields.io/badge/react-61DAFB?style=for-the-badge&logo=react&logoColor=white&style=flat"> <img src="https://img.shields.io/badge/nextjs-000000?style=for-the-badge&logo=next.js&logoColor=white&style=flat"> <img src="https://img.shields.io/badge/MaterialDesign-757575?style=for-the-badge&logo=material-design&logoColor=white&style=flat"> <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white&style=flat"> <img src="https://img.shields.io/badge/Mysql-4479a1?style=for-the-badge&logo=mysql&logoColor=white&style=flat"> <img src="https://img.shields.io/badge/AWS_S3-569A31?style=for-the-badge&logo=Amazon-s3&logoColor=white&style=flat"> <img src="https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white&style=flat"> <img src="https://img.shields.io/badge/Airflow-017CEE?style=for-the-badge&logo=apache-airflow&logoColor=white&style=flat"> <img src="https://img.shields.io/badge/Tensorflow-ff6f00?style=for-the-badge&logo=tensorflow&logoColor=white&style=flat"> <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white&style=flat"> 
## πΌ Project Summary
- StyleGAN κΈ°λ°μ μμ± λͺ¨λΈμΈ BabyGANμ μ¬μ©νμ¬ λ μ¬λμ μΌκ΅΄μ μλ ₯μΌλ‘ λ°μ 2μΈ μΌκ΅΄μ ν©μ±νλ μλΉμ€μλλ€.
- λͺ¨λΈ μλΉκ³Ό λ°°ν¬ κ²½νμ μν νλ‘μ νΈμ΄λ©°, <b> FastAPI, Airflow, AWS, Docker </b> λ₯Ό μ¬μ©νμμ΅λλ€.

<br/>

## πΌ Repository Structure
- Front-end, Back-end, Airflow, Docker


```
βββ README.md
βββ .env
βββ airflow
βΒ Β  βββ dag
βββ back-end
βΒ Β  βββ api
βΒ Β  βΒ Β  βββ controller
βΒ Β  βΒ Β  βββ model
βΒ Β  βΒ Β  βββ service
βΒ Β  βββ babygan
βΒ Β  βββ main
βββ docker
βββ front-end
```

<br/>

## πΌ Architecture Flow Map
![final_project](https://user-images.githubusercontent.com/58676931/146967626-1c5a4b50-f97f-45be-8d44-fc7b59daf876.png)

<br/>

## πΌ Demo 
> [λ°λͺ¨λ§ν¬](http://12war-front.s3-website.ap-northeast-2.amazonaws.com/) (12μ 25μΌ μ΄νλ‘ babyganμ inference κΈ°λ₯μ΄ μ€λ¨λ©λλ€.)
- Dashboard : airflowμ batchjobμ λΆμν κ²°κ³Όλ₯Ό λ³΄μ¬μ£Όλ νμ΄μ§
    <img width="1000" alt="dashboard" src="https://user-images.githubusercontent.com/58676931/147118544-919f9a8d-cfe8-4371-966b-69dace308d7f.png">
- BabyGAN : μ¬μ©μμ μλ ₯ μ΄λ―Έμ§μ λ°λ₯Έ μΈνΌλ°μ€ κ²°κ³Όλ¬Όμ λ³΄μ¬μ£Όλ νμ΄μ§
    * input
    <img width="1000" alt="babygan_input" src="https://user-images.githubusercontent.com/58676931/147118555-91e8a580-676a-4e34-abe2-04488e9c4aad.png">
    * output & share
    <img width="1220" alt="αα³αα³αα΅α«αα£αΊ 2021-12-23 αα©αα₯α« 12 43 29" src="https://user-images.githubusercontent.com/58676931/147119056-05b2351f-b0ef-4640-9c26-f400da4d6088.png">
- Gallery : μ¬μ©μκ° κ³΅μ ν κ²°κ³Όλ¬Όμ λͺ¨μ λ³Ό μ μλ νμ΄μ§
    <img width="1000" alt="αα³αα³αα΅α«αα£αΊ 2021-12-23 αα©αα₯α« 12 45 50" src="https://user-images.githubusercontent.com/58676931/147118585-d79119b7-7c3e-4518-acd3-35d92f1f621a.png">

<br/>

## πΌ Contributors <a name = 'Team'>

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/hojihun5516"><img src="https://avatars.githubusercontent.com/u/32387358?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Jihun Heo</b></sub></a><br /><a href="#projectManagement" title="Project Management">π</a> <a href="https://github.com/boostcampaitech2/final-project-level3-cv-02/commits/develop?author=hojihun5516" title="Code">π»</a> <a href="https://github.com/boostcampaitech2/final-project-level3-cv-02/commits/develop?author=hojihun5516" title="Documentation">π</a></td>
    <td align="center"><a href="https://github.com/JODONG2"><img src="https://avatars.githubusercontent.com/u/61579014?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Hyundong Jo</b></sub></a><br /><a href="https://github.com/boostcampaitech2/final-project-level3-cv-02/commits/develop?author=JODONG2" title="Code">π»</a> <a href="https://github.com/boostcampaitech2/final-project-level3-cv-02/commits/develop?author=JODONG2" title="Documentation">π</a></td>
    <td align="center"><a href="https://github.com/sejongjeong"><img src="https://avatars.githubusercontent.com/u/37677446?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Sejong Jeong</b></sub></a><br /><a href="https://github.com/boostcampaitech2/final-project-level3-cv-02/commits/develop?author=sejongjeong" title="Code">π»</a> <a href="https://github.com/boostcampaitech2/final-project-level3-cv-02/commits/develop?author=sejongjeong" title="Documentation">π</a></td>
    <td align="center"><a href="https://github.com/Yiujin"><img src="https://avatars.githubusercontent.com/u/43367868?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Yujin Lee</b></sub></a><br /><a href="https://github.com/boostcampaitech2/final-project-level3-cv-02/commits/develop?author=Yiujin" title="Code">π»</a> <a href="https://github.com/boostcampaitech2/final-project-level3-cv-02/commits/develop?author=Yiujin" title="Documentation">π</a></td>
    <td align="center"><a href="https://github.com/binlee52"><img src="https://avatars.githubusercontent.com/u/24227863?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Hanbin Lee</b></sub></a><br /><a href="https://github.com/boostcampaitech2/final-project-level3-cv-02/commits/develop?author=binlee52" title="Code">π»</a> <a href="https://github.com/boostcampaitech2/final-project-level3-cv-02/commits/develop?author=binlee52" title="Documentation">π</a></td>
    <td align="center"><a href="https://github.com/swkim-sm"><img src="https://avatars.githubusercontent.com/u/58676931?v=4?s=100" width="100px;" alt=""/><br /><sub><b>Seowon Kim</b></sub></a><br /><a href="https://github.com/boostcampaitech2/final-project-level3-cv-02/commits/develop?author=swkim-sm" title="Code">π»</a> <a href="https://github.com/boostcampaitech2/final-project-level3-cv-02/commits/develop?author=swkim-sm" title="Documentation">π</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!


<br/>

## πΌ Reference

- [BabyGAN](https://github.com/tg-bomze/BabyGAN)
- [FastAPI](https://fastapi.tiangolo.com/)