import {
  Avatar,
  Box,
  Button,
  Card,
  CardActions,
  CardContent,
  Divider,
  Typography,
} from "@mui/material";

export const AccountProfile = (props) => (
  <Card {...props}>
    <CardContent>
      <Box
        sx={{
          alignItems: "center",
          display: "flex",
          flexDirection: "column",
        }}
      >
        <Avatar
          src={props.user.avatar}
          sx={{
            height: 64,
            mb: 2,
            width: 64,
          }}
        />
        <Typography color="textPrimary" gutterBottom variant="h5">
          {props.user.name}
        </Typography>
        <Typography color="textSecondary" variant="body2">
          <a href={`${props.user.github}`}>{`${props.user.github}`} </a>
        </Typography>
        <Typography color="textSecondary" variant="body2">
          {props.user.blog}
        </Typography>
      </Box>
    </CardContent>
    <Divider />
  </Card>
);
