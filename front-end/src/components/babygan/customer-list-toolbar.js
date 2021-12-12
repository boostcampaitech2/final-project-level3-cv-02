import { useState, useEffect } from "react";
import {
  Box,
  Button,
  Card,
  CardContent,
  TextField,
  InputAdornment,
  SvgIcon,
  Typography,
} from "@mui/material";
import { Search as SearchIcon } from "../../icons/search";
import { Upload as UploadIcon } from "../../icons/upload";
import { Download as DownloadIcon } from "../../icons/download";
import FileInput from "./file_input";

export const CustomerListToolbar = (props) => {
  const [firstSelectedImage, setFirstSelectedImage] = useState(null);
  const [firstImageUrl, setFirstImageUrl] = useState(null);
  const [secondSelectedImage, setSecondSelectedImage] = useState(null);
  const [secondImageUrl, setSecondImageUrl] = useState(null);
  const [comment, setComment] = useState(null);
  const handleChange = (event) => {
    setComment(event.target.value);
  };

  useEffect(() => {
    if (firstSelectedImage) {
      setFirstImageUrl(URL.createObjectURL(firstSelectedImage));
    }
  }, [firstSelectedImage]);

  useEffect(() => {
    if (secondSelectedImage) {
      setSecondImageUrl(URL.createObjectURL(secondSelectedImage));
    }
  }, [secondSelectedImage]);

  return (
    <Box {...props}>
      <Box
        sx={{
          alignItems: "center",
          display: "flex",
          flexWrap: "wrap",
          m: -1,
        }}
      >
        <div style={{ width: "50%", maxHeight: "35%", height: "35%", padding: "0 5%" }}>
          <FileInput
            id={1}
            gender={"남성"}
            imgurl={firstImageUrl}
            imageSelected={firstSelectedImage}
            onChangeImage={setFirstSelectedImage}
          />
        </div>
        <div style={{ width: "50%", height: "35%", padding: "0 5%" }}>
          <FileInput
            gender={"여성"}
            id={2}
            imgurl={secondImageUrl}
            imageSelected={secondSelectedImage}
            onChangeImage={setSecondSelectedImage}
          />
        </div>
        <div style={{ margin: "100px 0px", width: "100%", textAlign: "center" }}>
          <Button variant="contained">아기 얼굴 확인하기</Button>
        </div>
        <div
          style={{
            marginTop: 100,
            width: "100%",
            height: "60%",
            padding: "0 5%",
            textAlign: "center",
            display: "flex; flex-direction: column",
          }}
        >
          <h2>결과</h2>
          <img
            src="static/images/baby.png"
            // style={{ width: 200, height: 200 }}
            style={{ width: "50%", height: "50%" }}
          ></img>
        </div>
        <div
          style={{
            width: "100%",
            height: 280,
            padding: "0 2%",
            textAlign: "center",
            display: "flex; flex-direction: column",
          }}
        >
          <div style={{ textAlign: "center", width: "100%", height: 200 }}>
            <TextField
              id="outlined-multiline-static"
              label="우리아기를 자랑해보세요!"
              multiline
              style={{ marginBottom: 40, width: "50%" }}
              value={comment}
              onChange={handleChange}
              rows={7}
              defaultValue="우리아기는 연예인가능함"
            />
          </div>
          <Button style={{ marginTop: 30, width: "30%" }} variant="contained">
            공유하기
          </Button>
        </div>
      </Box>
    </Box>
  );
};
