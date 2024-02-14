import React from "react";
import ReactDOM from "react-dom/client";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import "./index.css";
import App from "./App";
import CuratorList from "./Components/CuratorList.jsx";
import CuratorDetail from "./Components/CuratorDetail.jsx";
import reportWebVitals from "./reportWebVitals";

const router = createBrowserRouter([
  {
    path: "/curatorSignIn",
    element: <App />,
  },
  {
    path: "/admin",
    element: <CuratorList />,
  },
  {
    path: "/curators/:curatorId",
    element: <CuratorDetail />,
  },
]);
const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
