import { Menu } from "antd";
import { useNavigate } from "react-router-dom";
import type { MenuProps } from "antd";

interface SidebarProps {
  collapsed: boolean;
}

const items: MenuProps["items"] = [
  {
    key: "/",
    icon: <i className="ri-dashboard-line" />,
    label: "Dashboard",
  },
];

export default function Sidebar({ collapsed }: SidebarProps) {
  const navigate = useNavigate();

  const handleClick: MenuProps["onClick"] = (e) => {
    navigate(`/${e.key}`);
  };

  return (
    <div>
      <div
        style={{
          height: 64,
          display: "flex",
          alignItems: "center",
          justifyContent: collapsed ? "start" : "center",
          padding: "0 16px",
          color: "#fff",
          fontWeight: "bold",
          fontSize: 18,
          borderBottom: "1px solid rgba(255,255,255,0.1)",
        }}
      >
        {collapsed ? (
          <img src="/logo192.png" alt="logo" style={{ height: 32 }} />
        ) : (
          <img src="/logo192.png" alt="logo" style={{ height: 32 }} />
        )}
      </div>

      <Menu
        theme="light"
        mode="inline"
        defaultSelectedKeys={["dashboard"]}
        onClick={handleClick}
        inlineCollapsed={collapsed}
        items={items}
      />
    </div>
  );
}
