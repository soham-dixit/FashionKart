import React from "react";
import { useState } from "react";

import {
  AppBar,
  Toolbar,
  styled,
  Box,
  Typography,
  IconButton,
  Drawer,
  List,
} from "@mui/material";

import { Menu } from "@mui/icons-material";
import AddAPhotoIcon from "@mui/icons-material/AddAPhoto";
import Search from "./Search";
import CustomButtons from "./CustomButtons";

import { Link, useNavigate } from "react-router-dom";
import axios from "../../axios/axios";
import flask from "../../axios/flask";

const StyledHeader = styled(AppBar)`
  background: #2974f0;
  height: 55px;
`;

const Component = styled(Link)`
  margin-left: 12%;
  line-height: 0;
  text-decoration: none;
  color: inherit;
`;

const SubHeading = styled(Typography)`
  font-size: 10px;
  font-style: italic;
`;

const PlusImg = styled("img")({
  width: 10,
  height: 10,
  marginLeft: 4,
});

const CustomButtonWrapper = styled("span")(({ theme }) => ({
  margin: "0 2% 0 auto",
  [theme.breakpoints.down("md")]: {
    display: "none",
  },
}));

const MenuButton = styled(IconButton)(({ theme }) => ({
  display: "none",
  [theme.breakpoints.down("md")]: {
    display: "block",
  },
}));

const Header = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const logoUrl =
    "https://static-assets-web.flixcart.com/www/linchpin/fk-cp-zion/img/flipkart-plus_8d85f4.png";
  const subUrl =
    "https://static-assets-web.flixcart.com/fk-p-linchpin-web/fk-cp-zion/img/plus_aef861.png";

  const [open, setOpen] = useState(false);

  const handleOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  const submitFile = async (e) => {
    e.preventDefault();
    setLoading(true);
    const formData = new FormData();
    formData.append("file", e.target.files[0]);

    try {
      const { data } = await axios.post("/upload", formData);
      console.log(data);
      const id = await flask.post("/get_image_id", {
        imageUrl: `http://localhost:8000/uploads/${data.image.filename}`,
      });

      navigate(`/home/product/${id.data.image_id}`);
      setLoading(false);
    } catch (error) {
      console.log(error);
      setLoading(false);
    }
  };

  const list = () => (
    <Box style={{ width: 250 }} onClick={handleClose}>
      <List>
        <listItem button>
          <CustomButtons />
        </listItem>
      </List>
    </Box>
  );

  return (
    <StyledHeader position="fixed">
      <Toolbar style={{ minHeight: 55 }}>
        <MenuButton aria-label="delete" color="inherit" onClick={handleOpen}>
          <Menu />
        </MenuButton>

        <Drawer open={open} onClose={handleClose}>
          {list()}
        </Drawer>

        <Component to="/">
          <img src={logoUrl} alt="logo" style={{ width: 75 }} />
          <Box style={{ display: "flex" }}>
            <SubHeading>
              Explore{" "}
              <Box component="span" style={{ color: "#FFE500" }}>
                Plus
              </Box>{" "}
            </SubHeading>
            <PlusImg src={subUrl} alt="subLogo" />
          </Box>
        </Component>
        <Search />

        {/* <AddAPhotoIcon style={{ marginLeft: "16px", cursor: "pointer" }} />
         */}

        <form
          encType="multipart/form-data"
          style={{ marginLeft: "16px", cursor: "pointer" }}
        >
          <input type="file" name="avatar" onChange={submitFile} />
        </form>

        <CustomButtonWrapper>
          <CustomButtons />
        </CustomButtonWrapper>
      </Toolbar>
    </StyledHeader>
  );
};

export default Header;
