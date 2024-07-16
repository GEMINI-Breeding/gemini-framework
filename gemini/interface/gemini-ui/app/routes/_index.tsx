import CenterMessage from "app/components/centermessage/centermessage";

const welcomeMessage = "Welcome to GEMINI, please click on options in the sidebar to get started.";

export default function Home() {
    return (
        <CenterMessage message={welcomeMessage} />
    );
}