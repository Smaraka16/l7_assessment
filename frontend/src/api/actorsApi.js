// Import the pre-configured Axios instance
import api from "./client";

// Fetch all actors
export const getActors = async (params = {}) => {
  const response = await api.get("/actors/", { params });
  return response.data;
};

// Fetch a single actor by ID
export const getActor = async (id) => {
  const response = await api.get(`/actors/${id}/`);
  return response.data;
};
