import { logout } from "@/app/actions/login";
import { redirect } from "next/navigation";
import { getSession } from "./lib/session";

type User = {
  id: number;
  username: string;
  email: string;
  password: string;
};

async function getUsers(): Promise<User[]> {
  const response = await fetch("http://localhost:3000/mysql/users");

  if (!response.ok) {
    throw new Error("Failed to fetch users");
  }

  return response.json();
}

export default async function Home() {
  const session = await getSession();

  if (!session.isLoggedIn) {
    redirect('/login');
  }

  const users = await getUsers();

  return (
    <main>
      <h1>Users</h1>
      <table style={{ borderCollapse: "collapse", width: "100%", border: "1px solid black" }}>
        <thead>
          <tr>
            <th>ID</th>
            <th>Username</th>
            <th>Email</th>
            <th>Password</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr key={user.id}>
              <td>{user.id}</td>
              <td>{user.username}</td>
              <td>{user.email}</td>
              <td>{user.password}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <div>
        <p>Navigate to game page:</p>
        <a href="/game"><button>Go to Game</button></a>
      </div>
      <div>
        <p>Logout:</p>
        <form action={logout}>
          <button>Logout</button>
        </form>
      </div>
    </main>
  );
}