import React, { useEffect, useState } from "react";
import {
  Container,
  Grid,
  Paper,
  InputBase,
  IconButton,
  Button,
  Box,
} from "@mui/material";
import SendIcon from "@mui/icons-material/Send";
import MicIcon from "@mui/icons-material/Mic";
import { styled } from "@mui/system";
import SpeechRecognition, {
  useSpeechRecognition,
} from "react-speech-recognition";
import { Link } from "react-router-dom";
import axios from "../../axios/axios";
import flaskAxios from "../../axios/flask";
import { useSelector } from "react-redux";

const Sidebar = styled(Paper)(({ theme }) => ({
  height: "70vh",
  padding: theme.spacing(2),
  overflowY: "auto",
  display: "block",
}));

const Message = styled("div")(({ theme, type }) => ({
  marginBottom: theme.spacing(1),
  padding: theme.spacing(1),
  borderRadius: "8px",
  maxWidth: "80%",
  backgroundColor: type === "user" ? "#1976D2" : "#f0f0f0",
  color: type === "user" ? "#f0f0f0" : "#1976D2",
  alignSelf: type !== "user" ? "flex-start" : "flex-end",
  width: "fit-content",
}));

const ChatBox = styled(Paper)({
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
  padding: "8px",
});

const Input = styled(InputBase)({
  flex: 1,
  marginRight: "8px",
  borderRadius: "8px",
});

const IconButtonStyled = styled(IconButton)({
  color: "#757575",
});

const Conversation = styled("div")({
  height: "466px",
  display: "flex",
  flexDirection: "column",
  overflowY: "scroll",
});

const ButtonContainer = styled(Box)`
  margin-top: 75px;
  display: flex;
  justify-content: space-around;
  padding: 0 5px;
  margin-bottom: 20px;
`;

const RASA_API_URL = "http://localhost:5005";

function Chat() {
  const {
    transcript,
    listening,
    resetTranscript,
    browserSupportsSpeechRecognition,
  } = useSpeechRecognition();

  const { user } = useSelector((state) => state.user);

  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState("");
  const [productId, setProductId] = useState("");
  const [loading, setLoading] = useState(false);

  if (!browserSupportsSpeechRecognition) {
    return <span>Browser doesn't support speech recognition.</span>;
  }

  const fetchData = async (url) => {
    try {
      setLoading(true);
      const response = await flaskAxios.post("/get_image_id", {
        imageUrl: url,
      });
      setProductId(response.data.image_id);
      setLoading(false);
    } catch (err) {
      console.log(err);
    }
  };

  const handleSend = async () => {
    if (inputText.trim() !== "") {
      const newMessage = {
        text: inputText,
        type: "user",
      };
      setMessages([...messages, newMessage]);
      setInputText("");

      // Send user message to Rasa server
      try {
        const response = await axios.post(
          `${RASA_API_URL}/webhooks/rest/webhook`,
          {
            sender: user.userId,
            message: inputText,
          }
        );

        // Process Rasa response and extract image URL if available
        response.data.forEach(async (rasaResponse) => {
          const newMessage = {
            text: rasaResponse.text,
            type: "bot",
          };
          if (rasaResponse.attachment) {
            newMessage.image = rasaResponse.attachment.image;
            setMessages((messages) => [...messages, newMessage]);
            await fetchData(rasaResponse.attachment.image);
          } else {
            setMessages((messages) => [...messages, newMessage]);
          }
        });
      } catch (error) {
        console.error("Error sending message to Rasa:", error);
      }
    }
  };

  const handleVoice = async () => {
    if (!listening) {
      await SpeechRecognition.startListening();
      setInputText(transcript);
    } else {
      SpeechRecognition.stopListening();
      setInputText("");
      resetTranscript();
    }
  };

  const handleInputChange = (event) => {
    setInputText(event.target.value);
  };

  return (
    <>
      <ButtonContainer>
        {/* Add your buttons here */}
        <Link to="/">
          <Button variant="contained" color="primary" size="large">
            Ask AI 🧠
          </Button>
        </Link>
        <Link to="/home">
          <Button variant="contained" color="primary" size="large">
            Explore
          </Button>
        </Link>
      </ButtonContainer>
      <Container maxWidth="lg" sx={{ marginTop: "20px" }}>
        <Grid container spacing={2}>
          <Grid item xs={3}>
            <Sidebar>
              {loading && (
                <Message type="bot">
                  Loading... Please wait while we fetch the same product for you
                  we have.
                </Message>
              )}
              {productId && (
                <>
                  <Message type="bot">
                    Here is the product available with us.
                  </Message>
                  <Link to={`/home/product/${productId}`}>
                    <img
                      // src={`https://fashionkart.blob.core.windows.net/test/$// {productId}.jpg`}
                      src={`http://localhost:8000/product_images/images/${productId}.jpg`}
                      alt="Generated image"
                      style={{ height: "200px", width: "200px" }}
                    />
                  </Link>
                </>
              )}
            </Sidebar>
          </Grid>
          <Grid item xs={9}>
            <Conversation>
              <Message>
                Hi there! I'm your personal stylist. I can help you find the
                perfect outfit for any occasion. Just ask me! Let's start by
                knowing your Age.
              </Message>
              {messages.map((message, index) => (
                <Message key={index} type={message.type}>
                  {message.text}
                  {message.image && (
                    <div>
                      <img
                        src={message.image}
                        alt="Generated Outfit"
                        style={{ maxWidth: "100%" }}
                      />
                    </div>
                  )}
                </Message>
              ))}
            </Conversation>
            <ChatBox>
              <Input
                placeholder="Type your message..."
                fullWidth
                value={inputText}
                onChange={handleInputChange}
              />
              <IconButtonStyled onClick={handleSend}>
                <SendIcon />
              </IconButtonStyled>
              <IconButtonStyled onClick={handleVoice}>
                <MicIcon color={listening ? "primary" : "inherit"} />
              </IconButtonStyled>
            </ChatBox>
          </Grid>
        </Grid>
      </Container>
    </>
  );
}

export default Chat;
