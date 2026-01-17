// Import the pre-configured Axios instance
import api from "./client";

// Fetch all genres
export const getGenres = async (params = {}) => {
  const response = await api.get("/genres/", { params });
  return response.data;
};
