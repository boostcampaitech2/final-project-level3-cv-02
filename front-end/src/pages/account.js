import Head from "next/head";
import { Box, Container, Grid, Typography } from "@mui/material";
import { AccountProfile } from "../components/account/account-profile";
import { AccountProfileDetails } from "../components/account/account-profile-details";
import { DashboardLayout } from "../components/dashboard-layout";

const users = [
  {
    avatar: "/static/images/contributor/jihoon.jpg",
    name: "허지훈",
    github: "https://github.com/hojihun5516",
    blog: "https://modernflow.tistory.com/",
  },
  {
    avatar: "/static/images/contributor/sejong.png",
    name: "정세종",
    github: "https://github.com/sejongjeong",
    blog: "sejongjeong@kakao.com",
  },
  {
    avatar: "/static/images/contributor/yujin.jpg",
    name: "이유진",
    github: "https://github.com/Yiujin",
    blog: "https://velog.io/@dust_potato",
  },
  {
    avatar: "/static/images/contributor/seowon.jpg",
    name: "김서원",
    github: "https://github.com/swkim-sm",
    blog: "https://seoftware.tistory.com/",
  },
  {
    avatar: "/static/images/contributor/hyundong.jpg",
    name: "조현동",
    github: "https://github.com/JODONG2",
    blog: "whgusehd96@gmail.com",
  },
  {
    avatar: "/static/images/contributor/hanbeen.jpg",
    name: "이한빈",
    github: "https://github.com/binlee52",
    blog: "hanbin@kakao.com",
  },
];
const listItem = users.map((user) => (
  <>
    <AccountProfile
      style={{
        marginRight: 50,
        minWidth: 300,
        marginBottom: 50,
      }}
      user={user}
    ></AccountProfile>
  </>
));
const Account = () => {
  return (
    <>
      <Head>
        <title>team</title>
      </Head>
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          py: 8,
        }}
      >
        <Container maxWidth="lg">
          <Typography sx={{ mb: 3 }} variant="h4">
            팀원 소개
          </Typography>
          <Grid style={{ width: "100%" }}>
            <Grid
              style={{
                flexWrap: "wrap",
                display: "flex",
                width: "100%",
                flexBiasis: "100%",
              }}
            >
              {listItem}
            </Grid>
          </Grid>
        </Container>
      </Box>
    </>
  );
};

Account.getLayout = (page) => <DashboardLayout>{page}</DashboardLayout>;

export default Account;
