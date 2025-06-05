import { Button, Form, Input, Card, Typography, message } from "antd";
import { useDispatch } from "react-redux";
import { login } from "../../features/authSlice";
import { Link, useNavigate } from "react-router-dom";

interface ILogin {
  name: string;
  email: string;
  token: string;
}
const { Title } = Typography;

export default function LoginPage() {
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const onFinish = (values: ILogin) => {
    const fakeUser = {
      name: "Mad",
      email: values.email,
      token: "fake-jwt-token",
    };

    dispatch(login(fakeUser));
    message.success("Login successful!");
    navigate("/");
  };

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        minHeight: "100vh",
        background: "#f0f2f5",
        padding: 16,
      }}
    >
      <Card style={{ width: 300 }}>
        <Title level={3} style={{ textAlign: "center" }}>
          Login
        </Title>

        <Form layout="vertical" onFinish={onFinish}>
          <Form.Item
            label="Email"
            name="email"
            rules={[{ required: true, message: "Please enter your email" }]}
          >
            <Input type="email" />
          </Form.Item>

          <Form.Item
            label="Password"
            name="password"
            rules={[{ required: true, message: "Please enter your password" }]}
          >
            <Input.Password />
          </Form.Item>

          <Form.Item>
            <Button type="primary" htmlType="submit" block>
              Login
            </Button>
          </Form.Item>
          <p style={{ marginTop: 16 }}>
            ليس لديك حساب؟ <Link to="/signup">إنشاء حساب</Link>
          </p>
        </Form>
      </Card>
    </div>
  );
}
