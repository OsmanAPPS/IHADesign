import { render, screen } from '@testing-library/react';
import App from './App';

test('renders airplane controls heading', () => {
  render(<App />);
  const headingElement = screen.getByText(/Airplane Controls/i);
  expect(headingElement).toBeInTheDocument();
});
