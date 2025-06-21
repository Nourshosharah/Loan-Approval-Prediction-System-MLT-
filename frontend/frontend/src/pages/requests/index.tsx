import { useState } from "react";
import {
  Table,
  Button,
  Card,
  Popconfirm,
  Tag,
  Modal,
  Form,
  Input,
  InputNumber,
  message,
} from "antd";
import { mockRequests } from "../../mocking";

const RequestsPage = () => {
  const [data, setData] = useState(mockRequests);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [form] = Form.useForm();

  const showModal = () => setIsModalOpen(true);
  const handleCancel = () => {
    setIsModalOpen(false);
    form.resetFields();
  };

  const handleAddRequest = (values: any) => {
    const newRequest = {
      ...values,
      id: Date.now(),
      result: Math.random() > 0.5 ? 1 : 0,
    };

    setData((prev) => [...prev, newRequest]);
    message.success("Request added!");
    handleCancel();
  };

  const handleDelete = (id: number) => {
    setData((prev) => prev.filter((item) => item.id !== id));
  };

  const columns = [
    {
      title: "Name",
      dataIndex: "name",
    },
    {
      title: "Age",
      dataIndex: "age",
    },
    {
      title: "Income",
      dataIndex: "income",
    },
    {
      title: "Loan Amount",
      dataIndex: "loan_amount",
    },
    {
      title: "Decision",
      dataIndex: "result",
      render: (val: number) =>
        val === 1 ? (
          <Tag color="green">Approved</Tag>
        ) : (
          <Tag color="red">Rejected</Tag>
        ),
    },
    {
      title: "Action",
      render: (_: any, record: any) => (
        <Popconfirm
          title="Delete this request?"
          onConfirm={() => handleDelete(record.id)}
        >
          <Button danger size="small">
            Delete
          </Button>
        </Popconfirm>
      ),
    },
  ];

  return (
    <Card
      title="Bank Requests"
      extra={
        <Button type="primary" onClick={showModal}>
          Add Request
        </Button>
      }
    >
      <Table
        rowKey="id"
        columns={columns}
        dataSource={data}
        pagination={{ pageSize: 5 }}
      />
      <Modal
        title="Add New Request"
        open={isModalOpen}
        onCancel={handleCancel}
        footer={null}
      >
        <Form layout="vertical" onFinish={handleAddRequest} form={form}>
          <Form.Item name="name" label="Name" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="age" label="Age" rules={[{ required: true }]}>
            <InputNumber min={18} style={{ width: "100%" }} />
          </Form.Item>
          <Form.Item name="income" label="Income" rules={[{ required: true }]}>
            <InputNumber min={0} style={{ width: "100%" }} />
          </Form.Item>
          <Form.Item
            name="loan_amount"
            label="Loan Amount"
            rules={[{ required: true }]}
          >
            <InputNumber min={0} style={{ width: "100%" }} />
          </Form.Item>
          <Button htmlType="submit" type="primary" block>
            Submit
          </Button>
        </Form>
      </Modal>
    </Card>
  );
};

export default RequestsPage;
