import axios from "axios";

export default axios.create({
    base URL: "http://localhost:5000/api"
});