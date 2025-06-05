import { useIntl } from "react-intl";

const DashboardPage = () => {
  const intl = useIntl();

  return <h1>{intl.formatMessage({ id: "app.hello" })}</h1>;
};
export default DashboardPage;
