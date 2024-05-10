import { useEffect } from "react";

import {
  ChainlitAPI,
  sessionState,
  useChatSession,
} from "@chainlit/react-client";
import { Playground } from "./components/playground";
import { useRecoilValue } from "recoil";

const CHAINLIT_SERVER = "http://0.0.0.0:8000";
const userEnv = {};

const apiClient = new ChainlitAPI(CHAINLIT_SERVER, "app");

function App() {
  const { connect } = useChatSession();
  const session = useRecoilValue(sessionState);
  useEffect(() => {
    if (session?.socket.connected) {
      return;
    }
    //connect({wsEndpoint: CHAINLIT_SERVER, userEnv});
    fetch(apiClient.buildEndpoint("/custom-auth"))
      .then((res) => {
        return res.json();
      })
      .then((data) => {
        console.log("Data: ", data)
        connect({
          client: apiClient,
          userEnv,
          accessToken: `Bearer: ${data.token}`,
        });
      });
  }, [connect]);

  return (
    <>
      <div>
        <Playground />
      </div>
    </>
  );
}

export default App;
