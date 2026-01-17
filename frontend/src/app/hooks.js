import { useDispatch, useSelector } from "react-redux";

// Custom hook to get the Redux dispatch function
// Used to dispatch actions to the store
export const useAppDispatch = () => useDispatch();

// Custom hook for selecting data from Redux state
// Used instead of useSelector directly for consistency
export const useAppSelector = useSelector;
