import { redirect } from "next/navigation";

import { readSession } from "../actions/dal";
import GameClient from "./GameClient";

export default async function GamePage() {
  const session = await readSession();

  if (!session.isLoggedIn || !session.username) {
    redirect("/login");
  }

  return <GameClient username={session.username} />;
}
