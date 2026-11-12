import { render, screen } from "@testing-library/react";
import App from "./App";

test("renders EnvyLead brand", () => {
  render(<App />);
  expect(screen.getAllByText("EnvyLead").length).toBeGreaterThan(0);
});