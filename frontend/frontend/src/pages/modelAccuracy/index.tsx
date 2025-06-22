import { Card, Col, Row } from "antd";

const ModelAccuracy = () => {
  const metrics = [
    { title: "Accuracy", value: "0.87" },
    { title: "Precision", value: "0.84" },
    { title: "Recall", value: "0.90" },
    { title: "F1 Score", value: "0.87" },
  ];

  return (
    <div style={{ padding: 24 }}>
      <h2 style={{ marginBottom: 24 }}>Model Evaluation Metrics</h2>
      <Row gutter={16}>
        {metrics.map((metric) => (
          <Col span={6} key={metric.title}>
            <Card bordered={false}>
              <h3>{metric.title}</h3>
              <p style={{ fontSize: 24, fontWeight: "bold" }}>{metric.value}</p>
            </Card>
          </Col>
        ))}
      </Row>
    </div>
  );
};
export default ModelAccuracy;
