import Image from "next/image";
import styles from "./page.module.css";
import DragDrop from "@/components/dragdrop/dragdrop";

export default function Home() {
  return (
    <div>
      <DragDrop />
    </div>
  );
}
