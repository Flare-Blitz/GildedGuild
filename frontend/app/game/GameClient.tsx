"use client";

import { Unity, useUnityContext } from "react-unity-webgl";

type GameClientProps = {
  username: string;
};

export default function GameClient({ username }: GameClientProps) {
  const { unityProvider, sendMessage } = useUnityContext({
    loaderUrl: "WebGL Build/Build/WebGL Builds.loader.js",
    dataUrl: "WebGL Build/Build/WebGL Builds.data",
    frameworkUrl: "WebGL Build/Build/WebGL Builds.framework.js",
    codeUrl: "WebGL Build/Build/WebGL Builds.wasm",
  });

  // Send player information to the Unity game
  const playerInfo = `${username},Bob,Charlie,Doug`;
  sendMessage("Players", "LoadPlayerInfo", playerInfo);

  return <Unity unityProvider={unityProvider} />;
}
