import { Layout, Dropdown, Menu, Button, Space } from "antd";
import {
  UserOutlined,
  GlobalOutlined,
  LogoutOutlined,
} from "@ant-design/icons";
import { useDispatch } from "react-redux";
import { useI18n } from "../../i18n";
import { useNavigate } from "react-router-dom";
import { logout } from "../../features/authSlice";

const { Header } = Layout;

export default function AppHeader({
  onToggleSidebar,
}: {
  onToggleSidebar: () => void;
}) {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const { setLocale } = useI18n();

  const changeLanguage = (lang: "en" | "ar") => {
    setLocale(lang);
    document.dir = lang === "ar" ? "rtl" : "ltr";
  };

  const handleLogout = () => {
    dispatch(logout());
    navigate("/login");
  };

  const userMenu = (
    <Menu>
      <Menu.Item key="logout" icon={<LogoutOutlined />} onClick={handleLogout}>
        تسجيل الخروج
      </Menu.Item>
    </Menu>
  );

  const languageMenu = (
    <Menu>
      <Menu.Item key="ar" onClick={() => changeLanguage("ar")}>
        العربية
      </Menu.Item>
      <Menu.Item key="en" onClick={() => changeLanguage("en")}>
        English
      </Menu.Item>
    </Menu>
  );

  return (
    <Header
      style={{
        background: "#fff",
        display: "flex",
        justifyContent: "space-between",
        padding: "0 16px",
        alignItems: "center",
        boxShadow: "0 1px 4px rgba(0,0,0,0.1)",
      }}
    >
      <Button onClick={onToggleSidebar}>☰</Button>

      <Space>
        <Dropdown overlay={languageMenu} placement="bottomRight">
          <Button icon={<GlobalOutlined />} />
        </Dropdown>

        <Dropdown overlay={userMenu} placement="bottomRight">
          <Button icon={<UserOutlined />} />
        </Dropdown>
      </Space>
    </Header>
  );
}
