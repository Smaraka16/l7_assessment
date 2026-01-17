import { configureStore } from "@reduxjs/toolkit";

// Import reducers for each feature
import moviesReducer from "../features/movies/moviesSlice";
import actorsReducer from "../features/actors/actorsSlice";
import directorsReducer from "../features/directors/directorsSlice";
import genresReducer from "../features/genres/genresSlice";

// Create the Redux store
export const store = configureStore({
  reducer: {
    movies: moviesReducer,
    actors: actorsReducer,
    directors: directorsReducer,
    genres: genresReducer,
  },
});

export default store;
