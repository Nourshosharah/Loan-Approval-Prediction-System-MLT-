import { RouterProvider } from "react-router-dom";
import { Provider } from "react-redux";
import store from "./store";
import { router } from "./routes/AppRoutes";
import { I18nProvider } from "./i18n";

function App() {
  return (
    <Provider store={store}>
      <I18nProvider>
        <RouterProvider router={router} />
      </I18nProvider>
    </Provider>
  );
}

export default App;
