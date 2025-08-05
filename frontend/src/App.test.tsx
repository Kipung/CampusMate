import React from "react";
import { render, screen } from "@testing-library/react";
import App from "./App";

test("renders CampusMate title", () => {
  render(<App />);
  const titleElement = screen.getByText(/CampusMate/i);
  expect(titleElement).toBeInTheDocument();
});
