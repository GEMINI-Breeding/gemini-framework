const plotsAPI = require("./api/plots");
import { Experiment } from "./types";

export default async function Home() {
  // const data = await experimentsAPI.getExperiments({experiment_name: "GEMINI"});
  return (
    <div>
      {/* <h1>Experiments</h1>
      <ul>
        {data.map((experiment: Experiment) => (
          <li key={experiment.id}>
            <h2>{experiment.experiment_name}</h2>
          </li>
        ))}
      </ul> */}
    </div>
  )
} 