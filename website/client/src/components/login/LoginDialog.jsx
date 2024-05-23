import React from "react";
import { useState, useContext } from "react";
import {
  Dialog,
  Box,
  TextField,
  Button,
  Typography,
  styled,
  ClickAwayListener,
} from "@mui/material";

import { DataContext } from "../../context/DataProvider";
import axios from "../../axios/axios";
import { Navigate, useNavigate } from "react-router-dom";
import { useDispatch } from "react-redux";
import {
  loginUserAction,
  registerUserAction,
} from "../../redux/actions/userActions";

const Component = styled(Box)`
  height: 83vh;
  width: 100vh;
  padding: 0;
  padding-top: 0;
`;

const Image = styled(Box)`
  background: #2874f0
    url(https://static-assets-web.flixcart.com/www/linchpin/fk-cp-zion/img/login_img_c4a81e.png)
    center 85% no-repeat;
  height: 83%;
  width: 40%;
  padding: 45px 35px;
  & > h5 {
    font-weight: bold;
    color: #ffffff;
  }
  & > p {
    font-family: Arial;
    color: #dbdbdb;
  }
`;

const Wrapper = styled(Box)`
  display: flex;
  flex-direction: column;
  padding: 25px 35px;
  flex: 1;
  & > div,
  & > button,
  & > p {
    margin-top: 20px;
  }
`;

const LoginButton = styled(Button)`
  text-transform: none;
  background: #fb641b;
  color: #fff;
  height: 48px;
  border-radius: 2px;
`;

const RequestOTP = styled(Button)`
  text-transform: none;
  background: #fff;
  color: #2874f0;
  height: 48px;
  border-radius: 2px;
  box-shadow: 0 2px 4px 0 rgb(0 0 0 / 20%);
`;

const Text = styled(Typography)`
  font-size: 12px;
  color: #878787;
`;

const CreateAccount = styled(Typography)`
  margin: auto 0 5px 0;
  font-size: 14px;
  text-align: center;
  color: #2874f0;
  font-weight: 600;
  cursor: pointer;
`;

const Error = styled(Typography)`
  font-size: 10px;
  color: #ff6161;
  line-height: 0;
  margin-top: 10px;
  font-weight: 600;
`;

const accountInitialValues = {
  login: {
    view: "login",
    heading: "Login",
    subHeading: "Get access to your Orders, Wishlist and Recommendations",
  },
  signup: {
    view: "signup",
    heading: "Looks like you're new here!",
    subHeading: "Sign up with your mobile number to get started",
  },
};

const signupInitialValues = {
  name: "",
  email: "",
  password: "",
  age: "",
  gender: "",
  city: "",
};

const loginInitialValues = {
  email: "",
  password: "",
};

const LoginDialog = ({ open = true }) => {
  const [account, toggleAccount] = useState(accountInitialValues.login);
  const [signup, setSignup] = useState(signupInitialValues);
  const [login, setLogin] = useState(loginInitialValues);
  const [error, setError] = useState(false);
  const [message, setMessage] = useState("");
  const [errorType, setErrorType] = useState("");

  const dispatch = useDispatch();

  const navigate = useNavigate();

  const handleClose = () => {
    toggleAccount(accountInitialValues.login);
    setError(false);
  };

  const toggleSignup = () => {
    toggleAccount(accountInitialValues.signup);
  };

  const onInputChange = (e) => {
    // console.log(e.target.value);
    setSignup({ ...signup, [e.target.name]: e.target.value });
  };

  const signupUser = async () => {
    await axios
      .post("/auth/signup", signup)
      .then((response) => {
        // setAccount(response.data.data.name);
        dispatch(registerUserAction(response?.data?.data));
        navigate("/");
        handleClose();
      })
      .catch((err) => {
        console.log("Error is: ", err);
        alert(err.response.data?.message);
      });
  };

  const onValueChange = (e) => {
    setLogin({ ...login, [e.target.name]: e.target.value });
  };

  const loginUser = async () => {
    await axios
      .post("/auth/login", login, { withCredentials: true })
      .then((response) => {
        console.log("Response is: ", response);
        // setAccount(response.?data?.user.name);
        dispatch(loginUserAction(response?.data?.user));
        navigate("/");
        handleClose();
      })
      .catch((err) => {
        console.log("Error is: ", err);
        setMessage(err.response?.data?.message);
        setError(true);
        if (err.response?.data?.message === "User doesn't exist") {
          setErrorType("email");
        } else {
          setErrorType("password");
        }
      });
  };

  

  return (
    <>
      { open && 
        <Dialog
          open={open}
          onClose={handleClose}
          PaperProps={{ sx: { maxWidth: "unset" } }}
        >
          <Component style={{ overflow: "hidden" }}>
            <Box style={{ display: "flex", height: "100%" }}>
              <Image>
                <Typography variant="h5"> {account.heading} </Typography>
                <Typography style={{ marginTop: 20 }}>
                  {" "}
                  {account.subHeading}{" "}
                </Typography>
              </Image>
              {account.view === "login" ? (
                <Wrapper>
                  <TextField
                    variant="standard"
                    onChange={(e) => onValueChange(e)}
                    name="email"
                    label="Enter Email"
                  />
                  {error && errorType === "email" && <Error>{message}</Error>}
                  <TextField
                    variant="standard"
                    onChange={(e) => onValueChange(e)}
                    name="password"
                    type="password"
                    label="Enter Password"
                  />
                  {error && errorType === "password" && (
                    <Error>{message}</Error>
                  )}
                  <Text>
                    By continuing, you agree to FashionKart's Terms of Use and
                    Privacy Policy.
                  </Text>
                  <LoginButton onClick={() => loginUser()}>Login</LoginButton>
                  <Typography style={{ textAlign: "center" }}>OR</Typography>
                  <RequestOTP>Request OTP</RequestOTP>
                  <CreateAccount onClick={() => toggleSignup()}>
                    New to FashionKart? Create an account
                  </CreateAccount>
                </Wrapper>
              ) : (
                <Wrapper>
                  <TextField
                    variant="standard"
                    required
                    onChange={(e) => onInputChange(e)}
                    name="name"
                    label="Enter Name"
                  />
                  <TextField
                    variant="standard"
                    required
                    onChange={(e) => onInputChange(e)}
                    name="email"
                    label="Enter Email"
                  />
                  <TextField
                    variant="standard"
                    type="password"
                    required
                    onChange={(e) => onInputChange(e)}
                    name="password"
                    label="Enter Password"
                  />
                  <TextField
                    variant="standard"
                    required
                    onChange={(e) => onInputChange(e)}
                    name="age"
                    label="Enter Age"
                  />
                  <TextField
                    variant="standard"
                    required
                    onChange={(e) => onInputChange(e)}
                    name="gender"
                    label="Enter Gender"
                  />
                  <TextField
                    variant="standard"
                    required
                    onChange={(e) => onInputChange(e)}
                    name="city"
                    label="Enter City"
                  />

                  <LoginButton onClick={() => signupUser()}>
                    Continue
                  </LoginButton>
                </Wrapper>
              )}
            </Box>
          </Component>
        </Dialog>
      }
    </>
  );
};

export default LoginDialog;
