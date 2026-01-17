// Import the pre-configured Axios instance
import api from "./client";

// Fetch all movies
export const getMovies = async (params = {}) => {
  const response = await api.get("/movies/", { params });
  return response.data;
};

// Fetch a single movie by ID
export const getMovie = async (id) => {
  const response = await api.get(`/movies/${id}/`);
  return response.data;
};
