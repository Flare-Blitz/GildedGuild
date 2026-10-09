import { Metadata } from "next";
import { login } from "../actions/login";

export const metadata: Metadata = {
  title: "🛠 iron-session examples: Server components, and server actions",
};

export default async function Login() {
  return (
    <main className="p-10 space-y-5">

      <p className="italic max-w-xl">
        <u>Login to Gilded Guild</u>
      </p>

      <div className="grid grid-cols-1 gap-4 p-10 border border-slate-500 rounded-md max-w-xl">

        <form action={login}>
          <label className="block text-lg">
            <span>Username</span>
            <input id="username" name="username" placeholder="Username" />
            <span>Password</span>
            <input id="password" name="password" type="password" placeholder="Password" />
          </label>
          <div>
            <input type="submit" value={"Login"} />
          </div>
        </form>
        <div>
          <p>Don't have an account? <a href="/register">Register</a></p>
        </div>
      </div>
    </main>
  );
}