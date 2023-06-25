import React from "react";
import ReactDOM from "react-dom";
import "./assets/main.css";
import App from "./App";
import axios from "axios";

axios.defaults.baseURL = process.env.REACT_APP_BACKEND_BASE_URL;
axios.defaults.withCredentials = true;

ReactDOM.render(<App />, document.getElementById("root"));
