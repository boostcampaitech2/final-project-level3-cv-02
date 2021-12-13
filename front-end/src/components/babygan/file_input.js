import { useState, useEffect } from "react";

import { Box, Button, Card } from "@mui/material";
const FileInput = (props) => {
  let defaultImgUrl = "static/images/user_male.png";
  if (props.gender == "여성") defaultImgUrl = "static/images/user_woman.png";

  return (
    <div style={{ textAlign: "center", display: "flex; flex-direction: column" }}>
      <h2>{props.gender}</h2>
      {!props.imgurl && !props.imageSelected && (
        <Box>
          <div style={{ width: "100%", height: 500 }}>
            {<img src={defaultImgUrl} width="80%" height="500px" />}
          </div>
        </Box>
      )}
      {props.imgurl && props.imageSelected && (
        <Box style={{ width: "100%", height: 500 }}>
          {/* <Box mt={2} textAlign="center"> */}
          <img src={props.imgurl} alt={props.imageSelected.name} width="100%" height="500px" />
        </Box>
      )}

      <input
        accept="image/*"
        type="file"
        id={props.id}
        style={{ display: "none" }}
        onChange={(e) => props.onChangeImage(e.target.files[0])}
      />
      <label htmlFor={props.id}>
        <Button variant="contained" color="primary" component="span">
          Upload Image
        </Button>
      </label>
    </div>
  );
};

export default FileInput;
