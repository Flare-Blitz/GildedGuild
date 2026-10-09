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

      <div style={{ padding: "20px", border: "1px solid #ccc", borderRadius: "5px", margin: "20px" }}>

        <form action={login}>
          <label className="block text-lg font-medium text-gray-700">
            <span>Username</span>
            <input id="username" name="username" placeholder="Username" 
              style={{ border: "1px solid #ccc", borderRadius: "5px", padding: "5px" }} />
            <span>Password</span>
            <input id="password" name="password" type="password" placeholder="Password"
              style={{ border: "1px solid #ccc", borderRadius: "5px", padding: "5px" }} />
          </label>
          <div>
            <input type="submit" value={"Login"} />
          </div>
        </form>
        <div>
          <p>Don&apos;t have an account? <a href="/register">Register</a></p>
        </div>
      </div>
    </main>
  );
}