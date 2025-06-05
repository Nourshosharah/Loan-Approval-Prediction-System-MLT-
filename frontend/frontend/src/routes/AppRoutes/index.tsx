import { createBrowserRouter } from "react-router-dom";
import AdminLayout from "../../layouts/AdminLayout";
import DashboardPage from "../../pages/dashboard";
import LoginPage from "../../pages/login";
import ProtectedRoute from "../ProtectedRoutes";
import SignUpPage from "../../pages/signup";

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
