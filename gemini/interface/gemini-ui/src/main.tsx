import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "@/app";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import Uploady from "@rpldy/uploady";

const queryClient = new QueryClient();

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Uploady customInput>
          <App />
        </Uploady>
      </BrowserRouter>
    </QueryClientProvider>
  </React.StrictMode>
);
