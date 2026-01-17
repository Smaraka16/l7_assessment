import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { getDirectors } from "../../api/directorsApi";
import { getErrorMessage } from "../../utils/errorHandler";

// Async thunk to fetch directors from the API
export const fetchDirectors = createAsyncThunk(
  "directors/fetchDirectors",
  async (filters = {}, { rejectWithValue }) => {
    try {
      console.log("RAW filters:", filters);
      // Remove empty/null filters
      const cleanFilters = Object.fromEntries(
        Object.entries(filters).filter(([_, v]) => v != null && v !== ""),
      );

      const data = await getDirectors(cleanFilters);
      return data;
    } catch (error) {
      const errorMessage = getErrorMessage(error);
      return rejectWithValue(errorMessage);
    }
  },
);

// Directors slice
// Handles director list, loading state, filters, and pagination
const directorsSlice = createSlice({
  name: "directors",
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
      .addCase(fetchDirectors.pending, (state) => {
        state.status = "loading";
        state.error = null;
      })
      .addCase(fetchDirectors.fulfilled, (state, action) => {
        state.status = "succeeded";
        state.items = action.payload.results ?? action.payload;
        state.pagination = action.payload.pagination ?? null;
      })

      .addCase(fetchDirectors.rejected, (state, action) => {
        state.status = "failed";
        state.error = action.payload;
      });
  },
});

export const { setFilters, clearFilters, appendItems } = directorsSlice.actions;
export default directorsSlice.reducer;
