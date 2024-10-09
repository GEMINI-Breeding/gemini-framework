import CenterMessage from "@/components/centermessage/centermessage";

export default function Home() {
  const welcomeMessage = "Welcome to GEMINI";

  return (
    <div>
      <CenterMessage message={welcomeMessage} />
    </div>
  );
}
