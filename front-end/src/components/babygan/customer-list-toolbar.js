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
        <div style={{ height: 280, padding: "0 5%" }}>
          <FileInput
            id={1}
            gender={"남성"}
            imgurl={firstImageUrl}
            imageSelected={firstSelectedImage}
            onChangeImage={setFirstSelectedImage}
          />
        </div>
        <div style={{ height: 280, padding: "0 5%" }}>
          <FileInput
            gender={"여성"}
            id={2}
            imgurl={secondImageUrl}
            imageSelected={secondSelectedImage}
            onChangeImage={setSecondSelectedImage}
          />
        </div>
        <div
          style={{
            height: 280,
            padding: "0 5%",
            textAlign: "center",
            display: "flex; flex-direction: column",
          }}
        >
          <h2>결과</h2>
          <img
            src="https://i1.wp.com/sharehows.com/wp-content/uploads/2017/09/0-4.jpg?fit=800%2C400&ssl=1"
            style={{ width: 200, height: 200 }}
          ></img>
        </div>
        <div
          style={{
            height: 280,
            padding: "0 2%",
            textAlign: "center",
            display: "flex; flex-direction: column",
          }}
        >
          <div style={{ width: 200, height: 200 }}>
            <TextField
              id="outlined-multiline-static"
              label="우리아기를 자랑해보세요!"
              multiline
              style={{ marginBottom: 40 }}
              value={comment}
              onChange={handleChange}
              rows={7}
              defaultValue="우리아기는 연예인가능함"
            />
            <Button variant="contained">공유하기</Button>
          </div>
        </div>
      </Box>
    </Box>
  );
};
