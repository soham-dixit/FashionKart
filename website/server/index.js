import express from "express";
import path from "path";
import { fileURLToPath } from "url";
import { dirname } from "path";

import firebaseAdmin from "firebase-admin";
import { v4 as uuidv4 } from "uuid";
import { createRequire } from "module";

const require = createRequire(import.meta.url);
const serviceAccount = require("./firebase-admin-sdk.json");

import multer from "multer";

const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, "./uploads");
  },
  filename: function (req, file, cb) {
    const uniqueSuffix = Date.now() + "-" + Math.round(Math.random() * 1e9);
    cb(null, uniqueSuffix + file.originalname);
  },
});

const upload = multer({ storage: storage });

import connectToMongo from "./database/mongo.db.js";
import dotenv from "dotenv";
import errorHandler from "./middleware/errorHandler.js";

import cors from "cors";
import bodyParser from "body-parser";
import cookieParser from "cookie-parser";

import authRouter from "./routes/auth.route.js";
import productRouter from "./routes/products.route.js";
import purchasingHistoryRouter from "./routes/purchasingHistory.route.js";
import browsingHistoryRouter from "./routes/browsingHistory.route.js";
import cartHistoryRouter from "./routes/cartHistory.route.js";
import frequentDataRouter from "./routes/frequentData.route.js";
import UserModel from "./model/user.model.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const app = express();
const imagesDirectory = path.join(__dirname, "product_images", "images");
const uploadsDirectory = path.join(__dirname, "uploads");

dotenv.config();

app.use(
  cors({
    origin: [
      "http://localhost:8080",
      "http://localhost:3000",
      "https://fashionkart.azurewebsites.net",
    ],
    credentials: true,
  })
);

app.use(bodyParser.json({ extended: true }));
app.use(bodyParser.urlencoded({ extended: true }));
app.use(cookieParser());

app.post("/api/v4/upload", upload.single("file"), (req, res) => {
  res.status(200).json({
    success: true,
    message: "Image uploaded successfully",
    image: req.file,
  });
});

const admin = firebaseAdmin.initializeApp({
  credential: firebaseAdmin.credential.cert(serviceAccount),
});

const storageRef = admin
  .storage()
  .bucket(`gs://fashionkart-26db7.appspot.com/`);

async function uploadFile(filePath, filename) {
  const storage = await storageRef.upload(filePath, {
    public: true,
    destination: `userImages/${filename}`,
    metadata: {
      firebaseStorageDownloadTokens: uuidv4(),
    },
  });

  return storage[0].metadata.mediaLink;
}

app.post("/api/v4/try-on", upload.single("file"), async (req, res) => {
  const file = req.file;
  const filePath = file.path;
  var filename = file.filename;
  filename = filename.replace(/\s/g, "");
  const userId = req.body.userId;
  console.log("userId", userId);

  const imageUrl = await uploadFile(filePath, filename);

  const user = await UserModel.findOne({ userId });
  console.log("user", user);

  if (!user) {
    return createError(req, res, next, "User doesn't exist", 404);
  }

  await UserModel.updateOne({ userId }, { $set: { imageUrl } });

  res.status(200).json({
    success: true,
    message: "Image uploaded successfully",
    imageUrl: imageUrl,
  });
});

app.use("/api/v4/auth", authRouter);
app.use("/api/v4/product", productRouter);
app.use("/api/v4/purchasingHistory", purchasingHistoryRouter);
app.use("/api/v4/browsingHistory", browsingHistoryRouter);
app.use("/api/v4/cartHistory", cartHistoryRouter);
app.use("/api/v4/frequentData", frequentDataRouter);

// Serve static files from the React build folder
app.use(express.static(path.join(__dirname, "build")));
app.use("/product_images/images", express.static(imagesDirectory));
app.use("/uploads", express.static(uploadsDirectory));

// This route will serve the index.html from the build folder
app.get("*", (req, res) => {
  res.sendFile(path.join(__dirname, "build", "index.html"));
});

// Global Error Handler
app.use(errorHandler);

const PORT = process.env.PORT || 8000;

const USERNAME = process.env.DB_USERNAME;
const PASSWORD = process.env.DB_PASSWORD;

connectToMongo();

app.listen(PORT, () =>
  console.log(`Server is Running Successfully on PORT ${PORT}`)
);
