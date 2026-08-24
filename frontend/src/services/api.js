import axios from "axios";

// Shared API client so every page uses the same backend URL and session-cookie settings.
export default axios.create({
    baseURL: "http://localhost:5000/api",
    withCredentials: true
});

