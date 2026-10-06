'use client';

import { Unity, useUnityContext } from "react-unity-webgl";

export default function Game() {
  const { unityProvider } = useUnityContext({
    loaderUrl: "WebGL Build/Build/WebGL Builds.loader.js",
    dataUrl: "WebGL Build/Build/WebGL Builds.data",
    frameworkUrl: "WebGL Build/Build/WebGL Builds.framework.js",
    codeUrl: "WebGL Build/Build/WebGL Builds.wasm",
  });

  return <Unity unityProvider={unityProvider} />;
}