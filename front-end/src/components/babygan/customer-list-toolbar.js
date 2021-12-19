import { useState, useEffect } from "react";
import axios, { AxiosResponse } from "axios";
import {
  Box,
  Button,
  Card,
  CardContent,
  TextField,
  InputAdornment,
  SvgIcon,
  Typography,
  CircularProgress,
} from "@mui/material";
import { Search as SearchIcon } from "../../icons/search";
import { Upload as UploadIcon } from "../../icons/upload";
import { Download as DownloadIcon } from "../../icons/download";
import FileInput from "./file_input";
import CircularIntegration from "./progressbar";

export const CustomerListToolbar = (props) => {
  const [firstSelectedImage, setFirstSelectedImage] = useState(null);
  const [firstImageUrl, setFirstImageUrl] = useState(null);
  const [secondSelectedImage, setSecondSelectedImage] = useState(null);
  const [secondImageUrl, setSecondImageUrl] = useState(null);
  const [comment, setComment] = useState(null);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [babyImg, setBabyImg] = useState("static/images/baby.png");

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

  const inferenceButtonClick = async (event) => {
    if (!loading) {
      setSuccess(false);
      setLoading(true);
      let bodyFormData = new FormData();
      bodyFormData.append("father_image", firstSelectedImage);
      bodyFormData.append("mother_image", secondSelectedImage);

      event.preventDefault();
      await axios
        .post(`http://3.37.197.179/uploadfiles`, bodyFormData)
        .then((response) => {
          setBabyImg(response.data.baby_image_path);
        })
        .catch((error) => {
          console.log("failed", error);
        });
      setSuccess(true);
      setLoading(false);
    }
  };

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
        <div className="upload_div">
          <FileInput
            id={1}
            gender={"남성"}
            imgurl={firstImageUrl}
            imageSelected={firstSelectedImage}
            onChangeImage={setFirstSelectedImage}
          />
        </div>
        <div className="upload_div">
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
            display: "flex",
            justifyContent: "center",
            margin: "100px 0px",
            width: "100%",
            textAlign: "center",
          }}
        >
          <CircularIntegration
            onclick={inferenceButtonClick}
            success={success}
            loading={loading}
          ></CircularIntegration>
        </div>
        <div
          style={{
            marginTop: 100,
            width: "100%",
            height: "60%",
            padding: "0 5%",
            justifyContent: "center",
            textAlign: "center",
            display: "block",
            flexDirection: "column",
          }}
        >
          <h2>결과</h2>
          <img
            src={babyImg}
            // style={{ width: 200, height: 200 }}
            style={{ margin: "auto", width: "50%", height: "50%" }}
          ></img>
        </div>
        <div
          style={{
            marginTop: 50,
            width: "100%",
            height: 280,
            padding: "0 2%",
            textAlign: "center",
            display: "block",
            flexDirection: "column",
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
