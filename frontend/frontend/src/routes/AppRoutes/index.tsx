import { createBrowserRouter } from "react-router-dom";
import AdminLayout from "../../layouts/AdminLayout";
import DashboardPage from "../../pages/dashboard";
import LoginPage from "../../pages/login";
import ProtectedRoute from "../ProtectedRoutes";
import SignUpPage from "../../pages/signup";
import RequestsPage from "../../pages/requests";
import ModelAccuracy from "../../pages/modelAccuracy";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <ProtectedRoute />,
    children: [
      {
        path: "/",
        element: <AdminLayout />,
        children: [
          {
            index: true,
            element: <DashboardPage />,
          },
          {
            path: "requests",
            element: <RequestsPage />,
          },
          {
            path: "modelaccuracy",
            element: <ModelAccuracy />,
          },
        ],
      },
    ],
  },
  {
    path: "/login",
    element: <LoginPage />,
  },
  {
    path: "/signup",
    element: <SignUpPage />,
  },
]);
