import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { getMovies } from "../../api/moviesApi";
import { getErrorMessage } from "../../utils/errorHandler";

// -------------------- Async Thunk --------------------

export const fetchMovies = createAsyncThunk(
  "movies/fetchMovies",
  async (filters = {}, { rejectWithValue }) => {
    try {
      // Remove empty/null filters
      const cleanFilters = Object.fromEntries(
        Object.entries(filters).filter(([_, v]) => v != null && v !== ""),
      );

      const data = await getMovies(cleanFilters);
      return data;
    } catch (error) {
      const errorMessage = getErrorMessage(error);
      return rejectWithValue(errorMessage);
    }
  },
);

// Movies slice
// Handles movies list, loading state, filters, and pagination
const moviesSlice = createSlice({
  name: "movies",
  initialState: {
    items: [],
    status: "pending",
    error: null,
    filters: {},
    pagination: null,
  },
  reducers: {
    setFilters(state, action) {
      state.filters = action.payload;
    },
    clearFilters(state) {
      state.filters = {};
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchMovies.pending, (state) => {
        state.status = "loading";
        state.error = null;
      })
      .addCase(fetchMovies.fulfilled, (state, action) => {
        state.status = "succeeded";
        state.items = action.payload.results ?? action.payload;
        state.pagination = action.payload.pagination ?? null;
      })
      .addCase(fetchMovies.rejected, (state, action) => {
        state.status = "failed";
        state.error = action.payload;
      });
  },
});

export const { setFilters, clearFilters } = moviesSlice.actions;

export default moviesSlice.reducer;
