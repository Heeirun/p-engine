# Plan for Simple React Frontend

## 1. Objective

Create a single-page React application to interact with the p-engine backend. The application will allow users to view and search audit logs.

## 2. Technology Stack

*   **Framework:** React (using Vite)
*   **Language:** TypeScript
*   **Styling:** Plain CSS for simplicity.

## 3. Project Structure

The frontend code will live in a new `frontend` directory.

```
/
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.css
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── README.md
└── ... (backend files)
```

## 4. Component Breakdown

*   **`App.tsx`**: The main component that will hold the application state, including the list of logs, search query, and search type. It will render the search bar and the log list.
*   **`SearchBar.tsx`**: A component containing the text input for the search query and radio buttons to select the search type (Keyword, Semantic, Hybrid).
*   **`LogList.tsx`**: A component that takes a list of logs as a prop and renders them.

## 5. State Management (within `App.tsx`)

*   `logs`: An array to store the log data fetched from the backend.
*   `searchQuery`: A string to hold the user's input from the search bar.
*   `searchType`: A string ('keyword', 'semantic', or 'hybrid') to manage the selected search mode.

## 6. API Interaction

*   **Endpoint:** `http://localhost:8000/search`
*   **Method:** `GET`
*   **Query Parameters:**
    *   `query`: The search term from the user.
    *   `search_type`: The selected search type (`keyword`, `semantic`, or `hybrid`).
*   **Initial Load:** On component mount, the app will fetch all logs by making a request with an empty query.

## 7. Implementation Steps

1.  **Setup:** Use `npm create vite@latest frontend -- --template react-ts` to bootstrap the React project.
2.  **Component Creation:** Create the `App.tsx`, `SearchBar.tsx`, and `LogList.tsx` components.
3.  **State:** Implement the necessary state management in `App.tsx` using `useState` and `useEffect` hooks.
4.  **API Fetching:** Write the logic to fetch data from the backend API. An initial fetch will run on page load, and subsequent fetches will be triggered by search submissions.
5.  **UI:**
    *   Build the search bar with a text input.
    *   Add radio buttons for selecting the search type.
    *   Create a simple list or table to display the log entries.
6.  **Styling:** Apply basic CSS for layout and readability.
