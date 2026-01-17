import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { getGenres } from "../../api/genresApi";
import { getErrorMessage } from "../../utils/errorHandler";

// Async thunk to fetch genres from the API
export const fetchGenres = createAsyncThunk(
  "genres/fetchGenres",
  async (filters = {}, { rejectWithValue }) => {
    try {
      const cleanFilters = Object.fromEntries(
        Object.entries(filters).filter(([_, v]) => v != null && v !== ""),
      );
      const data = await getGenres(cleanFilters);
      return data;
    } catch (error) {
      const errorMessage = getErrorMessage(error);
      return rejectWithValue(errorMessage);
    }
  },
);

// Genres slice
// Handles genres list, loading state, filters, and pagination
const genresSlice = createSlice({
  name: "genres",
  initialState: {
    items: [],
    status: "idle",
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
      state.items = [];
      state.pagination = null;
    },
    appendItems(state, action) {
      state.items = [...state.items, ...action.payload];
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchGenres.pending, (state) => {
        state.status = "loading";
        state.error = null;
      })
      .addCase(fetchGenres.fulfilled, (state, action) => {
        state.status = "succeeded";
        const results = action.payload.results ?? action.payload;
        const pagination = action.payload.pagination ?? null;

        // If we have existing items and pagination shows we're not on page 1, append
        if (
          state.items.length > 0 &&
          pagination &&
          pagination.current_page > 1
        ) {
          state.items = [...state.items, ...results];
        } else {
          state.items = results;
        }
        state.pagination = pagination;
      })
      .addCase(fetchGenres.rejected, (state, action) => {
        state.status = "failed";
        state.error = action.payload;
      });
  },
});

export const { setFilters, clearFilters, appendItems } = genresSlice.actions;
export default genresSlice.reducer;
