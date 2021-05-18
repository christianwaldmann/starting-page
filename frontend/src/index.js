import React from "react";
import ReactDOM from "react-dom";
import "./assets/main.css";
import App from "./App";
import axios from "axios";

axios.defaults.baseURL = "https://localhost:1338/api";
axios.defaults.withCredentials = true;

ReactDOM.render(<App />, document.getElementById("root"));
