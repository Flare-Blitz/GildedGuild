'use client';

import { Unity, useUnityContext } from "react-unity-webgl";

export default function Game() {
  const { unityProvider, sendMessage } = useUnityContext({
    loaderUrl: "WebGL Build/Build/WebGL Builds.loader.js",
    dataUrl: "WebGL Build/Build/WebGL Builds.data",
    frameworkUrl: "WebGL Build/Build/WebGL Builds.framework.js",
    codeUrl: "WebGL Build/Build/WebGL Builds.wasm",
  });

  // Send player information to the Unity game
  const playerInfo = "Alice,Bob,Charlie,David";
  sendMessage("Players", "LoadPlayerInfo", playerInfo);

  return <Unity unityProvider={unityProvider} />;
}