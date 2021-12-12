import { useState, useEffect } from "react";

import { Box, Button, Card } from "@mui/material";
const FileInput = (props) => {
  return (
    <div style={{ textAlign: "center", display: "flex; flex-direction: column" }}>
      <h2>{props.gender}</h2>
      {!props.imgurl && !props.imageSelected && (
        <Box>
          <div style={{ width: 200, height: 200 }} />
        </Box>
      )}
      {props.imgurl && props.imageSelected && (
        <Box>
          {/* <Box mt={2} textAlign="center"> */}
          <img src={props.imgurl} alt={props.imageSelected.name} width="200px" height="200px" />
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
