import Image from "next/image";
import { Button } from "@nextui-org/button";

import { getAllExperiments } from "./api/experiments";

export default async function Home() {
  const data = await getAllExperiments();

  return (
    <div>
      <Button>Button</Button>
    </div>
  )
}
