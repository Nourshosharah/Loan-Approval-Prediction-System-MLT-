import { Layout } from "antd";
import { Outlet } from "react-router-dom";
import Sidebar from "../components/common/Sidebar";
import { useState } from "react";
import AppHeader from "../components/common/Header";

const { Sider, Content } = Layout;

export default function AdminLayout() {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <Layout style={{ minHeight: "100vh" }}>
      <Sider
        collapsible
        collapsed={collapsed}
        trigger={null}
        width={200}
        collapsedWidth={80}
        theme="light"
      >
        <Sidebar collapsed={collapsed} />
      </Sider>
      <Layout>
        <AppHeader onToggleSidebar={() => setCollapsed(!collapsed)} />

        <Content style={{ margin: "16px" }}>
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  );
}
