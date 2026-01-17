// Import the pre-configured Axios instance
import api from "./client";

// Fetch all directors
export const getDirectors = async (params = {}) => {
  const response = await api.get("/directors/", { params });
  return response.data;
};

// Fetch a single director by ID
export const getDirector = async (id) => {
  const response = await api.get(`/directors/${id}/`);
  return response.data;
};
