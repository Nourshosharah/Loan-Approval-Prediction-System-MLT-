import { Form, Input, Button, Typography } from "antd";
import { useNavigate } from "react-router-dom";

const { Title } = Typography;

export default function SignUpPage() {
  const navigate = useNavigate();

  const handleSignUp = (values: any) => {
    console.log("User info:", values);
    localStorage.setItem("token", "dummyToken");
    navigate("/");
  };

  return (
    <div
      style={{
        maxWidth: 400,
        margin: "80px auto",
        padding: 24,
        background: "#fff",
        borderRadius: 8,
        boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
      }}
    >
      <Title level={3}>إنشاء حساب</Title>
      <Form layout="vertical" onFinish={handleSignUp}>
        <Form.Item
          label="الاسم"
          name="name"
          rules={[{ required: true, message: "الرجاء إدخال الاسم" }]}
        >
          <Input />
        </Form.Item>

        <Form.Item
          label="البريد الإلكتروني"
          name="email"
          rules={[
            { required: true, message: "الرجاء إدخال البريد" },
            { type: "email", message: "بريد غير صالح" },
          ]}
        >
          <Input />
        </Form.Item>

        <Form.Item
          label="كلمة المرور"
          name="password"
          rules={[{ required: true, message: "الرجاء إدخال كلمة المرور" }]}
        >
          <Input.Password />
        </Form.Item>

        <Form.Item>
          <Button type="primary" htmlType="submit" block>
            تسجيل
          </Button>
        </Form.Item>
      </Form>

      <Button type="link" onClick={() => navigate("/login")}>
        لديك حساب؟ تسجيل الدخول
      </Button>
    </div>
  );
}
