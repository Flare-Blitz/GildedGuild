import { SessionData } from "../lib/session";
import { defaultSession, sessionOptions } from "../lib/session";
import { getIronSession } from "iron-session";
import { cookies } from "next/headers";
import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";

export async function getSession() {
  const session = await getIronSession<SessionData>(await cookies(), sessionOptions);

  if (!session.isLoggedIn) {
    session.id = defaultSession.id;
    session.username = defaultSession.username;
    session.email = defaultSession.email;
    session.isLoggedIn = defaultSession.isLoggedIn;
  }

  return session;
}

export async function logout() {
  "use server";

  const session = await getSession();
  session.destroy();
  revalidatePath("/");
  redirect("/");
}

export async function login(formData: FormData) {
  "use server";

  const session = await getSession();

  if (!session.isLoggedIn) {
    session.id = 0;
    session.username = "";
    session.email = "";
    session.isLoggedIn = false;
  }
  session.username = (formData.get("username") as string) ?? "No username";
  session.email = (formData.get("email") as string) ?? "No email";
  session.isLoggedIn = true;
  await session.save();
  revalidatePath("/");
  redirect("/");
}