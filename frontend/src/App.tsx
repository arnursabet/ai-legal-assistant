import { useEffect } from "react";

import {
  ChainlitAPI,
  sessionState,
  useChatSession,
} from "@chainlit/react-client";
import { Playground } from "./components/playground";
import { useRecoilValue } from "recoil";
import axios from 'axios';

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
    // connect({wsEndpoint: CHAINLIT_SERVER, userEnv});
    axios.get(apiClient.buildEndpoint("/custom-auth"), {headers: {Accept: 'application/json'}})
      .then((response) => {
        console.log("Data: ", response.data)
        connect({
          client: apiClient,
          userEnv,
          accessToken: `Bearer: ${response.data.token}`,
        });
      })
      .catch((error) => {
        console.error('Error fetching auth token:', error);
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
