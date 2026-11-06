import "server-only";
import { SessionData } from "../lib/session";
import { defaultSession, sessionOptions } from "../lib/session";
import { getIronSession } from "iron-session";
import { cookies } from "next/headers";
import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import bcrypt from "bcryptjs";
import mysql, { type RowDataPacket } from "mysql2/promise";

type UserCredential = RowDataPacket & {
  user_id: number;
  username: string;
  email: string;
  password: string;
};

const pool = mysql.createPool({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
  port: Number(process.env.DB_PORT ?? 3306),
});

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

  const username = formData.get("username");
  const password = formData.get("password");

  if (
    typeof username !== "string" ||
    !username ||
    typeof password !== "string" ||
    !password
  ) {
    redirect("/login?error=invalid");
  }

  const [users] = await pool.execute<UserCredential[]>(
    "SELECT user_id, username, email, password FROM users WHERE username = ?",
    [username]
  );
  const [user] = users;

  if (!user) {
    redirect("/login?error=invalid");
  }

  const match = await bcrypt.compare(password, user.password);

  if (!match) {
    redirect("/login?error=invalid");
  }

  const session = await getSession();
  session.id = user.user_id;
  session.username = user.username;
  session.email = user.email;
  session.isLoggedIn = true;
  await session.save();
  revalidatePath("/");
  redirect("/");
}

export async function guestLogin() {
  "use server";

  const session = await getSession();
  session.id = defaultSession.id;
  session.username = defaultSession.username;
  session.email = defaultSession.email;
  session.isLoggedIn = true;
  await session.save();
  revalidatePath("/");
  redirect("/");
}