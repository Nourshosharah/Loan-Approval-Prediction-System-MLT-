import { Card } from "antd";
import { Pie, Column } from "@ant-design/plots";

const DashboardPage = () => {
  const approvalData = [
    { status: "Approved", value: 60 },
    { status: "Rejected", value: 40 },
  ];

  const genderData = [
    { gender: "Male", count: 70 },
    { gender: "Female", count: 30 },
  ];

  const pieConfig = {
    appendPadding: 10,
    data: approvalData,
    angleField: "value",
    colorField: "status",
    radius: 0.8,
    label: {
      type: "inner",
      offset: "-30%",
      content: "{value}",
      style: { fontSize: 14, textAlign: "center" },
    },
    interactions: [{ type: "element-active" }],
  };

  const columnConfig = {
    data: genderData,
    xField: "gender",
    yField: "count",
    label: { position: "middle", style: { fill: "#fff" } },
    xAxis: { label: { autoHide: true, autoRotate: false } },
    meta: { gender: { alias: "Gender" }, count: { alias: "Count" } },
  };

  return (
    <div style={{ padding: 24 }}>
      <h2 style={{ marginBottom: 24 }}>Exploratory Data Analysis</h2>
      <Card title="Approval Status Distribution" style={{ marginBottom: 24 }}>
        <Pie {...pieConfig} />
      </Card>
      <Card title="Gender Distribution">
        <Column {...columnConfig} />
      </Card>
    </div>
  );
};

export default DashboardPage;
